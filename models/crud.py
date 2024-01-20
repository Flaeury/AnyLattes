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


def saveID(idlattes, nomedocente):

    if idlattes is not None:
        db = database.conexao()
        cursor = db.cursor()
        sql = """ insert into iddocentes (idlattes, nomedocente) values (?, ?);"""
        cursor.execute(sql, (idlattes, nomedocente))
        db.commit()


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
