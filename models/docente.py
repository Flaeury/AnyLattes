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
    sql = ("SELECT ano_evento, estratos, COUNT(estratos) AS quantidade "
           "FROM resultados "
           "WHERE ano_evento >= ? AND ano_evento <= ? ")

    params = [from_year, to_year]

    if nome_docente != '*':
        docentes = nome_docente.split(';')
        sql += "AND nome_docente IN ({}) ".format(','.join(['?'] * len(docentes)))
        params.extend(docentes)

    sql += "GROUP BY estratos, ano_evento ORDER BY estratos ASC"

    cursor = db.cursor()
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
    return resultado

def todosPeriodicos(from_year, to_year, nome_docente='*'):
    sql = ("SELECT ano_evento, estratos, COUNT(estratos) AS quantidade "
           "FROM resultados "
           "WHERE documento LIKE '%Peri%' AND ano_evento >= ? AND ano_evento <= ? ")
    
    params = [from_year, to_year]
    
    if nome_docente != '*':
        docentes = nome_docente.split(';')
        sql += "AND nome_docente IN ({}) ".format(','.join(['?'] * len(docentes)))
        params.extend(docentes)
    
    sql += "GROUP BY estratos, ano_evento ORDER BY estratos ASC"
    
    cursor = db.cursor()
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
    return resultado

def todosConferencias(from_year, to_year, nome_docente='*'):
    sql = ("SELECT ano_evento, estratos, COUNT(estratos) AS quantidade "
           "FROM resultados "
           "WHERE documento LIKE '%Conf%' AND ano_evento >= ? AND ano_evento <= ? ")
    
    params = [from_year, to_year]
    
    if nome_docente != '*':
        docentes = nome_docente.split(';')
        sql += "AND nome_docente IN ({}) ".format(','.join(['?'] * len(docentes)))
        params.extend(docentes)
    
    sql += "GROUP BY estratos, ano_evento ORDER BY estratos ASC"

    cursor = db.cursor()
    cursor.execute(sql, params)
    resultado = cursor.fetchall()
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