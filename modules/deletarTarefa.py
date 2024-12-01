from flask import redirect, request, url_for

from functions.db_tarefa import delete_task


def mod_deletar_tarefa(mysql, tarefa_id):    

    # Exclui a tarefa do banco de dados
    delete_task(mysql, tarefa_id)

    # Após deletar, redireciona de volta para a página do projeto
    return redirect(url_for('projeto', projeto_id=request.form['projeto_id']))