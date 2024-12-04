
```markdown
# Projeto Final do curso de Programação Python do SENAC.

# Sistema de Gestão de Projetos com Flask

Este é um sistema de gestão de projetos desenvolvido com **Flask** e **MySQL**, projetado para atender diferentes perfis de usuários (administradores, gerentes e membros). Ele permite gerenciar usuários, projetos, tarefas e equipes de forma simples e eficiente.

## 🚀 Funcionalidades

### 📂 Gestão de Usuários
- Criação, edição e exclusão de usuários.
- Atribuição de permissões (Administrador, Gerente, Membro).
- Sistema de login seguro com controle de acesso baseado em permissões.
- Edição de perfil para atualização de informações pessoais.

### 🗂️ Gestão de Projetos e Tarefas
- Criação, edição e exclusão de projetos.
- Gerenciamento de tarefas associadas a projetos.
- Adição e remoção de membros nos projetos.
- Painel de visualização detalhado para cada projeto.

### 📊 Painéis Personalizados
- **Painel do Administrador**:
  - Estatísticas gerais (número de usuários, projetos, etc.).
  - Gerenciamento completo dos usuários do sistema.
- **Painel do Gerente**:
  - Exibição de projetos gerenciados.
  - Listagem de tarefas e membros relacionados.
- **Painel de Membros**:
  - Visualização das tarefas atribuídas.

### 🔎 Funcionalidades Adicionais
- Busca e filtro de projetos, tarefas e membros.
- Mensagens flash para feedback do usuário (sucesso ou erro).

---

## 🛠️ Tecnologias Utilizadas
- **Python**: Framework Flask para desenvolvimento web.
- **MySQL**: Banco de dados relacional.
- **Bootstrap**: Para estilização e design responsivo.
- **Flask-Login**: Controle de autenticação e sessões.
- **Jinja2**: Motor de templates para renderização das páginas.
- **Werkzeug**: Segurança e gerenciamento de requisições HTTP.

---

## ⚙️ Instalação e Configuração

### Pré-requisitos
- Python 3.9 ou superior.
- MySQL Server.
- Pipenv (opcional, para gerenciar ambientes virtuais).

### Passo a passo

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-gestao-projetos.git
   cd sistema-gestao-projetos
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o banco de dados:
   - Crie um banco de dados no MySQL com o nome desejado.
   - Atualize as configurações de conexão no arquivo `config.py`.

5. Execute as migrações para criar as tabelas:
   ```bash
   python scripts/create_tables.py
   ```

6. Inicie o servidor:
   ```bash
   python app.py
   ```

7. Acesse o sistema no navegador:
   ```
   http://127.0.0.1:5000
   ```

---

## 📁 Estrutura do Projeto

```
sistema-gestao-projetos/
│
├── app.py                     # Arquivo principal da aplicação
├── config.py                  # Configurações globais da aplicação
├── modules/                   # Lógica modular do sistema
│   ├── adminDashboard.py      # Painel do administrador
│   ├── criarUser.py           # Criação de usuários
│   ├── editUser.py            # Edição de usuários
│   ├── ...
│
├── static/                    # Arquivos estáticos (CSS, JS, imagens)
├── templates/                 # Templates HTML do sistema
│   ├── _layout.html           # Layout base
│   ├── login.html             # Página de login
│   ├── admin_dashboard.html   # Painel do administrador
│   ├── ...
│
├── utils/                     # Funções auxiliares
│   ├── access_control.py      # Controle de permissões
│   ├── db_utils.py            # Conexões com o banco de dados
│
└── requirements.txt           # Dependências do projeto
```

---

## 🛡️ Controle de Acesso

O sistema possui controle de acesso baseado em permissões. Algumas rotas e funcionalidades são exclusivas para determinados perfis:

- **Administrador**:
  - Acesso ao painel administrativo.
  - Gerenciamento completo de usuários e projetos.
- **Gerente**:
  - Gerenciamento de projetos e equipes.
- **Membro**:
  - Visualização e gerenciamento de tarefas atribuídas.

---

## 📈 Próximos Passos

- Implementar relatórios automáticos de progresso.
- Notificações por e-mail para eventos importantes.
- Suporte multilíngue para usuários internacionais.
- Melhorar a interface para dispositivos móveis.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Faça o commit das alterações:
   ```bash
   git commit -m "Minha nova feature"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

---

## 📝 Licença

Este projeto está licenciado sob a licença **MIT**. Consulte o arquivo `LICENSE` para mais informações.

---

---
```