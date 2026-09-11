from flask import Flask, render_template, request, redirect, url_for, flash

from flask_login import (
    login_required,
    current_user,
    login_user,
    logout_user,
)

from Python_Web.hw22.messenger_project_db import Session, Users, Friends, Messages
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
app.config["MAX_FORM_MEMORY_SIZE"] = 1024 * 1024
app.config["MAX_FORM_PARTS"] = 500

app.config["SECRET_KEY"] = '#cv)3e7b$;s3fk;5c!@y0?4:U3"9)#'
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    with Session() as session:
        user = session.query(Users).filter_by(id=user_id).first()
        if user:
            return user


@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("index.html", username=current_user.nickname)


class LoginForm(FlaskForm):
    nickname = StringField("Nickname", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Увійти")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        nickname = form.nickname.data
        password = form.password.data

        with Session() as session:
            user = session.query(Users).filter_by(nickname=nickname).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for("home"))

            flash("Неправильний nickname або пароль!", "danger")

    return render_template("login.html", form=form)


class RegisterForm(FlaskForm):
    nickname = StringField("Nickname", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Увійти")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        nickname = form.nickname.data
        email = form.email.data
        password = form.password.data

        with Session() as session:
            existing_user_for_nickname = (
                session.query(Users).filter_by(nickname=nickname).first()
            )
            existing_user_for_email = (
                session.query(Users).filter_by(email=email).first()
            )

            if not (existing_user_for_email or existing_user_for_nickname):
                new_user = Users(nickname=nickname, email=email)
                new_user.set_password(password)
                session.add(new_user)
                session.commit()
                login_user(new_user)
                return redirect(url_for("home"))

            flash("Користувач з таким nickname або email вже існує!", "danger")

    return render_template("register.html", form=form)


class SearchFriendsForm(FlaskForm):
    name = StringField("Ім'я користувача", validators=[DataRequired()])
    submit = SubmitField("Запит на дружбу")


@app.route("/search_friends", methods=["GET", "POST"])
@login_required
def search_friends():
    form = SearchFriendsForm()
    if form.validate_on_submit():
        user_search_name = form.name.data
        with Session() as session:
            search_user = (
                session.query(Users).filter_by(nickname=user_search_name).first()
            )
            if search_user:

                check_request1 = (
                    session.query(Friends)
                    .filter_by(sender=search_user.id, recipient=current_user.id)
                    .first()
                )
                check_request2 = (
                    session.query(Friends)
                    .filter_by(sender=current_user.id, recipient=search_user.id)
                    .first()
                )

                if not check_request1 and not check_request2:
                    new_friend_request = Friends(
                        sender=current_user.id, recipient=search_user.id, status=False
                    )
                    session.add(new_friend_request)
                    session.commit()
                    flash("Запит на дружбу успішно надіслано!", "success")
                else:
                    flash(
                        "Ви вже являєтеся друзями або між вами вже є активниз запит на дружбу",
                        "danger",
                    )
            else:
                flash("Користувача з таким нікнеймом не знайдено", "danger")
    return render_template("search_friends.html", form=form)


class FriendsRequestsForm(FlaskForm):
    accept = SubmitField("yes")
    decline = SubmitField("no")


@app.route("/friend_requests")
@login_required
def friend_requests():
    form = FriendsRequestsForm()
    with Session() as session:
        all_friend_requests = (
            session.query(Friends)
            .filter_by(recipient=current_user.id, status=False)
            .all()
        )
        id_names_dict = {}
        for i in all_friend_requests:
            id_names_dict[i.sender_user.id] = i.sender_user.nickname
        return render_template("friend_requests.html", data=id_names_dict, form=form)


@app.route("/friend_requests_confirm/<int:user_id>", methods=["POST"])
@login_required
def friend_requests_confirm(user_id):
    form = FriendsRequestsForm()
    if not form.validate_on_submit():
        return redirect(url_for("home"))
    request_sender_id = user_id
    with Session() as session:
        select_request = (
            session.query(Friends)
            .filter_by(
                sender=request_sender_id, recipient=current_user.id, status=False
            )
            .first()
        )
        if not select_request:
            return "Сталася помилка при підтвердженні"

        if form.accept.data:
            select_request.status = True
            session.commit()

        elif form.decline.data:
            session.delete(select_request)
            session.commit()
        else:
            return redirect(url_for("home"))
    return redirect(url_for("friend_requests"))


class DeleteFriendForm(FlaskForm):
    submit = SubmitField("Видалити друга")


@app.route("/my_friends")
@login_required
def my_friends():
    form = DeleteFriendForm()
    with Session() as session:
        all_friends1 = (
            session.query(Friends).filter_by(sender=current_user.id, status=True).all()
        )
        all_friends2 = (
            session.query(Friends)
            .filter_by(recipient=current_user.id, status=True)
            .all()
        )
        friend_names = []
        for i in all_friends1:
            friend_names.append(i.recipient_user.nickname)
        for i in all_friends2:
            friend_names.append(i.sender_user.nickname)
        return render_template("my_friends.html", data=friend_names, form=form)


@app.route("/del_friend/<string:user_name>", methods=["POST"])
@login_required
def delete_friend(user_name):
    form = DeleteFriendForm()
    if form.validate_on_submit():
        with Session() as session:
            friend_to_del = session.query(Users).filter_by(nickname=user_name).first()
            if not friend_to_del:
                flash("Друга для видалення не знайдено", "danger")
                return redirect(url_for("my_friends"))
            friendship = (
                session.query(Friends)
                .filter(
                    (
                        (Friends.sender == current_user.id)
                        & (Friends.recipient == friend_to_del.id)
                    )
                    | (
                        (Friends.sender == friend_to_del.id)
                        & (Friends.recipient == current_user.id)
                    )
                )
                .first()
            )
            if not friendship:
                flash("Дружба не знайдена", "danger")
            else:
                session.delete(friendship)
                session.commit()
    return redirect(url_for("my_friends"))


class CreateMessageForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    submit = SubmitField("Відправити")


@app.route("/create_message/<string:user_name>", methods=["GET", "POST"])
@login_required
def create_message(user_name):
    form = CreateMessageForm()
    if form.validate_on_submit():
        message_text = form.text.data
        with Session() as session:
            user_recipient = session.query(Users).filter_by(nickname=user_name).first()
            if not user_recipient:
                flash("Отримувача не знайдено", "danger")
                return render_template("create_message.html", form=form)

            check_request1 = (
                session.query(Friends)
                .filter_by(
                    sender=user_recipient.id, recipient=current_user.id, status=True
                )
                .first()
            )
            check_request2 = (
                session.query(Friends)
                .filter_by(
                    sender=current_user.id, recipient=user_recipient.id, status=True
                )
                .first()
            )
            if check_request1 or check_request2:
                new_message = Messages(
                    sender=current_user.id,
                    recipient=user_recipient.id,
                    message_text=message_text,
                )
                session.add(new_message)
                session.commit()
                flash("Повідомлення надіслано!", "success")

            else:
                flash("Отримувача не являється другом", "danger")
                return render_template("create_message.html", form=form)

    return render_template("create_message.html", form=form)


@app.route("/new_messages")
@login_required
def new_messages():
    with Session() as session:
        new_messages = (
            session.query(Messages)
            .filter_by(recipient=current_user.id, status_check=False)
            .all()
        )
        name_text_dict = {}
        for i in new_messages:
            name_text_dict[i.sender_user.nickname] = i.message_text
            i.status = True
            session.commit()
        return render_template("new_messages.html", data=name_text_dict)


@app.route("/user_messages/<string:user_name>", methods=["GET"])
@login_required
def user_messages(user_name):
    with Session() as session:
        user_sender = session.query(Users).filter_by(nickname=user_name).first()
        if not user_sender:
            flash("Отримувача не знайдено", "danger")
            return redirect(url_for("new_messages"))
        messages = (
            session.query(Messages)
            .filter_by(recipient=current_user.id, sender=user_sender.id)
            .all()
        )
    print(messages)
    return render_template("user_messages.html", messages=messages)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5002)
