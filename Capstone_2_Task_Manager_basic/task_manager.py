
#====Libraries section====

# Import libraries
from datetime import datetime

#====Login Section====

# Create an empty dictionary to store user names as a keys and passwords as a values.
user_library = {}

# Open file with user data and read lines to add usernames and passwords to the dictionary.
# .split method is used to split items in the list by ", ".
# .strip method is used to remove whitespace from the end of the second item.
# [x] is used to indicate location of the item in the list.
with open("user.txt", "r", encoding='utf-8') as user_file:  
        user_data = user_file.readlines()
        for user in user_data:
            user_library[user.split(", ")[0]] = user.split(", ")[1].strip()


# Create boolean for the Login while loop 
logged_in = False


# This block is used to get user's login details and validate user name and password.
while not logged_in:
    
    # Ask for user's input.
    # Check if username is in the user dictionary:
    # if it is and password matches, change boolean value to True and break the loop,
    # if it is, but password doesn't match, display message password is wrong and to try again,
    # if username is not in dictionary, display a message username is invalid and to try again.
    print("\nPlease Login to access Task Manager. \n")
    username = input("Please enter your username: \t")
    password = input("Please enter your password: \t")

    if username in user_library:
        if user_library[username] == password:
            logged_in = True
            break
        else:
            print("Incorrect password. Please try again.")
    else:
        print("Invalid username. Please try again.")



# This block is used to display menu and allow user select options and work with the Task Manager.
while logged_in:
    
    # If user is admin they have additional menu option - display statistics
    if username == "admin":
        menu = input('''\nPlease select one of the following options:
        r - Register a new user
        a - Add a new task
        va - View all tasks
        vm - View my task
        ds - Display statistics
        e - Exit
        : ''').lower()

    # All other users have standard menu options
    else:
        menu = input('''\nPlease select one of the following options:
        r - Register a new user
        a - Add a new task
        va - View all tasks
        vm - View my task
        e - Exit
        : ''').lower()


    # This block is used to allow a user to add new users and their passwords to user.txt file.
    if menu == "r":
        print("\nYou have selected: Register a new user\n")
        
        # If username of current user is admin, create while loop to:
        # request input of a new username,
        # request input of a new password,
        # request input of password confirmation.
        # Check if the new password and confirmed password are the same.
        # If they are the same, add them to the user.txt file and display message that task was successful and break the loop.
        # Otherwise display a message asking user to try again.
        # If username of current user is not admin, display message they are not allowed to add new users
        # and ask to select a different option.
        if username == "admin":
            while True:
                new_username = input("\Please enter new user name: \t")
                new_password = input("Please enter the password: \t")
                conf_password = input("Please confirm the password: \t")
            
                if new_password == conf_password:
                    with open("user.txt", "a") as user_file:
                        user_file.write(f"{new_username}, {new_password}\n")
                        print("New user added successfully!\n")
                        break
                else:
                    print("Passwords do not match. Please try again.\n")
        else:
            print("Only admin is allowed to add new users. Please select a different option from the menu.\n ")


    # This block is used to allow user add a new task to task.txt file.
    elif menu == "a":
        print("\nYou have selected: Add a new task\n")
       
        # Get user input for the following: 
        # a username of the person whom the task is assigned to,
        # a title of the task,
        # a description of the task and 
        # the due date of the task - create while loop to check if date is entered in required format
        # Then get the current date and format to required format for the task file.
        new_task_user = input("Please enter the username of the person responsible for this task: \n")
        new_task_title = input("Please enter the title for the task: \n")
        new_task_desc = input("Please enter description of the task: \n")
        
        while True:
            try:
                new_task_due = input("Please enter due date for the task in the following format \"10 Jan 2023\": \n")
                date_format = "%d %b %Y"
                valid_date = datetime.strptime(new_task_due, date_format)
                break
            except ValueError:
                print("Invalid date format. Please enter the date in the correct format.\n")

        new_task_date = datetime.now().date().strftime("%d %b %Y")
        
        # Add the data to the file task.txt and include "No" at the end to indicate task is not yet completed
        with open("tasks.txt", "a") as task_file:
            task_file.write(f"{new_task_user}, {new_task_title}, {new_task_desc}, {new_task_date}, {new_task_due}, No\n") 
            print("Task successfully added!\n")


    # This block is used to allow user to see all tasks recorded in task.txt file 
    elif menu == "va":
        print("\nYou have selected: View all tasks\n")
        
        # Open file tasks.txt and read lines from the file
        # For each line:
        # strip whitespaces,
        # split line where there is comma and space,
        # then print the results in the required user friendly format.  
        with open("tasks.txt", "r", encoding='utf-8') as task_file:
            task_data = task_file.readlines()
            
            for task in task_data:
                task = task.strip()
                task = task.split(", ")
                
                print(f"Task:\t\t{task[1]}\nAssigned to:\t{task[0]}\n"
                f"Date assigned:\t{task[3]}\nDue date:\t{task[4]}\n"
                f"Task complete?:\t{task[5]}\nDescription:\t{task[2]}\n")


    # This block is used to allow user to see all tasks assigned to them in task.txt file
    elif menu == "vm":
        print("\nYou have selected: View my tasks\n")
        
        # Open file tasks.txt and read lines from the file
        # For each line:
        # strip whitespaces,
        # split line where there is comma and space,
        # check if username of the person logged in is the same as username in the line,
        # if yes, print the results in the required user friendly format.  
        with open("tasks.txt", "r", encoding='utf-8') as task_file:
            task_data = task_file.readlines()
            
            for task in task_data:
                task = task.strip()
                task = task.split(", ")
                
                if username == task[0]:
                    print(f"Task:\t\t{task[1]}\nAssigned to:\t{task[0]}\n"
                    f"Date assigned:\t{task[3]}\nDue date:\t{task[4]}\n"
                    f"Task complete?:\t{task[5]}\nDescription:\t{task[2]}\n")


    # This block is used to display statistics
    elif menu == "ds":
        print("\nYou have selected: Display statistics\n")

        
        # Display total number of users by counting number of lines from user.txt file
        with open("user.txt", "r", encoding='utf-8') as user_file:
            print(f"Total number of users: {len(user_file.readlines())}\n")

        # Display total number of all tasks by counting number of lines from tasks.txt file
        with open("tasks.txt", "r", encoding='utf-8') as task_file:
            print(f"Total number of tasks: {len(task_file.readlines())}\n")


    # This block is used to exit the Task Manager
    elif menu == "e":
        print("\nGoodbye!!!")
        exit()


    # This block is used to direct user back to menu options if they enter invalid characters.
    else:
        print("You have made a wrong choice. Please Try again.")