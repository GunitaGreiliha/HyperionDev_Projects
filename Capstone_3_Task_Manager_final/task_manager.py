# ====Task Manager is a program for small businesses to manage tasks assigned to each member of the team==== #

#====Libraries section====

from datetime import datetime

#====Function section====

# Main function of the program to display menu and coordinate functionality. Admin has additional menu options.
def main_menu():
    
    if username == "admin":
        menu = input("""\nPlease select one of the following options:
        r   - Register a new user
        a   - Add a new task
        va  - View all tasks
        vm  - View my task
        gr  - Generate reports
        ds  - Display statistics
        e   - Exit
        : """).lower()

    else:
        menu = input("""\nPlease select one of the following options:
        a   - Add a new task
        va  - View all tasks
        vm  - View my task
        e   - Exit
        : """).lower()


    # This block is used to call a function that allows user to add new users.
    if menu == "r":
        reg_user()
 
    # This block is used to call a function that allows user add a new task.
    elif menu == "a":
        add_task()
        
    # This block is used to call a function that allows user to see all tasks. 
    elif menu == "va":
        view_all()

    # This block is used to call a function that allows user to view and edit tasks assigned to them.
    elif menu == "vm":
        view_mine()

    # This block is used to call a function that allows user to generate reports.
    elif menu == "gr":
        generate_reports()
        
    # This block is used to display statistics.
    elif menu == "ds":
            try:
                display_stats()
            except FileNotFoundError:
                generate_reports()
                display_stats()

    # This block is used to exit the Task Manager.
    elif menu == "e":
        print("\nGoodbye!!!\n")
        exit()

    # This block is used to direct user back to menu options if they enter invalid characters.
    else:
        print("You have made a wrong choice. Please Try again.\n")


# Function to add new users
def reg_user():
    print("\nYou have selected: Register a new user\n")
        
    # If username of current user is admin, create while loop to:
    # request input of a new username, if username already exists, ask user to enter different username,
    # request input of a new password,
    # request input of password confirmation.
    # Check if the new password and confirmed password are the same.
    # If they are the same, add them to the user.txt file and display message that task was successful and break the loop.
    # Otherwise display a message asking user to try again.
    # If username of current user is not admin, display message they are not allowed to add new users
    # and ask to select a different option.
    if username == "admin":
        while True:
            new_username = input("Please enter new user name: \t")
            if not new_username:
                print("Username cannot be empty. Please start again!\n")
                continue
            if new_username in user_library():
                print("\nThis username is already taken. Please start again! \n")
                continue
            new_password = input("Please enter the password: \t")
            if not new_password:
                print("Password cannot be empty. Please start again! \n")
                continue
            conf_password = input("Please confirm the password: \t")
            
            if new_password == conf_password:
                with open("user.txt", "a") as user_file:
                    user_file.write(f"{new_username}, {new_password}\n")
                    print("New user added successfully!\n")
                    break
            else:
                print("Passwords do not match. Please start again.\n")
    else:
        print("Only admin is allowed to add new users. Please select a different option from the menu.\n ")

# Function to create a user dictionary that stores usernames and passwords.
def user_library():
    user_library = {}

    # Open file with user data and read lines to add usernames and passwords to the dictionary.
    # .split method is used to split items in the list by ", ".
    # .strip method is used to remove whitespace from the end of the second item.
    with open("user.txt", "r", encoding='utf-8') as user_file:  
            user_data = user_file.readlines()
            for user in user_data:
                user_library[user.split(", ")[0]] = user.split(", ")[1].strip()
    
    return user_library

# Function to create a task dictionary to store all tasks with a unique key - task number.
def task_library():
    
    task_library = {}
    task_numb = 1
    # Open file tasks.txt and read lines from the file
    # For each line:
    # strip whitespaces and split line where there is comma and space,
    # check if username of the person logged in is the same as username in the line,
    # if yes, add task to the dictionary
    with open("tasks.txt", "r", encoding='utf-8') as task_file:
        task_data = task_file.readlines()
        
        for i, task in enumerate(task_data):
            task = task.strip().split(", ")
            task_library[task_numb] = task
            task_numb += 1                            
    
    return task_library

# Function to get from the user and validate due date for the task.
def get_due_date():
    while True:
        try:
            new_task_due = input("Please enter due date for the task in the following format \"10 Jan 2023\": \n")
            date_format = "%d %b %Y"
            valid_date = datetime.strptime(new_task_due, date_format)
            break
        except ValueError:
            print("Invalid date format. Please enter the date in the correct format.\n")

    return new_task_due

# Function to allow user to add new tasks.
def add_task():
    print("\nYou have selected: Add a new task\n")
       
    # Get user input for the following: 
    # a username of the person whom the task is assigned to,
    # a title of the task,
    # a description of the task and 
    # a due date of the task.
    # Then get the current date and format to required string format for the task file.
    new_task_user = input("Please enter the username of the person responsible for this task: \n")
    new_task_title = input("Please enter the title for the task: \n")
    new_task_desc = input("Please enter description of the task: \n")    
    new_task_due = get_due_date()
    new_task_date = datetime.now().date().strftime("%d %b %Y")
        
    # Add the data to the file task.txt and include "No" at the end to indicate task is not yet completed
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"{new_task_user}, {new_task_title}, {new_task_desc}, {new_task_date}, {new_task_due}, No\n") 
        print("Task successfully added!\n")

