import models.connection as database

db = database.conexao()
cursor = db.cursor()
def contador(nome_docente):

    sql = "select ano_evento,estratos,count(estratos), SUM(notas) from resultados where nome_docente = '"+nome_docente+"' group by estratos, ano_evento order by ano_evento asc"
    resultado = cursor.execute(sql)

    return resultado

def todosContador(from_year, to_year):
    sql = "select ano_evento, estratos, count(estratos) as quantidade from resultados WHERE ano_evento >= " + from_year + " AND ano_evento <= " + to_year + " group by estratos, ano_evento order by ano_evento asc"
    resultado = cursor.execute(sql)
    
    return resultado

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

