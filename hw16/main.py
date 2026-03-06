from flask import Flask, render_template, request, redirect, url_for

from databases import Session, Parfume, Order

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/parfumes")
def parfumes():
    with Session() as session:
        all_parfumes = session.query(Parfume).all()

    return render_template("parfumes.html", parfumes=all_parfumes)


@app.route("/order/<int:parfume_id>", methods=["GET", "POST"])
def order(parfume_id):
    with Session() as session:
        parfume = session.query(Parfume).get(parfume_id)

        if not parfume:
            return "Товар не знайдено", 404

        if request.method == "POST":
            phone = request.form["phone"]
            email = request.form["email"]

            new_order = Order(phone=phone, email=email, parfume_id=parfume_id)
            session.add(new_order)
            session.commit()

            return redirect(url_for("index"))

        return render_template("order.html", parfume=parfume)


if __name__ == "__main__":
    app.run(debug=True, port=1700)
