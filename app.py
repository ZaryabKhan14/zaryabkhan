from flask import Flask,render_template
from chatbot import chatbot_app
from codegenerator import codegenerator_app
from pdfsummarizer import pdfsummarizer_app
from imagegenerator import imagegenerator_app
from healthassistant import healthassitant_app

app = Flask(__name__)
app.secret_key = 'zaryab khan'  # Replace with a strong secret key



@app.route('/')
def index():
    return render_template('index.html')
# Register the project-specific apps
app.register_blueprint(chatbot_app, url_prefix='/chatbot')

app.register_blueprint(codegenerator_app)  # Register the Blueprint
app.register_blueprint(pdfsummarizer_app, url_prefix='/pdfsummarizer')
app.register_blueprint(imagegenerator_app)
app.register_blueprint(healthassitant_app)

if __name__ == '__main__':
    app.run(debug=True)