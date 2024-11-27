from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# Configuração do banco de dados MySQL
app.config.update(
    MYSQL_HOST='localhost',         # Servidor MySQL
    MYSQL_USER='root',              # Usuário MySQL
    MYSQL_PASSWORD='',              # Senha do MySQL
    MYSQL_DB='projeto_gestao',      # Nome da base de dados
    MYSQL_CURSORCLASS='DictCursor', # Retorna dados como dicionário
    MYSQL_CHARSET='utf8mb4',        # Suporte completo a Unicode
    MYSQL_USE_UNICODE=True          # Converte caracteres para Unicode
)

# Inicializa a extensão MySQL
mysql = MySQL(app)

# Configura a conexão para UTF-8 e português do Brasil antes de cada requisição
@app.before_request
def before_request():
    cur = mysql.connection.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")
    cur.execute("SET lc_time_names = 'pt_BR'")
    cur.close()

# Rota principal: listar todos os projetos
@app.route('/')
def index():
    sql = '''
        SELECT p.id, p.nome, p.descricao, p.data_inicio, m.nome AS responsavel_nome
        FROM projeto p
        JOIN membro m ON p.responsavel_id = m.id;
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql)
    projetos = cur.fetchall()
    cur.close()
    return render_template('index.html', projetos=projetos)

# Rota para criar um novo projeto
@app.route('/criar_projeto', methods=['GET', 'POST'])
def criar_projeto():

    if request.method == 'POST':  # Lógica de inserção de projeto
        nome = request.form['nome']
        descricao = request.form['descricao']
        responsavel_id = request.form['responsavel_id']

        sql = '''
            INSERT INTO projeto (nome, descricao, responsavel_id, data_inicio)
            VALUES (%s, %s, %s, %s)
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (nome, descricao, responsavel_id, datetime.utcnow()))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    # Seleciona membros para atribuir ao projeto
    sql = "SELECT * FROM membro"
    cur = mysql.connection.cursor()
    cur.execute(sql)
    membros = cur.fetchall()
    cur.close()

    return render_template('criar_projeto.html', membros=membros)

# Rota para editar um projeto existente
@app.route('/editar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
def editar_projeto(projeto_id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':  # Lógica de atualização
        nome = request.form['nome']
        descricao = request.form['descricao']
        responsavel_id = request.form['responsavel_id']
        sql = '''
            UPDATE projeto 
            SET nome = %s, descricao = %s, responsavel_id = %s 
            WHERE id = %s
        '''
        cur.execute(sql, (nome, descricao, responsavel_id, projeto_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    # Obtem detalhes do projeto e membros para edição
    cur.execute("SELECT * FROM projeto WHERE id = %s", [projeto_id])
    projeto = cur.fetchone()
    cur.execute("SELECT * FROM membro")
    membros = cur.fetchall()
    cur.close()
    return render_template('editar_projeto.html', projeto=projeto, membros=membros)

# Rota para criar uma tarefa em um projeto específico
@app.route('/criar_tarefa/<int:projeto_id>', methods=['GET', 'POST'])
def criar_tarefa(projeto_id):
    if request.method == 'POST':  # Lógica de inserção de tarefa
        nome = request.form['nome']
        descricao = request.form['descricao']
        prazo = datetime.strptime(request.form['prazo'], '%Y-%m-%d')
        prioridade = request.form['prioridade']

        sql = '''
            INSERT INTO tarefa (nome, descricao, prazo, prioridade, projeto_id)
            VALUES (%s, %s, %s, %s, %s)
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (nome, descricao, prazo, prioridade, projeto_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('projeto', projeto_id=projeto_id))

    return render_template('criar_tarefa.html', projeto_id=projeto_id)

# Rota para editar uma tarefa existente
@app.route('/editar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
def editar_tarefa(tarefa_id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':  # Lógica de atualização de tarefa
        nome = request.form['nome']
        descricao = request.form['descricao']
        prazo_str = request.form['prazo'].split('T')[0]  # Remove o sufixo 'T00:00'
        prazo = datetime.strptime(prazo_str, '%Y-%m-%d')
        prioridade = request.form['prioridade']
        status = request.form['status']

        sql = '''
            UPDATE tarefa 
            SET nome = %s, descricao = %s, prazo = %s, prioridade = %s, status = %s 
            WHERE id = %s
        '''
        cur.execute(sql, (nome, descricao, prazo, prioridade, status, tarefa_id))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('projeto', projeto_id=request.form['projeto_id']))

    # Obtem detalhes da tarefa para edição
    sql = "SELECT * FROM tarefa WHERE id = %s"
    cur.execute(sql, [tarefa_id])
    tarefa = cur.fetchone()
    cur.close()
    
    return render_template('editar_tarefa.html', tarefa=tarefa)

# Rota para detalhes do projeto (tarefas e membros)
@app.route('/projeto/<int:projeto_id>', methods=['GET'])
def projeto(projeto_id):
    cur = mysql.connection.cursor()
    
    # Listagem de tarefas agrupadas por status
    cur.execute("SELECT * FROM tarefa WHERE projeto_id = %s AND status = 'Pendente'", [projeto_id])
    tarefas_pendentes = cur.fetchall()

    cur.execute("SELECT * FROM tarefa WHERE projeto_id = %s AND status = 'Em andamento'", [projeto_id])
    tarefas_andamento = cur.fetchall()

    cur.execute("SELECT * FROM tarefa WHERE projeto_id = %s AND status = 'Concluída'", [projeto_id])
    tarefas_concluidas = cur.fetchall()

    # Membros associados ao projeto
    cur.execute("""
        SELECT m.id, m.nome, m.email 
        FROM membro m
        INNER JOIN projeto_membro pm ON m.id = pm.membro_id
        WHERE pm.projeto_id = %s
    """, [projeto_id])
    membros = cur.fetchall()

    # Detalhes do projeto
    cur.execute("SELECT * FROM projeto WHERE id = %s", [projeto_id])
    projeto = cur.fetchone()
    cur.close()

    
    page = {
        "projeto": projeto,
        "pendentes": tarefas_pendentes,
        "andamento": tarefas_andamento,
        "concluidas" :tarefas_concluidas,
        "membros": membros
    }
    return render_template('projeto_detalhes.html', page=page)

# Rota para criar um novo membro
@app.route('/criar_membro', methods=['GET', 'POST'])
def criar_membro():
    if request.method == 'POST':  # Lógica de inserção de membro
        nome = request.form['nome']
        email = request.form['email']

        sql = "INSERT INTO membro (nome, email) VALUES (%s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(sql, (nome, email))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    
    return render_template('membro.html')

# Inicia o servidor
if __name__ == "__main__":
    app.run(debug=True)
