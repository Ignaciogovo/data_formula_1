from bs4 import BeautifulSoup
import requests
import re
# Metodo para recoger todas las páginas de las carreras de cada año para extraer posteriormente sus estadisticas
# Listamos los años que queremos obtener

def obtener_tabla(response): 
    soup=BeautifulSoup(response.content,'lxml')
    table=soup.find('table',class_="infobox")
    table=table.find_all('tr')
    for filas in table:
        fila = filas.find('th')
        pattern=r"Carreras|Partidos"
        if re.search(pattern,str(fila)):
            carreras=(filas.find('td')).contents[0]
            try:
                carreras=int(carreras)
            except:
                lista=re.split("y", carreras)
                carreras=lista.pop()
            print(carreras)
            return(carreras)
        
        


correlacion = {}
years=list(range(2010,2023))
for year in years:
    print("")
    print("Año: "+str(year))
    print("")
    web="https://es.wikipedia.org/wiki/Temporada_"+str(year)+"_de_F%C3%B3rmula_1"

    response = requests.get(web)
    carreras=obtener_tabla(response)
    soup=str(BeautifulSoup(response.content,'lxml'))
    # Filtramos a partir de un inicio y final para acotar mejor
    inicio=soup.find('id="Campeonato_de_Pilotos"')
    if inicio==-1:
        inicio=soup.find('Campeonato de Pilotos')
    final=soup.rfind('id="Estadísticas_del_Campeonato_de_Pilotos"')
    if final == -1:
        final=soup.rfind('id="Campeonato_de_Constructores"')
    # El html reducido lo pasamos a la variable table
    table=soup[inicio:final]
    # Volvemos acotar para recoger la tabla donde se encuentrán los enlaces de las carreras
    inicio=table.find('valign="middle">Piloto')
    if inicio == -1:
        inicio=table.find('<th>Piloto\n</th>')
    final= table.rfind('<th valign="middle">Puntos')
    if final ==-1:
        final= table.rfind('<th>Puntos\n</th>')
    table=table[inicio:final]
    soup=(BeautifulSoup(table,'lxml'))
    # Escogemos todos los enlaces de la tabla
    enlaces=soup.find_all('a')
    grandes_premios=[]
    # Filtramos por los enlaces que contienen la palabra gran premio
    for enlace in enlaces:
        pattern = 'Gran_Premio'
        if re.search(pattern,str(enlace)):
            gran_premio="https://es.wikipedia.org"+enlace.get('href')
            if gran_premio not in grandes_premios:
                grandes_premios.append(gran_premio)

    if carreras == len(grandes_premios):
        correlacion[year] = "YES"#, carreras:"+str(carreras)+" grandes premios: "+str(len(grandes_premios))
    else:
        correlacion[year] = "NO, carreras: "+str(carreras)+" grandes premios: "+str(len(grandes_premios))
for x in correlacion:
    valor = correlacion.get(x)
    print(x," --> ",valor)


print("")
print(len(correlacion))
print("")
print(list(correlacion.values()).count("YES"))







