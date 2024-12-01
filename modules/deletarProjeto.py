from flask import redirect, url_for

from functions.db_projeto import delete_project


def mod_deletar_projeto(mysql, projeto_id):

    # Chama a função delete_project para remover o projeto do banco de dados
    delete_project(mysql, projeto_id)

    # Após a exclusão do projeto, redireciona o usuário para a página principal (index)
    return redirect(url_for('index'))
