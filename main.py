import json
from datetime import datetime

print("🔍 main.py has started running.")

DATA_FILE = 'data.json'

# Load the data from the JSON file
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"expenses": [], "budgets": {}}

# Save the data back to the JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Add a new expense
def add_expense():
    data = load_data()
    date = input("Enter date (YYYY-MM-DD) [default: today]: ") or datetime.today().strftime('%Y-%m-%d')
    category = input("Enter category (e.g., Food, Transport, Entertainment): ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    }

    data['expenses'].append(expense)
    save_data(data)
    check_budget(data, category)

# Set a monthly budget
def set_budget():
    data = load_data()
    category = input("Enter category: ")
    amount = float(input("Enter monthly budget: "))
    data['budgets'][category] = amount
    save_data(data)
    print(f"✅ Budget set for {category} = ₹{amount}")

# Check if the user exceeded the budget
def check_budget(data, category):
    budget = data['budgets'].get(category)
    if budget is None:
        return

    current_month = datetime.today().strftime('%Y-%m')
    total = sum(
        e['amount'] for e in data['expenses']
        if e['category'] == category and e['date'].startswith(current_month)
    )

    if total > budget:
        print(f"⚠️ ALERT: You have exceeded your budget for {category}!")
    else:
        print(f"✅ {category} spending is within budget.")

# Generate a monthly report
def show_report():
    data = load_data()
    current_month = datetime.today().strftime('%Y-%m')
    print(f"📅 Current month is: {current_month}")  # Debug line
    category_totals = {}

    for expense in data['expenses']:
        print(f"🧾 Found expense: {expense}")  # Debug line
        if expense['date'].startswith(current_month):
            cat = expense['category']
            category_totals[cat] = category_totals.get(cat, 0) + expense['amount']

    print("\n📊 --- Monthly Report ---")
    if not category_totals:
        print("No expenses for this month.")
    else:
        for cat, spent in category_totals.items():
            budget = data['budgets'].get(cat, 0)
            print(f"{cat}: Spent = ₹{spent:.2f}, Budget = ₹{budget:.2f}, Remaining = ₹{budget - spent:.2f}")

# Main menu
def main():
    while True:
        print("\n==== EXPENSE TRACKER ====")
        print("1. Add Expense")
        print("2. Set Budget")
        print("3. Show Report")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            add_expense()
        elif choice == '2':
            set_budget()
        elif choice == '3':
            show_report()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option, try again.")

# Entry point
if __name__ == '__main__':
    main()
