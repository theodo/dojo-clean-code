import os
from time import sleep

from services.file_service import save_data_to_file, load_data_from_file
from services.encryption_service import encrypt, decrypt


def prompt_account_input():
    account = input("Enter password account:\n").lower()
    print("\n")
    return account


def handle_find_password(password_list):
    account = prompt_account_input()
    found_password_list = [
        password_object
        for password_object in password_list
        if password_object['account'] == account
    ]
    print(found_password_list)


def delete_password(account, password_list):
    new_password_list = [
        password_object
        for password_object in password_list
        if password_object['account'] != account
    ]
    return new_password_list


def handle_delete_password(password_list, master_password):
    account = prompt_account_input()
    new_password_list = delete_password(account, password_list)

    if len(new_password_list) == len(password_list):
        print("No password was found matching this account in the vault!")
    else:
        print("Password {} successfully deleted from vault".format(account))

    save_password_list(new_password_list, master_password)
    return new_password_list


def add_password(password_object, password_list):
    new_list = password_list.copy()
    new_list.append(password_object)
    return new_list


def prompt_add_password():
    account = input("Enter password account:\n").lower()
    print("\n")
    username = input("Enter username for {}: \n".format(account))
    print("\n")
    password = input("Enter password: \n")
    print("\n")
    return {"account": account, "username": username, "password": password}


def handle_add_password(password_list, master_password):
    password_object = prompt_add_password()
    new_password_list = add_password(
        password_object, password_list)
    save_password_list(new_password_list, master_password)
    print("Your new password has been saved \n")
    print("Returning...")
    return new_password_list


def load_password_list(password):
    """Load the password list from the encrypted vault"""
    ciphered_data = load_data_from_file("./ciphered_vault")
    return decrypt(ciphered_data, password)


def save_password_list(password_list, password):
    """Save the password list in the encrypted vault"""
    ciphered_list = encrypt(password_list, password)
    save_data_to_file("./ciphered_vault", ciphered_list)


def prompt_login_existing_account():
    password = input("Enter your master password: ")
    print("")

    # Try and decipher the vault to check master password
    try:
        password_list = load_password_list(password)
        return password_list, password
    except Exception:
        print("WRONG PASSWORD !\n")
        exit(1)


def prompt_register_new_account():
    print("This is a new account !\n")
    password = input("Please enter a master password:\n")
    print("")
    save_password_list([], password)
    return [], password


def main():
    files = os.listdir()
    print("Welcome to PassKeep\n")

    # Account already exists
    if "ciphered_vault" in files:
        password_list, master_password = prompt_login_existing_account()

    # Account creation phase
    else:
        password_list, master_password = prompt_register_new_account()

    while True:
        print("")
        print("Type in 1 to store a new password! \n")
        print("Type in 2 to retrieve one of your passwords \n")
        print("Type in 3 to delete one of your saved accounts \n")
        print("Type in 4 to quit the program \n")
        print("Type in 5 to see all saved accounts \n")
        print("Type in 6 to delete everything \n")

        option = input()
        if option == "1":
            password_list = handle_add_password(password_list, master_password)
        elif option == "2":
            handle_find_password(password_list)
        elif option == "3":
            password_list = handle_delete_password(
                password_list, master_password)
        elif option == "4":
            print("Quitting...")
            quit()
        elif option == "5":
            print(password_list)
        elif option == "6":
            pass
        else:
            print("Invalid command...")
            print("Restarting...")
            sleep(1)


if __name__ == "__main__":
    main()
