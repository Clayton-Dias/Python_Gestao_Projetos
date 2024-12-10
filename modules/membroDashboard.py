from flask import render_template
from flask_login import current_user

from functions.db_projeto import get_projetos_por_membro
from functions.db_tarefa import get_tarefas_por_membro


def mod_membro_dashborad(mysql):
    # Buscando os projetos e tarefas do usuário logado
    usuario_id = current_user.id  # ID do usuário logado
    projetos = get_projetos_por_membro(mysql, usuario_id)  # Função personalizada para filtrar projetos
    tarefas = get_tarefas_por_membro(mysql, usuario_id)    # Função personalizada para filtrar tarefas
    
    return render_template(
        'membro_dashboard.html',
        projetos=projetos,
        tarefas=tarefas
    )