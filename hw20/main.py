from flask import Flask, render_template, request, redirect, url_for, session
from databases import Session, Parfume, Order
import os, magic, uuid, random, itertools, string
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "hw20"

ADMIN_PASSWORD = "".join(
    random.choice(
        list(itertools.chain(string.ascii_letters, string.digits, string.punctuation))
    )
    for _ in range(10)
)
HOST = "127.0.0.1"
PORT = 4001

FILES_PATH = "static/parfumes"
ADMIN_PATH = f"/admin_{uuid.uuid4()}"
ADMIN_LINK = f"http://{HOST}:{PORT}{ADMIN_PATH}\nADMIN_PASSWORD= '{ADMIN_PASSWORD}'"

with open("admin_link.txt", "w") as f:
    f.write(ADMIN_LINK)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/parfumes")
def parfumes():
    with Session() as db_session:
        all_parfumes = db_session.query(Parfume).all()

    all_parfumes.sort(key=lambda x: x.id)
    return render_template("parfumes.html", parfumes=all_parfumes)


@app.route("/order/<int:parfume_id>", methods=["GET", "POST"])
def order(parfume_id):
    with Session() as db_session:
        parfume = db_session.query(Parfume).get(parfume_id)

        if not parfume:
            return "Товар не знайдено", 404

        if request.method == "POST":
            phone = request.form["phone"]
            email = request.form["email"]

            new_order = Order(phone=phone, email=email, parfume_id=parfume_id)
            db_session.add(new_order)
            db_session.commit()

            return redirect(url_for("index"))

        return render_template("order.html", parfume=parfume)


@app.route(ADMIN_PATH, methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        product_id = request.form.get("product-id")
        password = request.form.get("password")
        if product_id:
            user_file = request.files.get("product-photo")

            if not user_file:
                return "Недостатньо даних"

            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(user_file.read(1024))
            user_file.seek(0)

            if file_type not in ["image/png", "image/jpeg", "image/jpg"]:
                return "Обрано файл неправильного типу"

            if user_file.content_length > 5 * 1024 * 1024:
                return "Обрано файл великого розміру, допустимий розмір: менше 10 Мб"

            filename = secure_filename(user_file.filename)
            if not filename:
                return "Обрано файл неприйнятної назви"

            new_photo_name = f"{uuid.uuid4()}_{filename}"

            file_path = os.path.join(FILES_PATH, new_photo_name)
            user_file.save(file_path)

            with Session() as db_session:
                parfume = db_session.get(Parfume, product_id)

                if parfume:
                    parfume.picture = file_path
                    db_session.commit()

                else:
                    return "Такий парфюм не знайдено"

        if password == ADMIN_PASSWORD:
            session["isadmin"] = True

    if session.get("isadmin"):
        with Session() as db_session:
            all_parfumes = db_session.query(Parfume).all()

        all_parfumes.sort(key=lambda x: x.id)
        return render_template("admin.html", parfumes=all_parfumes)
    else:
        return render_template("admin_login.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)
