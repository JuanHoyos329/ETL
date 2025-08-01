from calculator import add, subtract, multiply, divide
from utils import str_to_bool

def main():
    while True:
        print("Welcome to the Calculator App")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")
        choice = input("Choose an operation (1-5): ")

        if choice == "1":
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print("Result:", add(a, b))
        elif choice == "2":
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print("Result:", subtract(a, b))
        elif choice == "3":
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print("Result:", multiply(a, b))
        elif choice == "4":
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
            print("Result:", divide(a, b))
        elif choice == "5":
            print("Are you sure you want to exit? (y/n)")
            confirm = input()
            if (str_to_bool(confirm)):
                print("Exiting...")
                break
            else:
                print("Returning to menu...")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()