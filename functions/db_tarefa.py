from datetime import datetime
from flask import request

def create_task(mysql, projeto_id):
    # Obtém o prazo enviado no formulário e converte para o formato datetime
    prazo = datetime.strptime(request.form['prazo'], '%Y-%m-%d')

    # SQL para inserir uma nova tarefa associada ao projeto
    sql = '''
            INSERT INTO tarefa (nome, descricao, prazo, prioridade, projeto_id)
            VALUES (%s, %s, %s, %s, %s)
        '''
    cur = mysql.connection.cursor()  # Cria um cursor para executar a consulta
    # Executa o comando SQL com os valores fornecidos no formulário
    cur.execute(sql, (request.form['nome'], request.form['descricao'],
                prazo, request.form['prioridade'], projeto_id))
    mysql.connection.commit()  # Confirma a transação no banco de dados
    cur.close()  # Fecha o cursor para liberar recursos

def update_task(mysql, tarefa_id):
    # Obtém o prazo do formulário e remove qualquer sufixo 'T00:00' (se existir)
    prazo_str = request.form['prazo'].split('T')[0]  # Separa apenas a data sem a parte do tempo
    prazo = datetime.strptime(prazo_str, '%Y-%m-%d')  # Converte para datetime

    # SQL para atualizar os detalhes de uma tarefa específica
    sql = '''
            UPDATE tarefa 
            SET nome = %s, descricao = %s, prazo = %s, prioridade = %s, status = %s 
            WHERE id = %s
        '''
    cur = mysql.connection.cursor()  # Cria um cursor
    # Executa o comando SQL com os valores fornecidos no formulário
    cur.execute(sql, (request.form['nome'], request.form['descricao'], prazo,
                      request.form['prioridade'], request.form['status'], tarefa_id))
    mysql.connection.commit()  # Confirma a transação
    cur.close()  # Fecha o cursor

def get_details_task(mysql, tarefa_id):
    # SQL para obter os detalhes de uma tarefa específica pelo ID
    sql = "SELECT * FROM tarefa WHERE id = %s"
    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, [tarefa_id])  # Executa o comando com o ID da tarefa
    tarefa = cur.fetchone()  # Recupera o resultado
    cur.close()  # Fecha o cursor
    return tarefa  # Retorna os detalhes da tarefa

def get_task_pending(mysql, projeto_id):
    # SQL para obter tarefas pendentes de um projeto específico
    sql = '''
        SELECT * FROM tarefa 
        WHERE projeto_id = %s AND status = 'Pendente' 
        ORDER BY prioridade DESC
    '''
    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, [projeto_id])  # Executa o comando com o ID do projeto
    tarefas_pendentes = cur.fetchall()  # Recupera todas as tarefas pendentes
    cur.close()  # Fecha o cursor
    return tarefas_pendentes  # Retorna as tarefas pendentes

def get_task_progess(mysql, projeto_id):
    # SQL para obter tarefas em andamento de um projeto
    sql = '''
        SELECT * FROM tarefa 
        WHERE projeto_id = %s AND status = 'Em andamento' 
        ORDER BY prioridade DESC
    '''
    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, [projeto_id])  # Executa o comando com o ID do projeto
    tarefas_andamento = cur.fetchall()  # Recupera todas as tarefas em andamento
    cur.close()  # Fecha o cursor
    return tarefas_andamento  # Retorna as tarefas em andamento

def get_task_completed(mysql, projeto_id):
    # SQL para obter tarefas concluídas de um projeto
    sql = '''
       SELECT * FROM tarefa 
       WHERE projeto_id = %s AND status = 'Concluída' 
       ORDER BY prioridade DESC
    '''
    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, [projeto_id])  # Executa o comando com o ID do projeto
    tarefas_concluidas = cur.fetchall()  # Recupera todas as tarefas concluídas
    cur.close()  # Fecha o cursor
    return tarefas_concluidas  # Retorna as tarefas concluídas

def delete_task(mysql, tarefa_id):
    # SQL para deletar uma tarefa pelo ID
    sql = "DELETE FROM tarefa WHERE id = %s"
    cur = mysql.connection.cursor()  # Cria um cursor
    cur.execute(sql, [tarefa_id])  # Executa o comando com o ID da tarefa
    mysql.connection.commit()  # Confirma a exclusão da tarefa no banco de dados
    cur.close()  # Fecha o cursor
