from jinja2 import Template, Environment, FileSystemLoader
import sqlite3
from poisk_book_model import *

#типо пользователь натыкал
genre_list=("Детектив", "Роман","Приключения")
author_list=("Агата Кристи", "Жюль Верн", "Ильф И.А.,Петров Е.П.")
publisher_list=()



conn = sqlite3.connect("library.sqlite")
df_book_info = get_book_info(conn, genre_list,author_list,publisher_list)
df_author = get_author(conn)
df_publisher = get_publisher(conn)
df_genre = get_genre(conn)
conn.close()



f_template = open('poisk_book_templ.html','r', encoding ='utf-8-sig')
html = f_template.read()
f_template.close()

# создаем объект-шаблон
template = Template(html)
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('poisk_book_templ.html')
template.globals['len'] = len
template.globals['print'] = print




# генерируем результат на основе шаблона
result_html = template.render(
    genre=df_genre,
    author= df_author,
    publisher = df_publisher,
    book_info=df_book_info,
    len=len,
    print=print,

    genre_list=genre_list,
    author_list=author_list,
    publisher_list=publisher_list
)



# создаем файл для HTML-страницы
f = open('poisk_book.html', 'w', encoding='utf-8-sig')
# выводим сгенерированную страницу в файл
f.write(result_html)
f.close()
