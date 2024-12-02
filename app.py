from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from functions.db_usuario import get_all_users, get_user_by_email, validate_user_password, create_user, update_user
from utils.access_control import permission_required


# Importação da classe Config
from config import Config

# Importação dos módulos responsáveis por funcionalidades específicas
from modules.adicionarMembro import mod_adicionar_membro
from modules.buscar import mod_buscar
from modules.criarMembro import mod_criar_membro
from modules.criarProjeto import mod_criar_projeto
from modules.criarTarefa import mod_criar_tarefa
from modules.deletarProjeto import mod_deletar_projeto
from modules.deletarTarefa import mod_deletar_tarefa
from modules.editarMembro import mod_editar_membro
from modules.editarProjeto import mod_editar_projeto
from modules.editarTarefa import mod_editar_tarefa
from modules.excluirMembro import mod_excluir_membro
from modules.index import mod_index
from modules.listarMembro import mod_listar_membros
from modules.projeto import mod_projeto
from modules.removerMembro import mod_remover_membro
from modules.start import mod_start
from modules.user import User

app = Flask(__name__)  # Inicializa a aplicação Flask
app.secret_key = "sua_chave_secreta"  # Substitua por uma chave segura

# Configurando o Flask-Login
login_manager = LoginManager(app)
# Redireciona para a rota de login quando necessário
login_manager.login_view = "login"


# Configuração do banco de dados MySQL
# Carregar configurações do banco de dados a partir da classe Config
app.config.from_object(Config)

# Inicializa a extensão MySQL
mysql = MySQL(app)

# Configurações globais executadas antes de cada requisição


@app.before_request
def before_request():
    return mod_start(mysql)  # Configurações gerais do ambiente (e.g., charset)

# Rota principal para a página inicial


@app.route('/')
@login_required
def index():
    return mod_index(mysql)  # Redireciona para a função do módulo `index`

# Rota para criar um novo projeto


@app.route('/criar_projeto', methods=['GET', 'POST'])
@login_required
def criar_projeto():
    # Lógica de criação de projeto está no módulo
    return mod_criar_projeto(mysql)

# Rota para editar um projeto existente


