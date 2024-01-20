# -*- coding: utf-8 -*-
# import mysql.connector
from flask import Flask, jsonify, redirect, render_template, request, flash
from flask_cors import CORS
import glob
import os
import zipfile
from werkzeug.utils import secure_filename
from models.import_projetos import import_project
from flask import send_from_directory
from models.consulta import *
from models.docente import *
from models.crud import *
import json
import plotly
import plotly.express as px
from models.grafico import graficos
from models.grafico import pizza
from models.grafico import *
import models.BaseDeCorrecoes
import models.connection as database
from flask_sqlalchemy import SQLAlchemy
from zipfile import ZipFile
import os
import time
import random
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import speech_recognition as sr
import urllib
import pydub
import shutil
from pathlib import Path
import datetime

app = Flask(__name__)
CORS(app)
app.app_context().push()

idLattes = ''

# configurações de upload arquivos

ALLOWED_EXTENSIONS = {'xml', 'XML', 'pdf', 'xls',
                      'xlsx', 'zip', 'ZIP'}  # extensões validas

# verifica se pasta existe
if os.path.isdir('curriculos'):
    UPLOAD_FOLDER = 'curriculos'
    print('Currículos')
else:
    os.mkdir('curriculos')
    UPLOAD_FOLDER = 'curriculos'

if os.path.isdir('arquivos'):
    print('Arquivos')
else:
    os.mkdir('arquivos')

if os.path.isdir('static/images'):
    print('Images')
else:
    os.mkdir('static/images')
    os.mkdir('static/images/nuvem_docente')


