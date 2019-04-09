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
               "Cookie":"utag_main=v_id:0169fdbf1ee60012334d76079b4f0004d002e00d00bd0$_sn:1$_ss:0$_pn:4%3Bexp-session$_st:1554742180343$ses_id:1554740354790%3Bexp-session$vapi_domain:milanuncios.com; AMCV_05FF6243578784B37F000101%40AdobeOrg=-1303530583%7CMCIDTS%7C17995%7CMCMID%7C86401202813001670741111701639523113036%7CMCAAMLH-1555345155%7C6%7CMCAAMB-1555345155%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1554747555s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; __utma=204290060.1503549214.1554740355.1554740355.1554740355.1; __utmc=204290060; __utmz=204290060.1554740355.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); optimizelyEndUserId=oeu1554740355404r0.7546927991751203; AMCVS_05FF6243578784B37F000101%40AdobeOrg=1; s_cc=true; aam_uuid=85936740755703892181137313199619485964; cto_lwid=2aaabebc-5e14-4b18-ab2f-e847e784123e; _pulse2data=b0f0db27-e0b0-4484-8630-2ddcd669bd32%2Cv%2C%2C1554741259354%2CeyJpc3N1ZWRBdCI6IjIwMTktMDQtMDhUMTY6MTk6MTNaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..6SDtk0jGhRZAy6ndoT4BKA.1DShJpo_fwxc5EQmRLdikCCfjqyXL2pX3mcxe6J78Fn33OOXVO9mgW8NTgiYq8ncAUbf20l4P5iNzzKLfBmX_y5_V2fIRifmqXNjOMAUeVRoUJUmnXOGXrYdgvSFQ1Oqvuya6ANVM6J07mm31dirW1G060Q6pfKCcf1FlXgxNG0pr5Y3xjorWeM09glipdRc8vZJxzwgkEijURrbUA7Ymw.wchoYMV-EIRHDT89_gMosA%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..LhlEkY984i97wGj5SWzbeGuG-zX5pjYvINL3tlAk-YE; cto_idcpy=b445e006-9f99-4fe7-b3a0-c86fab8482a3; s_sq=%5B%5BB%5D%5D; PHPSESSID=00f3bfae269aeed984fabc1037bcd692; pv=2; D_IID=6EA5190D-B579-3039-8A3A-2AA23CFA183C; D_UID=EADDDD80-E7DA-329C-AA05-E00EDFF37BE4; D_ZID=843C5DD3-9B1E-3E65-8A79-8E93968FE8E1; D_ZUID=C60960B7-6C70-3C0A-A40D-CE354CB42363; D_HID=0B646FD9-1620-3843-8F40-44A9558ADD3B; D_SID=85.56.96.69:h3ITzqscyjHvH3HugSqLDPBzhogL3sFO/S7tvMdvm94; euconsent=BOeso2YOeso2ZCBAABESCN-AAAAmd7_______9______5uz_Ov_v_f__33e8__9v_l_7_-___u_-3zd4-_1vf99yfm1-7etr3tp_87ues2_Xur__59__3z3_9phPrsk89ryw",                
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
    dataset = pd.DataFrame(lista)
    cabeceras = ['Coche','Link', 'Precio', 'Año', 'Kms', 'Combustible', 'Potencia', 'Puertas', 'Cambio', 'Localizacion']
    dataset.columns = cabeceras
    dataset.to_csv("FindMyCar.csv", index = False)    
    
from random import randint
from time import sleep

#obtenemos los resultados de las 5 primeras paginas 
listaCoches=[]
for i in range (1,5): 
    #dormimos un numero aleatorio de segundos entre 5 y 10 para prevenir que nos baneen    
    sleep(randint(5,10))
    pagina = getResultados(i, fromYear, toYear, fromPrice, toPrice)
    soup = BeautifulSoup(pagina.text,'html.parser')    
    for coches in soup.find_all('div', class_='aditem-detail'):        
            titulo = coches.find(class_="aditem-detail-title")
            #obtener el href del titulo
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
        
print ("Encontrados: "+str(len(listaCoches)))
#for i in range(len(listaCoches)):
#    print(listaCoches[i])
if len(listaCoches)> 0:
	guardar_resultados(listaCoches)

