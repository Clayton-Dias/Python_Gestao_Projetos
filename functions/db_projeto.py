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
    mysql.connection.commit()  # Confirma a transação
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
    mysql.connection.commit()  # Confirma a transação
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

    mysql.connection.commit()  # Confirma as transações
    cur.close()  # Fecha o cursor


def count_project(mysql):

    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) AS total FROM projeto")
    total_projetos = cur.fetchone()['total']
    cur.close()

    return total_projetos


def get_projects_current_page(mysql, itens_por_pagina, offset):

    sql = "SELECT * FROM projeto LIMIT %s OFFSET %s"

    cur = mysql.connection.cursor()
    cur.execute(sql, (itens_por_pagina, offset))
    projetos = cur.fetchall()
    cur.close()

    return projetos


def search_project(mysql, termo_busca, pagina_atual):

    # Consulta de busca
    sql = """
            SELECT * FROM projeto
            WHERE nome LIKE %s
            ORDER BY data_inicio DESC
            LIMIT %s OFFSET %s
        """
    valores = (f"%{termo_busca}%", 5, (pagina_atual - 1) * 5)

    cur = mysql.connection.cursor()
    cur.execute(sql, valores)
    projetos = cur.fetchall()
    cur.close()

    return projetos


def count_project_search(mysql, termo_busca):

    sql = "SELECT COUNT(*) AS total FROM projeto WHERE nome LIKE %s"
    
    cur = mysql.connection.cursor()
    cur.execute(sql, (f"%{termo_busca}%",))  # Passa o valor como uma tupla
    result = cur.fetchone()
    return result['total']


