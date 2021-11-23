from flask import Flask, Blueprint, render_template, session, redirect
from forms import getForm
from utils import obtener_id_from_url, obtener_df_reviews

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'


@app.route("/")
@app.route("/home")
def home():
    """vista de la home"""
    return render_template("home.html")


@app.route("/products-compare", methods=["GET","POST"])
def products_compare():
    """Vista del template de comparacion de productos"""
    form = getForm()
    if form.validate_on_submit():
        id_prod1 = obtener_id_from_url(form.url1.data)
        id_prod2 = obtener_id_from_url(form.url2.data)
        df_prod1 = obtener_df_reviews(id_prod1)
        df_prod2 = obtener_df_reviews(id_prod2)
    return  render_template("products-compare.html", form=form)


@app.route("/results")
def results():
    """vista de los resultados"""
    return render_template("results.html")


if __name__ == '__main__':
    app.run(debug=True)