app.secret_key = 'lattes4web'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_webdriver_error(driver):
    try:
        driver.quit()
    except Exception as e:
        print(f"Erro ao fechar o WebDriver: {e}")


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/imports", methods=['GET', 'POST'])
def imports():
    if request.method == 'POST':
        if 'lattes_id' in request.form:
            try:
                lattes = ",".join(request.form.get(
                    'lattes_id', "").split(";")).split(",")

                if len(lattes) == 0:
                    flash("Lattes ID is required.")
                    return redirect(url_for('index'))

                path_to_download = os.getcwd() + '/outputs'
                options = Options()
                options.set_preference('browser.download.folderList', 2)
                options.set_preference(
                    'browser.download.dir', path_to_download)
                options.set_preference(
                    'browser.helperApps.alwaysAsk.force', False)
                options.set_preference(
                    'browser.download.manager.showWhenStarting', False)
                options.set_preference(
                    'browser.helperApps.neverAsk.saveToDisk', 'application/zip')

                driver = webdriver.Firefox(options=options)
                width = height = 800
                ss_w, ss_h = pyautogui.size()
                driver.set_window_size(width, height)
                driver.set_window_position(
                    ss_w / 2 - width / 2, ss_h / 2 - height / 2)

                lattes_url = 'http://buscatextual.cnpq.br/buscatextual/download.do?metodo=apresentar&idcnpq='

                for idcnpq in lattes:
                    idcnpq = idcnpq.strip()
                    location = lattes_url + idcnpq
                    driver.get(location)

                    frames = driver.find_elements(By.TAG_NAME, 'iframe')
                    driver.switch_to.frame(frames[0])

                    driver.find_element(
                        By.CLASS_NAME, 'recaptcha-checkbox-border').click()
                    driver.switch_to.default_content()

                    button = driver.find_element(By.ID, 'submitBtn')
                    time.sleep(random.randint(1, 2))
                    worked = True
                    time.sleep(1)
                    if not button.is_enabled():
                        time.sleep(1)
                        frames = driver.find_element(
                            By.XPATH, '/html/body/div[2]/div[4]').find_elements(By.TAG_NAME, 'iframe')
                        driver.switch_to.frame(frames[0])

                        time.sleep(random.randint(1, 2))
                        driver.find_element(
                            By.ID, 'recaptcha-audio-button').click()
                        driver.switch_to.default_content()

                        frames = driver.find_elements(By.TAG_NAME, 'iframe')
                        driver.switch_to.frame(frames[-1])

                        time.sleep(1)
                        driver.find_element(
                            By.XPATH, '/html/body/div/div/div[3]/div/button').click()
                        time.sleep(1)
                        src = driver.find_element(
                            By.ID, 'audio-source').get_attribute('src')
                        time.sleep(1)
                        file_name = path_to_download + '/sample.mp3'
                        urllib.request.urlretrieve(src, file_name)
                        time.sleep(1)
                        sound = pydub.AudioSegment.from_mp3(file_name)
                        time.sleep(1)
                        file_name = file_name.replace('.mp3', '.wav')
                        sound.export(file_name, format='wav')

                        sample_audio = sr.AudioFile(file_name)
                        r = sr.Recognizer()
                        with sample_audio as source:
                            audio = r.record(source)

                        key = r.recognize_google(audio)

                        driver.find_element(
                            By.ID, 'audio-response').send_keys(key.lower())
                        driver.find_element(
                            By.ID, 'audio-response').send_keys(Keys.ENTER)
                        driver.switch_to.default_content()

                        time.sleep(1)
                        driver.find_element(By.ID, 'submitBtn').click()

                        shutil.move(str(Path.home()) + "/Downloads/" + idcnpq +
                                    ".zip", os.getcwd() + "/arquivos/" + idcnpq + ".zip")

                        path_to_zipfile = os.getcwd() + "/arquivos/" + idcnpq + ".zip"
                        destino_arquivo = "arquivos/"

                        if os.path.exists(path_to_zipfile):
                            with zipfile.ZipFile(path_to_zipfile, 'r') as zip_ref:
                                zip_ref.extractall(destino_arquivo)
                            os.remove(path_to_zipfile)
                        else:
                            worked = False

                    else:
                        time.sleep(1)
                        button.click()

                        shutil.move(str(Path.home()) + "/Downloads/" + idcnpq +
                                    ".zip", os.getcwd() + "/arquivos/" + idcnpq + ".zip")

                        path_to_zipfile = os.getcwd() + "/arquivos/" + idcnpq + ".zip"
                        destino_arquivo = "arquivos/"

                        if os.path.exists(path_to_zipfile):
                            with zipfile.ZipFile(path_to_zipfile, 'r') as zip_ref:
                                zip_ref.extractall(destino_arquivo)
                            os.remove(path_to_zipfile)
                        else:
                            worked = False

                    if not worked:
                        continue

                    shutil.move(os.getcwd() + "/arquivos/curriculo.xml",
                                os.getcwd() + "/arquivos/" + idcnpq + ".xml")

                driver.quit()
                page = "upload"
                start_date = "1800"
                end_date = str(datetime.date.today().year)
                return render_template('loading.html', inicio=start_date, fim=end_date, page=page)

            except Exception as e:
                print(f"Erro geral: {e}")
                flash(
                    "Ocorreu um erro durante a importação. Consulte os logs para mais detalhes.")
                return render_template('index.html')

            finally:
                handle_webdriver_error(driver)

        elif 'files[]' in request.files:
            files = request.files.getlist('files[]')
            for file in files:
                if file.filename == '':
                    flash("No Selected file(s)")
                else:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join('arquivos/' + filename))
                        f = file.filename.rsplit('.', 1)[1].lower()
                        dir = 'arquivos/'

                        if f == 'pdf' or f == 'PDF':
                            old = os.path.join(dir, filename)
                            new = os.path.join(dir, 'QUALIS_novo.pdf')
                            os.rename(old, new)
                        elif f == 'xls' or f == 'xlsx':
                            old = os.path.join(dir, filename)
                            new = os.path.join(dir, 'QualisConferencias.xlsx')
                            os.rename(old, new)
                        else:
                            flash("Erro no sistema")

                        flash('File(s) uploaded successfully')

                    else:
                        flash(
                            "Não foi possível efetuar upload. Arquivo com extensão inválida")

            page = "upload"
            start_date = "1800"
            end_date = str(datetime.date.today().year)
            return render_template('loading.html', inicio=start_date, fim=end_date, page=page)

        else:
            flash("Invalid form data")

    return render_template('imports.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for f in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))

        xml_files = [f for f in os.listdir("xml") if f.endswith(".xml")]

        for xml_file in xml_files:
            file_path = os.path.join("xml", xml_file)

            with open(file_path, 'r', encoding='utf-8') as file:

                xml_content = file.read()
                print(f"Processing XML file: {xml_file}")
                print(xml_content)

        anos = []
        result = []
        page = "upload"
        start_date = "1800"
        end_date = str(datetime.date.today().year)
        return render_template('loading.html', inicio=start_date, fim=end_date, page=page)


@app.route('/resultado_total')
def resultado_total():
    upload()

    dados = todosContador()

    listar = lista()
    totalNotas = soma_nota()
    contadorEstratos = total_estratos()

    conteudo = {}
    div = []
    for d in dados:
        conteudo = {'Ano': d[0], 'Estratos': d[1], 'Quantidade': d[2]}
        div.append(conteudo)
        conteudo = {}
    json_object = json.dumps(div, indent=4)
    with open("todos.json", "w") as outfile:
        outfile.write(json_object)

    with open('todos.json', 'r') as file:
        data = json.load(file)

    fig = px.bar(data, x='Ano', y='Quantidade',
                 color='Estratos', barmode='stack')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    anos = []
    for c in data:
        anos.append(c['Ano'])

    anos = sorted(set(anos))
    print(anos)
    names = []
    values = []
    pizza()
    with open('pizza.json', 'r') as piz:
        d = json.load(piz)
        names.append(d[0]['Conferencia'])
        names.append(d[0]['Periodico'])
        values.append(d[0]['PercConferencia'])
        values.append(d[0]['PercPeriodico'])

    figs = px.pie(names=names, values=values)

    graph = json.dumps(figs, cls=plotly.utils.PlotlyJSONEncoder)

    grafico_media()
    with open('media_docentes.json', 'r') as med:
        dados = json.load(med)

    docente = []
    media = []
    mediana = []
    m = []
    for d in dados:
        docente.append(d['Docente'])
        media.append(d['Média'])
        mediana.append(d['Mediana'])

    m.append(dados[-1]['Mediana'])
    print(m)
    val1 = str(m[-1])
    figura = px.bar(dados, x='Docente', y='Média',
                    color_discrete_sequence=px.colors.qualitative.T10, template='plotly_white', text='Média')
    figura.add_scatter(x=docente, y=mediana, xaxis='x',
                       name="Mediana: "+val1, marker=dict(color="crimson"))

    figura.update_layout(
        yaxis=dict(
            tickmode="array",
            tickfont=dict(size=15), tickangle=0
        ),
        font=dict(size=12)
    )
    figura.update_traces(
        textfont_size=15, texttemplate='%{text:.3rs}')
    figura.update_yaxes(showticklabels=True)

    medias = json.dumps(figura, cls=plotly.utils.PlotlyJSONEncoder)

    colaboracao = grafico_colaboracao()

    valor_padrao = 'circular'

    tipo_grafo(valor_padrao, colaboracao)

    titulosRepetidos = titulos_qualis()

    return render_template("resultados.html", anos=anos, graphJSON=graphJSON, graph=graph, medias=medias, listar=listar, totalNotas=totalNotas,
                           contadorEstratos=contadorEstratos, data=data, titulosRepetidos=titulosRepetidos)


@app.route("/projetos/inicio=<inicio>&fim=<fim>", methods=['POST'])
def projetos(inicio, fim):
    if request.method == 'POST':
        anos = []
        result = []
        ano_inicio = inicio
        ano_fim = fim

        for r in range(int(ano_inicio), int((ano_fim))+1):
            anos.append(r)
            r+1

    return import_project(anos)


@app.route("/tabela_periodicos_e_qualis")
def gerar_tabela_qualis():
    return render_template('qualis.html'), load_qualis()


@app.route('/resultado_por_docente')
def resultado_por_docente():

    listar = lista()
    # prof = busca_prof()
    totalNotas = soma_nota()
    contadorEstratos = contador_estratos()
    return render_template("resultados_por_docente.html", listar=listar, totalNotas=totalNotas, contadorEstratos=contadorEstratos)


@app.route('/listar')
def listar():
    contadorEstratos = contador_estratos()
    listar = lista()
    totalNotas = soma_nota()
    return render_template("resultados_por_docente.html", listar=listar, totalNotas=totalNotas, contadorEstratos=contadorEstratos)


@app.route('/corrige_notas', methods=['POST', 'GET'])
def corrige_notas():
    titulosRepetidos = titulos_qualis()

    for tits in titulosRepetidos:
        for t in tits:
            rep = titulo_repetido(t)
            if rep == 0:
                continue
            else:
                for r in rep:
                    estrato = r[2]
                    nota_temp = busca_pontuacao_estrato(estrato)
                    nota = float(nota_temp[0])
                    update_notas(nota, r[0])
            reps = qualis_repetidos(titulo=t)
            for r in reps:
                print(r)
                if r[0] == t:
                    media = float(r[1]) / float(r[3])
                    update_qualis_repetido(titulo=r[0], valor=str(media))
                    # showinfo(title="VALIDADO",message="Corrigido com Sucesso!")
                    break
    return redirect('/configuracoes')


@app.route('/contadores', methods=["POST", "GET"])
def contadores():
    if request.method == 'POST':
        busca = request.form['query']
        print(busca)
        cont = contador(busca)
        print("all list")
        # os.remove('arq.json')
        totalNotas = soma_nota_docente(busca)

    return jsonify({'htmlresponse': render_template('tabela_notas.html', cont=cont, totalNotas=totalNotas)})


@app.route('/producao_intelectual/<docente>', methods=["POST", "GET"])
def producao_intelectual(docente):
    listar = lista_docente(docente)

    return jsonify({'htmlresponse': render_template('producao_intelectual.html', listar=listar)})


@app.route('/grafico', methods=['POST', 'GET'])
def gerar_grafico():
    busca = request.form['query']

    graficos(busca)
    with open('arq.json', 'r') as file:
        data = json.load(file)

    fig = px.bar(data, x='Ano', y='Quantidade',
                 color='Estratos', barmode='stack')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # print(graphJSON)
    names = []
    values = []
    pizza_por_docente(busca)
    with open('pizza_docente.json', 'r') as piz:
        d = json.load(piz)
        names.append(d[0]['Conferencia'].capitalize())
        names.append(d[0]['Periodico'].capitalize())
        values.append(d[0]['PercConferencia'])
        values.append(d[0]['PercPeriodico'])

    figs = px.pie(names=names, values=values)

    graph = json.dumps(figs, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify({'htmlresponse': render_template('graficos.html', graphJSON=graphJSON, graph=graph)})


@app.route("/visualiza_dados/<id>", methods=['POST', 'GET'])
def visualizaDados(id):
    mostra = mostra_dados_faltantes(id)
    retorna = {'dados': id}
    return jsonify(mostra=mostra)


@app.route("/visualizar_dados/<titulo>", methods=['POST'])
def visualizarDados(titulo):
    mostra = titulo_repetido(titulo)
    retorna = {'dados': titulo}
    return jsonify(mostra=mostra)


@app.route("/edita_publicacao/<id>", methods=['POST', 'GET'])
def edita_publicacao(id):
    mostra = mostra_publicacao(id)
    return render_template('edita_publicacao.html', mostra=mostra)


@app.route("/edita_publicacao_docente/<id>", methods=['POST', 'GET'])
def edita_publicacao_docente(id):
    mostra = mostra_publicacao(id)
    return render_template('edita_publicacao_docente.html', mostra=mostra)


@app.route('/atualiza', methods=['POST'])
def atualiza():
    if request.method == "POST":
        id = request.form['id']
        # docente = request.form['nome_docente']
        # titulo = request.form['titulo']
        nome_evento = request.form['nome_evento']
        doi = request.form['doi']
        sigla = request.form['sigla']
        estratos = request.form['estratos']
        estratos = estratos.upper()

        nota_temp = busca_pontuacao_estrato(estratos)
        nota = nota_temp[0]

        versao = lista_por_id(id)

        atualizar(id, doi, sigla, nome_evento, estratos, nota, versao[11])

        flash("Atualizado com Sucesso! ")
    return resultado_total()


@app.route('/atualiza_docente', methods=['POST'])
def atualiza_docente():
    if request.method == "POST":
        id = request.form['id']
        docente = request.form['hidden_nome_docente']
        # titulo = request.form['titulo']
        nome_evento = request.form['nome_evento']
        doi = request.form['doi']
        sigla = request.form['sigla']
        estratos = request.form['estratos']
        estratos = estratos.upper()

        nota_temp = busca_pontuacao_estrato(estratos)
        nota = nota_temp[0]

        versao = lista_por_id(id)

        atualizar(id, doi, sigla, nome_evento, estratos, nota, versao[11])

        flash("Atualizado com Sucesso! ")
    return resultado_docente(docente)


@app.route('/resultado_docente', methods=['POST'])
def resultado_docente(docente):
    return resultado_editado(docente)


def resultado_editado(docente):

    listar = lista()
    # prof = busca_prof()
    totalNotas = soma_nota()
    contadorEstratos = contador_estratos()
    return render_template("resultados_por_docente.html", docente=docente, listar=listar, totalNotas=totalNotas, contadorEstratos=contadorEstratos)


@app.route("/deletarDocente/<docente>", methods=['POST'])
def deletarDocente(docente):
    deletar_docente(docente)

    return render_template('resultados_por_docente.html')


@app.route("/mostra_grafo", methods=['POST', 'GET'])
def mostra_grafo():
    if request.method == "POST":
        tipo = request.form['query']

        g = grafico_colaboracao()
        grafo = tipo_grafo(tipo, g)
        return tipo


@app.route("/wordcloud")
def wordcloud():
    page = "nuvem"
    return render_template("loading.html", page=page)


@app.route("/nuvem")
def nuvem():
    nuvem_de_palavras()
    prof = busca_prof()
    return render_template('nuvem.html', prof=prof)


@app.route("/nuvem_docente", methods=['POST', 'GET'])
def nuvem_docente():
    docente = request.form['query']
    nuvem_por_docente(docente)
    return render_template('nuvem.html')


@app.route("/configuracoes")
def configuracoes():
    valor = lista_pontuacoes()
    return render_template('notas.html', valor=valor)


@app.route("/tabela_qualis", methods=['POST'])
def tabela_qualis():
    nota = request.form.getlist('nota')
    estrato = request.form.getlist('estrato')
    notas = []
    for n in nota:

        notas.append(float(n.replace(",", ".")))

    dados = {}
    dados = zip(estrato, notas)
    print(dados)

    for dado in dados:
        update_pontuacoes(dado[0], dado[1])
    return recalcula_notas()


def recalcula_notas():
    titulos = lista()

    for t in titulos:
        estratos = t[9]
        nota_temp = busca_pontuacao_estrato(estratos)
        nota = float(nota_temp[0])
        update_notas(nota, t[4])
        # for t in tits:
        #     rep = titulo_repetido(t)
        #     if rep == 0:
        #         continue
        #     else:
        #         for r in rep:
        #             estrato = r[2]
        #             nota_temp = busca_pontuacao_estrato(estrato)
        #             nota = nota_temp[0]
        #             update_notas(nota,r[0])
    flash("Tabela atualizada com sucesso!")
    return configuracoes()


if __name__ == "__main__":
    database.tabela_resultados()
    database.tabela_pontuacoes()
    database.insert_pontuacoes()

    # app.run(debug=True)
    app.run(host='0.0.0.0')
