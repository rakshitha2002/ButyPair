from flask import Flask
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'application\static\images'

from application import routes