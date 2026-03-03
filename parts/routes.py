from flask import render_template, request, redirect, url_for, flash, make_response, current_app
from parts import parts_bp
from extensions import db
from models import Part
from utils.pagination import paginate
from weasyprint import HTML, CSS

import qrcode
import base64
from io import BytesIO
import barcode
from barcode.writer import ImageWriter
import os
from datetime import datetime  # usado para gerar data em relatórios/PDF
from werkzeug.utils import secure_filename  # para salvar arquivos com nome seguro

ITEMS_PER_PAGE = 10  # quantidade de itens por página na listagem

# Extensões permitidas para upload de imagens
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    """Verifica se o arquivo possui uma extensão válida de imagem."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ============================ # LISTAR PEÇAS (com busca + paginação) # ============================
@parts_bp.route("/")
def list_parts():
    termo = request.args.get("q", "").strip()

    query = Part.query
    if termo:
        like = f"%{termo}%"
        query = query.filter(
            (Part.nome.ilike(like)) |
            (Part.codigo.ilike(like)) |
            (Part.descricao.ilike(like))
        )

    parts = paginate(query.order_by(Part.nome.asc()), per_page=ITEMS_PER_PAGE)
    return render_template("parts/list.html", parts=parts, termo=termo)


# ============================ # NOVA PEÇA # ============================
@parts_bp.route("/novo", methods=["GET", "POST"])
def create_part():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        codigo = request.form.get("codigo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        quantidade = request.form.get("quantidade", "").strip()
        valor_custo = request.form.get("valor_custo", "").strip()

        if not nome or not codigo or not quantidade or not valor_custo:
            flash("Preencha todos os campos obrigatórios.", "danger")
            return render_template("parts/form.html", part=None)

        existente = Part.query.filter_by(codigo=codigo).first()
        if existente:
            flash("Já existe uma peça com esse código.", "danger")
            return render_template("parts/form.html", part=None)

        # Normalizar valor_custo (aceitar vírgula ou ponto)
        valor_custo = valor_custo.replace(",", ".")

        # Upload da foto com validação
        foto_file = request.files.get("foto_arquivo")
        foto_filename = None
        if foto_file and foto_file.filename:
            if allowed_file(foto_file.filename):
                filename = secure_filename(foto_file.filename)
                upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                foto_file.save(upload_path)
                foto_filename = filename
            else:
                flash("Formato de arquivo inválido. Envie apenas imagens (png, jpg, jpeg, gif).", "danger")
                return render_template("parts/form.html", part=None)

        part = Part(
            nome=nome,
            codigo=codigo,
            descricao=descricao,
            quantidade=int(quantidade),
            valor_custo=float(valor_custo),
            foto=foto_filename
        )
        db.session.add(part)
        db.session.commit()
        flash("Peça cadastrada com sucesso!", "success")
        return redirect(url_for("parts.list_parts"))

    return render_template("parts/form.html", part=None)


# ============================ # EDITAR PEÇA # ============================
@parts_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def edit_part(id):
    part = Part.query.get_or_404(id)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        codigo = request.form.get("codigo", "").strip()
        descricao = request.form.get("descricao", "").strip()
        quantidade = request.form.get("quantidade", "").strip()
        valor_custo = request.form.get("valor_custo", "").strip()

        if not nome or not codigo or not quantidade or not valor_custo:
            flash("Preencha todos os campos obrigatórios.", "danger")
            return render_template("parts/form.html", part=part)

        existente = Part.query.filter(Part.codigo == codigo, Part.id != part.id).first()
        if existente:
            flash("Já existe outra peça com esse código.", "danger")
            return render_template("parts/form.html", part=part)

        # Normalizar valor_custo (aceitar vírgula ou ponto)
        valor_custo = valor_custo.replace(",", ".")

        part.nome = nome
        part.codigo = codigo
        part.descricao = descricao
        part.quantidade = int(quantidade)
        part.valor_custo = float(valor_custo)

        # Upload da foto com validação
        foto_file = request.files.get("foto_arquivo")
        if foto_file and foto_file.filename:
            if allowed_file(foto_file.filename):
                filename = secure_filename(foto_file.filename)
                upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                foto_file.save(upload_path)
                part.foto = filename
            else:
                flash("Formato de arquivo inválido. Envie apenas imagens (png, jpg, jpeg, gif).", "danger")
                return render_template("parts/form.html", part=part)

        db.session.commit()
        flash("Peça atualizada com sucesso!", "success")
        return redirect(url_for("parts.list_parts"))

    return render_template("parts/form.html", part=part)


# ============================ # EXCLUIR PEÇA # ============================
@parts_bp.route("/excluir/<int:id>")
def delete_part(id):
    part = Part.query.get_or_404(id)

    if part.movements:
        flash("Não é possível excluir peça com movimentações vinculadas.", "danger")
        return redirect(url_for("parts.list_parts"))

    db.session.delete(part)
    db.session.commit()
    flash("Peça excluída com sucesso!", "success")
    return redirect(url_for("parts.list_parts"))


# ============================ # MENU DE ETIQUETAS # ============================
@parts_bp.route("/etiquetas")
def etiquetas_menu():
    return render_template("parts/etiquetas_menu.html")


# ============================ # GERAR PDF DE ETIQUETAS # ============================
@parts_bp.route("/etiquetas/pdf/<modelo>")
def etiquetas_pdf(modelo):
    parts = Part.query.order_by(Part.nome.asc()).all()
    etiquetas = []

    for p in parts:
        qr_base64 = None
        barcode_base64 = None

        if modelo in ["qrcode", "completo"]:
            qr = qrcode.make(str(p.codigo))
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        if modelo in ["barcode", "completo"]:
            EAN = barcode.get_barcode_class('code128')
            ean = EAN(str(p.codigo), writer=ImageWriter())
            buffer = BytesIO()
            ean.write(buffer)
            barcode_base64 = base64.b64encode(buffer.getvalue()).decode()

        etiquetas.append({
            "codigo": p.codigo,
            "nome": p.nome,
            "qr": qr_base64,
            "barcode": barcode_base64
        })

    html = render_template(f"parts/etiquetas_{modelo}.html", etiquetas=etiquetas)
    css_path = os.path.join(current_app.root_path, "static/css/styles.css")
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css_path)])

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=etiquetas_{modelo}.pdf"
    return response


# ============================ # RELATÓRIO GERAL DE PEÇAS (PDF) # ============================
@parts_bp.route("/pdf")
def relatorio_pecas():
    parts = Part.query.order_by(Part.nome.asc()).all()
    dia = datetime.now().strftime("%d-%m-%Y")

    html = render_template("parts/relatorio_pecas.html", pecas=parts, dia=dia)
    css_path = os.path.join(current_app.root_path, "static/css/styles.css")
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(css_path)])

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"inline; filename=relatorio_pecas_{dia}.pdf"
    return response
