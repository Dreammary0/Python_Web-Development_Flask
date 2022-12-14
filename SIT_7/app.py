from flask import Flask, session
import controllers.index

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

if __name__ == '__main__':
    app.run(debug=True)
#import controllers.search
#import controllers.new_reader
