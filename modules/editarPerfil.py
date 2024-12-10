from flask import flash, redirect, render_template, request, url_for
from flask_login import  current_user
from werkzeug.security import generate_password_hash

from functions.db_usuario import update_user

def mod_editar_perfil(mysql):
    """Página para editar as informações do usuário."""

    # Valida se o usuário tem permissão para editar o perfil
    """if current_user.permissao not in ['administrador', 'gerente']:
        flash('Você não tem permissão para editar esse perfil.', 'danger')
        # Redireciona para a página inicial ou outra página
        return redirect(url_for('index'))"""

    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        permissao = request.form['permissao']

        # Se a senha foi modificada, gera o hash
        if senha:
            senha_hash = generate_password_hash(senha)
        else:
            senha_hash = current_user.senha  # Mantém a senha atual se não for alterada

        # Chama a função para atualizar os dados no banco
        update_user(mysql, current_user.id, nome, email, senha_hash, permissao)

        # Redireciona para a página inicial ou outra página
        return redirect(url_for('index'))

    # Se for um GET, exibe o formulário de edição com os dados atuais
    return render_template('editar_perfil.html', usuario=current_user)