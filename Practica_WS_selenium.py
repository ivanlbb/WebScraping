import requests
import os
import csv
import argparse
import random
# importamos pandas para guardar la informacion en un csv
import pandas as pd
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.chrome.service as service

parser = argparse.ArgumentParser(description='Web Scraping de www.milanuncios.com')
parser.add_argument('paginaDesde', type=int, help="Pagina desde", default=1)
parser.add_argument('paginaHasta', type=int, help="Pagina hasta", default=5)
parser.add_argument('fromYear', type=int, help="Año mínimo de matriculación", default=2008)
parser.add_argument("toYear", type=int, help="Año máximo de matriculación", default=2018)
parser.add_argument("fromPrice", type=int, help="Precio desde",default=5000)
parser.add_argument("toPrice", type=int, help="Precio hasta",default=15000)

parametros = parser.parse_args()
paginaDesde = parametros.paginaDesde
paginaHasta = parametros.paginaHasta
fromYear = parametros.fromYear;
toYear = parametros.toYear;
fromPrice = parametros.fromPrice;
toPrice = parametros.toPrice;
baseURL = 'www.milanuncios.com'

def getFicheroRobots():
    urlRobots = baseURL+'/robots.txt'
    return requests.get(urlRobots)
    
#lista de user agents para simular que hay un humano haciendo las peticiones
def getUserAgent():
    user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',

    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    ]
    return random.choice(user_agent_list)

def getURL(pagina, fromYear = 2006, toYear = 2016,fromPrice = 5000,toPrice = 12000):
    url = 'https://www.milanuncios.com/coches-de-segunda-mano/?demanda=n&anod={0}&anoh={1}&desde={2}&hasta={3}'.format(fromYear, toYear, fromPrice, toPrice)
    if pagina > 1:
        url = url+"&pagina="+str(pagina)       
    return url
    
def __ie(url):
    print(url)
    driver = webdriver.Ie()    
    driver.get(url)
    contenido = driver.page_source
    sleep(randint(10,20))
    driver.quit()    
    return contenido
    
def __chrome (url):
    print(url)
    driver = webdriver.Chrome()    
    driver.get(url);
    contenido = driver.page_source
    sleep(randint(10,20))
    driver.quit()    
    return contenido

    
def getResultados(pagina, fromYear = 2006, toYear = 2016,fromPrice = 5000,toPrice = 12000):
    print ("Pagina "+str(pagina))
    #https://www.milanuncios.com/coches-de-segunda-mano/?fromSearch=1&desde=1000&hasta=2500&demanda=n&anod=2006&anoh=2017
    #url = "https://www.milanuncios.com/coches-de-segunda-mano-en-madrid/?fromSearch=1&demanda=n&anod=2008&anoh=2018"
    url = 'https://www.milanuncios.com/coches-de-segunda-mano/?demanda=n&anod={0}&anoh={1}desde={2}&hasta={3}'.format(fromYear, toYear, fromPrice, toPrice)
    #url = 'https://www.milanuncios.com/coches-de-segunda-mano/'
    if pagina > 1:
        url = url+"&pagina="+str(pagina)
        
    print (url)
    
        
    #vamos cambiando el user-agent
    referer = 'https://www.milanuncios.com/coches-de-segunda-mano/'
    #headers2 = {'User-Agent': getUserAgent(),
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'
    headers2 = {'User-Agent': user_agent,
               'referer':referer,
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",                
               "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
               "Connection": "keep-alive",
               "Cookie":"utag_main=v_id:016a013abaff001d3a0f1ca66c230004d001c00d00bd0$_sn:1$_ss:0$_pn:5%3Bexp-session$_st:1554800724273$ses_id:1554798787327%3Bexp-session$vapi_domain:milanuncios.com; AMCV_05FF6243578784B37F000101%40AdobeOrg=-1303530583%7CMCIDTS%7C17996%7CMCMID%7C00363153532708056901843593687525795943%7CMCAAMLH-1555403588%7C6%7CMCAAMB-1555403588%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1554805988s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18003%7CvVersion%7C3.3.0; AMCVS_05FF6243578784B37F000101%40AdobeOrg=1; cto_lwid=d5cb3b90-61ce-46b8-9d9b-2fa914831a2d; optimizelyEndUserId=oeu1554798788563r0.2254370489728008; s_cc=true; aam_uuid=00101397439086136261815161914665238823; _pulse2data=8f7653e6-5a77-48b4-9b95-f4892898f8ba%2Cv%2C%2C1554799689395%2CeyJpc3N1ZWRBdCI6IjIwMTktMDQtMDlUMDg6MzM6MDNaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..Q98RTM93knTx8R8I7yW4VA.0ldirSwFaRLdFx3_9Z6v9SDLeGvVGClZh8nM4w0NuIiHjPH0M0ti_Mysx1WjBX_wrySaURMVY05KlhDIHVcwsQgsVIMdgbFUYFUx-P0pumOytoSkT1XvcRH-xznPaUWVzW4xPJHPN_VqFVWgPbrovlD1qXWndtuF6MeP-0N5fTp6dy2I8H1VMtAh2Eux3gUR-H5aUIV5e_PG2Q4IL_tqqg.xtK5mjX2LImT8R3Ug3muyA%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..T5nKXweEtfvBFyvfk5lA5qc0qKLnt3cHmVHH0yyI5H8; s_sq=schibstedspainmiscmilanunciosprod%3D%2526c.%2526a.%2526activitymap.%2526page%253DCoches%2526link%253DBUSCAR%2526region%253Dbusgen%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DCoches%2526pidt%253D1%2526oid%253Djavascript%25253Acabu%252528%252529%2526ot%253DA; PHPSESSID=c3789c21bd9dc275e6f9be74c0da85bc; pv=3; __utma=204290060.1157007430.1554798827.1554798827.1554798827.1; __utmc=204290060; __utmz=204290060.1554798827.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); D_IID=928C9A1B-1CE2-3231-B60F-1F35D3963ED1; D_UID=F5574E04-02DA-3FBE-B5DE-9929ED9EDB43; D_ZID=0A770E89-B581-397B-8F2D-959A05B088AB; D_ZUID=F0329786-DE6D-368C-9053-0EBF1A8C010A; D_HID=16A6D245-F844-3F11-8360-8A2FB45C08D1; D_SID=85.56.96.69:h3ITzqscyjHvH3HugSqLDPBzhogL3sFO/S7tvMdvm94; euconsent=BOeu3k7Oeu3k7CBAABESCN-AAAAmd7_______9______5uz_Ov_v_f__33e8__9v_l_7_-___u_-3zd4-_1vf99yfm1-7etr3tp_87ues2_Xur__59__3z3_9phPrsk89ryw",                
               "Host": "www.milanuncios.com"}

    
    headers = {'User-Agent': user_agent,'referer':referer}
    print (headers2)
    page = requests.get(url, headers=headers2)
    print (page.text)
    try:
        fichRespuesta = 'respuesta-'+str(pagina)+'.html'
        file = open(fichRespuesta, "wb+")
        contenido = page.text.encode('UTF-8')
        file.write(contenido)
        file.flush()
        file.close()
    except Exception as e:
        print (e)
        pass
    return page

