import os
from time import sleep
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from services.file_service import save_data_to_file, load_data_from_file
from services.encryption_service import encrypt, decrypt

console = Console()


def add_password(password_object, password_list):
    new_list = password_list.copy()
    new_list.append(password_object)
    return new_list


def prompt_add_password():
    website_name = Prompt.ask("Enter website name").lower()
    username = Prompt.ask("Enter username for {}".format(website_name))
    password = Prompt.ask("Enter password")
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
    console.print("Your new account and password have been saved \n")
    console.print("Returning...")
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
    console.print("")

    # Try and decipher the vault to check master password
    try:
        password_list = load_account_list(password)
        return password_list, password
    except Exception:
        console.print("WRONG PASSWORD !\n")
        exit(1)


def handle_register_new_account():
    console.print("This is a new account !\n")
    password = Prompt.ask("Please enter a master password")
    console.print("")
    write([], password)
    return [], password


def show_options():
    table = Table(title="Options")

    table.add_column("Option", style="cyan")
    table.add_column("Name", style="magenta")

    # adding the rows
    table.add_row("1", "Store new website account")
    table.add_row("2", "Retrieve website account")
    table.add_row("3", "Delete website account")
    table.add_row("4", "Quit the program")
    table.add_row("5", "Show all saved accounts")
    table.add_row("6", "Delete everything")

    console.print(table, justify="center")


def main():
    files = os.listdir()
    console.clear()
    console.print("[blue underline]WELCOME TO PASSKEEP", justify="center")

    # Account already exists
    if "ciphered_vault" in files:
        pList, master_password = handle_login_existing_account()

    # Account creation phase
    else:
        pList, master_password = handle_register_new_account()

    while True:
        console.rule()

        show_options()

        option = Prompt.ask("What do you want to do ? ")

        if option == "1":
            pList = handle_add_account(pList, master_password)
        elif option == "2":
            a = Prompt.ask("Enter account website name").lower()
            console.print("\n")

            temp = 0
            for i in range(len(pList)):
                if pList[i]['website_name'] == a:
                    console.print(pList[i])

        elif option == "3":
            l = len(pList)
            a = Prompt.ask("Enter website name").lower()
            console.print("\n")

            temp1 = 0
            for i in range(0, len(pList)):
                if pList[i]['website_name'] == a:
                    del pList[i]
                    break

            if len(pList) == l:
                console.print(
                    "No accounts were found matching this website name!"
                )
            else:
                console.print(
                    "Account {} successfully deleted from vault".format(a)
                )

        elif option == "4":
            console.print("Quitting...")
            quit()
        elif option == "5":
            console.print(pList)
        elif option == "6":
            pass
        else:
            print("Invalid command...")
            print("Restarting...")
            sleep(1)


if __name__ == "__main__":
    main()
