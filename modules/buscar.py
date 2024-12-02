from flask import render_template, request

from functions.db_projeto import count_project_search, search_project


def mod_buscar(mysql):

    termo_busca = request.args.get(
        'search', '').strip()  # Obtém o termo de busca
    pagina_atual = request.args.get(
        'pagina', 1, type=int)  # Controle de paginação

    projetos = search_project(mysql, termo_busca, pagina_atual)

    # Calcula o total de páginas
    total_projetos = count_project_search(mysql, termo_busca)
    total_paginas = (total_projetos + 4) // 5

    return render_template(
        'buscar.html',
        projetos=projetos,
        pagina_atual=pagina_atual,
        total_paginas=total_paginas,
        termo_busca=termo_busca  # Envia o termo para o template
    )
