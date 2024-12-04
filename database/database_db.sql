-- Remove o banco de dados existente (caso exista) para evitar conflitos
DROP DATABASE IF EXISTS projeto_gestao;

-- Cria um novo banco de dados chamado "projeto_gestao" com codificação e collation apropriados para suporte a múltiplos idiomas e emojis
CREATE DATABASE projeto_gestao 
    CHARACTER SET utf8mb4  -- Codificação compatível com caracteres especiais e emojis
    COLLATE utf8mb4_unicode_ci;  -- Collation que organiza os dados de forma mais precisa para múltiplos idiomas

-- Seleciona o banco de dados criado para ser usado
USE projeto_gestao;

-- =======================================
-- Tabela `usuários`
-- Armazena informações para autenticação de Usuários: Permitir login e 
-- controle de acesso (diferentes permissões para administradores, gerentes e membros)
-- =======================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    permissao ENUM('administrador', 'gerente', 'membro') NOT NULL DEFAULT 'membro'
);

-- =======================================
-- Tabela `membro`
-- Armazena informações dos membros (usuários do sistema)
-- =======================================
CREATE TABLE IF NOT EXISTS membro (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Chave primária com incremento automático
    nome VARCHAR(100) NOT NULL,         -- Nome do membro, obrigatório
    email VARCHAR(100) NOT NULL UNIQUE  -- Email único e obrigatório
);

-- =======================================
-- Tabela `projeto`
-- Armazena os dados dos projetos
-- =======================================
CREATE TABLE IF NOT EXISTS projeto (
    id INT AUTO_INCREMENT PRIMARY KEY,          -- Chave primária com incremento automático
    nome VARCHAR(100) NOT NULL,                 -- Nome do projeto, obrigatório
    descricao VARCHAR(200) NOT NULL,            -- Descrição do projeto, obrigatório
    data_inicio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Data de início padrão como o momento da criação
    responsavel_id INT NOT NULL,                -- ID do responsável pelo projeto (relacionado à tabela `membro`)
    FOREIGN KEY (responsavel_id) REFERENCES membro(id) -- Chave estrangeira vinculada à tabela `membro`
);

-- =======================================
-- Tabela `tarefa`
-- Armazena as tarefas associadas aos projetos
-- =======================================
CREATE TABLE IF NOT EXISTS tarefa (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- Chave primária com incremento automático
    nome VARCHAR(100) NOT NULL,                  -- Nome da tarefa, obrigatório
    descricao VARCHAR(200) NOT NULL,             -- Descrição da tarefa, obrigatório
    prazo DATETIME NOT NULL,                     -- Prazo de conclusão, obrigatório
    status VARCHAR(50) DEFAULT 'Pendente',       -- Status da tarefa (padrão: Pendente)
    prioridade VARCHAR(50) DEFAULT 'Média',      -- Prioridade da tarefa (padrão: Média)
    projeto_id INT NOT NULL,                     -- ID do projeto associado (relacionado à tabela `projeto`)
    FOREIGN KEY (projeto_id) REFERENCES projeto(id) -- Chave estrangeira vinculada à tabela `projeto`
);

-- =======================================
-- Tabela `projeto_membro`
-- Relacionamento N:M entre projetos e membros
-- =======================================
CREATE TABLE IF NOT EXISTS projeto_membro (
    projeto_id INT NOT NULL,                     -- ID do projeto
    membro_id INT NOT NULL,                      -- ID do membro
    PRIMARY KEY (projeto_id, membro_id),         -- Chave primária composta (projeto_id + membro_id)
    FOREIGN KEY (projeto_id) REFERENCES projeto(id), -- Chave estrangeira para `projeto`
    FOREIGN KEY (membro_id) REFERENCES membro(id)   -- Chave estrangeira para `membro`
);

-- =======================================
-- Inserção de dados de exemplo (opcional)
-- =======================================

-- Adiciona membros fictícios para testes
INSERT INTO membro (nome, email) VALUES 
    ('João Silva', 'joao@exemplo.com'),
    ('Maria Oliveira', 'maria@exemplo.com'),
    ('Carlos Souza', 'carlos@exemplo.com');

-- Adiciona projetos fictícios
INSERT INTO projeto (nome, descricao, responsavel_id) VALUES 
    ('Projeto A', 'Este é o primeiro projeto.', 1),
    ('Projeto B', 'Este é o segundo projeto.', 2);
    ('Projeto C', 'Este é o terceiro projeto.', 3);

-- Adiciona tarefas fictícias associadas aos projetos
INSERT INTO tarefa (nome, descricao, prazo, projeto_id, prioridade) VALUES 
    ('Tarefa 1', 'Descrição da tarefa 1', '2024-12-31 23:59:59', 1, 'Alta'),
    ('Tarefa 2', 'Descrição da tarefa 2', '2024-11-30 23:59:59', 1, 'Média'),
    ('Tarefa 3', 'Descrição da tarefa 3', '2024-12-15 23:59:59', 2, 'Baixa');

-- Relaciona membros a projetos
INSERT INTO projeto_membro (projeto_id, membro_id) VALUES
    (1, 1),  -- João está no Projeto A
    (1, 2),  -- Maria está no Projeto A
    (2, 3);  -- Carlos está no Projeto B