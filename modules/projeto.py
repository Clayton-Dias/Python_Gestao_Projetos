from flask import render_template

from functions.db_membro import get_member_available, get_member_by_project
from functions.db_projeto import get_project_responsible
from functions.db_tarefa import get_task_completed, get_task_pending, get_task_progess


def mod_projeto(mysql, projeto_id):
    # Obtém a lista de tarefas pendentes para o projeto especificado
    tarefas_pendentes = get_task_pending(mysql, projeto_id)

    # Obtém a lista de tarefas em andamento para o projeto especificado
    tarefas_andamento = get_task_progess(mysql, projeto_id)

    # Obtém a lista de tarefas concluídas para o projeto especificado
    tarefas_concluidas = get_task_completed(mysql, projeto_id)

    # Obtém os membros atualmente associados ao projeto
    membros = get_member_by_project(mysql, projeto_id)
    
    # Obtém todos os membros disponíveis (que não estão atualmente associados ao projeto)
    todos_membros = get_member_available(mysql, projeto_id)

    # Obtém os detalhes do projeto, incluindo o nome do responsável
    projeto = get_project_responsible(mysql, projeto_id)
        
    # Organiza todos os dados em um dicionário para facilitar o acesso no template
    page = {
        "projeto": projeto,
        "pendentes": tarefas_pendentes,
        "andamento": tarefas_andamento,
        "concluidas": tarefas_concluidas,
        "membros": membros,
        "todos_membros": todos_membros  # Passando os membros disponíveis que não estão no projeto
    }
    
    # Renderiza o template 'projeto_detalhes.html' e passa os dados organizados na variável 'page' para o template
    return render_template('projeto_detalhes.html', page=page)
