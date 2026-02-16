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
        c1 = customerMaster(customerData[0], customerData[1], customerData[2])
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
def bookBorrow(username): 

    df_customer = pd.read_csv('data_customer.csv')
    
    print(f"\n--- Borrowing Session: {username} ---")
    bookname = input("Which book are you borrowing? ")
    
   
    if 'borrowedBooks' not in df_customer.columns:
        df_customer['borrowedBooks'] = ""

  
    mask = df_customer['customerName'].str.lower() == username.lower()
    
   
    old_list = df_customer.loc[mask, 'borrowedBooks'].fillna("").iloc[0]
    df_customer.loc[mask, 'borrowedBooks'] = f"{old_list}{bookname}, "
    df_customer.to_csv('data_customer.csv', index=False)
    
    print(f"Success! '{bookname}' has been added to your record.")
    input("\nPress Enter to return to dashboard...")

def bookPurchase(username): 
    if not os.path.exists('data_customer.csv') or not os.path.exists('data_book.csv'):
        print("\n[!] Error: Database files missing.")
        input("\nPress Enter to go back...")
        return

    df_customer = pd.read_csv('data_customer.csv')
    df_book = pd.read_csv('data_book.csv')
    
    if 'loyaltyPoints' not in df_customer.columns:
        df_customer['loyaltyPoints'] = 0

    
    
    cust_mask = df_customer['customerName'].str.lower() == username.lower()
    print(f"\n--- Purchase Session: {username} ---")
    
    bookname = input("Which book are you purchasing? ")
    
    if bookname.lower() not in df_book['bookName'].str.lower().values:
        print(f"\n[!] Error: '{bookname}' is not available.")
        input("\nPress Enter...")
        return
    
    book_mask = df_book['bookName'].str.lower() == bookname.lower()
    price = df_book.loc[book_mask, 'bookPrice'].iloc[0]
    stock = df_book.loc[book_mask, 'bookStock'].iloc[0]

    if stock <= 0:
        print("Sorry, out of stock!")
        input("\nPress Enter...")
        return

    confirm = input(f"Price: {price}. Proceed? (yes/no) ")
    if confirm.lower() == 'yes':
        df_book.loc[book_mask, 'bookStock'] = stock - 1
        df_book.to_csv('data_book.csv', index=False)
        
        current_points = df_customer.loc[cust_mask, 'loyaltyPoints'].iloc[0]
        df_customer.loc[cust_mask, 'loyaltyPoints'] = current_points + 1
        df_customer.to_csv('data_customer.csv', index=False)
        
        print(f"Purchase successful! You earned 1 point. Total points: {current_points + 1}")
    else:
        print("Purchase cancelled.")
    
    input("\nPress Enter to return...")


    
def main():
    current_user = None
    while (True):
        if current_user is None:
            clear_screen()
            print("================== LIBRARY LOGIN ==================")
            print("  Welcome! Please identify yourself to enter.")
            print("  - Type your Name to Login")
            print("  - Type 'new' to Register a New Account") 
            print("  - Type 'exit' to shut down")
            print("====================================================")
            
            name_attempt = input("\nEnter choice/name: ").strip()

            if name_attempt.lower() == 'exit':
                break
            
           
            if name_attempt.lower() == 'new':
                getDataCustomer()
                continue
           
            if os.path.exists('data_customer.csv'):
                df_cust = pd.read_csv('data_customer.csv')
                if name_attempt.lower() in df_cust['customerName'].str.lower().values:
                    mask = df_cust['customerName'].str.lower() == name_attempt.lower()
                    current_user = df_cust.loc[mask, 'customerName'].iloc[0]
                    
                    print(f"\n[SUCCESS] Access Granted. Welcome, {current_user}!")
                    input("Press Enter to access the dashboard...")
                    continue  
                else:
                    print(f"\n[!] Error: '{name_attempt}' not found in records.")
                    print("Please use Option 2 in the main menu (once logged in as Admin) or register.")
                    input("Press Enter to try again...")
                    continue
            else:
                print("\n[!] Database error: data_customer.csv missing.")
                input("Press Enter to return...")
                continue
        display_name = "None"
        display_mood = "Unknown"
        
        if os.path.exists('data_employee.csv'):
            try:
                df_e = pd.read_csv('data_employee.csv')
                if not df_e.empty:
                    random_staff = df_e.sample().iloc[0]
                    display_name = random_staff['employeeName']
                    display_mood = random_staff['employeeBehaviour']
            except Exception:
                pass
        if os.path.exists('data_book.csv') and os.stat('data_book.csv').st_size > 0:
            try:
                df_b = pd.read_csv('data_book.csv')
                if not df_b.empty:
                    random_book = df_b.sample().iloc[0]
                    rec_text = f"'{random_book['bookName']}' by {random_book['bookAuthor']}"
            except Exception:
                rec_text = "Browsing the shelves..."
        clear_screen()
        print("==================LIBRARY SOFTWARE==================")
        print(f"       ACTIVE SESSION: {current_user.upper()}")
        print(f"       EMPLOYEE: {display_name} --> MOOD: {display_mood}")
        print(f"       MY BOOK RECCOMENDATION: {rec_text}")
        print("      1.ADD A NEW BOOK ENTRY.")
        print("      2.ADD A NEW CUSTOMER ENTRY.")
        print("      3.ADD A NEW EMPLOYEE ENTRY." )
        print("      4.SEARCH A BOOK IN DATABASE." )
        print("      5.DISPLAY ALL BOOKS IN DATABASE." )
        print("      6.BORROW A BOOK.")
        print("      7.PURCHASE A BOOK.")
        print("      8.LOGOUT.")  
        print("      9.EXIT.")  
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
            bookBorrow(current_user)
        elif (choice == "7"):
            bookPurchase(current_user)
        elif (choice == "8"):
            print(f"\n[LOGOUT] Goodbye, {current_user}!")
            current_user = None  
            input("Press Enter to return to the login screen...")
            continue
        elif (choice == "9"):
            print("\nThank you for using the Library Management System!")
            break
        else:
            print(f"\n'{choice}' is not a valid option.")
            input("Press Enter to try again...")
main()
    #--------------------------------------------------------------------------------------------------------------------------------