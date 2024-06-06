# -*- coding: utf-8 -*-
import models.connection as database
from flask import flash
import sqlite3

db = database.conexao()


def lista_por_titulo(titulo, docente):
    sql = "select * from resultados where titulo ='" + \
        titulo+"' and nome_docente = '"+docente+"' "

    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()

    if len(resultado) != 0:
        return resultado
    else:
        return 0


def lista_por_id(id):
    sql = "select * from resultados where id ='"+id+"' "

    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado


def lista(from_year, to_year, nome_docente='*'):

    sql = "SELECT id, nome_docente, documento,ano_evento, titulo,doi,sigla,nome_evento, autores,estratos, round(notas,5) from resultados r WHERE ano_evento >= " + \
        from_year+" AND ano_evento <= " + to_year + " order by ano_evento asc;"
    if nome_docente != '*':
        sql = "SELECT id, nome_docente, documento,ano_evento, titulo,doi,sigla,nome_evento, autores,estratos, round(notas,5) from resultados r WHERE nome_docente in('" + "','".join(nome_docente.split(';')) + "') AND ano_evento >= " + from_year + \
            " AND ano_evento <= " + to_year + " order by ano_evento asc;"

    cursor = db.cursor()
    cursor.execute(sql.upper())
    resultado = cursor.fetchall()

    return resultado


def busca_prof():

    sql = """ SELECT distinct(nome_docente) FROM resultados"""
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()

    return resultado


def soma_nota(from_year, to_year, nome_docente='*'):

    sql = ("SELECT distinct nome_docente , round(sum(notas),3) from resultados where nome_docente in (select distinct(nome_docente) from resultados) AND ano_evento >= " +
           from_year + " AND ano_evento <= " + to_year + " group by nome_docente order by nome_docente asc;")

    if nome_docente != '*':
        sql = ("SELECT distinct nome_docente , round(sum(notas),3) from resultados where nome_docente in (select distinct(nome_docente) from resultados) AND ano_evento >= " +
               from_year + " AND ano_evento <= " + to_year + " AND nome_docente in('" + "','".join(nome_docente.split(';')) + "') group by nome_docente order by nome_docente asc;")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def soma_nota_docente(docente):
    sql = (
        "SELECT DISTINCT nome_docente, ROUND(SUM(notas), 3) "
        "FROM resultados "
        "WHERE nome_docente IN (SELECT DISTINCT(nome_docente) FROM resultados WHERE nome_docente = ?) "
        "GROUP BY nome_docente "
        "ORDER BY ano_evento ASC;"
    )
    cursor = db.cursor()
    cursor.execute(sql, (docente,))
    resultado = cursor.fetchall()
    return resultado


def contador_estratos():

    sql = ('select DISTINCT(nome_docente), count(estratos), estratos, ano_evento from resultados group by nome_docente, estratos, ano_evento order by ano_evento asc')
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def titulos_qualis(nome_docente='*'):
    sql = ('SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1 ;')

    if nome_docente != '*':
        sql = ("SELECT DISTINCT titulo FROM resultados r WHERE nome_docente in('" +
               "','".join(nome_docente.split(';')) + "') group by titulo having COUNT(*) >1 ;")

    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()

    return resultado


def qualis_repetidos(titulo):
    sql = ("SELECT distinct titulo, notas, estratos, count(*) FROM resultados r WHERE titulo like '%" +
           titulo+"%' group by titulo, notas, estratos having COUNT(*) >1 ;")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def titulo_repetido(titulo):
    sql = "select distinct titulo, notas, estratos, count(*), nome_docente, doi from resultados r where titulo LIKE '%" + \
        titulo+"%' group by nome_docente;"

    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    if len(resultado) != 0:
        return resultado
    else:
        return 0

# verificar quais titulos se repetem e quais docentes publicaram


def titulos_repetidos(from_year, to_year, nome_docente='*'):
    # sql = ("select nome_docente, titulo from resultados r where titulo like '%"+titulo+"%' GROUP by titulo HAVING count(*)>1")
    sql = "SELECT distinct titulo, nome_docente FROM resultados r WHERE titulo in (SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1) AND ano_evento >= '" + \
        from_year+"'  AND ano_evento <= '"+to_year + \
        "' group by titulo,nome_docente  order by titulo;"

    if nome_docente != '*':
        sql = "SELECT distinct titulo, nome_docente FROM resultados r WHERE titulo in (SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1) AND ano_evento >= '" + \
            from_year+"'  AND ano_evento <= '"+to_year + \
            "' AND nome_docente in('" + "','".join(nome_docente.split(';')) + "')" + \
            " group by titulo,nome_docente  order by titulo;"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def titulo_repetidos(titulo):
    sql = ("select nome_docente, titulo from resultados r where titulo like '%" +
           titulo+"%' GROUP by titulo HAVING count(*)>1")
    # sql = "SELECT distinct titulo, nome_docente FROM resultados r WHERE titulo in (SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1) group by titulo,nome_docente  order by titulo;"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def docente_titulos_repetidos(from_year, to_year, nome_docente='*'):
    sql = "SELECT distinct nome_docente FROM resultados r WHERE titulo in (SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1) AND ano_evento >= '" + \
        from_year+"'  AND ano_evento <= '"+to_year + \
        "' group by titulo,nome_docente order by titulo;"

    if nome_docente != '*':
        sql = "SELECT distinct nome_docente FROM resultados r WHERE titulo in (SELECT DISTINCT titulo FROM resultados r group by titulo having COUNT(*) >1) AND ano_evento >= '" + \
            from_year+"'  AND ano_evento <= '"+to_year + \
            "' AND nome_docente in('" + "','".join(nome_docente.split(';')) + "')" + \
            " group by titulo,nome_docente order by titulo;"

    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def update_qualis_repetido(titulo, valor):
    sql = "update resultados set notas = ? where titulo = ?"
    cursor = db.cursor()
    cursor.execute(sql, (valor, titulo))
    try:
        db.commit()
        print(titulo + " Atualizado com Sucesso!")
    except:
        db.rollback()
        print("Sem Sucesso!")
    # db.close()


