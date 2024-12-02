from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nome, email, permissao):
        self.id = id
        self.nome = nome
        self.email = email
        self.permissao = permissao
