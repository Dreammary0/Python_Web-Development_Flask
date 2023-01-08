import pandas as pd
from app import app
from flask import render_template, request, session,Flask, redirect, url_for, flash, make_response
from utils import get_db_connection
from models.index_model import OrderListRegPage, Check_sum
@app.route('/regpage', methods=['get'])
def regpage():

     conn = get_db_connection()

     if request.values.get('record_button'):
          record_button_list=request.values.getlist('record_button')
          df_order_list_list=[]

          for proc in session['procedures']:
               df_order_list_list.append(OrderListRegPage(conn, record_button_list, proc))

          check_list=[]
          for serv in session['services']:
               if serv != '-':
                    for elem in serv:
                         check_list.append(elem)
          df_check_sum = Check_sum(conn, check_list)

     else:
          record_button_list=[]



     if request.values.get('submitSuccess'):
         if (request.values.get('username') and request.values.get('userphone')):
              print('дело сделать')
              print(record_button_list)
         else: print('дело не сделать')
         html = render_template('success.html', name= request.values.get('username'), phone=request.values.get('userphone'))
         return html

     elif request.values.get('exit'):
          return redirect('/')


     html = render_template(
          'reg_page.html',
          procedure_list=session['procedures'],
          service_list = session['services'],
          record_button_list=record_button_list,
          len=len,
          order_list = df_order_list_list,
          check_sum=df_check_sum
          )

     return html
