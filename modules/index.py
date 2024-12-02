# Importa a função render_template para renderizar templates HTML
from flask import render_template, request

# Importa a função get_all_projects de um módulo externo para obter todos os projetos
from functions.db_projeto import count_project, get_all_projects, get_projects_current_page


def mod_index(mysql):
    # Chama a função get_all_projects passando a conexão 'mysql' para obter todos os projetos armazenados no banco de dados
    # projetos = get_all_projects(mysql)

    # Retorna o template 'index.html' e passa a variável 'projetos' para ser utilizada dentro do template
    # return render_template('index.html', projetos=projetos)

    itens_por_pagina = 5  # Número de projetos por página
    pagina_atual = request.args.get('pagina', 1, type=int)  # Obtém a página atual da URL, padrão 1
    
    try:
        # Calcula o total de projetos
        total_projetos = count_project(mysql)

        # Calcula o total de páginas
        total_paginas = (total_projetos + itens_por_pagina - 1) // itens_por_pagina  # Arredonda para cima

        # Determina o offset para a consulta
        offset = (pagina_atual - 1) * itens_por_pagina

        # Recupera projetos para a página atual
        projetos = get_projects_current_page(mysql, itens_por_pagina, offset)

        # Renderiza a página com os projetos e informações de paginação
        return render_template(
            'index.html',
            projetos=projetos,
            pagina_atual=pagina_atual,
            total_paginas=total_paginas
        )
    except Exception as e:
        print(f"Erro ao recuperar projetos: {e}")
        return render_template('index.html', projetos=[], pagina_atual=1, total_paginas=1)
