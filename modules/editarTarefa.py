from flask import redirect, render_template, request, url_for

from functions.db_tarefa import get_details_task, update_task


def mod_editar_tarefa(mysql, tarefa_id):
    
    # Verifica se o método da requisição é 'POST' (indicando que o formulário foi enviado para atualizar a tarefa)
    if request.method == 'POST':  # Lógica de atualização de tarefa
        
        # Chama a função update_task para atualizar a tarefa no banco de dados, passando o tarefa_id
        update_task(mysql, tarefa_id)
         
        # Após a atualização da tarefa, redireciona para a página do projeto relacionado, passando o projeto_id extraído do formulário
        return redirect(url_for('projeto', projeto_id=request.form['projeto_id']))

    # Obtem detalhes da tarefa para edição
    tarefa = get_details_task(mysql,tarefa_id)
    
    # Converte o prazo para o formato 'YYYY-MM-DD'
    if tarefa and 'prazo' in tarefa:
        tarefa['prazo'] = tarefa['prazo'].strftime('%Y-%m-%d')
    
    return render_template('editar_tarefa.html', tarefa=tarefa)