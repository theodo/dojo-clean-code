import os
from time import sleep

from services.file_service import save_data_to_file, load_data_from_file
from services.encryption_service import encrypt, decrypt


def add_password(password_object, password_list):
    new_list = password_list.copy()
    new_list.append(password_object)
    return new_list


def prompt_add_password():
    website_name = input("Enter website name:\n").lower()
    print("\n")
    username = input("Enter username for {}: \n".format(website_name))
    print("\n")
    password = input("Enter password: \n")
    print("\n")
    return {
        "website_name": website_name,
        "username": username,
        "password": password
    }


def handle_add_account(password_list, master_password):
    account_object = prompt_add_password()
    new_password_list = add_password(
        account_object, password_list)
    write(new_password_list, master_password)
    print("Your new account and password have been saved \n")
    print("Returning...")
    return new_password_list


def load_account_list(password):
    """Load the account list from the encrypted vault"""
    ciphered_data = load_data_from_file("./ciphered_vault")
    return decrypt(ciphered_data, password)


def write(password_list, password):
    """Save the account list in the encrypted vault"""
    ciphered_list = encrypt(password_list, password)
    save_data_to_file("./ciphered_vault", ciphered_list)


def handle_login_existing_account():
    password = input("Enter your master password: ")
    print("")

    # Try and decipher the vault to check master password
    try:
        password_list = load_account_list(password)
        return password_list, password
    except Exception:
        print("WRONG PASSWORD !\n")
        exit(1)


def handle_register_new_account():
    print("This is a new account !\n")
    password = input("Please enter a master password:\n")
    print("")
    write([], password)
    return [], password


def main():
    files = os.listdir()
    print("Welcome to PassKeep\n")

    # Account already exists
    if "ciphered_vault" in files:
        pList, master_password = handle_login_existing_account()

    # Account creation phase
    else:
        pList, master_password = handle_register_new_account()

    while True:
        print("")
        print("Type in 1 to store a new website account! \n")
        print("Type in 2 to retrieve one of your website accounts \n")
        print("Type in 3 to delete one of your saved accounts \n")
        print("Type in 4 to quit the program \n")
        print("Type in 5 to see all saved accounts \n")
        print("Type in 6 to delete everything \n")

        option = input()
        if option == "1":
            pList = handle_add_account(pList, master_password)
        elif option == "2":
            a = input("Enter password account:\n").lower()
            print("\n")

            temp = 0
            for i in range(len(pList)):
                if pList[i]['account'] == a:
                    print(pList[i])

        elif option == "3":
            l = len(pList)
            a = input("Enter website name:\n").lower()
            print("\n")

            temp1 = 0
            for i in range(0, len(pList)):
                if pList[i]['account'] == a:
                    del pList[i]
                    break

            if len(pList) == l:
                print("No accounts were found matching this website name!")
            else:
                print("Account {} successfully deleted from vault".format(a))

        elif option == "4":
            print("Quitting...")
            quit()
        elif option == "5":
            print(pList)
        elif option == "6":
            pass
        else:
            print("Invalid command...")
            print("Restarting...")
            sleep(1)


if __name__ == "__main__":
    main()
