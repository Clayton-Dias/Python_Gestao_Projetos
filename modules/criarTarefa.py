from flask import redirect, render_template, request, url_for

from functions.db_tarefa import create_task


def mod_criar_tarefa(mysql, projeto_id):
    
    # Verifica se o método da requisição é 'POST' (indicando que o formulário foi enviado para criar uma nova tarefa)
    if request.method == 'POST':  # Lógica de inserção de tarefa
        
        # Chama a função update_task para inserir ou atualizar a tarefa no banco de dados
        create_task(mysql, projeto_id)
        
        # Após a inserção ou atualização da tarefa, redireciona para a página do projeto, passando o projeto_id como parâmetro
        return redirect(url_for('projeto', projeto_id=projeto_id))

    # Se o método não for 'POST', significa que o formulário de criação de tarefa está sendo exibido
    # Apenas renderiza o template de criação de tarefa, passando o projeto_id para o template
    return render_template('criar_tarefa.html', projeto_id=projeto_id)
