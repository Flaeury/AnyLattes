import models.connection as database
import sqlite3

db = database.conexao()
cursor = db.cursor()


def contador(nome_docente):

    sql = "select ano_evento,estratos,count(estratos), SUM(notas) from resultados where nome_docente = '" + \
        nome_docente+"' group by estratos, ano_evento order by ano_evento asc"
    resultado = cursor.execute(sql)

    return resultado


def todosContador(from_year, to_year, nome_docente='*'):
    sql = "select ano_evento, estratos, count(estratos) as quantidade from resultados WHERE ano_evento >= " + \
        from_year + " AND ano_evento <= " + to_year + \
        " group by estratos, ano_evento order by ano_evento asc"

    if nome_docente != '*':
        sql = "select ano_evento, estratos, count(estratos) as quantidade from resultados WHERE nome_docente in('" + "','".join(nome_docente.split(
            ';')) + "') AND ano_evento >= " + from_year + " AND ano_evento <= " + to_year + " group by estratos, ano_evento order by ano_evento asc"

    resultado = cursor.execute(sql)

    return resultado


# def todosPeriodicos(from_year, to_year, nome_docente='*'):
#     # Build the base SQL query
#     sql = ("SELECT ano_evento, estratos, COUNT(estratos) AS quantidade "
#            "FROM resultados r "
#            "WHERE r.documento LIKE '%Peri%' "
#            "AND r.ano_evento >= ? AND r.ano_evento <= ? ")
    
#     # Add condition for specific docente if provided
#     if nome_docente != '*':
#         docentes = "','".join(nome_docente.split(';'))
#         sql += f"AND r.nome_docente IN ('{docentes}') "
    
#     # Complete the SQL query
#     sql += "GROUP BY estratos, ano_evento ORDER BY ano_evento ASC"
    
#     # Connect to the database and execute the query
#     conn = sqlite3.connect('database.db')  # Use the correct database file
#     cursor = conn.cursor()
    
#     # Execute the query with parameters
#     cursor.execute(sql, (from_year, to_year))
    
#     # Fetch all results
#     resultado = cursor.fetchall()
    
#     # Close the connection
#     conn.close()
    
#     return resultado


# def todosConferencias(from_year, to_year, nome_docente='*'):
#     # Build the base SQL query
#     sql = ("SELECT ano_evento, estratos, COUNT(estratos) AS quantidade "
#            "FROM resultados r "
#            "WHERE r.documento LIKE '%Conf%' "
#            "AND r.ano_evento >= ? AND r.ano_evento <= ? ")
    
#     # Add condition for specific docente if provided
#     if nome_docente != '*':
#         docentes = "','".join(nome_docente.split(';'))
#         sql += f"AND r.nome_docente IN ('{docentes}') "
    
#     # Complete the SQL query
#     sql += "GROUP BY estratos, ano_evento ORDER BY ano_evento ASC"
    
#     # Connect to the database and execute the query
#     conn = sqlite3.connect('database.db')  # Use the correct database file
#     cursor = conn.cursor()
    
#     # Execute the query with parameters
#     cursor.execute(sql, (from_year, to_year))
    
#     # Fetch all results
#     resultado = cursor.fetchall()
    
#     # Close the connection
#     conn.close()
    
#     return resultado


def periodicos():
    sql = "select count(1) from resultados where documento = 'Periodico' GROUP by nome_docente,documento"
    resultado = cursor.execute(sql)
    return resultado


def lista_docente(docente):
    sql = """select id, nome_docente, documento,ano_evento, titulo,doi,sigla,nome_evento, autores,estratos, round(notas,5) from resultados r
            where nome_docente = '"""+docente+"""'
            order by ano_evento asc"""
    cursor = db.cursor()
    cursor.execute(sql.upper())
    resultado = cursor.fetchall()

    return resultado


def listar_docentes():
    sql = """SELECT nome_docente FROM resultados GROUP BY nome_docente"""
    cursor = db.cursor()
    cursor.execute(sql)
    resultados = cursor.fetchall()
    docentes = [resultado[0] for resultado in resultados]
    return docentes