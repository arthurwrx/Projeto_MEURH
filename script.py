""" 01 - Documente o projeto
    02 - Consiga fazer o pedido
    03 - Dê sugestões de melhorias e faça além do pedido
    """
import time
from openpyxl import load_workbook
import openpyxl
import pyautogui
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By 
import PySimpleGUI as sg

service = Service(executable_path="./chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

class My_RH:

    def __init__(self, val = 1):

        driver.get("https://test.flowpro.com.br/")

        user = driver.find_element(By.XPATH,"//input[@name='username']").send_keys("teste.rpa")
        password = driver.find_element(By.XPATH,"//input[@name='password']").send_keys("Teste@rpa2024")
        entry_buttom = driver.find_element(By.XPATH,"//button[@type='submit']").click()





start = My_RH()





