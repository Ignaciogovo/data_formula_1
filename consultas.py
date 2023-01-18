import json
import re
import conexionddbb as ddbb

def get_key(val,dicc):
    for key, value in dicc.items():
         if val == value:
             return key


def consultar_circuitos():
    f= open("json/circuits/api_postman/circuits.json","r")
    d_12 = json.load(f)
    circuitos=d_12["MRData"]["CircuitTable"]["Circuit"]
    f= open("json/circuits/rapidapi_formula_1/circuits.json","r")
    d_12 = json.load(f)
    circuitos2=d_12["response"]
    lista=[]
    for circuito2 in circuitos2:

        id_circuit=circuito2["name"]
        for circuito in circuitos:
            if re.search(circuito["CircuitName"],id_circuit):
                dictionary={
                    "name":circuito2["name"],
                    "country":circuito2["competition"]["location"]["country"],
                    "city": circuito2["competition"]["location"]["city"],
                    "lat": circuito["Location"]["lat"],
                    "long": circuito["Location"]["long"],
                    "laps": circuito2["laps"],
                    "legth": circuito2["length"],
                    "race_distance": circuito2["race_distance"],
                    "capacity": circuito2["capacity"],
                    "opened": circuito2["opened"],
                    "first_grand_prix": circuito2["first_grand_prix"],
                    "id_api_postman": circuito["circuitId"],
                    "id_api_formula_1": circuito2["id"],
                    "url": circuito["url"]
                     }
                lista.append(dictionary)

    for circuito in circuitos:
        dictionary={
        "name":circuito["CircuitName"],
        "country":circuito["Location"]["Country"],
        "city": circuito["Location"]["Locality"],
        "lat": circuito["Location"]["lat"],
        "long": circuito["Location"]["long"],
        "laps": None,
        "legth": None,
        "race_distance": None,
        "capacity": None,
        "opened": None,
        "first_grand_prix":None,
        "id_api_postman": circuito["circuitId"],
        "id_api_formula_1": None,
        "url": circuito["url"]
            }
        nombres=[]
        for l in lista:
            nombres.append(l["name"])
        if dictionary["name"] not in nombres:
            lista.append(dictionary)
    # exceptiones:
    # insert vietnam: ( ha estado pospuesto)
    dictioanry={"name":'Hanoi Street Circuit',"country":'Vietnam',"city": 'Hanoï',"lat": None,"long": None,"laps": None,"legth": None,"race_distance": None,"capacity": None,"opened": None,"first_grand_prix":2020,"id_api_postman": None,"id_api_formula_1": 3,"url": 'https://en.wikipedia.org/wiki/Hanoi_Circuit'}
    lista.append(dictioanry)
    print(len(lista))
    for dictionary in lista:
        print(dictionary)
        # lis.append(dictionary["name"]+dictionary["city"]+dictionary["country"])
        # ddbb.insert_circuit(dictionary["name"],dictionary["country"],dictionary["city"],dictionary["lat"],dictionary["long"],dictionary["laps"],dictionary["legth"],dictionary["race_distance"],dictionary["capacity"],dictionary["opened"],dictionary["first_grand_prix"],dictionary["id_api_postman"],dictionary["id_api_formula_1"],dictionary["url"])
    # lis.sort()
    # for l in lis:
    #     print(l)
            # elif city1==city2:
            #     cuenta=cuenta+1
            #     lista=[str(cuenta),circuito2["name"], circuito["CircuitName"]]
            #     estan.append(circuito2["name"])





