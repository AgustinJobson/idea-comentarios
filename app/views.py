from flask import Flask, Blueprint, render_template, session, redirect
from forms import getForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/products-compare", methods=["GET","POST"])
def about():
    form = getForm()
    if form.validate_on_submit():
        url_1 = form.url1.data
        url_2 = form.url2.data
    return  render_template("products-compare.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
