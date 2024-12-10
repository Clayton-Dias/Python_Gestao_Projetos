from werkzeug.security import generate_password_hash
import mysql.connector

# Gerar hashes das senhas
senha_admin = generate_password_hash('123456', method='pbkdf2:sha256', salt_length=8)
senha_gerente = generate_password_hash('123456', method='pbkdf2:sha256', salt_length=8)
senha_membro = generate_password_hash('123456', method='pbkdf2:sha256', salt_length=8)

# Conectar ao banco de dados
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='projeto_gestao'
)
cursor = conexao.cursor()

# Inserir os usuários com hash
cursor.execute("""
    INSERT INTO usuarios (nome, email, senha, permissao) 
    VALUES (%s, %s, %s, %s)
""", ('admin', 'admin@example.com', senha_admin, 'administrador'))

cursor.execute("""
    INSERT INTO usuarios (nome, email, senha, permissao) 
    VALUES (%s, %s, %s, %s)
""", ('gerente', 'gerente@example.com', senha_gerente, 'gerente'))

cursor.execute("""
    INSERT INTO usuarios (nome, email, senha, permissao) 
    VALUES (%s, %s, %s, %s)
""", ('membro', 'membro@example.com', senha_membro, 'membro'))

# Confirmar e fechar a conexão
conexao.commit()
cursor.close()
conexao.close()