# Function that allows user to view all tasks.
def view_all():
    print("\nYou have selected: View all tasks\n")
        
    # Open file tasks.txt and read lines from the file
    # For each line:
    # strip whitespaces and split line where there is comma and space,
    # then print the results in the required user friendly format.  
    with open("tasks.txt", "r", encoding='utf-8') as task_file:
        task_data = task_file.readlines()
        if len(task_data) == 0:
            print("There are no tasks to display!")
        else:
            task_numb = 0    
            for task in task_data:
                task = task.strip().split(", ")
                task_numb += 1
                
                print(f"""
                Nbr:            {task_numb}
                Task:           {task[1]}
                Assigned to:    {task[0]}
                Date assigned:  {task[3]}
                Due date:       {task[4]}
                Task complete?: {task[5]}
                Description:    {task[2]}
                """)

# Function that displays all tasks assigned to the user. 
def print_mine():
    
    with open("tasks.txt", "r", encoding='utf-8') as task_file:
        task_data = task_file.readlines()
        if len(task_data) == 0:
            print("There are no tasks to display!")
        else:
            task_numb = 0    
            for task in task_data:
                task = task.strip().split(", ")
                task_numb += 1
                if task[0] == username:
                    print(f"""
                    Nbr:            {task_numb}
                    Task:           {task[1]}
                    Assigned to:    {task[0]}
                    Date assigned:  {task[3]}
                    Due date:       {task[4]}
                    Task complete?: {task[5]}
                    Description:    {task[2]}
                    """)

# Function that allows user to view and edit their tasks.
def view_mine():
    print("\nYou have selected: View my tasks")
        
    # Call for function print_mine.
    print_mine()
    
    # While loop manage operations based on user input.
    while True:
        tasks = task_library()                    
        try:
            task_nbr = int(input("Enter the task number you would like to edit or \"-1\" to return to main menu: \t"))
            if task_nbr == -1:
                break
        except ValueError:
            print("You haven't entered task number or -1 to exit to main menu, please try again!\n")
            continue
        
        if task_nbr not in tasks:
            print("Invalid task number.")
            continue            
        
        task = tasks[task_nbr] 
        
        if task[5] == "Yes":
            print("Task has already been completed and cannot be edited.\n")
            continue
        
        else:
            print(f"""
--- Selected task ---
Nbr:            {task_nbr}
Task:           {task[1]}
Assigned to:    {task[0]}
Date assigned:  {task[3]}
Due date:       {task[4]}
Task complete?: {task[5]}
Description:    {task[2]}
""")

        # Nested while loop to manage task editing operations based on user selection.
        while True:
            # Display task editing menu.
            action = input("""\nPlease select one of the following options:
                c      - To mark the task complete
                edit   - To edit the task
                e      - To exit the task            
                : """)
            
            # To mark task complete.
            if action.lower() == "c":
                task[5] = "Yes"
                with open("tasks.txt", "w") as task_file:
                    for key, task in tasks.items():
                        task_file.write(f"{task[0]}, {task[1]}, {task[2]}, {task[3]}, {task[4]}, {task[5]}\n")
                print("Task is marked as Complete now.\n")
                break
            
            # To edit task username and task due date.
            elif action.lower() == "edit":
                user_change = input("\nDo you want to reassign the task to a different user? y/n \t")
                
                if user_change.lower() == "y":
                    new_user = input("Enter username of a person you want to reassign this task to: \t")
                    
                    if new_user in user_library():
                        task[0] = new_user
                        with open("tasks.txt", "w") as task_file:
                            for key, task in tasks.items():
                                task_file.write(f"{task[0]}, {task[1]}, {task[2]}, {task[3]}, {task[4]}, {task[5]}\n")
                            print(f"The task has been assigned to {new_user}.")
                                            
                    else:
                        print("User not recognized, please try again.")
                        continue
                
                date_change = input("Do you want to change due date for this task? y/n: \t\t")
                if date_change.lower() == "y":
                    new_date = get_due_date()
                    task[4] = new_date
                    with open("tasks.txt", "w") as task_file:
                        for key, task in tasks.items():
                            task_file.write(f"{task[0]}, {task[1]}, {task[2]}, {task[3]}, {task[4]}, {task[5]}\n")
                    print(f"New task due date is changed to {new_date}.")
                    break
                
                else:
                    continue
            # To exit editing menu
            elif action.lower() == "e":
                break
            else:
                print("Invalid choice. Try again!")
    
