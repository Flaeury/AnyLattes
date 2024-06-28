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
import zipfile
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
from werkzeug.utils import secure_filename
import json
import plotly
import plotly.express as px

app = Flask(__name__)
CORS(app)
app.app_context().push()

idLattes = ''

# Configurações de upload de arquivos
ALLOWED_EXTENSIONS = {'xml', 'XML', 'pdf', 'xls', 'xlsx', 'zip', 'ZIP'}

# Verifica se as pastas existem e cria se não existirem
if not os.path.isdir('curriculos'):
    os.mkdir('curriculos')
UPLOAD_FOLDER = 'curriculos'

if not os.path.isdir('arquivos'):
    os.mkdir('arquivos')

if not os.path.isdir('static/images'):
    os.mkdir('static/images')
if not os.path.isdir('static/images/nuvem_docente'):
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

def fazer_automacao():
    lattes = ",".join(request.form.get('lattes_id', '').split(";")).split(",")
    path_to_download = os.path.join(os.getcwd(), 'outputs')
   

    options = Options()
    options.set_preference('browser.download.folderList', 2)
    options.set_preference('browser.download.dir', path_to_download)
    options.set_preference('browser.helperApps.alwaysAsk.force', False)
    options.set_preference('browser.download.manager.showWhenStarting', False)
    options.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/zip')

    driver = webdriver.Firefox(options=options)
    width = height = 800
    ss_w, ss_h = pyautogui.size()
    driver.set_window_size(width, height)
    driver.set_window_position(ss_w / 2 - width / 2, ss_h / 2 - height / 2)

    lattes_url = 'http://buscatextual.cnpq.br/buscatextual/download.do?metodo=apresentar&idcnpq='

    for idcnpq in lattes:
        idcnpq = idcnpq.strip()
        location = lattes_url + idcnpq
        driver.get(location)
        print('[INFO] Firefox: page loaded OK')

        frames = driver.find_elements(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(frames[0])

        driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()
        driver.switch_to.default_content()

        button = driver.find_element(By.ID, 'submitBtn')
        time.sleep(random.randint(1, 2))
        worked = True
        time.sleep(1)
        if not button.is_enabled():
            print(f'[INFO] Firefox: solve recaptcha for idcnpq {idcnpq}')
           
            frames = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]').find_elements(By.TAG_NAME, 'iframe')
            driver.switch_to.frame(frames[0])

            time.sleep(random.randint(1, 2))
            driver.find_element(By.ID, 'recaptcha-audio-button').click()
            driver.switch_to.default_content()

            frames = driver.find_elements(By.TAG_NAME, 'iframe')
            driver.switch_to.frame(frames[-1])

            time.sleep(1)
            driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/button').click()
            time.sleep(1)
            src = driver.find_element(By.ID, 'audio-source').get_attribute('src')
            time.sleep(1)
            file_name = os.path.join(path_to_download, 'sample.mp3')
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

            try:
                key = r.recognize_google(audio)
                print(f'[INFO] Recaptcha code: {key}')
            except sr.UnknownValueError:
                print('[ERROR] Google Speech Recognition could not understand audio')
            except sr.RequestError as e:
                print(f'[ERROR] Could not request results from Google Speech Recognition service; {e}')

            driver.find_element(By.ID, 'audio-response').send_keys(key.lower())
            driver.find_element(By.ID, 'audio-response').send_keys(Keys.ENTER)
            driver.switch_to.default_content()

            time.sleep(1)
            driver.find_element(By.ID, 'submitBtn').click()
            
            destino_arquivo = os.path.join(os.getcwd(), "arquivos")
            
            file_xml = os.path.join(path_to_download, idcnpq + ".zip")
            print(f"[DEBUG] Caminho do arquivo ZIP baixado: {file_xml}")

            if os.path.exists(file_xml):
                with zipfile.ZipFile(file_xml, 'r') as zip_ref:
                    zip_ref.extractall(destino_arquivo)
                print(f"[INFO] Arquivo ZIP extraído para: {destino_arquivo}")
                os.remove(file_xml)
            else:
                worked = False
                print("[ERROR] Arquivo ZIP não encontrado ou não foi baixado corretamente.")


        else:
            time.sleep(1)
            button.click()
            
            file_xml = os.path.join(path_to_download, idcnpq+".zip")

            destino_arquivo = os.path.join(os.getcwd(), "arquivos")

            if os.path.exists(file_xml):
                with zipfile.ZipFile(file_xml, 'r') as zip_ref:
                    zip_ref.extractall(destino_arquivo)
                os.remove(file_xml)
            else:
                worked = False

        if not worked:
            continue

        shutil.move(os.path.join(os.getcwd(), "arquivos", "curriculo.xml"),
                    os.path.join(os.getcwd(), "arquivos", idcnpq + ".xml"))

    driver.quit()
