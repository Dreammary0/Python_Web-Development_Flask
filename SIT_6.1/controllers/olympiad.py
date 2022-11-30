import constants
from app import app
from flask import render_template, request

@app.route('/olympiads/<oly>')

def olympiads(oly):
   html = render_template(
     'olympiad.html',
     oly = oly,
     discription = constants.olympiad_dict[oly]
   )
   return html
