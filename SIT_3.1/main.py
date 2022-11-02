from jinja2 import Template, Environment, FileSystemLoader


def add_spaces(text):
 return " ".join(text)

def sclonenie(n):
  match n:
   case 1:
    return "дисциплина:"
   case 2|3|4:
    return "дисциплины:"
   case 0|5|6|7|8|9|10:
    return "дисциплин:"







f_template = open('templates/ind_test_template.html','r', encoding ='utf-8-sig')
html = f_template.read()
f_template.close()

student =[
 ["Алина", "0.0.0. Бизнес-информатика", ["Базы данных",
 "Программирование", "Эконометрика", "Статистика"], "ж"],
 ["Вадим", "1.1.1. Экономика", ["Информатика", "Теория игр",
 "Экономика", "Эконометрика", "Статистика"], "м"],
 ["Ксения", "1.1.1. Экономика", ["Информатика", "Теория игр",
 "Статистика"], "ж"]
 ]



template = Template(html)
result_html = template.render(user = student[1], add_spaces = add_spaces, len= len, sclonenie = sclonenie)



#создадим файл для HTML-страницы
f = open('templates/test2.html', 'w', encoding ='utf-8-sig')
# выводим сгенерированную страницу в файл
f.write(result_html)
f.close()
