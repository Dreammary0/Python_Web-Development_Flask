from app import app
from flask import render_template, request

@app.route('/hello', methods=['GET'])
def hello():
    # для каждого передаваемого параметра формы нужно установить
    # значение по умолчание, на случай если пользователь ничего не введет
    name = ""

    # получаем параметр из формы
    name = request.values.get('username')
    html = render_template(
        'hello.html',
        name=name
    )
    return html
