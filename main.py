import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

DATA_FILE = "health_data.csv"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_data(data):
    with open(DATA_FILE, mode="w", newline="") as file:
        fieldnames = ['Date', 'Steps', 'Sleep', 'Calories', 'Water']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def add_daily_entry():
    date = input("Enter date (YYYY-MM-DD): ")
    steps = int(input("Enter steps walked: "))
    sleep = float(input("Enter sleep hours: "))
    calories = int(input("Enter calories consumed: "))
    water = float(input("Enter water intake (in liters): "))

    entry = {
        'Date': date,
        'Steps': steps,
        'Sleep': sleep,
        'Calories': calories,
        'Water': water
    }

    data = load_data()
    data.append(entry)
    save_data(data)
    print("Data saved.")

def show_full_data():
    data = load_data()
    if not data:
        print("No records found.")
        return

    for entry in data:
        print(entry)

def calculate_stats(group_by):
    data = load_data()
    grouped = defaultdict(lambda: {'Steps': 0, 'Sleep': 0.0, 'Calories': 0, 'Water': 0.0, 'Count': 0})

    for entry in data:
        date_obj = datetime.strptime(entry['Date'], "%Y-%m-%d")
        if group_by == 'week':
            key = date_obj.strftime("%Y-W%U")
        elif group_by == 'month':
            key = date_obj.strftime("%Y-%m")
        else:
            key = entry['Date']

        grouped[key]['Steps'] += int(entry['Steps'])
        grouped[key]['Sleep'] += float(entry['Sleep'])
        grouped[key]['Calories'] += int(entry['Calories'])
        grouped[key]['Water'] += float(entry['Water'])
        grouped[key]['Count'] += 1

    return grouped

def plot_goals_chart():
    print("Choose timeframe: day / week / month")
    choice = input("Enter choice: ").lower()
    if choice not in ('day', 'week', 'month'):
        print("Invalid choice.")
        return

    stats = calculate_stats(choice)
    labels = []
    avg_steps = []
    avg_sleep = []
    avg_water = []

    for period, data in sorted(stats.items()):
        labels.append(period)
        count = data['Count']
        avg_steps.append(data['Steps'] // count)
        avg_sleep.append(data['Sleep'] / count)
        avg_water.append(data['Water'] / count)

    plt.figure(figsize=(10, 6))
    plt.plot(labels, avg_steps, label='Avg Steps', marker='o')
    plt.plot(labels, avg_sleep, label='Avg Sleep (hrs)', marker='s')
    plt.plot(labels, avg_water, label='Avg Water (L)', marker='^')
    plt.title(f"Health Goals - {choice.capitalize()}ly")
    plt.xlabel(f"{choice.capitalize()}s")
    plt.xticks(rotation=45)
    plt.ylabel("Averages")
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    while True:
        print("\nHealth & Fitness Tracker")
        print("1. Add Daily Health Data")
        print("2. View All Records")
        print("3. Plot Goals Chart (Day/Week/Month)")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_daily_entry()
        elif choice == '2':
            show_full_data()
        elif choice == '3':
            plot_goals_chart()
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()