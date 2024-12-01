from flask import redirect, url_for

from functions.db_membro import remove_membro_by_project


def mod_remover_membro(mysql, projeto_id, membro_id):
    # Chama a função remove_membro_by_project para remover o membro do projeto no banco de dados
    remove_membro_by_project(mysql, projeto_id, membro_id)

    # Após a remoção do membro, redireciona o usuário para a página do projeto relacionado
    return redirect(url_for('projeto', projeto_id=projeto_id))

