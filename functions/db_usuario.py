from werkzeug.security import check_password_hash

def create_user(mysql, nome, email, senha, permissao):
    """Cria um novo usuário no banco de dados."""
    
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO usuarios (nome, email, senha, permissao) VALUES (%s, %s, %s, %s)",
        (nome, email, senha, permissao)
    )
    mysql.connection.commit()
    cur.close()

def get_user_by_email(mysql, email):
    """Obtém os dados do usuário pelo email."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user

def validate_user_password(user_data, senha):
    """Valida a senha do usuário."""
    return check_password_hash(user_data['senha'], senha)

def update_user(mysql, user_id, nome, email, senha_hash, permissao):
    """Atualiza os dados do usuário no banco de dados."""
    cur = mysql.connection.cursor()
    
    cur.execute("""
        UPDATE usuarios 
        SET nome = %s, email = %s, senha = %s, permissao = %s 
        WHERE id = %s
    """, (nome, email, senha_hash, permissao, user_id))
    
    mysql.connection.commit()
    cur.close()

def get_all_users(mysql):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nome, email, permissao FROM usuarios ORDER BY nome ASC")
    usuarios = cur.fetchall()
    cur.close()
    return usuarios
