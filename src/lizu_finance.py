from flask import Flask
from bokeh.embed import server_document
from flask.templating import render_template
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'lizu'
app.config['BASIC_AUTH_PASSWORD'] = 'S_Birkenstein'

basic_auth = BasicAuth(app)


@app.route("/")
@basic_auth.required
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
    # tag = server_document(url='/bokeh', relative_urls=True)
    # return render_template('index.html', tag=tag)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
