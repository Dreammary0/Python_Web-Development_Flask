import pandas as pd
from app import app
from flask import render_template, request, session,Flask, redirect, url_for, flash, make_response

from utils import get_db_connection
from models.index_model import Service, Record,Master_records
@app.route('/', methods=['get'])
def index():

     conn = get_db_connection()
     # session['service']=[]
     df_Service=Service(conn)
     add_procedure_list=[]
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
        df_Record = Record(conn,add_procedure_list)
        session['procedures']=add_procedure_list
     else:
          df_Record = pd.DataFrame

     if request.values.get('masters'):
          masters_list_list=[]
          masters_list = request.values.getlist('masters')
          for elem in masters_list:
               df_Master_record=Master_records(conn, elem)
               masters_list_list.append(df_Master_record)
     else:
          masters_list=[]
          masters_list_list=[]
          df_Master_record=pd.DataFrame

     if request.values.get('record_button'):
          record_button_list=request.values.getlist('record_button')
     else:
          record_button_list=[]

     if request.values.get('data_choise'):
          data_choise_list = request.values.getlist('data_choise')
     else:
          data_choise_list = []



     html = render_template(
     'index.html',
     service= df_Service,
     len = len,
     cosmetolog_list=cosmetolog_list,
     shugaring_list=shugaring_list,
     makeup_list=makeup_list,
     nail_list=nail_list,
     barber_list=barber_list,
     )

     if add_procedure_list :
          html = render_template(
               'index_2.html',
               len=len,
               masters=df_Record,
               masters_list=masters_list,
               add_procedure_list=list(session['procedures'])
          )

     if masters_list:
          uniq_date_list=[]
          for elem in masters_list_list:
               df_Master_record_uniq_date=elem.Дата.unique()
               uniq_date_list.append(df_Master_record_uniq_date)
          html = render_template(
               'index_3.html',
               master_records_list=masters_list_list,
               len=len,
               int=int,
               uniq_date_list=uniq_date_list
          )


     if record_button_list:
          html = render_template(
               'Record_list.html')


     if data_choise_list:
         html = render_template(
              'Record_list.html')

     return html
