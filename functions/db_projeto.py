from datetime import datetime
from flask import request


# Função para buscar todos os projetos
def get_all_projects(mysql):
    # SQL para obter todos os projetos com os nomes de seus responsáveis
    sql = '''
        SELECT p.id, p.nome, p.descricao, p.data_inicio, m.nome AS responsavel_nome
        FROM projeto p
        JOIN membro m ON p.responsavel_id = m.id;
    '''
    cur = mysql.connection.cursor()  # Cria um cursor para executar a consulta
    cur.execute(sql)  # Executa a consulta
    projetos = cur.fetchall()  # Busca todos os registros retornados
    cur.close()  # Fecha o cursor

    return projetos  # Retorna a lista de projetos


# Função para criar um novo projeto
def create_project(mysql):
    # SQL para inserir um novo projeto no banco
    sql = '''
            INSERT INTO projeto (nome, descricao, responsavel_id, data_inicio)
            VALUES (%s, %s, %s, %s)
        '''
    cur = mysql.connection.cursor()  # Cria um cursor
    # Executa a consulta com os dados enviados pelo formulário
    cur.execute(sql, (request.form['nome'], request.form['descricao'],
                request.form['responsavel_id'], datetime.utcnow()))
    mysql.connection.commit()  # Confirma a transação no banco de dados
    cur.close()  # Fecha o cursor


# Função para atualizar um projeto existente
def update_project(mysql, projeto_id):
    # SQL para atualizar os dados de um projeto
    sql = '''
            UPDATE projeto
            SET nome = %s, descricao = %s, responsavel_id = %s
            WHERE id = %s
        '''
    cur = mysql.connection.cursor()  # Cria um cursor
    # Executa a consulta com os novos dados enviados pelo formulário
    cur.execute(sql, (request.form['nome'], request.form['descricao'],
                request.form['responsavel_id'], projeto_id))
    mysql.connection.commit()  # Confirma a transação no banco de dados
    cur.close()  # Fecha o cursor


# Função para obter os detalhes de um projeto pelo seu ID
def get_details_project(mysql, projeto_id):
    # SQL para buscar um projeto específico
    sql = '''
        SELECT * FROM projeto WHERE id = %s
    '''

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, [projeto_id])  # Executa a consulta com o ID do projeto
    projeto = cur.fetchone()  # Obtém o primeiro registro encontrado
    cur.close()  # Fecha o cursor

    return projeto  # Retorna os detalhes do projeto


# Função para obter os detalhes de um projeto com o nome do responsável
def get_project_responsible(mysql, projeto_id):
    # SQL para buscar os detalhes do projeto com o responsável associado
    sql = '''
        SELECT p.*, m.nome AS responsavel_nome
        FROM projeto p
        LEFT JOIN membro m ON p.responsavel_id = m.id
        WHERE p.id = %s
    '''

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, [projeto_id])  # Executa a consulta com o ID do projeto
    projeto = cur.fetchone()  # Obtém o primeiro registro encontrado
    cur.close()  # Fecha o cursor

    return projeto  # Retorna os detalhes do projeto


# Função para deletar um projeto e suas associações
def delete_project(mysql, projeto_id):
    cur = mysql.connection.cursor()  # Cria um cursor

    # SQL para deletar as tarefas associadas ao projeto
    cur.execute("DELETE FROM tarefa WHERE projeto_id = %s", [projeto_id])

    # SQL para deletar os membros associados ao projeto
    cur.execute(
        "DELETE FROM projeto_membro WHERE projeto_id = %s", [projeto_id])

    # SQL para deletar o próprio projeto
    cur.execute("DELETE FROM projeto WHERE id = %s", [projeto_id])

    mysql.connection.commit()  # Confirma as transações no banco de dados
    cur.close()  # Fecha o cursor


def count_project(mysql):
    # Contabiliza o número total de projetos
    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute("SELECT COUNT(*) AS total FROM projeto")  # Executa a contagem
    total_projetos = cur.fetchone()['total']  # Obtém o total de projetos
    cur.close()  # Fecha o cursor

    return total_projetos  # Retorna o total de projetos


def get_projects_current_page(mysql, itens_por_pagina, offset):
    # Função para retornar os projetos na página atual, com base no limite de itens por página e offset
    sql = '''
        SELECT
            p.id,
            p.nome AS nome,
            p.descricao AS descricao,
            u.nome AS responsavel_nome
        FROM
            projeto p
        JOIN
            usuarios u
        ON
            p.responsavel_id = u.id
        LIMIT %s OFFSET %s
    '''

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, (itens_por_pagina, offset))  # Executa a consulta com limites de paginação
    projetos = cur.fetchall()  # Recupera os resultados
    cur.close()  # Fecha o cursor

    return projetos  # Retorna a lista de projetos da página atual


def search_project(mysql, termo_busca, pagina_atual):
    # Função para realizar a busca de projetos com base em um termo
    sql = """
            SELECT * FROM projeto
            WHERE nome LIKE %s OR descricao LIKE %s
            ORDER BY data_inicio DESC
            LIMIT %s OFFSET %s
        """
    valores = (f"%{termo_busca}%", f"%{termo_busca}%",
               5, (pagina_atual - 1) * 5)  # Limita a 5 resultados por página

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, valores)  # Executa a consulta com os parâmetros de busca
    projetos = cur.fetchall()  # Recupera os resultados
    cur.close()  # Fecha o cursor

    return projetos  # Retorna os projetos encontrados


def count_project_search(mysql, termo_busca):
    # Conta o número total de projetos encontrados pela busca
    sql = "SELECT COUNT(*) AS total FROM projeto WHERE nome LIKE %s"

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, (f"%{termo_busca}%",))  # Executa a consulta com o termo de busca
    result = cur.fetchone()  # Obtém o resultado da contagem
    return result['total']  # Retorna o total de projetos encontrados


def get_projetos_por_gerente(mysql, gerente_id):
    # Retorna os projetos atribuídos a um gerente específico
    sql = "SELECT * FROM projeto WHERE gerente_id = %s"

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, (gerente_id,))  # Executa a consulta com o ID do gerente
    projetos = cur.fetchall()  # Recupera os projetos
    cur.close()  # Fecha o cursor

    return projetos  # Retorna a lista de projetos do gerente


def get_projetos_recentes(mysql, limite=5):
    # Retorna os projetos mais recentes, com base no limite definido (default 5)
    sql = """
            SELECT * FROM projeto
            ORDER BY data_inicio DESC
            LIMIT %s
        """

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, (limite,))  # Executa a consulta com o limite de resultados
    projetos = cur.fetchall()  # Recupera os resultados
    cur.close()  # Fecha o cursor

    return projetos  # Retorna a lista de projetos recentes


def count_projetos(mysql):
    # Conta o número total de projetos no banco de dados
    sql = "SELECT COUNT(*) AS total FROM projeto"

    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql)  # Executa a consulta
    result = cur.fetchone()  # Obtém o resultado da contagem
    cur.close()  # Fecha o cursor

    return result['total']  # Retorna o total de projetos


def get_projetos_por_membro(mysql, usuario_id):
    
    sql = """
        SELECT p.id, p.nome, p.descricao
        FROM projeto p
        INNER JOIN projeto_membro mp ON mp.projeto_id = p.id
        WHERE mp.membro_id = %s
    """
    
    cursor = mysql.connection.cursor()    
    cursor.execute(sql, (usuario_id,))
    projetos = cursor.fetchall()
    cursor.close()
    
    return projetos
