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
    # Obter os anos e estratos possíveis
    sql_anos = "SELECT DISTINCT ano_evento FROM resultados WHERE ano_evento >= ? AND ano_evento <= ?"
    cursor = db.cursor()
    cursor.execute(sql_anos, [from_year, to_year])
    anos_disponiveis = [row[0] for row in cursor.fetchall()]

    sql_estratos = "SELECT DISTINCT estratos FROM resultados"
    cursor.execute(sql_estratos)
    estratos_disponiveis = [row[0] for row in cursor.fetchall()]

    # Obter os resultados existentes
    sql = ("SELECT ano_evento, estratos, COUNT(estratos) AS quantidade "
           "FROM resultados "
           "WHERE ano_evento >= ? AND ano_evento <= ? ")

    params = [from_year, to_year]

    if nome_docente != '*':
        docentes = nome_docente.split(';')
        sql += "AND nome_docente IN ({}) ".format(','.join(['?'] * len(docentes)))
        params.extend(docentes)

    sql += "GROUP BY estratos, ano_evento ORDER BY estratos ASC, ano_evento ASC"
    
    cursor.execute(sql, params)
    resultado = cursor.fetchall()

    # Criar um dicionário para armazenar os resultados com contagens 0
    resultado_completo = {(ano, estrato): 0 for ano in anos_disponiveis for estrato in estratos_disponiveis}

    # Atualizar o dicionário com os resultados obtidos
    for (ano_evento, estrato, quantidade) in resultado:
        resultado_completo[(ano_evento, estrato)] = quantidade

    # Converter o dicionário em uma lista de tuplas para retornar
    resultado_final = [(ano, estrato, quantidade) for (ano, estrato), quantidade in resultado_completo.items()]
    
    return resultado_final



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
    cursor = db.cursor()
    cursor.execute("SELECT nomedocente, dataatualizacao, dataanylattes, idlattes FROM iddocentes order by nomedocente asc")
    docentes = cursor.fetchall()
    
    return [(docente[0], formatar_data(docente[1]), docente[2], docente[3] ) for docente in docentes]

def formatar_data(data):
    data_str = str(data)
    dia = data_str[:-6].zfill(2)
    mes = data_str[-6:-4].zfill(2)
    ano = data_str[-4:]
    return f"{dia}/{mes}/{ano}"