@app.route('/editar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def editar_projeto(projeto_id):
    # Chama a lógica de edição no módulo
    return mod_editar_projeto(mysql, projeto_id)

# Rota para deletar um projeto


@app.route('/deletar_projeto/<int:projeto_id>', methods=['POST'])
@login_required
def deletar_projeto(projeto_id):
    # Lógica de exclusão no módulo
    return mod_deletar_projeto(mysql, projeto_id)

# Rota para exibir detalhes de um projeto (tarefas e membros)


@app.route('/projeto/<int:projeto_id>', methods=['GET'])
@login_required
def projeto(projeto_id):
    # Chama a lógica de detalhamento no módulo
    return mod_projeto(mysql, projeto_id)

# Rota para criar uma nova tarefa dentro de um projeto específico


@app.route('/criar_tarefa/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def criar_tarefa(projeto_id):
    return mod_criar_tarefa(mysql, projeto_id)  # Lógica de criação de tarefas

# Rota para editar uma tarefa existente


@app.route('/editar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(tarefa_id):
    # Chama o módulo responsável pela edição
    return mod_editar_tarefa(mysql, tarefa_id)

# Rota para deletar uma tarefa


@app.route('/deletar_tarefa/<int:tarefa_id>', methods=['POST'])
@login_required
def deletar_tarefa(tarefa_id):
    return mod_deletar_tarefa(mysql, tarefa_id)  # Módulo cuida da exclusão

# Rota para criar um novo membro


@app.route('/criar_membro', methods=['GET', 'POST'])
@login_required
def criar_membro():
    return mod_criar_membro(mysql)  # Módulo cuida da criação de membros

# Rota para remover um membro de um projeto


@app.route('/projeto/<int:projeto_id>/remover_membro/<int:membro_id>', methods=['POST'])
@login_required
def remover_membro(projeto_id, membro_id):
    # Chama o módulo de remoção
    return mod_remover_membro(mysql, projeto_id, membro_id)

# Rota para adicionar um membro a um projeto


@app.route('/projeto/<int:projeto_id>/adicionar_membro', methods=['POST'])
@login_required
def adicionar_membro(projeto_id):
    # Lógica de adição no módulo
    return mod_adicionar_membro(mysql, projeto_id)


@app.route('/membros')
@login_required
def listar_membros():
    return mod_listar_membros(mysql)


@app.route('/membros/editar/<int:membro_id>', methods=['GET', 'POST'])
@login_required
def editar_membro(membro_id):
    return mod_editar_membro(mysql, membro_id)


@app.route('/membros/excluir/<int:membro_id>', methods=['POST'])
@login_required
def excluir_membro(membro_id):
    return mod_excluir_membro(mysql, membro_id)


@app.route('/buscar', methods=['GET'])
@login_required
def buscar():
    return mod_buscar(mysql)


@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()

    if user_data:
        return User(user_data['id'], user_data['nome'], user_data['email'], user_data['permissao'])
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user_data = get_user_by_email(mysql, email)

        if user_data and validate_user_password(user_data, senha):
            user = User(user_data['id'], user_data['nome'],
                        user_data['email'], user_data['permissao'])
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('index'))
        else:
            flash("Credenciais inválidas. Tente novamente.", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash("Logout realizado com sucesso!", "success")
    return redirect(url_for('login'))


@app.route('/admin')
@permission_required(['administrador'])
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/gerente')
@permission_required(['administrador', 'gerente'])
def gerente_dashboard():
    return render_template('gerente_dashboard.html')


@app.route('/criar_usuario', methods=['GET', 'POST'])
def criar_usuario():

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']
        
        permissao = request.form.get('permissao', 'membro')

        # Se o usuário atual não for administrador, define a permissão como 'membro'
        #if current_user.permissao != 'administrador':
        #    permissao = 'membro'

        # Verifica se as senhas coincidem
        if senha != confirmar_senha:
            flash("As senhas não coincidem.", "danger")
            return redirect(url_for('criar_usuario'))

         # Verifica se o email já está cadastrado
        if get_user_by_email(mysql, email):
            flash("Email já cadastrado. Faça login.", "danger")
            return redirect(url_for('criar_usuario'))

        # Criptografa a senha e cria o usuário
        hashed_password = generate_password_hash(senha)
        create_user(mysql, nome, email, hashed_password, permissao)

        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for('login'))

    return render_template('criar_usuario.html')


@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    """Página para editar as informações do usuário."""

    # Valida se o usuário tem permissão para editar o perfil
    if current_user.permissao not in ['administrador', 'gerente']:
        flash('Você não tem permissão para editar esse perfil.', 'danger')
        # Redireciona para a página inicial ou outra página
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Obtém os dados do formulário
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        permissao = request.form['permissao']

        # Se a senha foi modificada, gera o hash
        if senha:
            senha_hash = generate_password_hash(senha)
        else:
            senha_hash = current_user.senha  # Mantém a senha atual se não for alterada

        # Chama a função para atualizar os dados no banco
        update_user(mysql, current_user.id, nome, email, senha_hash, permissao)

        # Redireciona para a página inicial ou outra página
        return redirect(url_for('index'))

    # Se for um GET, exibe o formulário de edição com os dados atuais
    return render_template('editar_usuario.html', usuario=current_user)


@app.route('/listar_user')
@login_required
def listar_user():
    # Verifica se o usuário tem permissão
    if current_user.permissao not in ['administrador', 'gerente']:
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('index'))

    # Busca todos os usuários do banco de dados
    usuarios = get_all_users(mysql)
    return render_template('listar_user.html', usuarios=usuarios)


@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    if current_user.permissao not in ['administrador', 'gerente']:
        flash("Você não tem permissão para editar usuários.", "danger")
        return redirect(url_for('listar_user'))

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT id, nome, email, permissao FROM usuarios WHERE id = %s", (usuario_id,))
    usuario = cur.fetchone()
    cur.close()

    if not usuario:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for('listar_user'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        permissao = request.form['permissao']

        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE usuarios SET nome = %s, email = %s, permissao = %s WHERE id = %s",
            (nome, email, permissao, usuario_id),
        )
        mysql.connection.commit()
        cur.close()

        flash("Usuário atualizado com sucesso.", "success")
        return redirect(url_for('listar_user'))

    return render_template('editar_usuario.html', usuario=usuario)


# Inicia o servidor Flask no modo de depuração
if __name__ == "__main__":
    app.run(debug=True)
