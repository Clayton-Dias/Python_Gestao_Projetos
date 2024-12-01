from datetime import datetime
from flask import redirect, render_template, request, url_for

from functions.db_membro import get_member
from functions.db_projeto import create_project


def mod_criar_projeto(mysql):
    # Verifica se o método da requisição é 'POST' (indicando que o formulário foi enviado)
    if request.method == 'POST':  # Lógica de inserção de projeto
        
        # Chama a função create_project para inserir o novo projeto no banco de dados
        create_project(mysql)
        
        # Redireciona para a página principal (index) após o projeto ser criado
        return redirect(url_for('index'))

    # Se o método não for 'POST', significa que o formulário de criação de projeto ainda não foi enviado
    # Aqui, busca-se os membros para atribuir a um projeto
    membros = get_member(mysql)

    # Renderiza o template 'criar_projeto.html' e passa os membros obtidos para o template
    return render_template('criar_projeto.html', membros=membros)