def mostra_publicacao(id):
    sql = "select id, nome_docente, titulo, doi, sigla, nome_evento, estratos from resultados r where id= "+id+";"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado


def mostra_dados_faltantes(id):
    sql = "select id, nome_docente, titulo, autores, sigla, nome_evento from resultados r where id= "+id+";"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado


def atualizar(id, doi, sigla, nome_evento, estratos, nota, versao):

    versao = versao + 1

    sql = ("update resultados set doi = ?, sigla= ?, nome_evento = ?, estratos = ?, notas = ?, versao = ? where id = ?")
    cursor = db.cursor()
    cursor.execute(sql, (doi, sigla, nome_evento,
                   estratos, nota, str(versao), id))

    db.commit()
    print("Atualizado com Sucesso!")


def total_estratos(from_year, to_year, nome_docente='*'):
    sql = "SELECT ano_evento,estratos, COUNT(estratos) from resultados r WHERE ano_evento >= '" + \
        from_year + "' AND ano_evento <= '" + to_year + "' group by ano_evento,estratos;"

    if nome_docente != '*':
        sql = "SELECT ano_evento,estratos, COUNT(estratos) from resultados r WHERE nome_docente in('" + "','".join(nome_docente.split(';')) + "') AND ano_evento >= '" + \
            from_year + "' AND ano_evento <= '" + to_year + "' group by ano_evento,estratos;"

    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()

    return resultado


def get_nome_docente():
    sql = "select distinct(nome_docente) from resultados;"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def perc(from_year, to_year, nome_docente='*'):
    sql = ("select distinct total, 'Periódico', 'Conferência', round(periodico * 100 / total,3 ) as percentual_periodico, round(conferencia * 100 / total,3 ) as percentual_conferencia " +
           "from (select " +
           "(select count(1) from resultados r  WHERE ano_evento >= " +
           from_year + " AND ano_evento <= " + to_year + ") as total,"
           "(select count(1) from resultados r where r.documento like '%Peri%'  AND ano_evento >= " + from_year + " AND ano_evento <= " + to_year + ") as periodico," +
           "(select count(1) from resultados r where r.documento like '%Conf%'  AND ano_evento >= " + from_year + " AND ano_evento <= " + to_year + ") as conferencia from resultados);")

    if nome_docente != '*':
        sql = ("select distinct total, 'Periódico', 'Conferência', round(periodico * 100 / total,3 ) as percentual_periodico, round(conferencia * 100 / total,3 ) as percentual_conferencia " +
               "from (select " +
               "(select count(1) from resultados r  WHERE ano_evento >= " +
               from_year + " AND ano_evento <= " + to_year +
               " AND nome_docente in('" +
               "','".join(nome_docente.split(';')) + "')) as total,"
               "(select count(1) from resultados r where r.documento like '%Peri%'  AND ano_evento >= " + from_year + " AND ano_evento <= " + to_year + " AND nome_docente in('" + "','".join(nome_docente.split(';')) + "')) as periodico," +
               "(select count(1) from resultados r where r.documento like '%Conf%'  AND ano_evento >= " + from_year + " AND ano_evento <= " + to_year + " AND nome_docente in('" + "','".join(nome_docente.split(';')) + "')) as conferencia from resultados);")

    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()

    return resultado


def totalPeriodicos(from_year, to_year, nome_docente='*'):
    # Consulta base para todos os registros sem filtro de docentes
    sql = (
        "SELECT "
        "(SELECT COUNT(1) FROM resultados r WHERE ano_evento >= ? AND ano_evento <= ? AND r.documento LIKE '%Peri%') AS periodico "
        "FROM resultados"
    )
    
    params = [from_year, to_year]

    # Ajusta a consulta se um ou mais docentes forem especificados
    if nome_docente != '*':
        docentes = nome_docente.split(';')
        docente_filter = " AND nome_docente IN ({})".format(','.join(['?'] * len(docentes)))
        
        sql = (
            "SELECT "
            "(SELECT COUNT(1) FROM resultados r WHERE ano_evento >= ? AND ano_evento <= ? AND r.documento LIKE '%Peri%'"
            + docente_filter + ") AS periodico "
            "FROM resultados"
        )
        params.extend(docentes)

    cursor = db.cursor()
    cursor.execute(sql, params)
    resultado = cursor.fetchone()

  
    total_periodicos = resultado[0] if resultado else 0
    
    print(f"Total de Periódicos: {total_periodicos}")
    return total_periodicos


