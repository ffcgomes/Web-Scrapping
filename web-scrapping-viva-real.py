import requests, re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Sites:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/87.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                        'referer':'https://www.vivareal.com.br/venda/ceara/fortaleza/apartamento_residencial/?__vt=ranking:default',
                        'content-type':'text/html; charset=utf-8'}

    def acessar(self,link,tries=5,timeout=10):
        for tries in range(tries):
            try:
                self.page = requests.get(link,headers=self.headers,timeout=timeout,allow_redirects=True) # Acessando página de busca
                return self.page
            except:
                pass
        else:
            return False

    def html(self,website):
        try:
            self.page_html = BeautifulSoup(website.text, 'html.parser')
        except:
            self.page_html = BeautifulSoup(website, 'html.parser')
        return self.page_html

# class Olx(Sites):
#
#     def __init__(self):
#         website =
#         super().__init__(website)
#
#     def get_data(self):

class VivaReal(Sites):

    def __init__(self):
        self.variables = {"LINK":[],"TIPO":[],"AREA":[],"UND_AREA":[],"QUARTOS":[],"BANHEIROS":[],"SUITES":[],"VAGAS":[],"PRECO":[],"MOEDA_PRECO":[],"CONDOMINIO":[],"MOEDA_CONDOMINIO":[],"ENDERECO":[],"BAIRRO":[],"LAVANDERIA":[],"JARDIM":[],"CONDOMÍNIO FECHADO":[],"VIGIA":[],"CIRCUITO DE SEGURANÇA":[],"ACADEMIA":[],"CHURRASQUEIRA":[],"PISCINA":[],"PLAYGROUND":[],"QUADRA POLIESPORTIVA":[],"ELEVADOR":[],"SALÃO DE FESTAS":[],"SALÃO DE JOGOS":[],"SAUNA":[],"AR-CONDICIONADO":[],"ESPAÇO GOURMET":[],"MOBILIADO":[],"VARANDA GOURMET":[],"CINEMA":[],"ESPAÇO VERDE / PARQUE":[],"GERADOR ELÉTRICO":[],"PISCINA PARA ADULTO":[],"ESCRITÓRIO":[],"ÁREA DE SERVIÇO":[],"CONEXÃO À INTERNET":[],"DEPÓSITO":[],"INTERFONE":[],"GRAMADO":[],"PISCINA INFANTIL":[],"SISTEMA DE ALARME":[],"VARANDA":[],"TV A CABO":[],"COZINHA":[],"QUINTAL":[],"PERTO DE VIAS DE ACESSO":[],"PRÓXIMO A SHOPPING":[],"PRÓXIMO A ESCOLA":[],"PRÓXIMO A HOSPITAIS":[],"PRÓXIMO A TRANSPORTE PÚBLICO":[],"ACESSO PARA DEFICIENTES":[],"ARMÁRIO NA COZINHA":[],"ARMÁRIO EMBUTIDO":[],"CLOSET":[],"COZINHA AMERICANA":[],"ESCADA":[],"GÁS ENCANADO":[],"GESSO - SANCA - TETO REBAIXADO":[],"JANELA DE ALUMÍNIO":[],"JANELA GRANDE":[],"LAVABO":[],"MÓVEL PLANEJADO":[],"SALA DE ALMOÇO":[],"SALA DE JANTAR":[],"SALA GRANDE":[],"VENTILAÇÃO NATURAL":[],"VISTA PANORÂMICA":[],"ÁREA DE LAZER":[],"VISTA PARA O MAR":[],"HALL DE ENTRADA":[],"DESPENSA":[],"VISTA EXTERIOR":[],"RECEPÇÃO":[],"PISTA DE COOPER":[],"ESPAÇO TEEN":[],"QUADRA DE TÊNIS":[],"SPA":[],"CABEAMENTO ESTRUTURADO":[],"GARAGEM":[],"SEGURANÇA 24H":[],"QUADRA DE SQUASH":[],"SERVIÇOS PÚBLICOS ESSENCIAIS":[],"VISTA PARA LAGO":[],"MAIS DE UM ANDAR":[],"BOX BLINDEX":[],"AQUECIMENTO":[],"PORTARIA 24H":[],"PORTÃO ELETRÔNICO":[]} #Criação do dicionário que dará origem a tabela final
        super().__init__()

    def search_page(self,pagina,attr):
        try:
            self.attr = attr
            if pagina == 1:
                url = "https://www.vivareal.com.br/venda/"+self.attr["estado"].lower()+"/"+self.attr["cidade"].lower()+"/"+self.attr["tipo"]
                self.driver = webdriver.Chrome()
                self.driver.get(url)
            if pagina != 1:
                WebDriverWait(self.driver, 120).until(lambda driver: "pagina" in driver.current_url and "="+str(pagina) in driver.current_url)
            print(self.driver.current_url)
            html = self.driver.page_source
            return html
        except:
            return False

    def close_search_page(self):
        self.driver.close()

    def next_page(self):
        element = self.driver.find_element_by_xpath("/html/body/main/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/a")
        self.driver.execute_script("arguments[0].click();", element)

    def ad_page(self,href):
        self.href = href
        website = "https://www.vivareal.com.br"+self.href
        return self.acessar(website)

    def get_data(self,ad_html):
        self.variables["LINK"].append("https://www.vivareal.com.br" + self.href)
        self.variables["TIPO"].append(self.attr["tipo"])
        for feature in ad_html.find_all("li", attrs={"class": "features__item"}): # Iterando pelas features do anúncio
            titulo = feature.get("title")
            if titulo == "Área":
                try:
                    self.variables["AREA"].append(re.search("\d+", feature.text.strip()).group(0).strip())
                except:
                    self.variables["AREA"].append("")
                try:
                    self.variables["UND_AREA"].append(re.search("\D+", feature.text.strip()).group(0).strip())
                except:
                    self.variables["UND_AREA"].append("")
            elif titulo == "Quartos":
                try:
                    self.variables["QUARTOS"].append(feature.span.text)
                except:
                    self.variables["QUARTOS"].append("")
            elif titulo == "Banheiros":
                try:
                    self.variables["BANHEIROS"].append(feature.span.text)
                except:
                    self.variables["BANHEIROS"].append("")
                try:
                    self.variables["SUITES"].append(re.search("\d+", feature.small.text).group(0))
                except:
                    self.variables["SUITES"].append("")
            elif titulo == "Vagas": #Pode ser um else, mas caso mais informação seja inserida já está na estrutura
                try:
                    self.variables["VAGAS"].append(feature.span.text)
                except:
                    self.variables["VAGAS"].append("")
        try:
            self.variables["PRECO"].append(re.sub("\D", "", ad_html.find("h3", attrs={"class": "price__price-info js-price-sale"}).text.strip()))
        except:
            self.variables["PRECO"].append("")
        try:
            self.variables["MOEDA_PRECO"].append(re.sub("[\d \.]", "", ad_html.find("h3", attrs={"class": "price__price-info js-price-sale"}).text.strip()))
        except:
            self.variables["MOEDA_PRECO"].append("")
        try:
            self.variables["CONDOMINIO"].append(re.sub("\D", "", ad_html.find("span", attrs={"class": "price__list-value condominium js-condominium"}).text.strip()))
        except:
            self.variables["CONDOMINIO"].append("")
        try:
            self.variables["MOEDA_CONDOMINIO"].append(re.sub("[\d \.]", "", ad_html.find("span", attrs={"class": "price__list-value condominium js-condominium"}).text.strip()))
        except:
            self.variables["MOEDA_CONDOMINIO"].append("")
        try:
            self.variables["ENDERECO"].append(ad_html.find("p", attrs={"class": "map__address"}).text.strip())
        except:
            self.variables["ENDERECO"].append("")
        try:
            self.variables["BAIRRO"].append(ad_html.find("p", attrs={"class": "map__address"}).text.strip().split(" - ")[1].split(",")[0])
        except:
            self.variables["BAIRRO"].append("")
        try:
            amenities = map(lambda x: x.text.strip(),ad_html.find("ul", attrs={"class": "amenities__list"}).findChildren("li")) # Lendo amenities
            for amenitie in amenities:
                self.variables[amenitie.upper()].append(1)
        except:
            pass

    def length(self):
        size = len(self.variables["LINK"])  # Número de páginas
        self.variables = {k:v+[""]*(size-len(v))for k, v in self.variables.items()} # Adicionando "" nas variáveis que não foram populadas

    def save(self):
        table = pd.DataFrame.from_dict(self.variables) #Transformando dicionário em DataFrame
        table.drop_duplicates(subset=["LINK"],keep="first",inplace=True) # Dropa anúncios repetidos
        table.to_csv("resultado.csv", sep=";", decimal=",", index=False,encoding='iso-8859-1') # Salvando DataFrame
        return table

