from flask import render_template  # Importa a função render_template para renderizar templates HTML

from functions.db_projeto import get_all_projects  # Importa a função get_all_projects de um módulo externo para obter todos os projetos

def mod_index(mysql):
    # Chama a função get_all_projects passando a conexão 'mysql' para obter todos os projetos armazenados no banco de dados
    projetos = get_all_projects(mysql)
    
    # Retorna o template 'index.html' e passa a variável 'projetos' para ser utilizada dentro do template
    return render_template('index.html', projetos=projetos)
