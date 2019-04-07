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

parser = argparse.ArgumentParser(description='Web Scraping de www.milanuncios.com')
parser.add_argument('fromYear', type=int, help="Año mínimo de matriculación", default=2008)
parser.add_argument("toYear", type=int, help="Año máximo de matriculación", default=2018)
parser.add_argument("fromPrice", type=int, help="Precio desde",default=5000)
parser.add_argument("toPrice", type=int, help="Precio hasta",default=15000)

parametros = parser.parse_args()
fromYear = parametros.fromYear;
toYear = parametros.toYear;
fromPrice = parametros.fromPrice;
toPrice = parametros.toPrice;

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
    
    
def getResultados(pagina, fromYear = 2006, toYear = 2016,fromPrice = 5000,toPrice = 12000):
    print ("Pagina "+str(pagina))
    #https://www.milanuncios.com/coches-de-segunda-mano/?fromSearch=1&desde=1000&hasta=2500&demanda=n&anod=2006&anoh=2017
    #url = "https://www.milanuncios.com/coches-de-segunda-mano-en-madrid/?fromSearch=1&demanda=n&anod=2008&anoh=2018"
    url = "https://www.milanuncios.com/coches-de-segunda-mano/?fromSearch=1&demanda=n&anod={0}&anoh={1}desde={2}&hasta={3}".format(fromYear, toYear, fromPrice, toPrice)
    #url = "https://www.milanuncios.com/coches-de-segunda-mano/?fromSearch=1&demanda=n&anod=2008&anoh=2018&desde=1000&hasta=2500"
    if pagina > 1:
        url = url+"&pagina="+str(pagina)
    print (url)
        
    #vamos cambiando el user-agent
    headers = {'User-Agent': getUserAgent(),
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", 
               "Accept-Encoding": "gzip, deflate, sdch, br",
               "Accept-Language": "es-ES,es;q=0.9,ca;q=0.8,en;q=0.7", 
               "Cache-Control": "no-cache","dnt": "1","Pragma": "no-cache","Upgrade-Insecure-Requests": "1"} 
    print (headers)
    page = requests.get(url, headers=headers)
    #print (page.text)
    return page

#guardar los resultados en un csv    
def guardar_resultados(lista):
    dataset = pd.DataFrame(lista)
    cabeceras = ['Coche','Link', 'Precio', 'Año', 'Kms', 'Combustible', 'Potencia', 'Puertas', 'Cambio']
    dataset.columns = cabeceras
    dataset.to_csv("FindMyCar.csv", index = False)    
    
from random import randint
from time import sleep

#obtenemos los resultados de las 5 primeras paginas 
listaCoches=[]
for i in range (1,6): 
    #dormimos un numero aleatorio de segundos entre 5 y 10 para prevenir que nos baneen    
    sleep(randint(5,10))
    pagina = getResultados(i, fromYear, toYear, fromPrice, toPrice)
    soup = BeautifulSoup(pagina.text,"html.parser")    
    for coches in soup.find_all('div', class_='aditem-detail'):
            titulo = coches.find(class_="aditem-detail-title")
            #obtener el href del titulo
            href = titulo['href']
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
            region =  div1.find(class_="list-location-region")
            try:
                listaCoches.append((titulo.text,href,precio.text,year.text,kms.text,diesel.text,potencia.text, puertas.text,cambio.text, region.text))
            except AttributeError:
                #algun elemento es nulo, seguimos avanzando
                pass
        
print ("Encontrados: "+str(len(listaCoches)))
#for i in range(len(listaCoches)):
#    print(listaCoches[i])
if len(listaCoches)> 0:
	guardar_resultados(listaCoches)

