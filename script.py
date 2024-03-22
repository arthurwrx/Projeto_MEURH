import time
import datetime
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By 
from datetime import datetime
import cx_Oracle
from metodos_sql import *
import sys
import subprocess
options = webdriver.ChromeOptions()
options.add_argument('--headless')

## Configurações do Chrome
# Definir o caminho para o diretório de download
caminho_download = {"download.default_directory": "C:\\Users\\arthurwrx\\Downloads"}
options.add_experimental_option("prefs", caminho_download)


driver = webdriver.Chrome(options=options)

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
        num_demandas = driver.find_elements(By.XPATH,"//tr[@class='listViewEntries']")

        print(len("Quantidade de demandas" + str(num_demandas)))

        ### Esse Script Acessa as Demandas em cada rodagem.
        for i in range(len(num_demandas)):


            ##Estou capturando a linha inteira de demanda e tratando o dado para capturar apenas o Número da Demanda
            demand = f"//tr[@id='HelpDesk_listView_row_{str(i+1)}']"
            num_demanda = driver.find_element(By.XPATH,demand).text
            num_demanda = num_demanda.split(" ")
            num_demanda = num_demanda[0]

            self.num_demanda = num_demanda

            ## Aproveito a variável demand que é a linha de cada demanda, para acessa-la e seguir para documentos
            driver.find_element(By.XPATH,demand).click()
            time.sleep(4)
            element_document = driver.find_element(By.XPATH,"//a[@displaylabel='Documentos']").click()
            time.sleep(4)
            
            ##Escolhi esse elemento para listar o número de arquivos na página
            elements_list_download = driver.find_elements(By.XPATH,"//a[@name='downloadfile']")

            print(len("Número de arquivos para baixar:" + str(elements_list_download)))
            
            ## Utilizei essa lógica para obter o link de download de cada documento disponível e em seguida
            ## Com o método get do chromedriver baixar pelo for
            for i in range(len(elements_list_download)):

                ## Esse bloco faz uma visita a cada página de Documento, escolhi capturar o href de cada linha e ir visitando
                caminho_pag_docs = driver.find_elements(By.XPATH,f'//td[contains(@class, "relatedListEntryValues")]/span/a')
                caminho_pag_doc_url = caminho_pag_docs[i]
                caminho_pag_doc_url = caminho_pag_doc_url.get_attribute('href')

                driver.get(caminho_pag_doc_url)

                print("Número da demanda: " + self.num_demanda)

                self.responsavel = driver.find_element(By.XPATH,"//span[@data-field-type='owner']").text
                print("Responsável " + self.responsavel)

                ## Porque existe dois elementos com o mesmo nome, 
                ## e eu sei que o segundo elemento sempre será o numero downloads.
                num_downloads = driver.find_element(By.XPATH,"(//span[@data-field-type='integer'])[2]").text
                print("Quantidade de downloads desse arquivo: " + num_downloads)

                ## Nesta Linha peço para obter a url de download do arquivo e com isso uso o método get para baixar o arquivo.
                download_arquivo = driver.find_element(By.XPATH,'//a[@title="Arquivo Download"]')
                download_arquivo = download_arquivo.get_attribute('href')
                download_arquivo = driver.get(download_arquivo)

                ## Nestas linhas de datas, acessei os elementos e converti para o formato aceito pelo banco.
                ## Criei data_criacao, data_modificacao e data_consulta para dar mais informação ao banco.
                data_criacao = driver.find_element(By.XPATH,"//span[@data-field-type='datetime']").text
                self.data_criacao = datetime.strptime(data_criacao, "%d-%m-%Y %I:%M %p")
                print("Data de criação: " + str(self.data_criacao))

                data_ultima_modificacao = driver.find_element(By.XPATH,"(//span[@data-field-type='datetime'])[2]").text
                self.data_ultima_modificao = datetime.strptime(data_ultima_modificacao, "%d-%m-%Y %I:%M %p")
                print("Data de modificação: " + (str(self.data_ultima_modificao)))

                self.data_hora_consulta = datetime.now()    
                print("Data de consulta:" + str(self.data_hora_consulta))
                
                self.insere_banco()

                driver.back()
                time.sleep(1)
               
            ## Após ele capturar todas as informações da demanda atual e enviar pro banco, 
            ## ele volta para a página de demandas e  vai para a próxima próxima demanda e repete o script.
            driver.get("https://test.flowpro.com.br/index.php?module=HelpDesk&view=List&app=SUPPORT")
            time.sleep(3)
    
    def insere_banco(self):
    
        try:
            cx_Oracle.init_oracle_client(lib_dir=r"C:\instantclient_21_13")
        
        except:
            pass


        dsn = cria_dsn(host="oracle.fiap.com.br", port = 1521, sid= "ORCL")
        conn = conecta_banco("rm551054", "271297", dsn)
        cursor = conn.cursor()

        print("Recebendo informações do banco...")

        ## Método de INSERT no banco de dados
        query = "INSERT INTO TB_DEMANDAS (NUMERO_DEMANDA, RESPONSAVEL, DATA_CRIACAO,DATA_ULTIMA_MODIFICACAO,DATA_HORA_CONSULTA) VALUES (:v,:v,:v,:v,:v)"
        valores = (self.num_demanda, self.responsavel, self.data_criacao,self.data_ultima_modificao,self.data_hora_consulta)
        cursor.execute(query,valores)
        conn.commit()

        print("Dados enviados ao banco!")
        
        
start = My_RH()
print("Processo Finalizado!")

# Fecha a janela do terminal
if sys.platform.startswith('win'):
    subprocess.Popen('taskkill /F /IM WindowsTerminal.exe', shell=True)
