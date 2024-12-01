from flask import redirect, render_template, request, url_for

from functions.db_membro import get_member
from functions.db_projeto import get_details_project, update_project


def mod_editar_projeto(mysql, projeto_id):
    # Cria um cursor para executar comandos SQL no banco de dados
    cur = mysql.connection.cursor()
    
    # Verifica se o método da requisição é 'POST' (indicando que o formulário foi enviado para atualizar o projeto)
    if request.method == 'POST':  # Lógica de atualização
        
        # Chama a função update_project para atualizar os dados do projeto no banco de dados
        update_project(mysql, projeto_id)
        
        # Redireciona para a página principal (index) após a atualização do projeto
        return redirect(url_for('index'))

    # Se o método não for 'POST', significa que o formulário de edição do projeto está sendo exibido
    # Obtem os detalhes do projeto com base no projeto_id
    projeto = get_details_project(mysql, projeto_id)
    
    # Obtem os membros disponíveis que podem ser atribuídos ao projeto
    membros = get_member(mysql)
    
    # Renderiza o template 'editar_projeto.html' e passa os detalhes do projeto e membros para o template
    return render_template('editar_projeto.html', projeto=projeto, membros=membros)
