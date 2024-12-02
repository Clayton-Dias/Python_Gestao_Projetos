from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

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

app = Flask(__name__)  # Inicializa a aplicação Flask

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
def index():
    return mod_index(mysql)  # Redireciona para a função do módulo `index`

# Rota para criar um novo projeto
@app.route('/criar_projeto', methods=['GET', 'POST'])
def criar_projeto():
    return mod_criar_projeto(mysql)  # Lógica de criação de projeto está no módulo

# Rota para editar um projeto existente
@app.route('/editar_projeto/<int:projeto_id>', methods=['GET', 'POST'])
def editar_projeto(projeto_id):
    return mod_editar_projeto(mysql, projeto_id)  # Chama a lógica de edição no módulo

# Rota para deletar um projeto
@app.route('/deletar_projeto/<int:projeto_id>', methods=['POST'])
def deletar_projeto(projeto_id):
    return mod_deletar_projeto(mysql, projeto_id)  # Lógica de exclusão no módulo

# Rota para exibir detalhes de um projeto (tarefas e membros)
@app.route('/projeto/<int:projeto_id>', methods=['GET'])
def projeto(projeto_id):
    return mod_projeto(mysql, projeto_id)  # Chama a lógica de detalhamento no módulo

# Rota para criar uma nova tarefa dentro de um projeto específico
@app.route('/criar_tarefa/<int:projeto_id>', methods=['GET', 'POST'])
def criar_tarefa(projeto_id):
    return mod_criar_tarefa(mysql, projeto_id)  # Lógica de criação de tarefas

# Rota para editar uma tarefa existente
@app.route('/editar_tarefa/<int:tarefa_id>', methods=['GET', 'POST'])
def editar_tarefa(tarefa_id):
    return mod_editar_tarefa(mysql, tarefa_id)  # Chama o módulo responsável pela edição

# Rota para deletar uma tarefa
@app.route('/deletar_tarefa/<int:tarefa_id>', methods=['POST'])
def deletar_tarefa(tarefa_id):
    return mod_deletar_tarefa(mysql, tarefa_id)  # Módulo cuida da exclusão

# Rota para criar um novo membro
@app.route('/criar_membro', methods=['GET', 'POST'])
def criar_membro():
    return mod_criar_membro(mysql)  # Módulo cuida da criação de membros

# Rota para remover um membro de um projeto
@app.route('/projeto/<int:projeto_id>/remover_membro/<int:membro_id>', methods=['POST'])
def remover_membro(projeto_id, membro_id):
    return mod_remover_membro(mysql, projeto_id, membro_id)  # Chama o módulo de remoção

# Rota para adicionar um membro a um projeto
@app.route('/projeto/<int:projeto_id>/adicionar_membro', methods=['POST'])
def adicionar_membro(projeto_id):
    return mod_adicionar_membro(mysql, projeto_id)  # Lógica de adição no módulo

@app.route('/membros')
def listar_membros():
    return mod_listar_membros(mysql)

@app.route('/membros/editar/<int:membro_id>', methods=['GET', 'POST'])
def editar_membro(membro_id):
    return mod_editar_membro(mysql, membro_id)

@app.route('/membros/excluir/<int:membro_id>', methods=['POST'])
def excluir_membro(membro_id):
    return mod_excluir_membro(mysql, membro_id)

@app.route('/buscar', methods=['GET'])
def buscar():
    return mod_buscar(mysql)

# Inicia o servidor Flask no modo de depuração
if __name__ == "__main__":
    app.run(debug=True)
