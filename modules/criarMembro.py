from flask import redirect, render_template, request, url_for

from functions.db_membro import create_member


def mod_criar_membro(mysql):
    # Verifica se o método da requisição é 'POST', indicando que o formulário foi enviado para criar um novo membro
    if request.method == 'POST':  # Lógica de inserção de membro
        
        # Chama a função create_member para adicionar o novo membro ao banco de dados
        create_member(mysql)
        
        # Após criar o membro, redireciona o usuário para a página principal (index)
        return redirect(url_for('index'))
    
    # Se o método não for 'POST', renderiza o formulário de criação de membro
    return render_template('membro.html')
