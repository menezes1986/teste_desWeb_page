import mysql.connector

def criar_connection(host, usuario, senha, banco):
    return mysql.connector.connection(host = host, user= usuario, password = senha, database = banco)



def close_connection(con):
    return con.close()