if __name__ == "__main__":
    import time

    start = time.time()

    attrs = ({"estado": "Ceara", "cidade": "Fortaleza", "tipo": "apartamento_residencial"},
             {"estado": "Ceara", "cidade": "Fortaleza", "tipo": "casa_residencial"},
             {"estado": "Ceara", "cidade": "Fortaleza", "tipo": "lote-terreno_residencial"},
             {"estado": "Ceara", "cidade": "Fortaleza", "tipo": "lote-terreno_comercial"})  # Definindo o que vai ser buscado

    vivaReal = VivaReal()
    for attr in attrs:
        pagina = 0  # Inicializando contador que será utilizado como página
        #while True:
        for pagina in range(10):
            #pagina += 1  # Contador que passa página a cada iteração
            page = vivaReal.search_page(pagina, attr)
            print(pagina)

            if page:  # Se page não tiver sido False
                page_html = vivaReal.html(page)  # HTML da página de busca
                print(page_html)
                for link in page_html.find_all('a', "property-card__title js-cardLink js-card-title"):  # Iterando pelos links dos anuncios
                    href = link.get("href")
                    print(href)
                    ad = vivaReal.ad_page(href)

                    if ad:  # Se ad não tiver sido False
                        ad_html = vivaReal.html(ad)  # HTML da página do anúncio
                        vivaReal.get_data(ad_html)
                        vivaReal.length()
                    else: # Se ad for False, vai para a próxima iteração
                        continue

            else: # Se page for False, vai para a próxima iteração
                continue

            if page_html.find("a", attrs={"title": "Próxima página"}).get("data-page") == "": # Encerra caso o botão de próxima página estiver desativado
                vivaReal.close_search_page()
                break
            else:
                vivaReal.next_page()

    print(time.time() - start)

    vivaReal.save() # Salvar planilha com dados