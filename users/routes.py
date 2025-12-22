from flask import render_template, request, redirect, url_for, flash
from users import users_bp
from extensions import db
from models import User
from utils.pagination import paginate   # <-- paginação geral

ITEMS_PER_PAGE = 10

@users_bp.route("/")
def list_users():
    termo = request.args.get("q", "").strip()

    query = User.query
    if termo:
        like = f"%{termo}%"
        query = query.filter(
            (User.nome.ilike(like)) |
            (User.email.ilike(like)) |
            (User.telefone.ilike(like)) |
            (User.funcao.ilike(like))
        )

    # Paginação geral
    users = paginate(query.order_by(User.nome.asc()), per_page=ITEMS_PER_PAGE)

    return render_template("users/list.html", users=users, termo=termo)


@users_bp.route("/novo", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        funcao = request.form.get("funcao", "").strip()

        if not nome or not email or not telefone or not funcao:
            flash("Preencha todos os campos obrigatórios.", "danger")
            return render_template("users/form.html", user=None)

        existente = User.query.filter_by(email=email).first()
        if existente:
            flash("Já existe um usuário com esse e-mail.", "danger")
            return render_template("users/form.html", user=None)

        user = User(nome=nome, email=email, telefone=telefone, funcao=funcao)
        db.session.add(user)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("users.list_users"))

    return render_template("users/form.html", user=None)


@users_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        funcao = request.form.get("funcao", "").strip()

        if not nome or not email or not telefone or not funcao:
            flash("Preencha todos os campos obrigatórios.", "danger")
            return render_template("users/form.html", user=user)

        existente = User.query.filter(User.email == email, User.id != user.id).first()
        if existente:
            flash("Já existe outro usuário com esse e-mail.", "danger")
            return render_template("users/form.html", user=user)

        user.nome = nome
        user.email = email
        user.telefone = telefone
        user.funcao = funcao

        db.session.commit()
        flash("Usuário atualizado com sucesso!", "success")
        return redirect(url_for("users.list_users"))

    return render_template("users/form.html", user=user)


@users_bp.route("/excluir/<int:id>")
def delete_user(id):
    user = User.query.get_or_404(id)

    if user.movements:
        flash("Não é possível excluir usuário com movimentações vinculadas.", "danger")
        return redirect(url_for("users.list_users"))

    db.session.delete(user)
    db.session.commit()
    flash("Usuário excluído com sucesso!", "success")
    return redirect(url_for("users.list_users"))
