from flask import Flask, render_template

app = Flask(__name__)

menuApp = ["Установка", "Первое приложение", "Обратная связь"]

@app.route("/")
def index():
    return render_template('index.html', menu=menuApp)

@app.route("/about")
def about():
    return render_template('about.html', title="О сайте",  menu=menuApp)

if __name__=="__main__":
    app.run(debug=True)