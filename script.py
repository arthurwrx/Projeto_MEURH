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
        time.sleep(2)
        
        ## Achei mais fácil usar o get pois já estou logado e sei que a página de demandas é sempre a mesma, ou seja
        ## só redirecionar direto para página de demandas sem precisar envolver clicks e inclusive é mais rápido.

        driver.get("https://test.flowpro.com.br/index.php?module=HelpDesk&view=List&app=SUPPORT")
        time.sleep(2)

        ## Como eu não sei quantas demandas vão ter, sempre vou pedir para ele listar para mim antes...
        num_demands = driver.find_elements(By.XPATH,"//tr[@class='listViewEntries']")
        print(len(num_demands))

        for i in range(len(num_demands)):


            demand = f"//tr[@id='HelpDesk_listView_row_{str(i+1)}']"
            print(demand)
            driver.find_element(By.XPATH,demand).click()

            element_documents = driver.find_element(By.XPATH,"//li[@data-label-key='Documents']").click()

















start = My_RH()





