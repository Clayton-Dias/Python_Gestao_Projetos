from flask import request
from werkzeug.security import check_password_hash

from modules.user import User


def create_user(mysql, nome, email, senha, permissao):
    """Cria um novo usuário no banco de dados."""
    cur = mysql.connection.cursor()
    # Executa o SQL para inserir um novo usuário na tabela 'usuarios'
    cur.execute(
        "INSERT INTO usuarios (nome, email, senha, permissao) VALUES (%s, %s, %s, %s)",
        (nome, email, senha, permissao)
    )
    mysql.connection.commit()  # Confirma a transação no banco de dados
    cur.close()  # Fecha o cursor


def get_user_by_email(mysql, email):
    """Obtém os dados do usuário pelo email."""
    cur = mysql.connection.cursor()
    # Executa a consulta para buscar o usuário com o email especificado
    cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cur.fetchone()  # Obtém o primeiro registro encontrado
    cur.close()  # Fecha o cursor
    return user  # Retorna os dados do usuário


def validate_user_password(user_data, senha):
    """Valida a senha do usuário usando a senha armazenada no banco e a senha fornecida."""
    return check_password_hash(user_data['senha'], senha)  # Valida a senha usando o hash


def update_user(mysql, user_id, nome, email, senha_hash, permissao):
    """Atualiza os dados do usuário no banco de dados."""
    cur = mysql.connection.cursor()
    # Executa a consulta SQL para atualizar os dados de um usuário específico
    cur.execute("""
        UPDATE usuarios 
        SET nome = %s, email = %s, senha = %s, permissao = %s 
        WHERE id = %s
    """, (nome, email, senha_hash, permissao, user_id))

    mysql.connection.commit()  # Confirma a transação no banco de dados
    cur.close()  # Fecha o cursor


def get_all_users(mysql):
    """Obtém todos os usuários do banco de dados, ordenados por nome."""
    cur = mysql.connection.cursor()
    # Executa a consulta SQL para obter todos os usuários, ordenados por nome
    cur.execute(
        "SELECT id, nome, email, permissao FROM usuarios ORDER BY nome ASC")
    usuarios = cur.fetchall()  # Recupera todos os registros encontrados
    cur.close()  # Fecha o cursor
    return usuarios  # Retorna a lista de usuários


def get_load_user(mysql, user_id):
    """Obtém os dados completos de um usuário pelo ID e retorna um objeto User."""
    cur = mysql.connection.cursor()
    # Executa a consulta SQL para obter os dados do usuário pelo ID
    cur.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    user_data = cur.fetchone()  # Obtém os dados do usuário
    cur.close()  # Fecha o cursor

    if user_data:
        # Retorna um objeto User se os dados forem encontrados
        return User(user_data['id'], user_data['nome'], user_data['email'], user_data['permissao'])
    return None  # Retorna None caso o usuário não exista


def get_user_by_id(mysql, usuario_id):
    """Obtém um usuário pelo ID."""
    sql = '''
        SELECT id, nome, email, permissao FROM usuarios WHERE id = %s
    '''
    cur = mysql.connection.cursor()
    # Executa a consulta para buscar o usuário pelo ID
    cur.execute(sql, (usuario_id,))
    usuario = cur.fetchone()  # Obtém o primeiro registro encontrado
    cur.close()  # Fecha o cursor
    return usuario  # Retorna os dados do usuário


def update_user_by_id(mysql, usuario_id):
    """Atualiza os dados de um usuário pelo ID."""
    sql = '''
        UPDATE usuarios SET nome = %s, email = %s, permissao = %s WHERE id = %s
    '''
    cur = mysql.connection.cursor()
    # Executa a consulta para atualizar os dados do usuário com base no ID
    cur.execute(sql, (request.form['nome'], request.form['email'], request.form['permissao'], usuario_id))
    mysql.connection.commit()  # Confirma a transação no banco de dados
    cur.close()  # Fecha o cursor


def count_usuarios_por_permissao(mysql, permissao):
    """Conta o número de usuários com uma permissão específica."""
    try:
        sql = "SELECT COUNT(*) FROM usuarios WHERE permissao = %s"
        cur = mysql.connection.cursor()
        # Executa a consulta para contar o número de usuários com a permissão fornecida
        cur.execute(sql, (permissao,))
        result = cur.fetchone()  # Obtém o resultado da contagem
        return result[0]  # Retorna o número de usuários
    except Exception as e:
        print(f"Erro ao contar usuários por permissão: {e}")
        return 0  # Retorna 0 caso ocorra algum erro
    finally:
        cur.close()  # Fecha o cursor


def count_usuarios(mysql):
    """Conta o número total de usuários no banco de dados."""
    sql = "SELECT COUNT(*) AS total FROM usuarios"
    cur = mysql.connection.cursor()
    # Executa a consulta para contar o número total de usuários
    cur.execute(sql)
    result = cur.fetchone()  # Obtém o resultado da contagem
    cur.close()  # Fecha o cursor
    return result['total']  # Retorna o número total de usuários


def get_usuarios_recentes(mysql, limite=5):
    """Obtém os usuários mais recentes, limitando o número de resultados."""
    sql = """
            SELECT * FROM usuarios
            ORDER BY criado_em DESC
            LIMIT %s
        """
    cur = mysql.connection.cursor()
    # Executa a consulta para obter os usuários mais recentes com um limite especificado
    cur.execute(sql, (limite,))
    usuarios = cur.fetchall()  # Recupera os resultados
    cur.close()  # Fecha o cursor
    return usuarios  # Retorna a lista de usuários recentes
