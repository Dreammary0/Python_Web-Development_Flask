import pandas as pd
from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import Service, Record
@app.route('/masters', methods=['get'])
def masters():
     conn = get_db_connection()
     df_Service = Service(conn)
     add_procedure_list = []
     if request.values.get('barber'):
          barber_list = request.values.getlist('barber')
          add_procedure_list.append('Парикмахер')
          for elem in barber_list:
               if elem not in list(session['service']):
                    session['service'].append(elem)


     else:
          barber_list = []

     if request.values.get('nail'):
          nail_list = request.values.getlist('nail')
          add_procedure_list.append('Маникюр')
          for elem in nail_list:
               if elem not in list(session['service']):
                    session['service'].append(elem)


     else:
          nail_list = []

     if request.values.get('makeup'):
          makeup_list = request.values.getlist('makeup')
          add_procedure_list.append('Визажист')
          for elem in makeup_list:
               if elem not in list(session['service']):
                    session['service'].append(elem)


     else:
          makeup_list = []

     if request.values.get('shugaring'):
          shugaring_list = request.values.getlist('shugaring')
          add_procedure_list.append('Шугаринг')
          for elem in shugaring_list:
               if elem not in list(session['service']):
                    session['service'].append(elem)

     else:
          shugaring_list = []

     if request.values.get('cosmetolog'):
          cosmetolog_list = request.values.getlist('cosmetolog')
          add_procedure_list.append('Косметолог')
          for elem in cosmetolog_list:
               if elem not in list(session['service']):
                    session['service'].append(elem)

     else:
          cosmetolog_list = []

     if add_procedure_list:
          df_Record = Record(conn, add_procedure_list)
          session['procedures'] = add_procedure_list
     else:
          df_Record = pd.DataFrame

     if request.values.get('masters'):
          masters_list = request.values.getlist('masters')
     else:
          masters_list = []
     print(session['procedures'])
     print(makeup_list,nail_list)
     html = render_template(
          'index_3.html',
          len=len,
          masters=df_Record,
          masters_list=masters_list,
          add_procedure_list=list(session['procedures'])
     )

     # if masters_list:
     #      print(len(list(session['service'])))
     #      html = render_template(
     #           'index_3.html'
     #           # len=len,
     #           # masters=df_Record,
     #           # masters_list=masters_list,
     #           # add_procedure_list=list(session['procedures'])
     #      )
     return html
