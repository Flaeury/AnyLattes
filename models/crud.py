import models.connection as database

from flask import flash


def zera_banco():
    try:
        db = database.conexao()
        cursor = db.cursor()
        sql = """ delete from resultados where id >=1;"""
        cursor.execute(sql)
        db.commit()
    except:
        flash("Erro de conexão com o banco de dados")

def saveID(idlattes, nomedocente, dataatualizacao, dataanylattes):
    if idlattes is not None:
        db = database.conexao()
        cursor = db.cursor()
        sql = """INSERT INTO iddocentes (idlattes, nomedocente, dataatualizacao, dataanylattes) VALUES (?, ?, ?, ?);"""
        cursor.execute(sql, (idlattes, nomedocente, dataatualizacao, dataanylattes))
        db.commit()
        
# def saveDate(ultimaAtualizacao, nomedocente):
#     if ultimaAtualizacao is not None:
#         db = database.conexao()
#         cursor = db.cursor()
#         sql = """ insert into dataatualizacao (dataatualizacao, nomedocente)"""
 
def get_docentes():
    db = database.conexao()
    cursor = db.cursor()
    cursor.execute("SELECT nomedocente, dataatualizacao, dataanylattes FROM iddocentes;")
    docentes = cursor.fetchall()
    return docentes


def findIdLattes(idlattes):
    db = database.conexao()
    cursor = db.cursor()
    sql = " select * from iddocentes where idlattes = '"+idlattes+"' "
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if len(resultado) != 0:
        return 1
    else:
        return 0