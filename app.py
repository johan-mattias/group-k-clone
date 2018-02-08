from usermanager import UserManager
from loginmanager import LoginManager
from flask import Flask, request

app = Flask(__name__)
um = UserManager()
lm = LoginManager()

ENTER_USERNAME = "Please enter a valid username"
ENTER_PASSWORD = "Please enter a password"
ENTER_USERNAME_PASSWORD_VALID = "Please enter a valid username and password"

@app.route("/")
def home():
    return "Home page"

@app.route("/auth/register", methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if username is None:
        return ENTER_USERNAME, 400
    if password is None:
        return ENTER_PASSWORD, 400
    if um.get_by_username(username) is not None:
        return ENTER_USERNAME_PASSWORD_VALID, 400

    um.create_user(username, password)
    new_user = um.get_by_username(username)
    token = lm.encode_auth_token(new_user.id)

    return token, 200

@app.route("/auth/login", methods=["POST"])
def login():

    username = request.form.get('username')
    password = request.form.get('password')
    token = request.headers.get('Authorization')

    if token is not None:
        sub = lm.decode_auth_token(token)
        if um.get_by_id(sub) is not None:
            return token, 200
        return sub, 401

    if username is not None:
        user = um.get_by_username(username)

        if user is None:
            return ENTER_USERNAME_PASSWORD_VALID, 401

        if password is None:
            return ENTER_USERNAME_PASSWORD_VALID, 401

        if user.is_correct_password(password):
            return lm.encode_auth_token(user_id = user.id), 200
        else:
            return ENTER_USERNAME_PASSWORD_VALID, 401
    return ENTER_USERNAME_PASSWORD_VALID, 401

@app.route("/auth/logout")
def logout():
    return "Logout page"


def main():
    pass
    # um.create_user("Anton", "asdf")
    # um.create_user("Kasper", "lol123")

    # anton = um.get_by_id(1)
    # print(anton.id, anton.username, anton.password)
    # kasper = um.get_by_username("Kasper")
    # print(kasper.id, kasper.username, kasper.password)

    # fredrik = um.get_by_username("Fredrik") # Returns no results
    # # print(fredrik.id)
    # filip = um.get_by_id(3) # Returns no results
    # # print(filip.id)

    # users = um.get_all()
    # for user in users:
    #     print(user.id)


if __name__ == "__main__":
    # openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    app.run()
    main()