def consultar_races():
    datos_postman=[]
    datos=[]
    datos_formula=[]
    gps={}
    datosgp={}
    excepciones_paises={"USA":"United States"}
    # Cogemos datos de api_postman
    for year in range(1950,2024):
        f= open("json/races/api_postman/_"+str(year)+".json","r")
        data = json.load(f)
        datos_postman=datos_postman+data["MRData"]["RaceTable"]["Races"]
    # Cogemos datos de api_formula
    f= open("json/varios/competitions.json","r")
    data = json.load(f)
    datos=data["response"]
    for dato in datos:
        dictioanry={"id": dato["id"],"name": (re.sub("Grand Prix|Formula 1","",dato["name"])).strip()}
        diff={"Tuscan":"Toscana","British":"Great Britain", 'Chinese':'China', 'Dutch':'Netherlands', 'Spanish':'Spain', 'Canadian':'Canada', 'French':'France', 'German':'Germany', 'Hungarian':'Hungary','Belgian': 'Belgium','Italian': 'Italy','United States': 'USA','Portuguese': 'Portugal', 'Styrian':'Steiermark', 'Turkish':'Turkey'}
        if dictioanry["name"] in diff.values():
            dictioanry["name"]=get_key(dictioanry["name"],diff)
        datos_formula.append(dictioanry)
    for dato in datos_postman:
        gp_data=[]
        # gp_data=["circuitId"]
        # gp_data["circuitName"]=dato["Circuit"]["circuitName"]
        gp_data.append(dato["Circuit"])

        if dato["raceName"] not in gps:
            # Incluimos el id de la otra api para tenerlo más que sirva de ayuda
            for nombre_gp in datos_formula:
                name=nombre_gp["name"]
                country=dato["Circuit"]["Location"]["country"]
                if country in excepciones_paises.values():
                    country=get_key(country,excepciones_paises)
                if re.search(name,dato["raceName"]):
                    id=nombre_gp["id"]
                    break
                else:
                    id= None
            pattern=r'[0-9][0-9][0-9][0-9]_'
            url=re.sub(pattern,"",dato["url"])
            lista={"url":url,"date":dato["date"],"country":country,"id":id}
            gps[dato["raceName"]]= gp_data
            datosgp[dato["raceName"]]=lista

        else:
            previo_data=gps[dato["raceName"]]
            comprobacion=[]
            for t in  previo_data:
                comprobacion.append(t["circuitId"])
            if gp_data[0]["circuitId"] not in comprobacion:
                gps[dato["raceName"]]=previo_data+gp_data
    # Los premios que son cancelados no estan incluidos en la api_postman por tanto lo añadimos a continuación:
    datosgp["Vietnam Grand Prix"]={"url":"https://es.wikipedia.org/wiki/Gran_Premio_de_Vietnam","country":"Vietnam","date":None,"id":3}
    # print(gps)
    # print(datosgp)
    for dato in datosgp:
        url = datosgp[dato]["url"]
        primer_gp = datosgp[dato]["date"]
        id = datosgp[dato]["id"]
        country=datosgp[dato]["country"]
        # ddbb.insert_gp(dato,country,url,primer_gp,id)





# ronda, id_gp,id_circuito, año, url,fecha hora

