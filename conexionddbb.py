from datos import conexionddbb
def insert_gp(nombre,country,url,primer_gp,id_api):	
	db = conexionddbb()
	cursor = db.cursor()

		# Prepare SQL query to INSERT a record into the database.
	sql = "INSERT INTO grand_prix(name,country, url, primer_gp, id_api_formula_1) VALUES (%s,%s,%s,%s,%s)"
	valores = (nombre,country,url,primer_gp,id_api)
	# try:
	# Execute the SQL command
	cursor.execute(sql,valores)
	# Commit your changes in the database
	db.commit()
	# except:
	# 	# Rollback in case there is any error
	# 	db.rollback()
	# 	print("No se ha podido realizar el insert")


def insert_season(season,url):	
	db = conexionddbb()
	cursor = db.cursor()

		# Prepare SQL query to INSERT a record into the database.
	sql = "INSERT INTO seasons(season, url) VALUES (%s,%s)"
	valores = (season,url)
	# try:
	# Execute the SQL command
	cursor.execute(sql,valores)
	# Commit your changes in the database
	db.commit()
	# except:
	# 	# Rollback in case there is any error
	# 	db.rollback()
	# 	print("No se ha podido realizar el insert")


def insert_circuit(name,country,city,lat,long,laps,legth,race_distance,capacity,opened,first_grand_prix,id_api_postman,id_api_formula_1,url):	
	db = conexionddbb()
	cursor = db.cursor()

		# Prepare SQL query to INSERT a record into the database.
	sql = "INSERT INTO circuits(name,country,city,`lat`,`long`,laps,`legth`,`race_distance`,capacity,opened,first_grand_prix,id_api_postman,id_api_formula_1,url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	valores = (name,country,city,lat,long,laps,legth,race_distance,capacity,opened,first_grand_prix,id_api_postman,id_api_formula_1,url)
	#try:
	# Execute the SQL command
	cursor.execute(sql,valores)
	# Commit your changes in the database
	db.commit()
	# except:
	# 	# Rollback in case there is any error
	# 	db.rollback()
	# 	print("No se ha podido realizar el insert")


def insert_calendario(datos):
	db = conexionddbb()
	cursor = db.cursor()
		# Prepare SQL query to INSERT a record into the database.
	sql = "INSERT INTO calendario(id_circuit, id_gp, season, `round`, laps, fecha, status, weather, url, id_api_formula_1, fecha_3rdQualifying, weather_3rdQualifying, id_api_formula_3rdQualifying, fecha_2ndQualifying, weather_2ndQualifying, id_api_formula_2ndQualifying, fecha_1stQualifying, weather_1stQualifying, id_api_formula_1stQualifying, fecha_3rdPractice, weather_3rdPractice, id_api_formula_3rdPractice, fecha_2ndPractice, weather_2ndPractice, id_api_formula_2ndPractice, fecha_1stPractice, weather_1stPractice, id_api_formula_1stPractice, fecha_Sprint, weather_Sprint, id_api_formula_Sprint) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	valores = (datos)
	#try:
	# Execute the SQL command
	cursor.execute(sql,valores)
	# Commit your changes in the database
	db.commit()
def select_id_circuit(id_api,api):
	db = conexionddbb()
	cursor = db.cursor()
	if api ==1:
		sql=("SELECT id from circuits where id_api_postman = %s")
	elif api==2:
		sql=("SELECT id from circuits where id_api_formula_1 = %s")
	cursor.execute(sql,id_api)
	
	resultados = cursor.fetchone()
	
	db.close()
	return(resultados[0])


def select_id_grand_prix_nombre(nombre):
	db = conexionddbb()
	cursor = db.cursor()
	sql=("SELECT id from grand_prix where name= %s")
	cursor.execute(sql,nombre)
	
	resultados = cursor.fetchone()
	
	db.close()
	return(resultados[0])

def select_id_grand_prix(id_api):
	db = conexionddbb()
	cursor = db.cursor()
	sql=("SELECT id from grand_prix where id_api_formula_1 = %s")
	cursor.execute(sql,id_api)
	
	resultados = cursor.fetchone()
	
	db.close()
	return(resultados[0])
# insert_circuit("Las Vegas Strip Street Circuit","USA","Las Vegas", "36.1147", "-115.173",None,None,None,None,None,None,"vegas",None,"https://en.wikipedia.org/wiki/Las_Vegas_Grand_Prix#Circuit")

def select_total_rounds_season(season):
	db = conexionddbb()
	cursor = db.cursor()
	sql=("SELECT count(*) FROM FORMULA_1.calendario where season= %s")
	cursor.execute(sql,season)
	
	resultados = cursor.fetchone()
	
	db.close()
	return(resultados[0])