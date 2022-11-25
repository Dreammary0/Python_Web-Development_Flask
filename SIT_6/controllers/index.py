from app import app
from flask import render_template
@app.route('/', methods=['GET'])
def index():
 # выводим форму
 html = render_template('index.html')
 return html