from flask import flash, redirect, render_template, url_for
from flask_login import  current_user
from functions.db_usuario import get_all_users


def mod_listar_user(mysql):
    # Verifica se o usuário tem permissão
    if current_user.permissao not in ['administrador', 'gerente']:
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('index'))

    # Busca todos os usuários do banco de dados
    usuarios = get_all_users(mysql)
    return render_template('listar_user.html', usuarios=usuarios)