def consultas_races_temporada():
    # Nombramos las listas y diccionarios que vamos a necesitar posteriormente
    datos_formula=[]
    datos_postman=[]
    arreglos_formula={}
    no_completed_formula={}
    arreglos_postman={}

    # sacamos los datos de los json
    for year in range(2012,2023):
        f= open("json/races/rapidapi_formula_1/_"+str(year)+".json","r")
        data = json.load(f)
        datos_formula=datos_formula+data["response"]
    for year in range(1950,2023):
        f= open("json/races/api_postman/_"+str(year)+".json","r")
        data = json.load(f)
        datos_postman=datos_postman+data["MRData"]["RaceTable"]["Races"]

    #Filtramos los datos de la api de postman
    for dato in datos_postman:
        id_circuit=ddbb.select_id_circuit(dato["Circuit"]["circuitId"],1)
        id_gp=ddbb.select_id_grand_prix_nombre(dato["raceName"])
        season_postman= dato["season"]
        round_postman= dato["round"]
        url=dato["url"]
        if "time" in dato.keys():
            time=dato["time"]
            date=dato["date"]
            fecha=(date+" "+time.strip("Z"))
        else:
            fecha=dato["date"]
        if "Qualifying" in dato.keys():
            if "time" in dato["Qualifying"].keys():
                time=dato["Qualifying"]["time"]
                date=dato["Qualifying"]["date"]
                Qualifying=(date+" "+time.strip("Z"))
            else:
                Qualifying=dato["Qualifying"]["date"]

        else:
            Qualifying=None
        if "FirstPractice" in dato.keys():
            if "time" in dato["FirstPractice"].keys():
                time=dato["FirstPractice"]["time"]
                date=dato["FirstPractice"]["date"]
                FirstPractice=(date+" "+time.strip("Z"))
            else:
                FirstPractice=dato["FirstPractice"]["date"]
        else:
            FirstPractice=None
        if "SecondPractice" in dato.keys():
            if "time" in dato["SecondPractice"].keys():
                time=dato["SecondPractice"]["time"]
                date=dato["SecondPractice"]["date"]
                SecondPractice=(date+" "+time.strip("Z"))
            else:
                SecondPractice=dato["SecondPractice"]["date"]
        else:
            SecondPractice=None
        if "ThirdPractice" in dato.keys():
            if "time" in dato["ThirdPractice"].keys():
                time=dato["ThirdPractice"]["time"]
                date=dato["ThirdPractice"]["date"]
                ThirdPractice=(date+" "+time.strip("Z"))
            else:
                ThirdPractice=dato["ThirdPractice"]["date"]
        else:
            ThirdPractice=None
        if "Sprint" in dato.keys():
            if "time" in dato["Sprint"].keys():
                time=dato["Sprint"]["time"]
                date=dato["Sprint"]["date"]
                Sprint=(date+" "+time.strip("Z"))
            else:
                Sprint=dato["Sprint"]["date"]
        else:
            Sprint=None
        arreglos_postman[str(season_postman)+"_"+str(id_gp)]={'id_circuit': id_circuit, 'id_gp': id_gp, 'season': season_postman,'round': round_postman,'laps': None,'fecha': fecha, 'status': None, 'weather': None,'url':url, 'id_api_formula': None, 'fecha_3rdQualifying': None, 'weather_3rdQualifying': None, 'id_api_formula_3rdQualifying': None, 'fecha_2ndQualifying': None, 'weather_2ndQualifying': None, 'id_api_formula_2ndQualifying': None, 'fecha_1stQualifying': Qualifying, 'weather_1stQualifying': None, 'id_api_formula_1stQualifying': None, 'fecha_3rdPractice': ThirdPractice, 'weather_3rdPractice': None, 'id_api_formula_3rdPractice': None, 'fecha_2ndPractice': SecondPractice, 'weather_2ndPractice': None, 'id_api_formula_2ndPractice': None, 'fecha_1stPractice': FirstPractice, 'weather_1stPractice': None, 'id_api_formula_1stPractice': None,'fecha_Sprint': Sprint, 'weather_Sprint': None, 'id_api_formula_Sprint': None}
        print(str(season_postman)+"_"+str(id_gp))
    # for dato in datos_postman:
    #     print(dato)
    #     break
    # for dato in datos_formula:
    #     print(dato)
    #     break

    # ordenamos los datos de api_formula para evitar posibles errores a la hora de actualizar las listas
    datos_formula2=datos_formula.copy()
    no_races=[]
    for i in range(0,len(datos_formula)):
        tipo = datos_formula[i]["type"]
        if tipo != 'Race':
            intermedio=datos_formula[i]
            datos_formula2.remove(intermedio)
            no_races.append(intermedio)
    datos_formula.clear()
    datos_formula=datos_formula2+no_races

    # Filtramos los datos de api_formula
    for dato in datos_formula:
        id_circuit=ddbb.select_id_circuit(dato["circuit"]["id"],2)
        id_gp=ddbb.select_id_grand_prix(dato["competition"]["id"])
        tiempo=dato["weather"]
        estado=dato["status"]
        season=dato["season"]
        fecha=(dato["date"][:-6]).replace("T"," ")
        tipo=str(dato["type"].replace(" ", ""))
        clave=str(season)+"_"+str(id_gp)
        laps=dato["laps"]["total"]
        # Separamos las carreras no completadas
        if dato["status"] =="Completed":
            if dato["type"]== 'Race':
                arreglos_formula[clave]={"id_circuit": id_circuit, "id_gp": id_gp,"laps":laps,"season": season, "fecha": fecha, "status": estado, "weather": tiempo,"id_api_formula": dato["id"]}
            else:
                arreglos_formula[clave].update({"fecha_"+tipo: fecha, "weather_"+tipo:tiempo,"id_api_formula_"+tipo:dato["id"]})
        else:
            if dato["type"]== 'Race':
                no_completed_formula[clave]={"id_circuit": id_circuit, "id_gp": id_gp,"laps":laps,"season": season, "fecha": fecha, "status": estado, "weather": tiempo,"id_api_formula": dato["id"]}
            else:
                try:
                    no_completed_formula[clave].update({"fecha_"+tipo: fecha, "weather_"+tipo:tiempo,"id_api_formula_"+tipo:dato["id"]})
                except:
                    None
    # for i in no_completed_formula:
    #     if no_completed_formula[i]["id_gp"]
    # print(arreglos_formula["2022_19"])
