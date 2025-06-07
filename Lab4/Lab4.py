from user import User
from data_changing import EmailValidator, NameValidator
from data_changed import ConsoleLogger


def main():
    user = User()
    user.add_property_changing_listener(EmailValidator())
    user.add_property_changing_listener(NameValidator())
    user.add_property_changed_listener(ConsoleLogger())

    print("\nКорректный ввод")
    user.name = "Name"
    user.email = "NameDigits@example.com"

    print("\nНекорректный ввод")
    user.name = ""
    user.email = "AA@AAAA@AAAA.ru"

    print("\nИтоговые значения:")
    print(f"Имя: {user.name}, Email: {user.email}")

if __name__ == "__main__":
    main()