import datos as dt
import xmltodict
import json
import re
import conexionddbb as ddbb
import os
import time
inicio = time.time()


# url = "http://ergast.com/api/f1/circuits/vegas"
# archivo_final="json/circuits/api_postman/circuits.json"
def xml_origen(url,archivo_final):
    response = dt.extraer_postmanFormula1(url)

    dictionary = xmltodict.parse(response.text)
    dictionary=quitar_arrobas(dictionary)
    json_object = json.dumps(dictionary)
    print(json_object)
    f=open(archivo_final,"w")
    f.write(json_object )
    f.close()

def quitar_arrobas(dictionary):
    x = dictionary.copy()
    arroba = "@"
    if type(dictionary) is dict:
        for key_dicc in dictionary:
            valor = dictionary[key_dicc]
            modificar=0
            if type(valor) is dict or type(valor) is list:
                valor=quitar_arrobas(valor)
                modificar=1
            if re.search(arroba,key_dicc):
                nueva_key=re.sub("@","",key_dicc)
                x[nueva_key]=valor
                del(x[key_dicc])
            else:
                if modificar == 1:
                    x[key_dicc]=valor
    if type(dictionary) is list:
        for valor_list in dictionary:
            indice=dictionary.index(valor_list)
            x[indice]=quitar_arrobas(valor_list)
    return(x)



# url ='http://ergast.com/api/f1/{{year}}/drivers?limit=&offset=20'
# url = "http://ergast.com/api/f1/"+str(year)+"/drivers.json"

# "json/circuits/api_postman/_"+str(year)+".json"
def bucle_origen():
    years=list(range(1950,2023))
    
    for year in years:#years:
        rounds=ddbb.select_total_rounds_season(year)
        for round in range(1,rounds+1):
            
            url = "http://ergast.com/api/f1/"+str(year)+"/"+str(round)+"/sprint.json"
            # querystring = {"season":str(year)}

            archivo_final="json/races/results/api_postman/_"+str(year)+"/_"+str(round)+".json"
            response = dt.extraer_postmanFormula1(url)
            # dictionary= xmltodict.parse(response.text)
            # dictionary=quitar_arrobas(dictionary)
            # json_object = json.dumps(dictionary)
            # print (json_object)
            # pattern=r'{"RaceTable": {"season": "[0-9]*", "round": "[0-9]*"}'
            # if '"Races":[]'in json_object or re.findall(pattern,json_object):
            #     print(json_object)

            try:
                os.mkdir('json/races/results/api_postman/_'+str(year))
            except:
                1==1
            f=open(archivo_final,"w")
            f.write(response.text)
            f.close()
            # response = dt.extraer_postmanFormula1(url)
            # xml_origen(url,archivo_final)
            # print(response.text)

            # f=open(archivo_final,"w")
            # f.write(response.text)
            # f.close()



bucle_origen()
fin = time.time()
print(fin-inicio)
# url="http://ergast.com/api/f1/seasons?limit=140&offset=20"
# archivo_final="json/season/season_total.json"#api_postman/constructores_total.json"
# # Pilotos:
# xml_origen(url,archivo_final)
