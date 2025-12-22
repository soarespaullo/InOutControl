import os
from flask import send_from_directory, flash, redirect, request
from __init__ import create_app
from extensions import db
from models import User, Part, Movement

# ============================ # CRIAÇÃO DO APP # ============================
app = create_app()

# Define limite máximo de upload (exemplo: 5 MB)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


# ============================ # ROTA PARA SERVIR UPLOADS # ============================
@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    """
    Rota para servir arquivos enviados (fotos das peças).
    Busca o arquivo dentro da pasta configurada em UPLOAD_FOLDER.
    """
    upload_folder = app.config["UPLOAD_FOLDER"]
    return send_from_directory(upload_folder, filename)


# ============================ # TRATAMENTO DE ERRO 413 # ============================
@app.errorhandler(413)
def too_large(e):
    """
    Tratamento para uploads maiores que o limite definido.
    Retorna mensagem amigável ao usuário em vez da tela padrão.
    """
    flash("Arquivo muito grande. O limite é de 5 MB.", "danger")
    return redirect(request.url)


# ============================ # MAIN # ============================
if __name__ == "__main__":
    # Cria as tabelas no banco de dados se não existirem
    with app.app_context():
        db.create_all()
    # Executa o servidor em modo debug
    app.run(debug=True)
