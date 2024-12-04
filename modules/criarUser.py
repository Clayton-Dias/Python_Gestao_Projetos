from flask import flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash
from functions.db_usuario import create_user, get_user_by_email


def mod_criar_usuario(mysql):

    # Verifica se a requisição é do tipo POST, ou seja, se o formulário foi submetido
    if request.method == 'POST':
        # Obtém os valores enviados pelo formulário
        nome = request.form['nome']  # Nome do usuário
        email = request.form['email']  # Email do usuário
        senha = request.form['senha']  # Senha fornecida pelo usuário
        confirmar_senha = request.form['confirmar_senha']  # Confirmação da senha

        # Obtém a permissão enviada pelo formulário; se não for fornecida, define 'membro' como padrão
        permissao = request.form.get('permissao', 'membro')

        # (Comentado) Se o usuário atual não for administrador, força a permissão como 'membro'
        # Essa lógica está desativada, mas seria útil se apenas administradores pudessem definir permissões
        # if current_user.permissao != 'administrador':
        #     permissao = 'membro'

        # Valida se as senhas fornecidas coincidem
        if senha != confirmar_senha:
            # Exibe uma mensagem de erro ao usuário
            flash("As senhas não coincidem.", "danger")
            # Redireciona de volta para a página de criação de usuário
            return redirect(url_for('criar_usuario'))

        # Verifica se o email fornecido já está cadastrado no banco de dados
        if get_user_by_email(mysql, email):
            # Exibe uma mensagem de erro indicando que o email já está registrado
            flash("Email já cadastrado. Faça login.", "danger")
            # Redireciona para a página de criação de usuário
            return redirect(url_for('criar_usuario'))

        # Criptografa a senha fornecida pelo usuário para armazenamento seguro no banco de dados
        hashed_password = generate_password_hash(senha)

        # Chama a função para criar o novo usuário no banco de dados com os dados fornecidos
        create_user(mysql, nome, email, hashed_password, permissao)

        # Exibe uma mensagem de sucesso informando que a conta foi criada
        flash("Conta criada com sucesso! Faça login.", "success")
        # Redireciona para a página de login
        return redirect(url_for('login'))

    # Se a requisição for GET, renderiza a página de criação de usuário
    return render_template('criar_usuario.html')