def totalConferencias(from_year, to_year, nome_docente='*'):
   
    sql = (
        "SELECT "
        "(SELECT COUNT(1) FROM resultados r WHERE ano_evento >= ? AND ano_evento <= ? AND r.documento LIKE '%Conf%') AS conferencia "
        "FROM resultados"
    )
    
    params = [from_year, to_year]

  
    if nome_docente != '*':
        docentes = nome_docente.split(';')
        docente_filter = " AND nome_docente IN ({})".format(','.join(['?'] * len(docentes)))
        
        sql = (
            "SELECT "
            "(SELECT COUNT(1) FROM resultados r WHERE ano_evento >= ? AND ano_evento <= ? AND r.documento LIKE '%Conf%'"
            + docente_filter + ") AS conferencia "
            "FROM resultados"
        )
        params.extend(docentes)

    cursor = db.cursor()
    cursor.execute(sql, params)
    resultado = cursor.fetchone()

   
    total_conferencias = resultado[0] if resultado else 0
    
    print(f"Total de Conferências: {total_conferencias}")
    return total_conferencias


def perc_docente(docente):
    sql = ("select distinct total, 'Periódico', 'Conferência', round(periodico * 100 / total,3 ) as percentual_periodico, round(conferencia * 100 / total,3 ) as percentual_conferencia " +
           "from (select " +
           "(select count(1) from resultados r where nome_docente = '"+docente+"' ) as total," +
           "(select count(documento) from resultados r where r.documento like '%Peri%' and  r.nome_docente = '"+docente+"' ) as periodico," +
           "(select count(documento) from resultados r where r.documento like '%Conf%' and  r.nome_docente = '"+docente+"' ) as conferencia from resultados);")
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()

    return resultado


def busca_conferencias():
    sql = "SELECT COUNT(1) FROM RESULTADOS WHERE DOCUMENTO = 'Conferencia' group by nome_docente, documento;"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado

# media todos docentes


def media_docentes(from_year, to_year, nome_docente='*'):
    sql = "select nome_docente, round(sum(notas),3) as media from resultados r WHERE ano_evento >= " + \
        from_year + " AND ano_evento <= " + to_year + " group by nome_docente ;"
    if nome_docente != '*':
        sql = "select nome_docente, round(sum(notas),3) as media from resultados r WHERE nome_docente in('" + "','".join(nome_docente.split(';')) + "') AND ano_evento >= " + from_year + \
            " AND ano_evento <= " + to_year + " group by nome_docente ;"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def get_db_connection():
    connection = sqlite3.connect('anylattes.db', timeout=10)
    return connection


def deletar_docente(docente):
    resultado = False
    sql = "DELETE FROM resultados WHERE nome_docente = ?"
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(sql, (docente,))
        db.commit()
        print(docente + " Removido com Sucesso!")
        flash(docente + " Removido com Sucesso!")
        resultado = True
    except sqlite3.OperationalError as e:
        db.rollback()
        if 'database is locked' in str(e):
            print("Sem Sucesso! Database is locked")
            flash("Erro ao remover docente: O banco de dados está bloqueado")
        else:
            print("Sem Sucesso!", e)
            flash("Erro ao remover docente: " + str(e))
        resultado = False
    finally:
        db.close()
    return resultado


def deletar_iddocente(docente):
    resultado = False
    sql = "DELETE FROM iddocentes WHERE nomedocente = ?"
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(sql, (docente,))
        db.commit()
        print(docente + " Removido da tabela iddocente!")
        resultado = True
    except sqlite3.OperationalError as e:
        db.rollback()
        if 'database is locked' in str(e):
            print("Sem Sucesso! Database is locked")
            flash(
                "Erro ao remover docente da tabela iddocente: O banco de dados está bloqueado")
        else:
            print("Sem Sucesso!", e)
            flash("Erro ao remover docente da tabela iddocente: " + str(e))
        resultado = False
    finally:
        db.close()
    return resultado


def lista_especifica(docente):
    sql = "select nome_docente, titulo from resultados where nome_docente = '"+docente+"'"

    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def update_notas(nota, titulo):
    sql = "update resultados set notas = ? where titulo = ? "
    cursor = db.cursor()
    cursor.execute(sql, (nota, titulo))
    db.commit()


def lista_pontuacoes():
    sql = "select * from pontuacoes"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    return resultado


def busca_pontuacao_estrato(estrato):
    if estrato == '-' or estrato == '':
        estrato = 'SEM QUALIS'
    sql = "select nota from pontuacoes where estrato = '"+estrato+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado


def update_pontuacoes(estrato, nota):
    sql = ("update pontuacoes set nota = ? where estrato = ?")
    cursor = db.cursor()
    cursor.execute(sql, (nota, estrato))
    db.commit()