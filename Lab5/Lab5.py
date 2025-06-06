from user_repository import UserRepository
from user import User
from auth_service import AuthService
from serializers import JSONSerializer

def demo():
    user_repo = UserRepository("data/users.json", JSONSerializer())
    auth_service = AuthService(user_repo, "data/session.txt")

    users = [
        User(id = 0, login = "admin", password = "admin123", name = "Admin"),
        User(id = 1, login = "login", password = "pass", name = "Name", email = "NameDigits@example.com", address="example street")
             ]

    for user in users:
        if not user_repo.get_by_id(user.id):
            user_repo.add(user)

    print("Авторизация с неверными данными:")
    try:
        auth_service.sign_in(login="not login",password= "not pass")
        print(f"Авторизован: {auth_service.current_user}")
    except ValueError as e:
        print(e)


    print("\nАвторизация с верными данными:")
    try:
        auth_service.sign_in(login="login",password= "pass")
        print(f"Авторизован: {auth_service.current_user}")

        auth_service.current_user.name = "aaa"
        user_repo.update(auth_service.current_user)

        print(f"После изменения имени: {auth_service.current_user}")
    except ValueError as e:
        print(e)


def demo2():
    user_repo = UserRepository("data/users.json", JSONSerializer())
    auth_service = AuthService(user_repo, "data/session.txt")

    if auth_service.is_authorized:
        print(auth_service.current_user)
        auth_service.sign_out()
        print("\nАвторизован после выхода:", auth_service.is_authorized)

        auth_service.sign_in(login="admin", password="admin123")
        print(f"Авторизован: {auth_service.current_user}")

        auth_service.sign_out()
    else:
        print("Не авторизован")


if __name__ == "__main__":
    #demo()
    demo2()