# Function that generates task overview report and saves it in the text file.
def task_overview_rep():
    
    tasks = task_library()
    
    completed_tasks = 0
    open_tasks = 0
    overdue_tasks = 0

    for task in tasks.values():
        if task[5] == "Yes":
            completed_tasks += 1
        else:
            open_tasks += 1
    
    for i, task in enumerate(tasks.values()):
        if task[5] == "No":
            new_task_due = datetime.strptime(task[4], "%d %b %Y").date()
            if new_task_due < datetime.today().date():
                overdue_tasks += 1
            
    with open("task_overview.txt", "w+") as task_overview_file:
        task_overview_file.write(f""" 
-----------------------------------------------
TASK OVERVIEW REPORT: {datetime.today().strftime("%d %b %Y")}
        
Total tasks:     {len(tasks)}
Completed:       {completed_tasks}
Open:            {open_tasks}
Overdue:         {overdue_tasks}
% Incomplete:    {round((open_tasks / len(tasks)) * 100)} %
% Overdue:       {round((overdue_tasks / len(tasks)) * 100)} %
        
-----------------------------------------------
""")

# Function that generates first part of user overview report and writes it in the new text file.                   
def user_overview_rep():
    
    tasks = task_library()
    users = user_library()
    
    with open("user_overview.txt", "w+") as user_overview_file:
        user_overview_file.write(f""" 
------------------------------------------------
USER OVERVIEW REPORT: {datetime.today().strftime("%d %b %Y")}
        
Total users:         {len(users)}
Total tasks:         {len(tasks)}
------------------------------------------------

USER DETAILS:
""")
    
    # Empty dictionary to store user stats
    user_stats_dict = {}  
    # For loop to create a nested dictionary containing the stats for each user
    for user in user_library():  
        user_stats_dict[user] = {"Total tasks": 0,
                                 "Completed": 0,
                                 "Open": 0,
                                 "Overdue": 0,
                                 "% Complete": 0,
                                 "% Open": 0,
                                 "% Overdue": 0,
                                 "Percent from all": 0,
                                 }

    for task in tasks.values():  
        # Increment the Total Tasks count for the user.
        user_stats_dict[task[0]]["Total tasks"] += 1  
        # If task is completed, increment Completed count for the user.
        if task[5] == "Yes":  
            user_stats_dict[task[0]]["Completed"] += 1  
        # If task is open, increment Open count for the user.
        elif task[5] == "No":  
            user_stats_dict[task[0]]["Open"] += 1
            new_task_due = datetime.strptime(task[4], "%d %b %Y").date()
            # If this task due date is less than todays date, increment Overdue count.
            if new_task_due < datetime.today().date():
                user_stats_dict[task[0]]["Overdue"] += 1
                         
    # Calculate the percentage of tasks completed, open, and overdue for each user.
    for user in user_stats_dict:  
        total_tasks = user_stats_dict[user]["Total tasks"]
        if total_tasks > 0:  # to avoid ZeroDivision error.
            user_stats_dict[user]["% Complete"] = round((user_stats_dict[user]["Completed"] / total_tasks) * 100)
            user_stats_dict[user]["% Open"] = round((user_stats_dict[user]["Open"] / total_tasks) * 100)
            user_stats_dict[user]["% Overdue"] = round((user_stats_dict[user]["Overdue"] / total_tasks) * 100)

    # Calculate the percentage of user tasks from all tasks. 
    for user in user_stats_dict:
        if len(tasks) > 0:  # to avoid ZeroDivision error.
            user_stats_dict[user]["Percent from all"] = round((user_stats_dict[user]["Total tasks"] / len(tasks)) * 100)


    # For loop for second part of the report to write stats for each user and add to the user overview text file.
    for user in user_stats_dict:  
        with open("user_overview.txt", "a") as user_overview_file:
            user_overview_file.write(f"""

Username: --- {user} ---
        
Total Tasks - % of all tasks:        {user_stats_dict[user]["Total tasks"]} - {user_stats_dict[user]["Percent from all"]} %                
Completed Tasks - % of user tasks:   {user_stats_dict[user]["Completed"]} - {user_stats_dict[user]["% Complete"]} %     
Open Tasks - % of user tasks:        {user_stats_dict[user]["Open"]} - {user_stats_dict[user]["% Open"]} %          
Overdue Tasks - % of user tasks:     {user_stats_dict[user]["Overdue"]} - {user_stats_dict[user]["% Overdue"]} %     
""")

# Function that allows user to generate task overview and user overview reports.
def generate_reports():
    print("\nYou have selected: Generate reports")
    if username == "admin":
        task_overview_rep()
        user_overview_rep()
      
        print(f"\n Reports have been generated, please see text files. \n")
    else:
        print("Only admin is allowed to generate reports. Please select a different option from the menu.\n ")



# Function to display statistics from the generated reports.
def display_stats():
    if username == "admin":
        with open("task_overview.txt", "r", encoding='utf-8') as task_overview_file:
            task_overview = task_overview_file.read()
            print(task_overview)
        
        with open("user_overview.txt", "r", encoding='utf-8') as user_overview_file:
            user_overview = user_overview_file.read()
            print(user_overview)
    else:
        print("Only admin is allowed to display statistics. Please select a different option from the menu.\n ")


#====Login Section====

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

    if username in user_library():
        if user_library()[username] == password:
            logged_in = True
            break
        else:
            print("Incorrect password. Please try again.")
    else:
        print("Invalid username. Please try again.")


# This block is used to call function that displays Main menu if user is logged in.
while logged_in:
    main_menu()
    