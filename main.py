import pandas as pd
import os
import random


class bookMaster:
    def __init__(self, bookName, bookAuthor, bookType, bookPrice, bookStock):
        self.bookName = bookName
        self.bookAuthor = bookAuthor
        self.bookType = bookType
        self.bookPrice = bookPrice
        self.bookStock = bookStock
        
    def __str__(self):
        return f"Book: {self.bookName} | Author: {self.bookAuthor} | Price: {self.bookPrice}"
    
class customerMaster:
    def __init__(self, customerName, customerAddress, customerPhone):
        self.customerName = customerName
        self.customerAddress = customerAddress
        self.customerPhone = customerPhone

    def __str__(self):
        return f"Customer: {self.customerName} | Address: {self.customerAddress} | Phone: {self.customerPhone}"

class employeeMaster:
    def __init__(self, employeeName, employeeAddress, employeeSalary, employeeBehaviour):
        self.employeeName = employeeName
        self.employeeAddress = employeeAddress
        self.employeeSalary = employeeSalary
        self.employeeBehaviour = employeeBehaviour
    
    def __str__(self):
        return f"Employee: {self.employeeName} | Address: {self.employeeAddress} | Salary: {self.employeeSalary}"

 #-------------------------------------------------------------------------------------------------------------------------------


def clear_screen():
    
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def displayAllBooks():
    clear_screen()
    if not os.path.exists('data_book.csv') or os.stat('data_book.csv').st_size == 0:
        print("\n[!] The library shelves are empty! Add some books first.")
    else:
        try:
            df = pd.read_csv('data_book.csv')
            print("==================== CURRENT INVENTORY ====================")
            # This prints the dataframe without the index numbers on the left
            print(df.to_string(index=False))
            print("============================================================")
            print(f"Total Books in System: {len(df)}")
        except Exception as e:
            print(f"Error reading database: {e}")
            
    input("\nPress Enter to return to menu...")

def searchBook():
    
    if not os.path.exists('data_book.csv'):
        print("\nError: The database file does not exist yet.")
        input("Press Enter to return...")
        return


    if os.stat('data_book.csv').st_size == 0:
        print("\nError: The database file is empty. Add a book first!")
        input("Press Enter to return...")
        return

    try:
        search_name = input("\nEnter the name of the book you are looking for: ")
        df = pd.read_csv('data_book.csv')
    
        
        result = df[df['bookName'].str.lower() == search_name.lower()]
        
        if not result.empty:
            print("\n--- Book Found ---")
            print(result.to_string(index=False))
        else:
            print(f"\nSorry, '{search_name}' was not found.")
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    input("\nPress Enter to return to menu...")

def getDataBook():
    bookData = input("Enter book details (Name Author Type Price Stock): ").split()
    if len(bookData) == 5:
         b1 = bookMaster(bookData[0], bookData[1], bookData[2], int(bookData[3]), int(bookData[4]))
         df_book = pd.DataFrame([vars(b1)])
         file_path = 'data_book.csv'
         df_book.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))
         print("\nSuccessfully saved book to database")
         print(b1)
    else:
         print("Error: Please enter all 5 details.")
    answer = input("press enter to go back to the menu")
    

def getDataCustomer():
    customerData = input("Enter customer details (Name Address Phone): ").split()
    if len(customerData) == 3:
        c1 = customerMaster(customerData[0], customerData[1], int(customerData[2]))
        df_customer = pd.DataFrame([vars(c1)])
        file_path = 'data_customer.csv'
        df_customer.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))
        print("\nSuccessfully created customer to database")
        print(c1)
    else:
        print("Error: Please enter all 3 details.")
    answer = input("press enter to go back to the menu")
def getDataEmployee():
    employeeData = input("Enter employee details (Name Address Salary Behaviour): ").split()
    if len(employeeData) == 4:
        e1 = employeeMaster(employeeData[0], employeeData[1], int(employeeData[2]), employeeData[3])
        df_employee = pd.DataFrame([vars(e1)])
        file_path = 'data_employee.csv'
        df_employee.to_csv(file_path, mode='a', index=False, header=not os.path.exists(file_path))
        print("\nSuccessfully created employee to database")
        print(e1)
    else:
        print("Error: Please enter all 4 details.")
    answer = input("press enter to go back to the menu")
    
def main():
    while (True):
        display_name = "None"
        display_mood = "Unknown"
        
        if os.path.exists('data_employee.csv'):
            try:
                df_e = pd.read_csv('data_employee.csv')
                if not df_e.empty:
                    # Pick one random row
                    random_staff = df_e.sample().iloc[0]
                    display_name = random_staff['employeeName']
                    display_mood = random_staff['employeeBehaviour']
            except Exception:
                pass
        clear_screen()
        print("==================LIBRARY SOFTWARE==================")
        print(f"       EMPLOYEE: {display_name} --> MOOD: {display_mood}")
        print("      1.ADD A NEW BOOK ENTRY.")
        print("      2.ADD A NEW CUSTOMER ENTRY.")
        print("      3.ADD A NEW EMPLOYEE ENTRY." )
        print("      4.SEARCH A BOOK IN DATABASE." )
        print("      5.DISPLAY ALL BOOKS IN DATABASE." )
        print("      6.EXIT PROGRAM")
        choice = input("Enter your choice here (1 as in 1st option and 2 as in 2nd option and so on) \n ===> ")
        if (choice == "1"):
            getDataBook()
        elif (choice == "2"):
            getDataCustomer()
        elif (choice == "3"):
            getDataEmployee()
        elif (choice == "4"):
            searchBook()
        elif (choice == "5"):
            displayAllBooks()
        elif (choice == "6"):
            print("\nThank you for using the Library Management System!")
            break
        else:
            print(f"\n'{choice}' is not a valid option.")
            input("Press Enter to try again...")
main()
    #--------------------------------------------------------------------------------------------------------------------------------