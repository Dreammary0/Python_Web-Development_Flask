import constants
import numpy as np
from app import app
from flask import render_template, request


@app.route('/', methods=['GET'])
def index():
    # задаем реквесты
    name = request.values.get('username')
    gender = request.values.get('gender')
    program_id = request.values.get('program')
    subject_id = request.values.getlist('subject[]')
    olympiad_id = request.values.getlist('olympiad[]')

    # формируем список из выбранных пользователем дисциплин и олимпиад
    subjects_select = [constants.subjects[int(i)] for i in subject_id]
    olympiads_select = [constants.olympiads[int(i)] for i in olympiad_id]

    # Условия
    if not name:
        name = ''
    if program_id:
        program = constants.programs[int(program_id)]
    else:
        program = constants.programs[0]

    #Рендерим главную страницу
    html = render_template(
        'index.html',
        program_list=constants.programs,
        subject_list=constants.subjects,
        olympiad_list=constants.olympiads,
        len=len,
        name=name,
        gender=gender,
        program=program,
        subjects_select=subjects_select,
        olympiads_select=olympiads_select
    )

    #Добавляем вывод формы
    html += render_template(
        'hello.html',
        program_list=constants.programs,
        subject_list=constants.subjects,
        olympiad_list=constants.olympiads,
        len=len,
        name=name,
        gender=gender,
        program=program,
        subjects_select=subjects_select,
        olympiads_select=olympiads_select
    )
    return html