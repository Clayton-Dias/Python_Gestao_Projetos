from flask import flash, redirect, render_template, request, url_for
from flask_login import  current_user
from werkzeug.security import generate_password_hash

from functions.db_usuario import get_user_by_id, update_user_by_id

def mod_editar_usuario(mysql, usuario_id):
    # Verifica se o usuário atual tem permissão para editar usuários
    if current_user.permissao not in ['administrador', 'gerente']:
        # Se não tiver permissão, exibe uma mensagem de erro e redireciona para a lista de usuários
        flash("Você não tem permissão para editar usuários.", "danger")
        return redirect(url_for('listar_user'))

    # Obtém os dados do usuário a partir do ID
    usuario = get_user_by_id(mysql, usuario_id)

    # Se o usuário não for encontrado, exibe uma mensagem de erro e redireciona
    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for('listar_user'))

    # Verifica se o formulário foi submetido (método POST)
    if request.method == 'POST':
        # Atualiza o usuário no banco de dados com as informações fornecidas
        update_user_by_id(mysql, usuario_id)

        # Exibe uma mensagem de sucesso
        flash("Usuário atualizado com sucesso.", "success")
        # Redireciona para a lista de usuários
        return redirect(url_for('listar_user'))

    # Se a requisição for GET, renderiza a página de edição com os dados do usuário
    return render_template('editar_usuario.html', usuario=usuario)
