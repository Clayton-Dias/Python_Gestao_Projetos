from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import logout_user, login_required, LoginManager
from modules.adminDashboard import mod_admin_dashboard
from modules.criarUser import mod_criar_usuario
from modules.editUser import mod_editar_usuario
from modules.editarPerfil import mod_editar_perfil
from modules.listarUser import mod_listar_user
from modules.loadUser import mod_load_user
from modules.login import mod_login
from utils.access_control import permission_required


# Importação da classe Config, que contém as configurações do projeto
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

# Inicializa a aplicação Flask
app = Flask(__name__)
app.secret_key = "sua_chave_secreta"  # Chave secreta para a sessão do Flask, substitua por algo seguro

# Configurações do Flask-Login para gerenciamento de usuários
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redireciona para a página de login se o usuário não estiver autenticado

# Configuração do banco de dados MySQL com base nas configurações da classe Config
app.config.from_object(Config)

# Inicializa a extensão MySQL
mysql = MySQL(app)

# Configurações executadas antes de cada requisição
@app.before_request
def before_request():
    return mod_start(mysql)  # Configurações gerais (e.g., charset) antes de cada requisição

# Rota principal da aplicação, exibe a página inicial
@app.route('/')
@login_required
def index():
    return mod_index(mysql)  # Chama a função do módulo `index` para renderizar a página inicial

# Rota para criar um novo projeto
@app.route('/criar_projeto', methods=['GET', 'POST'])
@login_required
def criar_projeto():
    return mod_criar_projeto(mysql)  # Chama a lógica de criação de projeto no módulo

# Rota para editar um projeto existente, recebe o ID do projeto
@app.route('/editar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def editar_projeto(projeto_id):
    return mod_editar_projeto(mysql, projeto_id)  # Chama a lógica de edição de projeto no módulo

# Rota para deletar um projeto, recebe o ID do projeto
@app.route('/deletar_projeto/<int:projeto_id>', methods=['POST'])
@login_required
def deletar_projeto(projeto_id):
    return mod_deletar_projeto(mysql, projeto_id)  # Chama a lógica de exclusão de projeto no módulo

# Rota para exibir detalhes de um projeto, como tarefas e membros
@app.route('/projeto/<int:projeto_id>', methods=['GET'])
@login_required
def projeto(projeto_id):
    return mod_projeto(mysql, projeto_id)  # Chama a função para detalhar o projeto no módulo

# Rota para criar uma nova tarefa dentro de um projeto específico
@app.route('/criar_tarefa/<int:projeto_id>', methods=['GET', 'POST'])
@login_required
def criar_tarefa(projeto_id):
    return mod_criar_tarefa(mysql, projeto_id)  # Chama o módulo responsável pela criação de tarefas

# Rota para editar uma tarefa existente
@app.route('/editar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(tarefa_id):
    return mod_editar_tarefa(mysql, tarefa_id)  # Chama a função de edição de tarefa

# Rota para deletar uma tarefa, recebe o ID da tarefa
@app.route('/deletar_tarefa/<int:tarefa_id>', methods=['POST'])
@login_required
def deletar_tarefa(tarefa_id):
    return mod_deletar_tarefa(mysql, tarefa_id)  # Chama o módulo de exclusão de tarefa

# Rota para criar um novo membro
@app.route('/criar_membro', methods=['GET', 'POST'])
@login_required
def criar_membro():
    return mod_criar_membro(mysql)  # Chama o módulo de criação de membros

# Rota para remover um membro de um projeto específico
@app.route('/projeto/<int:projeto_id>/remover_membro/<int:membro_id>', methods=['POST'])
@login_required
def remover_membro(projeto_id, membro_id):
    return mod_remover_membro(mysql, projeto_id, membro_id)  # Chama o módulo de remoção de membro

# Rota para adicionar um membro a um projeto específico
@app.route('/projeto/<int:projeto_id>/adicionar_membro', methods=['POST'])
@login_required
def adicionar_membro(projeto_id):
    return mod_adicionar_membro(mysql, projeto_id)  # Chama o módulo de adição de membro

# Rota para listar todos os membros
@app.route('/membros')
@login_required
def listar_membros():
    return mod_listar_membros(mysql)  # Chama o módulo de listagem de membros

# Rota para editar os detalhes de um membro específico
@app.route('/membros/editar/<int:membro_id>', methods=['GET', 'POST'])
@login_required
def editar_membro(membro_id):
    return mod_editar_membro(mysql, membro_id)  # Chama a função de edição de membro

# Rota para excluir um membro
@app.route('/membros/excluir/<int:membro_id>', methods=['POST'])
@login_required
def excluir_membro(membro_id):
    return mod_excluir_membro(mysql, membro_id)  # Chama o módulo de exclusão de membro

# Rota para buscar projetos ou tarefas com filtros
@app.route('/buscar', methods=['GET'])
@login_required
def buscar():
    return mod_buscar(mysql)  # Chama a lógica de busca no módulo

# Função do Flask-Login para carregar um usuário baseado no ID
@login_manager.user_loader
def load_user(user_id):
    return mod_load_user(mysql, user_id)

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return mod_login(mysql)  # Chama a lógica de login no módulo

# Rota de logout, que encerra a sessão do usuário
@app.route('/logout')
def logout():
    logout_user()  # Encerra a sessão do usuário
    flash("Logout realizado com sucesso!", "success")  # Exibe uma mensagem de sucesso
    return redirect(url_for('login'))  # Redireciona para a página de login

# Rota para o painel de administração, acessível apenas por administradores
@app.route('/admin')
@permission_required(['administrador'])
def admin_dashboard():
    return mod_admin_dashboard(mysql)  # Chama o painel de administração

# Rota para o painel de gerente, acessível por administradores e gerentes
@app.route('/gerente')
@permission_required(['administrador', 'gerente'])
def gerente_dashboard():
    return render_template('gerente_dashboard.html')  # Renderiza o painel do gerente

# Rota para criar um novo usuário
@app.route('/criar_usuario', methods=['GET', 'POST'])
def criar_usuario():
    return mod_criar_usuario(mysql)  # Chama a lógica de criação de usuário

# Rota para editar o perfil de um usuário
@app.route('/editar_perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    return mod_editar_perfil(mysql)  # Chama a função de edição de perfil do usuário

# Rota para listar todos os usuários
@app.route('/listar_user')
@login_required
def listar_user():
    return mod_listar_user(mysql)  # Chama a listagem de usuários

# Rota para editar um usuário específico
@app.route('/editar_usuario/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    return mod_editar_usuario(mysql, usuario_id)  # Chama a função de edição de usuário

# Inicia o servidor Flask em modo de depuração
if __name__ == "__main__":
    app.run(debug=True)
