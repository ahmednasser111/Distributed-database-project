"""
To use the code run this file
"""
# pip install flask
from flask import Flask, render_template, request
from flask import render_template,render_template_string
from __init__ import db
import os

app = Flask(__name__)

"""
the @app.route(...) is used to move the user from one
page to another.
render_template("*.html") is for serving the html page
to the browser.
the POST and GET are for regalting the reading and writing
to and from the web page.
"""
@app.route("/about")
def hello():
    return render_template("about.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        cities=request.form.getlist('city')
        products=request.form.getlist("product")
        print(cities)
        print(products)
        db.query(cities,products)
    return render_template("search.html")


@app.route("/", methods = ['GET', 'POST'])
def account():
    data = request.form.get('server')
    os.environ['server'] = str(data)
    print(data)
    print(type(data))
    return render_template("index.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/products-details", methods=['GET', 'POST'])
def products_details():
    if request.method == 'POST':
        pid = request.form.get('pid')
        count = request.form.get('count')
        db.up(pid, count)
    return render_template("products-details.html")

if __name__ == "__main__":
    app.run()