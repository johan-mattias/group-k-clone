from UserManager import UserManager


def main():
    um = UserManager()
    um.create_user("Anton", "asdf")
    um.create_user("Kasper", "lol123")
    anton = um.get_user_by_id(1)
    print(anton.id, anton.username, anton.password)
    kasper = um.get_user_by_username("Kasper")
    print(kasper.id, kasper.username, kasper.password)


if __name__ == "__main__":
    main()