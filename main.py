# From system
import os
import time
import random
import pyautogui
# From selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
# For solving recaptcha
import speech_recognition as sr
import urllib
import pydub
import shutil
import zipfile
from pathlib import Path


def descompactar(idcnpq):
    shutil.move(str(Path.home()) + "/Downloads/" + idcnpq +
                ".zip", os.getcwd() + "/arquivos/" + idcnpq + ".zip")

    path_to_zipfile = os.getcwd() + "/arquivos/" + idcnpq + ".zip"

    destino_arquivo = "arquivos/"

    if os.path.exists(path_to_zipfile):
        with zipfile.ZipFile(path_to_zipfile, 'r') as zip_ref:
            zip_ref.extractall(destino_arquivo)
        print(
            f'Arquivo ZIP {path_to_zipfile} descompactado com sucesso em {destino_arquivo}')

        os.remove(path_to_zipfile)
        print(
            f'Arquivo ZIP {path_to_zipfile} removido após extração.')

    else:
        worked = False
        print(
            f'O arquivo ZIP {path_to_zipfile} não foi encontrado.')


# Define download path
path_to_download = os.getcwd() + '/outputs'

# Define a new instance of firefox with specific options
options = Options()
# options.headless = True # Hide firefox window
options.set_preference('browser.download.folderList', 2)  # use specific folder
options.set_preference('browser.download.dir',
                       path_to_download)  # Se path to download
# Do not ask anything (no pop up)
options.set_preference('browser.helperApps.alwaysAsk.force', False)
# Do not show anything (no pop up)
options.set_preference('browser.download.manager.showWhenStarting', False)
options.set_preference('browser.helperApps.neverAsk.saveToDisk',
                       'application/zip')  # MIME type for zip
print('[INFO] Preferences: OK')

# Define a new firefox instance
driver = webdriver.Firefox(options=options)
width = height = 800
ss_w, ss_h = pyautogui.size()  # Cross-platform to get screen resolution
driver.set_window_size(width, height)
driver.set_window_position(
    ss_w / 2 - width / 2, ss_h / 2 - height / 2)  # Center the window
print('[INFO] Firefox: opened OK')

# Graduação
lattes = [
    '2949449810540513',  # André Figueira Riker
    '5376253015721742',  # Antonio Jorge Gomes Abelém
    '7709951222407913',  # Benedito de Jesus Pinheiro Ferreira
    '3032638002357978',  # Bianchi Serique Meiguins
    '1614538302774823',  # Carla Alessandra Lima Reis
    '2948406243474342',  # Carlos Gustavo Resque dos Santos
    '9626971450974065',  # Cassia Maria Carneiro Kahwage
    '4742268936279649',  # Claudomiro de Souza de Sales Junior
    '6490014244112888',  # Cleidson Ronald Botelho de Souza
    '8273198217435163',  # Denis Lima do Rosário
    '4423219093583221',  # Dionne Cavalcante Monteiro
    '7676631005873564',  # Fabiola Pantoja Oliveira Araújo
    '5883877669437870',  # Filipe de Oliveira Saraiva
    '1631238943341152',  # Gustavo Henrique Lima Pinto
    '5219735119295290',  # Jefferson Magalhães de Morais
    '8158963767870649',  # Josivaldo de Souza Araújo
    '0970111009687779',  # Lídio Mauro Lima de Campos
    '2130563131041136',  # Marcelle Pereira Mota
    '6655468164115415',  # Marianne Kogut Eliasquevici
    '9756167788721062',  # Nelson Cruz Sampaio Neto
    '3286528998900137',  # Raimundo Viegas Junior
    '1572121571522063',  # Regiane Silva Kawasaki Francês
    '9157422386900321',  # Reginaldo Cordeiro dos Santos Filho
    '7469949213441010',  # Renato Hidaka Torres
    '6894507054383644',  # Roberto Samarone dos Santos Araújo
    '9839778710074372',  # Rodrigo Quites Reis
    '2080791630485427',  # Sandro Ronaldo Bezerra Oliveira
    '8798424081680540',  # Victor Hugo Santiago Costa Pinto
    '2484200467965399',  # Vinicius Augusto Carvalho de Abreu
    '8483188010111086',  # Jorge Amaro de Sarges Cardoso
    '1792273348137115'  # Adelaine Brandão Soares
]

# Define default URL
# # Note that the last option (idcnpq) is the professor lattes ID
lattes_url = 'http://buscatextual.cnpq.br/buscatextual/download.do?metodo=apresentar&idcnpq='

# Iterate through all professor's id
for idcnpq in lattes:
    location = lattes_url + idcnpq
    driver.get(location)
    print('[INFO] Firefox: page loaded OK')

    # Find iframe tag and switch to that iframe context
    frames = driver.find_elements(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(frames[0])

    # Click on recaptcha checkbox and switch to default context
    driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-border').click()
    driver.switch_to.default_content()

    # Investigate submit button
    button = driver.find_element(By.ID, 'submitBtn')
    time.sleep(random.randint(1, 2))

    # If true, do recaptcha
    # if button.get_attribute('disabled'):
    if not button.is_enabled():
        print('[INFO] Firefox: solve recaptcha for idcnpq {}'.format(idcnpq))
        # Find iframe tag and switch to that iframe context
        frames = driver.find_element(
            By.XPATH, '/html/body/div[2]/div[4]').find_elements(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(frames[0])

        # Click on recaptcha audio button (alternative way to solve recaptcha)
        time.sleep(random.randint(1, 2))
        driver.find_element(By.ID, 'recaptcha-audio-button').click()

        # Switch to default context again
        driver.switch_to.default_content()

        # Find iframe tag and switch to the last context
        frames = driver.find_elements(By.TAG_NAME, 'iframe')
        driver.switch_to.frame(frames[-1])

        # [Optional] Wait 1 second and play audio
        time.sleep(1)
        driver.find_element(
            By.XPATH, '/html/body/div/div/div[3]/div/button').click()

        # Download mp3 file
        src = driver.find_element(By.ID, 'audio-source').get_attribute('src')
        file_name = path_to_download + '/sample.mp3'
        urllib.request.urlretrieve(src, file_name)
        print('[INFO] Firefox: download audio OK')

        # Get file and convert to wav extension
        sound = pydub.AudioSegment.from_mp3(file_name)
        file_name = file_name.replace('.mp3', '.wav')
        sound.export(file_name, format='wav')
        print('[INFO] Firefox: converted audio OK')

        # Submit audio to a speechrecognition algorithm from Google
        sample_audio = sr.AudioFile(file_name)
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)

        try:
            key = r.recognize_google(audio)
            print('[INFO] Recaptcha code: {}'.format(key))
        except sr.UnknownValueError:
            print('[ERROR] Google Speech Recognition could not understand audio')
        except sr.RequestError as e:
            print(
                '[ERROR] Could not request results from Google Speech Recognition service; {0}'.format(e))

        # Send string (key) back to recaptcha page and switch to default context again
        driver.find_element(By.ID, 'audio-response').send_keys(key.lower())
        driver.find_element(By.ID, 'audio-response').send_keys(Keys.ENTER)
        driver.switch_to.default_content()

        # Submit solution by clicking the button
        time.sleep(1)
        driver.find_element(By.ID, 'submitBtn').click()
        print('[INFO] Firefox: download zip file OK\n')

        descompactar(idcnpq)

    else:  # If false, just click and download zip file
        print('[INFO] Firefox: no recaptcha to solve for {}'.format(idcnpq))
        time.sleep(1)
        button.click()
        print('[INFO] Firefox: download zip file OK\n')

        descompactar(idcnpq)

driver.quit(idcnpq)
