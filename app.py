from usermanager import UserManager
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Home page"


def main():
    um = UserManager()

    um.create_user("Anton", "asdf")
    um.create_user("Kasper", "lol123")

    anton = um.get_by_id(1)
    print(anton.id, anton.username, anton.password)
    kasper = um.get_by_username("Kasper")
    print(kasper.id, kasper.username, kasper.password)

    fredrik = um.get_by_username("Fredrik") # Returns no results
    # print(fredrik.id)
    filip = um.get_by_id(3) # Returns no results
    # print(filip.id)

    users = um.get_all()
    for user in users:
        print(user.id)


if __name__ == "__main__":
    # openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
    app.run(ssl_context=('cert.pem', 'key.pem'))
    main()