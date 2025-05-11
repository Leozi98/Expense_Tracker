import json
import csv
from datetime import datetime

# Configuration
PREDEFINED_CATEGORIES = ['Food', 'Transportation', 'Entertainment', 'Shopping', 'Health', 'Education', 'Other']
BUDGET_FILE = 'budgets.json'

def load_expenses():
    try:
        with open('expenses.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open('expenses.json', 'w') as file:
        json.dump(expenses, file, indent=4)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def add_expense(expenses):
    print("\nSelect Category:")
    for i, category in enumerate(PREDEFINED_CATEGORIES, 1):
        print(f"{i}. {category}")
    
    while True:
        try:
            cat_choice = int(input("Choose category (1-7): "))
            if 1 <= cat_choice <= len(PREDEFINED_CATEGORIES):
                category = PREDEFINED_CATEGORIES[cat_choice-1]
                if category == 'Other':
                    category = input("Enter custom category: ").strip()
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a number!")

    name = input("Expense Name: ").strip()
    
    while True:
        amount = input("Amount (e.g., 50.00): ").strip()
        try:
            amount = float(amount)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    date_str = input("Date (YYYY-MM-DD) [blank for today]: ").strip()
    date = datetime.today().strftime('%Y-%m-%d') if not date_str else date_str
    
    expenses.append({
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    })
    save_expenses(expenses)
    print("✔️ Expense added successfully!")

def delete_expense(expenses):
    if not expenses:
        print("❌ No expenses found")
        return
    
    print("\nExpense List:")
    for i, expense in enumerate(expenses, 1):
        print(f"{i}. {expense['name']} - ${expense['amount']} ({expense['category']})")
    
    while True:
        try:
            choice = int(input("\nEnter number to delete: ")) - 1
            if 0 <= choice < len(expenses):
                deleted = expenses.pop(choice)
                save_expenses(expenses)
                print(f"✔️ '{deleted['name']}' deleted successfully")
                break
            else:
                print("Invalid number")
        except ValueError:
            print("Please enter a valid number")

def update_expense(expenses):
    if not expenses:
        print("📭 No expense records")
        return
    
    view_expenses(expenses)
    
    while True:
        try:
            choice = int(input("\nEnter number to update: ")) - 1
            if 0 <= choice < len(expenses):
                expense = expenses[choice]
                
                # Update name
                new_name = input(f"New name [{expense['name']}]: ").strip()
                if new_name: expense['name'] = new_name
                
                # Update amount
                new_amount = input(f"New amount [{expense['amount']}]: ").strip()
                if new_amount:
                    while True:
                        try:
                            expense['amount'] = float(new_amount)
                            break
                        except ValueError:
                            new_amount = input("Invalid input. Enter number: ").strip()
                
                # Update category
                new_category = input(f"New category [{expense['category']}]: ").strip()
                if new_category: expense['category'] = new_category
                
                # Update date
                new_date = input(f"New date (YYYY-MM-DD) [{expense['date']}]: ").strip()
                if new_date:
                    while not validate_date(new_date):
                        print("Invalid date format!")
                        new_date = input("Enter date (YYYY-MM-DD): ").strip()
                    expense['date'] = new_date
                
                save_expenses(expenses)
                print("✔️ Expense updated successfully!")
                break
            
            else: print("Invalid number!")
        except ValueError:
            print("Please enter a valid number!")

def view_expenses(expenses, category_filter=None):
    filtered = expenses if not category_filter else [
        e for e in expenses if e['category'] == category_filter
    ]
    
    if not filtered:
        print("📭 No records found")
        return
    
    print("\n📋 Expense Records:")
    for idx, expense in enumerate(filtered, 1):
        print(f"{idx}. {expense['date']} | {expense['category']:15} | {expense['name']:20} | ${expense['amount']:10.2f}")

def filter_by_category(expenses):
    print("\nAvailable Categories:")
    categories = sorted(set([e['category'] for e in expenses]))
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    try:
        choice = int(input("Select category: ")) - 1
        if 0 <= choice < len(categories):
            view_expenses(expenses, category_filter=categories[choice])
        else:
            print("Invalid selection!")
    except ValueError:
        print("Invalid input!")

def set_budget():
    budgets = load_budgets()
    
    year = input(f"Enter year (default {datetime.now().year}): ").strip() or str(datetime.now().year)
    month = input("Enter month (1-12): ").strip()
    
    try:
        month_key = f"{year}-{int(month):02d}"
        amount = float(input("Enter budget amount: "))
        budgets[month_key] = amount
        save_budgets(budgets)
        print("✔️ Budget set successfully!")
    except (ValueError, KeyError):
        print("Invalid input!")

def check_budget(expenses, month, year):
    budgets = load_budgets()
    month_key = f"{year}-{month:02d}"
    budget = budgets.get(month_key)
    
    if not budget:
        return
    
    total = sum(e['amount'] for e in expenses 
              if datetime.strptime(e['date'], '%Y-%m-%d').month == month
              and datetime.strptime(e['date'], '%Y-%m-%d').year == year)
    
    if total > budget:
        print(f"\n⚠️ WARNING: Current month's expenses ({month}/{year})")
        print(f"Total: ${total:.2f} | Budget: ${budget:.2f}")
        print(f"Overspending: ${total - budget:.2f}")

def export_to_csv(expenses):
    filename = f"expenses_export_{datetime.now().strftime('%Y%m%d%H%M')}.csv"
    
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'category', 'name', 'amount'])
        writer.writeheader()
        writer.writerows(expenses)
    
    print(f"✔️ Data exported to {filename}")

def main():
    expenses = load_expenses()
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. Delete Expense")
        print("3. Update Expense")
        print("4. View All Expenses")
        print("5. Filter by Category")
        print("6. Set Monthly Budget")
        print("7. Show Total Summary")
        print("8. Show Monthly Summary")
        print("9. Export to CSV")
        print("0. Exit")
        
        choice = input("Select option: ")
        
        if choice == '1':
            add_expense(expenses)
            current_date = datetime.now()
            check_budget(expenses, current_date.month, current_date.year)
        elif choice == '2':
            delete_expense(expenses)
        elif choice == '3':
            update_expense(expenses)
        elif choice == '4':
            view_expenses(expenses)
        elif choice == '5':
            filter_by_category(expenses)
        elif choice == '6':
            set_budget()
        elif choice == '7':
            show_summary(expenses)
        elif choice == '8':
            show_monthly_summary(expenses)
        elif choice == '9':
            export_to_csv(expenses)
        elif choice == '0':
            print("👋 Goodbye!")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()