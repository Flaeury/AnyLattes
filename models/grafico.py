# -*- coding: utf-8 -*-
from models.gerar_nuvem import *
import matplotlib.pyplot as plt
import json
from models.docente import contador
from models.consulta import *
import statistics
import networkx as nx
import matplotlib
matplotlib.use('Agg')

# from wordcloud import WordCloud
# import nltk
# import wordcloud


def graficos(busca):
    nota = contador(busca)
    lista = []
    content = {}
    for n in nota:
        content = {'Ano': n[0], 'Estratos': n[1], 'Quantidade': n[2]}
        lista.append(content)
        content = {}

    json_object = json.dumps(lista, indent=4)
    with open("arq.json", "w") as outfile:
        outfile.write(json_object)


def pizza(from_year, to_year, nome_docente='*'):
    valor = perc(from_year, to_year, nome_docente)
    lista = []
    content = {}

    for n in valor:
        content = {'Total': n[0], 'Periodico': n[1], 'Conferencia': n[2],
                   'PercConferencia': n[4], 'PercPeriodico': n[3]}
        lista.append(content)
        content = {}

    json_object = json.dumps(lista, indent=4)
    with open("pizza.json", "w") as outfile:
        outfile.write(json_object)
        
    

def pizzaPeriodico(from_year, to_year, nome_docente='*'):
    valor = percPeriodico(from_year, to_year, nome_docente)
    lista = []
    content = {}

    for n in valor:
        content = {
            'Total': n[0], 'Percentual_A1': n[1], 'Percentual_A2': n[2],
            'Percentual_A3': n[3], 'Percentual_A4': n[4], 'Percentual_B1': n[5],
            'Percentual_B2': n[6], 'Percentual_B3': n[7], 'Percentual_B4': n[8],
            'Percentual_C': n[9], 'nao_classificado': n[10],
            'A1': n[0] * n[1] / 100.0, 'A2': n[0] * n[2] / 100.0, 'A3': n[0] * n[3] / 100.0,
            'A4': n[0] * n[4] / 100.0, 'B1': n[0] * n[5] / 100.0, 'B2': n[0] * n[6] / 100.0,
            'B3': n[0] * n[7] / 100.0, 'B4': n[0] * n[8] / 100.0, 'C': n[0] * n[9] / 100.0,
            'nao_classificado': n[0] * n[10] / 100.0
        }
        lista.append(content)

    json_object = json.dumps(lista)
    with open("pizzaPeriodico.json", "w") as outfile:
        outfile.write(json_object)
        
def pizzaConferencia(from_year, to_year, nome_docente='*'):
    valor = percConferencia(from_year, to_year, nome_docente)
    lista = []
    content = {}

    for n in valor:
        content = {
            'Total': n[0], 'Percentual_A1': n[1], 'Percentual_A2': n[2],
            'Percentual_A3': n[3], 'Percentual_A4': n[4], 'Percentual_B1': n[5],
            'Percentual_B2': n[6], 'Percentual_B3': n[7], 'Percentual_B4': n[8],
            'Percentual_C': n[9], 'nao_classificado': n[10],
            'A1': n[0] * n[1] / 100.0, 'A2': n[0] * n[2] / 100.0, 'A3': n[0] * n[3] / 100.0,
            'A4': n[0] * n[4] / 100.0, 'B1': n[0] * n[5] / 100.0, 'B2': n[0] * n[6] / 100.0,
            'B3': n[0] * n[7] / 100.0, 'B4': n[0] * n[8] / 100.0, 'C': n[0] * n[9] / 100.0,
            'nao_classificado': n[0] * n[10] / 100.0
        }
        lista.append(content)

    json_object = json.dumps(lista)
    with open("pizzaConferencia.json", "w") as outfile:
        outfile.write(json_object)


def pizza_por_docente(docente):
    valor = perc_docente(docente)
    lista = []
    content = {}

    for n in valor:
        content = {'Total': n[0], 'Periodico': n[1], 'Conferencia': n[2],
                   'PercConferencia': n[4], 'PercPeriodico': n[3]}
        lista.append(content)
        content = {}
        json_object = json.dumps(lista, indent=4)
    with open("pizza_docente.json", "w") as outfile:
        outfile.write(json_object)


def grafico_media(from_year, to_year, nome_docente='*'):

    nota = media_docentes(from_year=from_year,
                          to_year=to_year, nome_docente=nome_docente)

    notas = []

    for n in nota:
        notas.append(n[1])
    md = statistics.median(notas)
    mediana = "{:.3f}".format(md)
    print(mediana)

    lista = []
    content = {}
    for n in nota:

        content = {'Docente': n[0], 'Pontuação': n[1], 'Mediana': mediana}
        lista.append(content)
        content = {}

    json_object = json.dumps(lista, indent=4)
    with open("media_docentes.json", "w") as outfile:
        outfile.write(json_object)


def grafico_para_media(from_year, to_year, nome_docente='*'):

    nota = media_docentes(from_year=from_year,
                          to_year=to_year, nome_docente=nome_docente)

    notas = []

    for n in nota:
        notas.append(n[1])
    media = statistics.mean(notas)
    mediaTotal = "{:.3f}".format(media)

    return mediaTotal


def grafico_colaboracao(from_year, to_year, nome_docente='*'):
    lista_docente = []
    G = nx.Graph()
    docente = docente_titulos_repetidos(from_year, to_year, nome_docente)

    for doc in docente:
        for d in doc:
            lista_docente.append(d)
            d = d.split()[0] + " " + d.split()[-1]
            G.add_node(d)

    valor = titulos_repetidos(from_year, to_year, nome_docente)

    for i in range(0, len(valor)):
        atual = valor[i][0]
        anterior = valor[i-1][0]

        docente1 = valor[i][1].split()[0] + ' ' + valor[i][1].split()[-1]
        # print(docente1)
        docente2 = valor[i-1][1].split()[0] + ' ' + valor[i-1][1].split()[-1]
        # print(docente2)
        if atual == anterior:
            G.add_edge(docente1, docente2)
    # A = nx.adjacency_matrix(G)
    # fig = plt.figure(1,figsize=(20,15),dpi=100)
    # nx.draw_circular(G, with_labels=True, node_size=5000,font_size=15)
    # plt.savefig("static/images/matriz_colaboracao_circular.png")
    return G


def tipo_grafo(valor, G):
    # plt.cla()

    if valor == 'circular':
        fig = plt.figure(1, figsize=(18, 15), dpi=100)
        nx.draw_circular(G, with_labels=True, node_size=5000, font_size=15)
        plt.savefig("static/images/matriz_colaboracao_circular.png")

    elif valor == 'kamada_kawai':
        fig = plt.figure(1, figsize=(18, 15), dpi=100)
        nx.draw_kamada_kawai(G, with_labels=True, node_size=5000, font_size=15)
        plt.savefig("static/images/matriz_colaboracao_kamada_kawai.png")

    elif valor == 'planar':
        fig = plt.figure(1, figsize=(18, 15), dpi=100)
        nx.draw_planar(G, with_labels=True, node_size=5000, font_size=15)
        plt.savefig("static/images/matriz_colaboracao_planar.png")

    elif valor == 'random':
        fig = plt.figure(1, figsize=(18, 15), dpi=100)
        nx.draw_random(G, with_labels=True, node_size=5000, font_size=15)
        plt.savefig("static/images/matriz_colaboracao_random.png")

    plt.clf()


def nuvem_de_palavras():
    nuvem_geral()