# {'id_circuit': 22, 'id_gp': 38, 'laps': 55, 'season': 2022, 'fecha': '2022-11-20 13:00:00', 'status': 'Completed', 'weather': None, 'id_api_formula': 1598, 'fecha_1stQualifying': '2022-11-19 14:00:00', 'weather_1stQualifying': None, 'id_api_formula_1stQualifying': 1599, 'fecha_3rdPractice': '2022-11-19 10:30:00', 'weather_3rdPractice': None, 'id_api_formula_3rdPractice': 1600, 'fecha_2ndPractice': '2022-11-18 13:00:00', 'weather_2ndPractice': None, 'id_api_formula_2ndPractice': 1601, 'fecha_1stPractice': '2022-11-18 10:00:00', 'weather_1stPractice': None, 'id_api_formula_1stPractice': 1602, 'fecha_3rdQualifying': '2022-11-19 14:42:00', 'weather_3rdQualifying': None, 'id_api_formula_3rdQualifying': 1669, 'fecha_2ndQualifying': '2022-11-19 14:21:00', 'weather_2ndQualifying': None, 'id_api_formula_2ndQualifying': 1670}
    for arreglo in arreglos_formula:
        datos=arreglos_formula[arreglo]
        if arreglo in arreglos_postman.keys():
            tupla=tuple(arreglos_postman[arreglo].keys())
            for i in tupla:
                if i in datos.keys():
                    if datos[i] != None:
                        arreglos_postman[arreglo][i]=datos[i]
    for arreglo in arreglos_postman:
        # if arreglos_postman[arreglo]["id_api_formula_Sprint"]!= None:
            ddbb.insert_calendario(list(arreglos_postman[arreglo].values()))
    # print(arreglos_postman)
consultas_races_temporada()

def consultas_seasons():
        datos=[]
        f= open("json/season/season_total.json","r")
        data = json.load(f)
        datos=datos+data["MRData"]["SeasonTable"]["Season"]
        for dato in datos:
            print(dato["#text"],dato["url"])

#select_api_circuit("fuji")


# datos= {}
# id=2012
# f= open("json/constructores/api_postman/_"+str(id)+".json","r")
# d_12 = json.load(f)
# equipos=d_12["MRData"]["ConstructorTable"]["Constructors"]



# = d_12["response"]+d_13["response"]+d_14["response"]+d_15["response"]+d_16["response"]+d_17["response"]+d_18["response"]+d_19["response"]+d_20["response"]+d_21["response"]+d_22["response"]
# # print("2012: "+str(len(d_12["response"])))
# # print("2013: "+str(len(d_13["response"])))
# # print("2014: "+str(len(d_14["response"])))
# dic={
#     "2012":0,
#     "2013":0,
#     "2014":0,
#     "2015":0,
#     "2016":0,
#     "2017":0,
#     "2018":0,
#     "2019":0,
#     "2020":0,
#     "2021":0,
#     "2022":0

# }
# # Buscar carreras en paises
# for value in datos:
#     competition=value["competition"]
#     location=competition["location"]

#     if location["city"]!="Valencia":
#         circuit=value["circuit"]
#         season = value["season"]
#         status = value["status"]
#         tipo=value["type"]
#         if tipo=="Race" and status =="Completed":
#             if season == 2012:
#                 dic["2012"]=dic["2012"]+1
#             if season == 2013:
#                 dic["2013"]=dic["2013"]+1
#             if season == 2014:
#                 dic["2014"]=dic["2014"]+1
#             if season == 2015:
#                 dic["2015"]=dic["2015"]+1
#             if season == 2016:
#                 dic["2016"]=dic["2016"]+1
#             if season == 2017:
#                 dic["2017"]=dic["2017"]+1
#                 print(str(location["city"])+" en el circuito: "+str(circuit["name"])+"  tipo "+tipo+ " season: "+str(season)+" estado:"+status)
#             if season == 2018:
#                 dic["2018"]=dic["2018"]+1
#             if season == 2019:
#                 dic["2019"]=dic["2019"]+1
#             if season == 2020:
#                 dic["2020"]=dic["2020"]+1
#             if season == 2021:
#                 dic["2021"]=dic["2021"]+1
#             if season == 2022:
#                 dic["2022"]=dic["2022"]+1
#         #print(location["city"]+" en el circuito: "+circuit["name"]+"  tipo "+tipo+ " season: "+str(season))
# for key in dic:
#     print("Año: "+key+" total: "+str(dic[key]))

# # # print(datos["response"][1])