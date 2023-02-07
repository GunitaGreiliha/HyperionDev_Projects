
#========Importing libraries==========

from tabulate import tabulate

#========The beginning of the class==========

class Shoe:
    """Shoe class to store the shoe objects in the inventory. 
    It contains the constructor function and methods.
    """
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Method to get cost of the shoes.
    def get_cost(self):
        return self.cost

    # Method to get quantity of the shoes.    
    def get_quantity(self):
        return self.quantity

    # Method to return a string representation of the class.
    def __str__(self):
        return f"\n{self.country},{self.code},{self.product},{self.cost},{self.quantity}"

    # Method to make the class iterable.
    def __iter__(self):
        return iter([self.country, self.code, self.product, self.cost, self.quantity])


#=============Shoe list===========

# The list will be used to store a list of objects of shoes.
shoe_list = []


#==========Functions outside the class==============

def read_shoes_data():
    """This function will open the file inventory.txt, 
    read the data from this file and then create a shoes object with this data
    and append this object into the shoes list.
    Try-except is used to handle situation when the file is not available.
    First line in the file is skipped.
    """
    try:
        with open ("inventory.txt", "r", encoding='utf-8') as inventory:
            inventory_data = inventory.readlines()
        
        for shoe in inventory_data[1:]:
            shoe = shoe.strip().split(",")
            shoe_list.append(Shoe(shoe[0],shoe[1],shoe[2],float(shoe[3]),int(shoe[4])))
    
    except FileNotFoundError:
        print("File 'inventory.txt' does not exist.")


def capture_shoes():
    """This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    # It also adds new object to inventory.txt file.
    """
    print("\nPlease provide following information to add new shoes to the stock.")
    country = input("Enter the country: \t").capitalize()
    code = input("Enter the code: \t")
    product = input("Enter the product: \t")
    
    while True:
        try:
            cost = float(input("Enter the cost: \t"))
            break
        except ValueError:
            print("Invalid input. Only numbers are allowed.\n")    
            
    while True:
        try:
            quantity = int(input("Enter the quantity: \t"))
            break
        except ValueError:
            print("Invalid input. Only whole numbers are allowed.\n")      
    
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)

    try:
        with open("inventory.txt", "a") as inventory:
            inventory.write(str(new_shoe)) 
    except FileNotFoundError:
        print("File 'inventory.txt' does not exist. ")
    
    print("New shoes successfully added to the warehouse stock.")

def view_all():
    """This function will print the details of the shoes stored in the shoe list
    organized in a table format by using tabulate module.
    """
    
    if len(shoe_list) == 0:
        print("Inventory is empty!")
    else:
        print("\n---All shoes currently available in the warehouse---\n")  
        print(tabulate([shoe.__iter__() for shoe in shoe_list], headers=["Country", "Code", "Product", "Cost", "Quantity"]))
    

def re_stock():
    """This function will find the shoe objects with the lowest quantity, 
    which is the shoes that need to be re-stocked. 
    When user adds the quantity of shoes, list is updated.
    This quantity should be updated on the file for this shoe.
    """

    if len(shoe_list) == 0:
        print("Inventory is empty!")
        return

    min_quantity = min(shoe.quantity for shoe in shoe_list)
    shoes_to_restock = []
    for shoe in shoe_list:
        if shoe.quantity == min_quantity:
            shoes_to_restock.append(shoe)

    for shoe in shoes_to_restock:
        print(f"\nQuantity of the shoes --{shoe.product}-- with the code: {shoe.code} left in stock is {shoe.quantity}")
        while True:
            try:
                add_quantity = int((input("Please enter the quantity if you want to restock or \"0\" to skip: \t")))
                break
            except ValueError:
                print("You can enter only whole numbers, please try again")
        if add_quantity > 0:
            shoe.quantity += add_quantity
            print(f"The stock of shoes --{shoe.product}-- with the code: {shoe.code} is now {shoe.quantity}.")

    try:
        with open("inventory.txt", "w", encoding='utf-8') as inventory:
            inventory.write("Country,Code,Product,Cost,Quantity")
            for shoe in shoe_list:
                inventory.write(str(shoe))
    except FileNotFoundError:
        print("File 'inventory.txt' does not exist.")


def search_shoe(search_code):
    """
    This function will search for a shoe from the list
    using the shoe code and return this object so that it will be printed
    """    
    for shoe in shoe_list:
        if search_code == shoe.code:
            return shoe 
        else:
            continue
    return None

def value_per_item():
    """
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    """
    print("\nValue of each item in stock is:\n")
    for shoe in shoe_list:
        value = round((shoe.cost * shoe.quantity), 2)
        print(f"code: {shoe.code} --{shoe.product}--  value: {value}")

def highest_qty():
    """
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    """
    max_qty = max(shoe.quantity for shoe in shoe_list)
    highest_qty_shoes = []
    for shoe in shoe_list:
        if shoe.quantity == max_qty:
            highest_qty_shoes.append(shoe)

    for shoe in highest_qty_shoes:
        print(f"\n{shoe.quantity} pairs of {shoe.product} in {shoe.country} are available for sale!")


#==========Main Menu=============

print("\n---Welcome to the Shoe Warehouse Management System.---")

read_shoes_data()

while True:
    
    print("\nPlease choose from the following options:\n"
    "1 - View all shoes\n"
    "2 - Re-stock lowest quantity shoes\n"
    "3 - Add new shoes to stock\n"
    "4 - Search shoes by code\n"
    "5 - View stock value\n"
    "6 - Put on sale shoes with highest quantity in stock\n"
    "7 - Quit")

    menu = input("\nWhat would you like to do? \t")

    if menu == "1":
        view_all()

    elif menu == "2":
        re_stock()

    elif menu == "3":
        capture_shoes()

    elif menu == "4":
        search_code = input("Enter the code of the shoes you would like to find: \t")
        shoe = search_shoe(search_code)
        if shoe:
            print(str(shoe))
        else:
            print(f"Shoes with the code {search_code} not found!")

    elif menu == "5":
        value_per_item()

    elif menu == "6":
        highest_qty()

    elif menu == "7":
        break

    else:
        print("\nInvalid input. Please enter an option from the menu provided.")