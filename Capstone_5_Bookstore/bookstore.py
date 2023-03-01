""" Bookstore Management System"""

"""Libraries Section"""
import sqlite3
from tabulate import tabulate

"""Function Section"""
# Function that creates database and table with the initial books. 
def create_database():
    
    try:
        # Connect to the database.
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()

        # Create the books table if it doesn't exist.
        cursor.execute('''CREATE TABLE IF NOT EXISTS books
                    (id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)''')
        
        # Check if the table is empty.
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        
        if len(books) == 0:
            # Insert initial book data into database.
            books = [
                (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
                (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
                (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25),
                (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
                ]

            cursor.executemany("INSERT INTO books VALUES (?, ?, ?, ?)", books)
            print("\nBook database created successfully!")    
        else:
            print("\nBook database already exists.")
            pass
        
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")

    finally:
        cursor.close()
        conn.close()

# Function to display the main menu.
def display_menu():
    print("\nOperations available from the menu below:")
    print("DB - Create database")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit")


# Function to add a new book into the database.
def add_book():
    # Prompt and validate user input.
    try:        
        title = input("Enter the book's title: ")
        author = input("Enter the book's author: ")
        while True:
            try:
                qty = int(input("Enter the quantity of the books: "))
                break
            except ValueError:
                print("Quantity must be a number.")
            
        # Insert the new book into the database.
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, qty) VALUES (?, ?, ?)", (title, author, qty))
        conn.commit()

        # Retrieve last entry from database and display confirmation message.
        cursor.execute("SELECT * FROM books WHERE ID = (SELECT LAST_INSERT_ROWID())")
        result = cursor.fetchall()
        print("\nBook successfully added to the database.")
        print(tabulate(result, headers=["Id", "Title", "Author", "Qty"], tablefmt="fancy_grid"))
            
    except sqlite3.Error as e:
        print("Error inserting book:", e)
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()


# Function to update book information.
def update_book():
    # Prompt the user for the book ID and validate it.
    while True:
        try:
            book_id = int(input("Enter the ID of the book to update or '0' to exit: "))
            if book_id == 0:
                return
            else:
                conn = sqlite3.connect("bookstore.db")
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM books")
                book_ids = [row[0] for row in cursor.fetchall()]
                if book_id not in book_ids:
                    print("Book ID not found in the database.")                
                else:
                    break
        
        except sqlite3.Error as e:
            print("Error reading book information from the database:", e)
            return
   
    
    # Prompt the user for the field to update and validate it.
    while True:
        field = input("Enter the field to update (title, author, or qty): ").lower()
        if field not in ['title', 'author', 'qty']:
            print("Invalid field name. Please enter 'title', 'author', or 'qty'.")
        else:
            break
            
    # Prompt the user to input new value and validate it.
    while True:
        try:
            if field == "qty":
                new_value = int(input(f"Enter the new {field}: "))
            else:
                new_value = input(f"Enter the new {field}: ")
            break
        except ValueError:
            print("Invalid input. Please enter a number for the quantity.")
    
    # Update the book in the database.
    try:
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE books SET {field.title()} = ? WHERE id = ?", (new_value, book_id))
        conn.commit()
        # Retrieve updated entry from database and display confirmation message.
        cursor.execute("SELECT * FROM books WHERE ID = ?", (book_id,))
        result = cursor.fetchall()
        print("\nBook updated successfully.")
        print(tabulate(result, headers=["Id", "Title", "Author", "Qty"], tablefmt="fancy_grid"))
        

    except sqlite3.Error as e:
        print("Error updating book:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


# Function to delete a book from the database.
def delete_book():
    
    # Prompt the user for the book ID and validate it.
    while True:
        try:
            book_id = int(input("Enter the ID of the book to delete or '0' to Exit: "))
            if book_id == 0:
                return
            else:
                conn = sqlite3.connect("bookstore.db")
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM books")
                book_ids = [row[0] for row in cursor.fetchall()]
                if book_id not in book_ids:
                    print("Book ID not found in the database.")
                else:
                    break

        except sqlite3.Error as e:
            print("Error reading book information from the database:", e)
            return
        except ValueError as e:
            print(f" You've entered '{str(e)}'. Please enter a valid book ID.")
    
    # Delete the book from the database.
    try:
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        # Retrieve book entry from database used for confirmation message later.
        cursor.execute("SELECT * FROM books WHERE ID = ?", (book_id,))
        result = cursor.fetchall()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        print("\nBook deleted successfully.")
        print(tabulate(result, headers=["Id", "Title", "Author", "Qty"], tablefmt="fancy_grid"))
    
    except sqlite3.Error as e:
        print("Error deleting the book:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Function to search for a specific book.
def search_books():
    # Prompt the user for the search term.
    search_term = input("Enter a book title or author name to search for or '0' to exit: ")
    if search_term == "0":
        return

    try:
        # Search the database for matching books.
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE Title LIKE ? OR Author LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
        results = cursor.fetchall()

        # Print the matching books.
        if len(results) > 0:
            print("\nMatching books:")
            print(tabulate(results, headers=["Id", "Title", "Author", "Qty"], tablefmt="fancy_grid"))
        else:
            print("No matching books found.")
       
    except sqlite3.Error as e:
        print("Database error:", e)
    
    finally:
        cursor.close()
        conn.close()


"""Main program"""

print("\n ---- Welcome to the Bookstore management system! ----")
while True:
    display_menu()
    choice = input("\nEnter your choice: ")
    if choice == "DB":
        create_database()
    elif choice == "1":
        add_book()
    elif choice == "2":
        update_book()       
    elif choice == "3":
        delete_book()
    elif choice == "4":
        search_books()
    elif choice == "0":
        print("\n Thank you and see you next time!")
        break
    else:
        print("\nInvalid choice. Please try again.")


