from flask import request


def get_member(mysql):
    # Retorna todos os membros da tabela 'membro'
    sql = "SELECT * FROM membro ORDER BY nome"
    cur = mysql.connection.cursor()
    cur.execute(sql)
    membros = cur.fetchall()  # Recupera todos os resultados
    cur.close()
    return membros  # Retorna a lista de membros


def get_member_by_project(mysql, projeto_id):
    # Retorna os membros associados a um projeto específico
    sql = '''
        SELECT m.id, m.nome, m.email 
        FROM membro m
        INNER JOIN projeto_membro pm ON m.id = pm.membro_id
        WHERE pm.projeto_id = %s
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, [projeto_id])  # Filtra pelo ID do projeto
    membros = cur.fetchall()
    cur.close()
    return membros  # Retorna a lista de membros associados ao projeto


def get_member_available(mysql, projeto_id):
    # Retorna os membros que não estão associados ao projeto
    sql = '''
        SELECT id, nome FROM membro
        WHERE id NOT IN (SELECT membro_id FROM projeto_membro WHERE projeto_id = %s)
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, [projeto_id])  # Filtra pelo ID do projeto
    membros = cur.fetchall()
    cur.close()
    return membros  # Retorna a lista de membros disponíveis


def create_member(mysql):
    # Adiciona um novo membro à tabela 'membro'
    sql = "INSERT INTO membro (nome, email) VALUES (%s, %s)"
    cur = mysql.connection.cursor()
    # Dados fornecidos via formulário
    cur.execute(sql, (request.form['nome'], request.form['email']))
    mysql.connection.commit()  # Confirma a transação
    cur.close()


def remove_membro_by_project(mysql, projeto_id, membro_id):
    # Remove um membro de um projeto específico
    sql = 'DELETE FROM projeto_membro WHERE projeto_id = %s AND membro_id = %s'
    cur = mysql.connection.cursor()
    # Identifica o membro e o projeto
    cur.execute(sql, (projeto_id, membro_id))
    mysql.connection.commit()  # Confirma a remoção
    cur.close()


def add_member_to_project(mysql, projeto_id):
    # Adiciona um membro a um projeto, evitando duplicação
    cur = mysql.connection.cursor()

    # Verifica se o membro já está associado ao projeto
    cur.execute('SELECT * FROM projeto_membro WHERE projeto_id = %s AND membro_id = %s',
                (projeto_id, request.form['membro_id']))
    membro_existente = cur.fetchone()  # Retorna o membro se ele já estiver associado

    if not membro_existente:
        # Se o membro não estiver associado, insere na relação projeto-membro
        cur.execute('INSERT INTO projeto_membro (projeto_id, membro_id) VALUES (%s, %s)',
                    (projeto_id, request.form['membro_id']))
        mysql.connection.commit()  # Confirma a adição

    cur.close()  # Fecha o cursor


def edit_member(mysql, membro_id):

    sql = '''
        UPDATE membro SET nome = %s, email = %s WHERE id = %s
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (request.form['nome'], request.form['email'], membro_id))
    mysql.connection.commit()
    cur.close()


def get_member_by_id(mysql, membro_id):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM membro WHERE id = %s", (membro_id,))
    membro = cur.fetchone()
    cur.close()

    return membro


def delete_member(mysql, membro_id):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM membro WHERE id = %s", (membro_id,))
    mysql.connection.commit()
    cur.close()

