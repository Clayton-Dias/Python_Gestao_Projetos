from flask import request


def get_member(mysql):
    # Retorna todos os membros da tabela 'membro', ordenados por nome
    sql = "SELECT * FROM membro ORDER BY nome"
    cur = mysql.connection.cursor()  # Cria um cursor para a execução da consulta SQL
    cur.execute(sql)  # Executa a consulta SQL
    membros = cur.fetchall()  # Recupera todos os resultados da consulta
    cur.close()  # Fecha o cursor
    return membros  # Retorna a lista de membros


def get_member_by_project(mysql, projeto_id):
    # Retorna os membros associados a um projeto específico, filtrando pelo ID do projeto
    sql = '''
        SELECT m.id, m.nome, m.email 
        FROM membro m
        INNER JOIN projeto_membro pm ON m.id = pm.membro_id
        WHERE pm.projeto_id = %s
    '''
    cur = mysql.connection.cursor()  # Cria um cursor para a execução da consulta SQL
    cur.execute(sql, [projeto_id])  # Executa a consulta, passando o ID do projeto como parâmetro
    membros = cur.fetchall()  # Recupera todos os resultados da consulta
    cur.close()  # Fecha o cursor
    return membros  # Retorna a lista de membros associados ao projeto


def get_member_available(mysql, projeto_id):
    # Retorna os membros que não estão associados a um projeto específico
    sql = '''
        SELECT id, nome FROM membro
        WHERE id NOT IN (SELECT membro_id FROM projeto_membro WHERE projeto_id = %s)
    '''
    cur = mysql.connection.cursor()  # Cria um cursor para a execução da consulta SQL
    cur.execute(sql, [projeto_id])  # Executa a consulta, passando o ID do projeto como parâmetro
    membros = cur.fetchall()  # Recupera todos os resultados da consulta
    cur.close()  # Fecha o cursor
    return membros  # Retorna a lista de membros disponíveis


def create_member(mysql):
    # Adiciona um novo membro à tabela 'membro'
    sql = "INSERT INTO membro (nome, email) VALUES (%s, %s)"
    cur = mysql.connection.cursor()  # Cria um cursor para a execução da consulta SQL
    # Dados fornecidos via formulário (request.form)
    cur.execute(sql, (request.form['nome'], request.form['email']))  # Executa a inserção dos dados
    mysql.connection.commit()  # Confirma a transação no banco de dados
    cur.close()  # Fecha o cursor


def remove_membro_by_project(mysql, projeto_id, membro_id):
    # Remove um membro de um projeto específico
    sql = 'DELETE FROM projeto_membro WHERE projeto_id = %s AND membro_id = %s'
    cur = mysql.connection.cursor()  # Cria um cursor para a execução da consulta SQL
    # Executa a exclusão do membro associado ao projeto
    cur.execute(sql, (projeto_id, membro_id))  
    mysql.connection.commit()  # Confirma a remoção no banco de dados
    cur.close()  # Fecha o cursor


def add_member_to_project(mysql, projeto_id):
    # Adiciona um membro a um projeto, evitando duplicação (membro já associado)
    cur = mysql.connection.cursor()  # Cria um cursor para a execução da consulta SQL

    # Verifica se o membro já está associado ao projeto
    cur.execute('SELECT * FROM projeto_membro WHERE projeto_id = %s AND membro_id = %s',
                (projeto_id, request.form['membro_id']))  # Filtra pelo ID do projeto e membro
    membro_existente = cur.fetchone()  # Recupera o membro, se já estiver associado

    if not membro_existente:
        # Se o membro não estiver associado, insere a relação projeto-membro
        cur.execute('INSERT INTO projeto_membro (projeto_id, membro_id) VALUES (%s, %s)',
                    (projeto_id, request.form['membro_id']))
        mysql.connection.commit()  # Confirma a adição da relação no banco de dados

    cur.close()  # Fecha o cursor


def edit_member(mysql, membro_id):
    # Edita os dados de um membro (nome e email) no banco de dados
    sql = '''
        UPDATE membro SET nome = %s, email = %s WHERE id = %s
    '''
    cur = mysql.connection.cursor()  # Cria um cursor para a execução da consulta SQL
    cur.execute(sql, (request.form['nome'], request.form['email'], membro_id))  # Executa a atualização
    mysql.connection.commit()  # Confirma a transação no banco de dados
    cur.close()  # Fecha o cursor


def get_member_by_id(mysql, membro_id):
    # Retorna os dados de um membro específico pelo seu ID
    cur = mysql.connection.cursor()  # Cria um cursor para a execução da consulta SQL
    cur.execute("SELECT * FROM membro WHERE id = %s", (membro_id,))  # Filtra pelo ID do membro
    membro = cur.fetchone()  # Recupera o único membro correspondente ao ID
    cur.close()  # Fecha o cursor

    return membro  # Retorna o membro encontrado


def delete_member(mysql, membro_id):
    # Exclui um membro da tabela 'membro' pelo seu ID
    cur = mysql.connection.cursor()  # Cria um cursor para a execução da consulta SQL
    cur.execute("DELETE FROM membro WHERE id = %s", (membro_id,))  # Executa a exclusão do membro
    mysql.connection.commit()  # Confirma a exclusão no banco de dados
    cur.close()  # Fecha o cursor
