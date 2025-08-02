import csv
from datetime import datetime

FILENAME = "drug_intake_log.csv"

def log_drug_intake():
    print("\n=== Drug Intake Logger ===")
    drug_name = input("Enter drug name: ").strip()
    dosage = input("Enter dosage (e.g., 500 mg): ").strip()
    notes = input("Any notes? (optional): ").strip()
    time_taken = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = [drug_name, dosage, time_taken, notes]

    with open(FILENAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(entry)

    print(f"\n✅ Drug intake for '{drug_name}' logged at {time_taken}.")

def show_log():
    print("\n=== Drug Intake History ===")
    try:
        with open(FILENAME, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(f"🕒 {row[2]} | 💊 {row[0]} | 💉 {row[1]} | 📝 {row[3]}")
    except FileNotFoundError:
        print("No logs found yet.")

def main():
    while True:
        print("\nChoose an option:")
        print("1. Log new drug intake")
        print("2. Show intake history")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            log_drug_intake()
        elif choice == "2":
            show_log()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Please choose 1, 2, or 3.")

if _name_ == "_main_":
    main()
