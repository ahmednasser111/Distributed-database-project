# from sqlalchemy import create_engine, text # pip install sqlalchemy
# import pandas as pd

# server = "20.25.37.239"
# database = "test"
# username = "sa"
# password = "SQLServer123"
# driver = "ODBC Driver 17 for SQL Server"
# conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"

# engine = create_engine(conn_str)
# con = engine.connect()
# rs = con.execute(text(f"select * from testt"))
# print(rs.fetchall())





from flask import Flask, render_template, request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/products-details")
def products_details():
    return render_template("products-details.html")


if __name__ == "__main__":
    app.run()