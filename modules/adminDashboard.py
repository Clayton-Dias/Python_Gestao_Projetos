from flask import flash, render_template, redirect, url_for
from flask_login import current_user
from functions.db_usuario import count_usuarios, count_usuarios_por_permissao, get_usuarios_recentes
from functions.db_projeto import count_projetos, get_projetos_recentes


def mod_admin_dashboard(mysql):
    # Verifica se o usuário tem permissão de administrador
    if current_user.permissao != 'administrador':
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('index'))  # Redireciona para a página inicial se não for admin

    # Obtém os dados para o painel
    total_usuarios = count_usuarios(mysql)
    total_projetos = count_projetos(mysql)
    total_gerentes = count_usuarios_por_permissao(mysql, 'gerente')
    usuarios_recentes = get_usuarios_recentes(mysql, limite=5)
    projetos_recentes = get_projetos_recentes(mysql, limite=5)

    return render_template(
        'admin_dashboard.html',
        total_usuarios=total_usuarios,
        total_projetos=total_projetos,
        total_gerentes=total_gerentes,
        usuarios_recentes=usuarios_recentes,
        projetos_recentes=projetos_recentes
    )
