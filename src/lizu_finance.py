from flask import Flask
from bokeh.embed import server_document
from flask.templating import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"
    # tag = server_document(url='/bokeh', relative_urls=True)
    # return render_template('index.html', tag=tag)

if __name__ == "__main__":
    app.run(host='0.0.0.0')