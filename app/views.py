from flask import Flask, Blueprint, render_template, session, redirect, url_for
from forms import getForm
from utils import obtener_id_from_url, obtener_df_reviews, obtener_mejor_producto

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

@app.route("/")
@app.route("/home")
def home():
    """vista de la home"""
    return render_template("home.html")


# Links de ejemplo
# https://www.mercadolibre.com.ar/samsung-galaxy-a01-core-16-gb-azul-1-gb-ram/p/MLA16150548
# https://www.mercadolibre.com.ar/samsung-galaxy-a32-128-gb-awesome-black-4-gb-ram/p/MLA17706115
@app.route("/products-compare", methods=["GET","POST"])
def products_compare():
    """Vista del template de comparacion de productos"""
    form = getForm()
    if form.validate_on_submit():
        id_prod1 = obtener_id_from_url(form.url1.data)
        id_prod2 = obtener_id_from_url(form.url2.data)
        df_prod1 = obtener_df_reviews(id_prod1)
        df_prod2 = obtener_df_reviews(id_prod2)
        mejor_producto = obtener_mejor_producto(df_prod1, df_prod2)
        if mejor_producto == 1:
            return redirect(url_for("results", prod = id_prod1))
        return redirect(url_for("results", prod = id_prod2))
    return  render_template("products-compare.html", form=form)

@app.route("/results/<prod>")
def results(prod):
    """Vista del template de resultados"""
    return render_template("results.html", id = prod)


if __name__ == '__main__':
    app.run(debug=True)
