from jinja2 import Template, Environment, FileSystemLoader
import sqlite3
from library_model import *

conn = sqlite3.connect("library.sqlite")
# выбираем записи из таблицы publisher
df_author = get_author(conn)
df_book = get_book(conn)
df_book_author = get_book_author(conn)
df_book_reader = get_book_reader(conn)
df_publisher = get_publisher(conn)
df_genre = get_genre(conn)
df_reader = get_reader(conn)

conn.close()
# открываем шаблон из файла library_templ.html и читаем информацию
f_template = open('library_templ.html','r', encoding ='utf-8-sig')
html = f_template.read()
f_template.close()
# создаем объект-шаблон
template = Template(html)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('library_templ.html')
template.globals['len'] = len
# генерируем результат на основе шаблона
result_html = template.render(
    table_1="author",
    relation_1=df_author,
    len=len,

    table_2="book",
    relation_2=df_book,

    table_3="book_author",
    relation_3=df_book_author,

    table_4="book_reader",
    relation_4=df_book_reader,

    table_5="genre",
    relation_5=df_genre,

    table_6="publisher",
    relation_6=df_publisher,

    table_7="reader",
    relation_7=df_reader,

)
# создаем файл для HTML-страницы
f = open('library.html', 'w', encoding='utf-8-sig')
# выводим сгенерированную страницу в файл
f.write(result_html)
f.close()
