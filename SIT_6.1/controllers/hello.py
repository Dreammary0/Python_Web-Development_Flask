import constants
from app import app
from flask import render_template, request


@app.route('/hello', methods=['GET'])
def hello():
    # для каждого передаваемого параметра формы нужно задать
    # значение по умолчание, на случай если пользователь ничего не введет
    name = ""
    gender = ""
    program_id = 0
    # список из номеров выбранных пользователем дисциплин
    subject_id = []
    # список из выбранных пользователем дисциплин
    subjects_select = []
    name = request.values.get('username')
    gender = request.values.get('gender')
    program_id = request.values.get('program')
    subject_id = request.values.getlist('subject[]')
    # формируем список из выбранных пользователем дисциплин
    subjects_select = [constants.subjects[int(i)] for i in subject_id]
    html = render_template(
        'hello.html',
        name=name,
        gender=gender,
        program=constants.programs[int(program_id)],
        program_list=constants.programs,
        len=len,
        subjects_select=subjects_select,
        subject_list=constants.subjects
    )
    return html
