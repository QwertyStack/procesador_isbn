import csv
import requests
from os import listdir
import config
import json





def lectura_fichero():
    '''
    Procesamiento de cada uno de los ficheros *.txt que contienen los libros clasificados por categorías.
    '''
    Ficheros = listdir(config.RUTA_BASE+"datos/")
    for fichero in Ficheros:
        logging.debug("Lectura del fichero "+ fichero)
        EL_DICCIONARIO =  {}
        with open(config.RUTA_BASE+"datos/"+fichero, "r") as file:
            Lines = file.readlines()
            # Procesamiento de cada isbn
            for line in Lines:
                line = line.strip()
                to_dict(line, EL_DICCIONARIO, fichero)
        # Volcar los resultados por categoría en un fichero out/dict_<categoria>.json
        with open(config.RUTA_BASE+"out/dict_"+ fichero.split(".")[0]+".json", "w") as file:
            file.write(json.dumps(EL_DICCIONARIO, ensure_ascii=False))


def peticion(url, isbn):
    r = requests.get(url+isbn)
    return r.json()


def to_dict(isbn, EL_DICCIONARIO, fichero):
    '''
    Petición a la API de Google Books para obtener información sobre el ISBN.
    '''
    logging.info("Peticion a la API Google Books con el isbn " + isbn)
    r_json = peticion("https://www.googleapis.com/books/v1/volumes?q=isbn:", isbn)
    
    # Control si existe el ISBN en Google Books
    if r_json["totalItems"] > 0:
        # Procesamiento de los datos de Google Books
        for result in r_json["items"]:
            # Control de coincidencias en el isbn, se verifica el titulo del libro
            if isbn in EL_DICCIONARIO.keys() and "titulo" in EL_DICCIONARIO[isbn].keys() and result["volumeInfo"]["title"] == EL_DICCIONARIO[isbn]["titulo"]:
                EL_DICCIONARIO[isbn]["n_apariciones"]+=1
            # Añadir una nueva entrada
            elif isbn not in EL_DICCIONARIO.keys():
                EL_DICCIONARIO[isbn]={
					"ISBN": isbn,
                    "n_apariciones":1,
                    "titulo": result["volumeInfo"]["title"] if "title" in result["volumeInfo"].keys() else "",
                    "subtitulo": result["volumeInfo"]["subtitle"] if "subtitle" in result["volumeInfo"].keys() else "",
                    "fecha_publicacion": result["volumeInfo"]["publishedDate"] if "publishedDate" in result["volumeInfo"].keys() else "",
                    "autor/es": result["volumeInfo"]["authors"] if "authors" in result["volumeInfo"].keys() else "",
                    "idioma": result["volumeInfo"]["language"] if "language" in result["volumeInfo"].keys() else "",
                    "imagen": result["volumeInfo"]["imageLinks"]["thumbnail"] if "imageLinks" in result["volumeInfo"].keys() else "",
                    "descripcion": result["volumeInfo"]["description"] if "description" in result["volumeInfo"].keys() else ""
                }
            # Se ha encontrado un match con el isbn pero no coincide el título de la obra
            else:
                logging.info("Coincidencia con ISBN:"+ isbn)
    else:
        # No se han obtenido resultados
        logging.warning(f"No hay registros en Google Books para el ISBN: {isbn} del fichero {fichero}")
        r_json = peticion("https://api.itbook.store/1.0/books/", isbn)

        if r_json['error'] != '[books] Not found':
            logging.info(f"Hay registros en IT Bookstore API para el ISBN {isbn}")
            EL_DICCIONARIO[isbn]={
					"ISBN": isbn,
                    "n_apariciones":1,
                    "titulo": r_json["title"] if "title" in r_json.keys() else "",
                    "subtitulo": r_json["subtitle"] if "subtitle" in r_json.keys() else "",
                    "fecha_publicacion": r_json["year"] if "year" in r_json.keys() else "",
                    "autor/es":  r_json["authors"] if "authors" in  r_json.keys() else "",
                    "idioma": "",
                    "imagen": r_json["image"] if "image" in r_json.keys() else "",
                    "descripcion": r_json["desc"] if "desc" in r_json.keys() else ""
                }
        elif isbn in EL_DICCIONARIO.keys():
            EL_DICCIONARIO[isbn]["n_apariciones"]+=1
            logging.warning(f"No hay registros en IT Bookstore API para el ISBN: {isbn} del fichero {fichero}")
        else:
            EL_DICCIONARIO[isbn]={
                "ISBN": isbn, 
                "n_apariciones": 1,
                "titulo": "",
                "subtitulo": "",
                "fecha_publicacion": "",
                "autor/es": "",
                "idioma": "",
                "imagen": "",
                "descripcion": ""
            }
            logging.warning(f"No hay registros en IT Bookstore API para el ISBN: {isbn} del fichero {fichero}")
        



def to_csv():
    '''
    Conversión de los datos del diccionario al CSV.
    '''
    Diccionarios = listdir(config.RUTA_BASE+"out/")
    for dicc in Diccionarios:
        logging.info("Procesando datos del diccionario: "+ dicc)
        datos = json.load(open(config.RUTA_BASE+"out/"+dicc))
        with open(config.RUTA_BASE+"csv/"+dicc.split(".")[0]+".csv", 'w') as outfile:
            listWriter = csv.DictWriter(
            		outfile,
            		fieldnames=datos[list(datos.keys())[0]].keys(),
            		delimiter=';',
            		quotechar='|',
            		quoting=csv.QUOTE_MINIMAL
            )
            listWriter.writeheader()
            for libro in datos:
            	listWriter.writerows([datos[libro]])





if __name__== "__main__":
    logging = config.get_logging(fichero=config.RUTA_BASE+"log/main.log")
    # Procesar los datos
    logging.info("\n\n*********************************\nInicio procesamiento del fichero\n*********************************")
    lectura_fichero()

    # Pasar a csv y poder importarlo en Excel o Google Sheets
    logging.info("\n\n*********************************\nInicio de paso a CSV\n*********************************")
    to_csv()
