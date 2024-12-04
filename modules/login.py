# Importações necessárias para lidar com sessões, mensagens de feedback, templates, e métodos de autenticação
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user  # Função para gerenciar login de usuários na sessão atual
from functions.db_usuario import get_user_by_email, validate_user_password  # Funções para acessar e validar dados do banco de dados
from modules.user import User  # Classe representando o modelo de um usuário autenticado

# Função principal que gerencia o processo de login
def mod_login(mysql):
    # Verifica se o método da requisição é POST (ou seja, o formulário foi submetido)
    if request.method == 'POST':
        # Obtém os dados enviados pelo formulário de login
        email = request.form['email']  # E-mail digitado pelo usuário
        senha = request.form['senha']  # Senha digitada pelo usuário

        # Obtém as informações do usuário a partir do banco de dados usando o e-mail
        user_data = get_user_by_email(mysql, email)

        # Se o usuário foi encontrado e a senha fornecida é válida
        if user_data and validate_user_password(user_data, senha):
            # Cria uma instância do usuário autenticado com as informações obtidas
            user = User(user_data['id'], user_data['nome'],
                        user_data['email'], user_data['permissao'])

            # Registra o usuário como logado usando Flask-Login
            login_user(user)

            # Adiciona uma mensagem de sucesso que será exibida na próxima página
            flash("Login realizado com sucesso!", "success")

            # Redireciona o usuário para a página principal (index)
            return redirect(url_for('index'))
        else:
            # Caso as credenciais sejam inválidas, exibe uma mensagem de erro
            flash("Credenciais inválidas. Tente novamente.", "danger")

    # Renderiza o template de login caso o método seja GET ou as credenciais sejam inválidas
    return render_template('login.html')
