import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import date

def enter_personal_info():
    print("\n--- Personal Information ----")
    try:
        height = float(input("Height(cm): "))
        weight = float(input("Weight (kg): "))
        target_calories = int(input("Daily Target Calories: "))
    except ValueError:
        print("Invalid input! Please enter only numbers for height, weight, and calories.")
        return

    user_data = {
        "Height_cm": [height],
        "Weight_kg": [weight],
        "Target_Calories": [target_calories]
    }

    df = pd.DataFrame(user_data)
    df.to_csv("user_profile.csv", index=False)
    print("Great! Information successfully saved to user_profile.csv.\n")

def enter_nutrition_data():
    print("\n--- Nutrition(Macro) Data ---")
    date_input = input("Date (DD.MM.YYYY) or press 't' for today: ")
    if date_input.lower() == 't':
        date_input = date.today().strftime("%d.%m.%Y")
    try:
        protein = float(input("Protein(g): "))
        carbs = float(input("Carbonhydrates(g): "))
        fats = float(input("Fats(g): "))
    except ValueError:
        print("Invalid input! Please use numbers.")
        return

    total_calories = (protein * 4) + (carbs * 4) + (fats * 9)
    print(f"Total Calories = {total_calories}")

    nutrition_data = {
        "Date": [date_input],
        "Protein": [protein],
        "Carbs": [carbs],
        "Fats": [fats],
        "Total_Calories": [total_calories]
    }

    file_exists = os.path.isfile("nutrition_log.csv")
    df = pd.DataFrame(nutrition_data)
    df.to_csv("nutrition_log.csv", mode='a', index=False, header=not file_exists)
    print("Great! Nutrition data added to nutrition_log.csv.\n")

def view_nutrition_logs():
    print("\n--- Your Nutrition History ---")
    if os.path.isfile("nutrition_log.csv"):
        df = pd.read_csv("nutrition_log.csv")
        print(df.tail(10))
    else:
        print("No nutrition data found.Start logging first!")

def enter_workout_data():
    print("\n--- Workout Data ---")
    date_input = input("Date (DD.MM.YYYY) or press 't' for today: ")
    if date_input.lower() == 't':
        date_input = date.today().strftime("%d.%m.%Y")
    
    exercise_name = input("Exercise Name (e.g., Hip Thrust, Squat): ")
    try:
        sets = int(input("Sets: "))
        reps = int(input("Reps: "))
        weight = float(input("Weight (kg): "))
    except ValueError:
        print("Invalid input! Please use numbers for sets,reps,weights")
        return

    workout_data = {
        "Date": [date_input],
        "Exercise": [exercise_name],
        "Sets": [sets],
        "Reps": [reps],
        "Weight_kg": [weight]
    }

    df = pd.DataFrame(workout_data)
    file_exists = os.path.isfile("workout_log.csv")
    df.to_csv("workout_log.csv", mode='a', index=False, header=not file_exists)
    print(f"Great! {exercise_name} data added to workout_log.csv.\n")

def view_workout_logs():
    print("\n--- Your Workout History ---")
    if os.path.isfile("workout_log.csv"):
        df = pd.read_csv("workout_log.csv")
        print(df.tail(10))
    else:
        print("No workout data found. Start logging first!")

def plot_calorie_trend():
    print("\n--- Generating Calorie Trend Chart ---")
    if os.path.isfile("nutrition_log.csv"):
        df = pd.read_csv("nutrition_log.csv")
        df.columns = df.columns.str.strip()

        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        else:
            print(f"Hata: 'Date' sütunu bulunamadı. Mevcut sütunlar: {df.columns}")
            return

        last_7_days = df.tail(7)

        plt.figure(figsize=(10,5))
        plt.plot(last_7_days['Date'], last_7_days['Total_Calories'], marker='o', linestyle='-', color='magenta', label='Calories')
        plt.title('Last 7 Days Calories Intake')
        plt.xlabel('Date')
        plt.ylabel('Calories (kcal)')
        plt.grid(True)
        plt.legend()
        print("Closing the chart window will return you to the menu.")
        plt.show()
    else:
        print("Grafik çizilecek veri bulunamadı. Lütfen önce veri girin!")

def main_menu():
    while True:
        print("\n=== GLOW-UP PROJECT ANALYTICS ===")
        print("1. Enter Personal Info")
        print("2. Enter Nutrition (Macro) Data")
        print("3. Enter Workout Data")
        print("4. View Nutrition Logs")
        print("5. View Workout Logs")
        print("6. View Calorie Trend Chart")
        print("7. Exit")
        
        choice = input("Please select an action (1-7): ")
        
        if choice == '1':
            enter_personal_info()
        elif choice == '2':
            enter_nutrition_data()
        elif choice == '3':
            enter_workout_data()
        elif choice == '4':
            view_nutrition_logs()
        elif choice == '5':
            view_workout_logs()
        elif choice == '6':
            plot_calorie_trend()
        elif choice == '7':
            print("Exiting.See you later!")
            break
        else:
            print("Invalid selection, please try again.")

if __name__ == "__main__":
    main_menu()