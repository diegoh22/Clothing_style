
import gspread

from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open('Clothing-Style')


def get_sales_numbers():

    """
    Get the sales numbers of the day
    """
    while True:
        print('Please enter de sales numbers of the day')
        print('Enter the numbers separate by a commas')
        print(' six numbers, Explate 10,50,100,65,48,98,\n')

        numbers_str = input("Enter the numbers here: ")

        sales_numbers = numbers_str.split(",")

        if validate_data(sales_numbers):
            print("Data is valid!")
            break
    return sales_numbers


def validate_data(values):

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Enter six numbers, you enter:\n {len(values)}"
            )
    except ValueError as e:
        print(f"invalid date: {e}, please try again.\n")
        return False

    return True


def update_sale_worksheet(data):

    print("Updating sales woksheet...\n")
    sales_woksheet = SHEET.worksheet("sales")
    sales_woksheet.append_row(data)
    print("sales updated Successfully.\n")


def update_surplus_worksheet(data):

    print("Updating sales woksheet...\n")
    surplus_woksheet = SHEET.worksheet("surplus")
    surplus_woksheet.append_row(data)
    print("sales updated Successfully.\n")


def calculate_surplus_numbers(sales_row):
    print("calculation Surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(f"stock_row: {stock_row}")
    print(f"sales_row: {sales_row}")

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def main():
    data = get_sales_numbers()
    sales_numbers = [int(num) for num in data]
    update_sale_worksheet(sales_numbers)
    new_surplus_data = calculate_surplus_numbers(sales_numbers)
    update_surplus_worksheet(new_surplus_data)


print("Welcome to Clothing and Style Weekly numbers Automation")
main()
