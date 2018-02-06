from usermanager import UserManager
from loginmanager import LoginManager
from flask import Flask, request

app = Flask(__name__)
um = UserManager()
loginmanager = LoginManager()

@app.route("/")
def home():
    return "Home page"

@app.route("/auth/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']

    um.create_user(username, password)
    new_user = um.get_by_username(username)

    token = loginmanager.encode_auth_token(new_user.id)

    return token

@app.route("/auth/login")
def login():
    return "Login page"

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