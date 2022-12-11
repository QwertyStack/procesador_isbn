# Procesador ISBN
_Procesador y clasificador de ISBNs de libros para el fácil manejo de la información en fichero CSV._

![](https://img.shields.io/github/license/QwertyStack/procesador_isbn)
![](https://img.shields.io/github/issues/QwertyStack/procesador_isbn)
![](https://img.shields.io/github/issues-pr/QwertyStack/procesador_isbn)
![](https://img.shields.io/github/stars/QwertyStack/procesador_isbn)

## Comenzando 🚀
Herramienta funcional que permite la obtención de información asociada a los ISBNs de los libros de forma que, dada una lista ya clasificada por categorías, se obtiene un fichero CSV donde se puede obtener información sobre:
- ISBN
- Nº de apariciones en la lista
- Título
- Subtítulo
- Fecha de publicación
- Autor/es
- Idioma
- URL con la imagen de la portada
- Descripción

## Pre-requisitos 📋
- Contar con una lista en formato ".txt" ya clasificada por categorías con los ISBNs de los libros separados por saltos de línea tal y como aparecen en la carpeta de [datos](https://github.com/QwertyStack/procesador_isbn/tree/main/datos).
  
- Tener Python instalado, esto fue desarrollado bajo la [versión 3.10.6](https://www.python.org/downloads/release/python-3106/).


## Funcionamiento ⚙️
En primer lugar se realiza la lectura de cada uno de los ficheros con los ISBNs bajo el método [`lectura_fichero()`](https://github.com/QwertyStack/procesador_isbn/blob/main/main.py#L11), por cada línea de lectura se realiza la petición a la API de Google Books y  IT Bookstore API a través del método [`peticion()`](https://github.com/QwertyStack/procesador_isbn/blob/main/main.py#L30) y se crea un diccionario en el método [`to_dict()`](https://github.com/QwertyStack/procesador_isbn/blob/main/main.py#L35) con cada uno de los campos especificados anteriormente.

Una vez ya se han procesado todos los ISBNs y se obtienen todos los datos necesarios, se vuelcan en un fichero CSV según el método [`to_csv()`](https://github.com/QwertyStack/procesador_isbn/blob/main/main.py#L103) para facilitar su tratamiento en herramientas como Excel o Google Sheets.

****
## Licencia 📄

Este proyecto está bajo la Licencia GNU General Public License v3.0 - mira el archivo [LICENSE.md](https://github.com/QwertyStack/MiniShell/blob/main/LICENSE) para detalles.
