from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import re
from unicodedata import normalize
from selenium.common.exceptions import NoSuchElementException

filepath = './resource\whatsapp_session.txt'
driver = webdriver


def crear_driver_session():

    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            if cnt == 0:
                executor_url = line
            if cnt == 1:
                session_id = line

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    org_command_execute = RemoteWebDriver.execute

    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(
        command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver


def buscar_chats():
    print("BUSCANDO CHATS")
    chats = driver.find_elements_by_class_name("_3m_Xw")
    for chat in chats:

        element_name = chat.find_elements_by_class_name(
            'FqYAR')  # OBTENGO EL NOMBRE
        name = element_name[0].text.upper().strip()

        print("IDENTIFICANDO CONTACTO")
        mensaje = ""
        with open("./resource/contactos_autorizados.txt", mode='r', encoding='utf-8') as archivo:
            contactos = [{'name': x[0], 'message':x[1]}
                         for x in (linea.rstrip().split('|') for linea in archivo)]
            print(contactos)
            if not any(d['name'] == name for d in contactos):
                print("CONTACTO NO AUTORIZADO : ", name)
                continue
            else:
                mensaje = [val['message']
                           for val in contactos if val['name'] == name]
        print(name, "AUTORIZADO PARA SER ATENDIDO POR BOT")
        chat.click()  # selecciono el mensaje
        text_box_write = driver.find_elements_by_class_name("_13NKt")[1]
        text_box_write.clear()  # borrar mensaje por si tenia
        text_box_write.send_keys(mensaje)
        driver.find_elements_by_class_name("_4sWnG")[0].click()
        return True
    return False


def whatsapp_boot_init():
    global driver
    driver = crear_driver_session()
    buscar_chats()


whatsapp_boot_init()
