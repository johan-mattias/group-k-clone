from UserManager import UserManager


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


if __name__ == "__main__":
    main()