from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return "<h1>Hola Mundosss</h1>"

@app.route("/about")
def about():
    return "<h1>about page !!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
