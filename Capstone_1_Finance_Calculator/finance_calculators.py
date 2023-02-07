#import math library
import math

#define variables for the "investment" calculator
#invested amount
invest = 0.00
#investment interest rate
rate = 0.00
#length of investment in years
years = 0.00
#the type of interest
interest = ""
#the amount person will receive from simple investment
sum_sim = 0.00
#the amount person will receive from compound investment
sum_com = 0.00

#define variables for the "bond" calculator
#the value of the house
h_val = 0.00
#the loan interest rate
loan_rate = 0.00
#length of loan in months
months = 0.00
#monthly repayment
pay_per_month = 0.00


print("Choose either \"Investment\" or \"Bond\" from the menu below to proceed: \n")
print("Investment   - to calculate the amount of interest you'll earn on your investment")
print("Bond         - to calculate the amount you'll have to pay on a home loan \n")

#get input from the user which calculator they would like to use and convert to lower case
choice =input().lower()

#if user's choice is investment calculator get additional input for variables and calculate amount of money they will be able to withdraw at the end of investment based on interest type theyhave chosen
if choice == "investment":
    print(f"You have chosen the {choice.capitalize()} calculator. Please answer to the additional questions below.\n")
    invest =+ float(input("What's the amount of money you would like to invest? \t"))
    rate =+ float(input("What's the yearly interest rate in %? \t \t \t"))
    rate = rate / 100
    years =+ float(input("For how many years would you like to invest? \t \t"))
    interest = input("Would you prefer \"simple\" or \"compound\" interest? \t").lower()
    if interest == "simple":
        sum_sim = round((invest * (1 + rate * years)), 2)
        print()
        print(f"After {years} years you will be able to withdraw {sum_sim} GBP and your total earnings on the investment will be {round((sum_sim - invest), 2)} GBP.")
    elif interest == "compound":
        sum_com = round((invest * math.pow((1 + rate), years)), 2)
        print()
        print(f"After {years} years you will be able to withdraw {sum_com} GBP and your total earnings from the investment will be {round((sum_com - invest), 2)} GBP.")
    else:
        print("Invalid input. Please enter either \"simple\" or \"compound\".")

#if user's choice is bond calculator get additional input for variables and calculate amount of money they will be required to repay every month    
elif choice == "bond":
        print(f"You have chosen the {choice.capitalize()} calculator. Please answer to the additional questions below: \n")
        house_val =+ float(input("What's the value of the house in GBP you want to buy? \t"))
        loan_rate =+ float(input("What's the yearly interest rate in %? \t \t \t"))
        months =+ float(input("For how many months would you like to take a loan? \t"))
        loan_rate = loan_rate / 100
        loan_rate = loan_rate / 12
        pay_per_month = round(((loan_rate * house_val) / (1 - (1 + loan_rate) ** ( - months))), 2)
        print()
        print(f"Your monthly payment for the house will be {pay_per_month} GBP.")

#if user inputs wrong value display error message and ask user to try again
else:
    print("You can enter only \"Investment\" or \"Bond\". Please try again! \n")
    