def mod_start(mysql):
    # Cria um cursor para executar comandos SQL na conexão MySQL
    cur = mysql.connection.cursor()
    
    # Define a codificação de caracteres para utf8mb4, que suporta todos os caracteres Unicode, incluindo emojis
    cur.execute("SET NAMES utf8mb4")
    
    # Define a codificação de caracteres para a conexão com o MySQL
    cur.execute("SET character_set_connection=utf8mb4")
    
    # Define a codificação de caracteres para o cliente (quem envia as consultas)
    cur.execute("SET character_set_client=utf8mb4")
    
    # Define a codificação de caracteres para os resultados retornados do banco de dados
    cur.execute("SET character_set_results=utf8mb4")
    
    # Define a localidade de tempo para português do Brasil, afetando a formatação de datas e horas
    cur.execute("SET lc_time_names = 'pt_BR'")
    
    # Fecha o cursor, liberando recursos
    cur.close()

    
    