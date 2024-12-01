from flask import redirect, url_for

from functions.db_membro import add_member_to_project


def mod_adicionar_membro(mysql, projeto_id):
    # Chama a função add_member_to_project para adicionar um membro ao projeto no banco de dados
    add_member_to_project(mysql, projeto_id)

    # Após adicionar o membro ao projeto, redireciona o usuário para a página do projeto relacionado
    return redirect(url_for('projeto', projeto_id=projeto_id))
