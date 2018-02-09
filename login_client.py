import requests


class Client:
    def __init__(self, base_url):
        self.base_url = base_url

    def register(self, username, password):
        r = requests.post("http://" + self.base_url + "/auth/register",
                          data={"username": username, "password": password})
        # r = requests.post("https://" + self.base_url + "/auth/register",
        #                   data={"username": username, "password": password}, verify='cert.pem')

        if r.status_code == 200:
            with open("token.txt", "w") as token_file:  # Write token to file
                token_file.write(r.text)
            return "ok"
        else:
            return r.text

    def login_with_password(self, username, password):
        # print("Token not found, login with password")
        # username = input("username: ")
        # password = input("password: ")
        r = requests.post("http://" + self.base_url + "/auth/login", data={"username": username, "password": password})
        # r = requests.post("https://" + self.base_url + "/auth/login", data={"username": username, "password": password},
        #                   verify='cert.pem')

        if r.status_code == 200:
            with open("token.txt", "w") as token_file:
                token_file.write(r.text)
            return "ok"
        else:
            return r.text

    def login(self):
        try:
            with open("token.txt", "r") as token_file:
                token = token_file.readline().strip()
        except FileNotFoundError:
            return "token_not_found"
        else:
            print(token)
            r = requests.post("http://" + self.base_url + "/auth/login", headers={"Authorization": token})
            # r = requests.post("https://" + self.base_url + "/auth/login", headers={"Authorization": token},
            #                 verify='cert.pem')

            if r.status_code == 200:
                return "ok"
            else:
                return r.text


def main():
    base_url = input("Input server URL: ")
    c = Client(base_url)

    print("1. Register\n2. Login")
    choice = int(input())
    if choice == 1:
        username = input("Username: ")
        password = input("Password: ")
        c.register(username, password)
    elif choice == 2:
        c.login()


if __name__ == '__main__':
    main()