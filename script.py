import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By 

options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Definir o caminho para o diretório de download
caminho_download = {"download.default_directory": "C:\\Users\\ArthurLN\\Downloads"}
options.add_experimental_option("prefs", caminho_download)  # Correção do nome do argumento para "prefs"

service = Service(executable_path="./chromedriver.exe")

driver = webdriver.Chrome(service=service, options=options)

class My_RH:

    def __init__(self):

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
        ## E eu sei que o find_elements lista todos os elementos com esse endereço de baixo para cima
        num_demands = driver.find_elements(By.XPATH,"//tr[@class='listViewEntries']")
        print(len(num_demands))

        for i in range(len(num_demands)):

            demand = f"//tr[@id='HelpDesk_listView_row_{str(i+1)}']"
            print(demand)
            driver.find_element(By.XPATH,demand).click()
            time.sleep(4)
            element_documents = driver.find_element(By.XPATH,"//a[@displaylabel='Documentos']").click()
            time.sleep(4)
            
            elements_list_download = driver.find_elements(By.XPATH,"//a[@name='downloadfile']")

            print(len(elements_list_download))
            

            ## Utilizei essa lógica para obter o link de download de cada documento disponível e em seguida
            ## Com o método get do chromedriver baixar pelo for
             
            for i in range(len(elements_list_download)):

                download_arquivo = elements_list_download[i]
                download_arquivo = download_arquivo.get_attribute('href')
                
                print(download_arquivo)

                driver.get(download_arquivo)

            driver.get("https://test.flowpro.com.br/index.php?module=HelpDesk&view=List&app=SUPPORT")
            time.sleep(3)
            










                

















start = My_RH()





