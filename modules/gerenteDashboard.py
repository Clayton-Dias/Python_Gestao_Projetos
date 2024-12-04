from flask import flash, redirect, render_template, url_for
from flask_login import current_user
from functions.db_projeto import count_projetos, get_projetos_por_gerente, get_projetos_recentes

def mod_gerente_dashborad(mysql):
    if current_user.permissao != 'gerente':
        flash("Você não tem permissão para acessar esta página.", "danger")
        return redirect(url_for('index'))

    # Obtém os dados para o painel
    total_projetos = count_projetos(mysql)
    projetos_gerente = get_projetos_por_gerente(mysql, current_user.id)  # Obtenha os projetos do gerente
    projetos_recentes = get_projetos_recentes(mysql, limite=5)

    return render_template(
        'gerente_dashboard.html',
        total_projetos=total_projetos,
        projetos_gerente=projetos_gerente,  # Envia os projetos que o gerente está gerenciando
        projetos_recentes=projetos_recentes
    )