#guardar los resultados en un csv    
def guardar_resultados(lista):
    nombreFichero = "FindMyCar_"+(datetime.today().strftime('%Y%m%d%H%M%S'))+".csv" 
    dataset = pd.DataFrame(lista)
    cabeceras = ['Coche','Link', 'Precio', 'Año', 'Kms', 'Combustible', 'Potencia', 'Puertas', 'Cambio', 'Localizacion']
    dataset.columns = cabeceras
    dataset.to_csv(nombreFichero, index = False)    

def __guardaRespuesta(i, pagina):
    try:
        fichRespuesta = 'respuesta-'+str(i)+'.html'
        file = open(fichRespuesta, "wb+")
        #contenido = page.text.encode('UTF-8')
        file.write(pagina.encode('UTF-8'))
        file.flush()
        file.close()
    except Exception as e:
        print (e)
        pass
    return 'Respuesta guardada'
   

    
from random import randint
from time import sleep

#obtenemos los resultados de las 5 primeras paginas 
listaCoches=[]
for i in range (paginaDesde,paginaHasta+1): 
    #pagina = getResultados(i, fromYear, toYear, fromPrice, toPrice)    
    #pagina = getResultadosSelenium(i, fromYear, toYear, fromPrice, toPrice)
    url = getURL(i, fromYear, toYear, fromPrice, toPrice)
    #if i % 2 == 0:
     #   pagina = __ie(url)
    #else:
    pagina = __chrome(url)
    print(__guardaRespuesta(i, pagina))
    #soup = BeautifulSoup(pagina.text,'html.parser')
    soup = BeautifulSoup(pagina,'html.parser')    
    for coches in soup.find_all('div', class_='aditem-detail'):        
            titulo = coches.find(class_="aditem-detail-title")
            #obtener el href del titulo. Si no lo encontramos, consideramos que no es un vehiculo
            if titulo['href'] is not None:
                href = 'www.milanuncios.com'+titulo['href']
                #localizacion
                region = coches.find(class_="list-location-region")
                if region is None:
                    region = 'desconocido'
                #caracteristicas
                div1 = coches.find(class_="adlist-tagsbox-inlineblockline")
                precio = div1.find(class_="aditem-price")
                year = div1.find(class_="ano tag-mobile")
                kms = div1.find(class_="kms tag-mobile")
                diesel = div1.find(class_="die tag-mobile")              
                if diesel is None:
                    diesel = div1.find(class_="gas tag-mobile")
                potencia = div1.find(class_="cc tag-mobile")
                puertas = div1.find(class_="ejes tag-mobile")
                cambio = div1.find(class_="cmanual tag-mobile")
                if cambio is None:
                    cambio = div1.find(class_="cauto tag-mobile")
                
                try:
                    listaCoches.append((titulo.text,href,precio.text,year.text,kms.text,diesel.text,potencia.text, puertas.text,cambio.text, region.text))
                except AttributeError:
                    #algun elemento es nulo, seguimos avanzando
                    pass
    #dormimos un numero aleatorio de segundos entre 20 y 60 para prevenir que nos baneen
    dormir =  randint(20,60)   
    print ('Durmiendo '+str(dormir))
    sleep(dormir)
    
print ("Encontrados: "+str(len(listaCoches)))
#for i in range(len(listaCoches)):
#    print(listaCoches[i])
if len(listaCoches)> 0:
	guardar_resultados(listaCoches)

