import datetime
import difflib
import json
import os

import pandas as pd
from termcolor import colored

from DataStructures import HashMap, Linked_List, Stack


class CalorieCounter:
    food_database_filename = "C:\\Users\\TAKIKIDA\\Downloads\\programming\\food_database.xlsx"
    exercise_database_filename = "C:\\Users\\TAKIKIDA\\Downloads\\programming\\exercise_database_main.xlsx"

    def __init__(self, calories_limit, calories_consumed, foods_consumed, calorie_history):
        self.foods_stack = Stack.Stack()
        self.foods_eaten_so_far = Linked_List.Linked_List("Foods")
        self.food_list = []
        self.food_database = HashMap.HashTable()  # Food ->  (Category, Calories)
        self.exercise_list = []
        self.exercise_database = HashMap.HashTable()  # Exercise -> Calories/m
        self.calories_limit = calories_limit
        self.calories_consumed = calories_consumed
        self.calorie_history = calorie_history

        self.copy_food_history(foods_consumed)
        self.read_database_info()

    def read_database_info(self):
        food_excel = pd.read_excel(self.food_database_filename)
        for _, row in food_excel.iterrows():
            self.food_list.append(row[2])
            self.food_database.add(row[2], (row[1], float(row[3])))

        exercise_excel = pd.read_excel(self.exercise_database_filename)
        for _, row in exercise_excel.iterrows():
            self.exercise_list.append(row[1])
            self.exercise_database.add(row[1], row[2])

    def copy_food_history(self, foods_eaten):
        for food in foods_eaten:
            self.foods_eaten_so_far.add(food)
            self.foods_stack.push(food)

    def get_calories_consumed(self):
        return self.calories_consumed

    def get_calories_history(self):
        return self.calorie_history

    def show_foods_eaten(self):
        if self.foods_eaten_so_far.size():
            print("You have eaten the following foods: ")
            self.foods_eaten_so_far.display()

    def print_date_used_calories(self, date_input):
        date = date_input[5:]
        if date in self.calorie_history:
            print("In %s you have used %s calories" % (date, self.calorie_history[date][0]))
        else:
            print("There is no data for current date")

    def record_food_eaten(self, food):
        self.foods_eaten_so_far.add(food)
        self.foods_stack.push(food)

    def find_food(self, text):
        food_name = text[5:]
        print(food_name)
        match_result = difflib.get_close_matches(food_name, self.food_list)
        if not match_result:
            print("Food not found, try to write another food name")
            return

        for item in range(len(match_result)):
            print('* For %s type %i' % (match_result[item], item))
        try:
            food = match_result[int(input())]
        except ValueError:
            print("Not a valid input, try again")
            return
        (_, calories) = self.food_database.get(food)
        self.calories_consumed += calories
        self.record_food_eaten(food)
        print("Your food was %f calories" % calories)

        if self.calories_consumed > self.calories_limit:
            print("You have passed your daily limit by %i" % (self.calories_consumed - self.calories_limit))
        else:
            print("You have %i calories left" % (self.calories_limit - self.calories_consumed))

    def exercise_calories(self, text):
        exercise_type = text[8:]
        print(exercise_type)
        match_result = difflib.get_close_matches(exercise_type, self.exercise_list)
        if (not match_result):
            print("Exercise not found, try to write another exercise name")
            return

        for item in range(len(match_result)):
            print('* For %s type %i' % (match_result[item], item))
        exercise = match_result[int(input())]
        exercise_time = int(input("Exercise Time in minutes: "))
        calories_burned = float(self.exercise_database.get(exercise)) * exercise_time
        print('you have burnt %f calories' % calories_burned)
        self.calories_consumed -= calories_burned

    def save_data(self):
        date = datetime.datetime.today().date().isoformat()
        foods_list = []
        while not self.foods_stack.empty():
            foods_list.append(self.foods_stack.pop())
        self.calorie_history[date] = (self.calories_consumed, foods_list)


def read_user_data():
    while True:
        try:
            weight = int(input("Enter your weight(in kg): "))
            if weight > 150:
                raise ValueError
            else:
                break
        except ValueError:
            print("Please, enter correct values!")
    while True:
        try:
            height = int(input("Enter your height(in cm): "))
            if height > 250:
                raise ValueError
            else:
                break
        except ValueError:
            print("Please, enter correct values!")
    while True:
        try:
            age = int(input("Enter your age(in years): "))
            if age > 120:
                raise ValueError
            else:
                break
        except ValueError:
            print("Please, enter correct values!")
    while True:
        gender = input("Male or Female? ")
        if gender.lower() == 'male':
            BMR1 = (10 * weight) + (6.25 * height) - (5 * age) + 5
            break
        elif gender.lower() == 'female':
            BMR1 = (10 * weight) + (6.25 * height) - (5 * age) - 161
            break
        else:
            print("Please, enter correct values!")
    while True:
        activity_status = input('''Please choose one of the options
                                   \r\tEnter '1' if sedentary (little or no exercise)
                                   \r\tEnter '2' if lightly active (light exercise/sports 1-3 days/week)
                                   \r\tEnter '3' if moderately active (moderate exercise/sports 3-5 days/week)
                                   \r\tEnter '4' if active (hard exercise/sports 6-7 days a week)
                                   \r\tEnter '5' if extra active (very hard exercise/sports & physical job or 2x training)
                                   \r\t> ''')
        if activity_status == "1":
            BMR2 = BMR1 * 1.2
            break
        elif activity_status == "2":
            BMR2 = BMR1 * 1.375
            break
        elif activity_status == '3':
            BMR2 = BMR1 * 1.55
            break
        elif activity_status == '4':
            BMR2 = BMR1 * 1.725
            break
        elif activity_status == '5':
            BMR2 = BMR1 * 1.9
            break
        else:
            print("Please, enter correct values!")
    while True:
        goals = input('''Please, choose one of the following options: I want to
                         \rEnter '1' if you want to loose weight,
                         \rEnter '2' if you want to maintain my weight,
                         \rEnter '3' if you want to gain weight
                         \r> ''')
        if goals == '1':
            BMR2 -= 500
            break
        if goals == '2':
            BMR2 = BMR1
            break
        if goals == '3':
            BMR2 += 500
            break
        else:
            print("Please, enter correct values!")
    print("So, this is the amount of calories you shall take to reach your goal: " + str(BMR2))
    user_initial_info = {
        'weight': weight,
        'height': height,
        'age': age,
        'gender': gender,
        'calories_limit': BMR2}
    with open("user_data.json", "w+") as Writefile:
        json.dump(user_initial_info, Writefile, indent=True)
    return BMR2


def exit_app(calories_history):
    with open("daily_calories.json", "w+") as WRITE_FILE:
        json.dump(calories_history, WRITE_FILE, indent=True)
    exit(colored("Bye", 'blue'))


def main():
    print("Hello, this is the app to calculate your calories ")

    ## Read or ask for daily calorie limit
    calories_limit = 0
    if not os.path.exists("user_data.json"):
        print("Please input the following information... ")
        calories_limit = read_user_data()
    else:
        with open("user_data.json", "r") as read_file:
            calories_limit = float(json.loads(read_file.read())["calories_limit"])

    ## Read already consumed calories
    calorie_history = {}
    if not os.path.exists("daily_calories.json"):
        with open("daily_calories.json", 'w') as write_file:
            json.dump(calorie_history, write_file)
    else:
        with open("daily_calories.json", "r") as read_file:
            calorie_history = json.loads(read_file.read())

    calories_consumed = 0
    foods_consumed = []
    for (date, food_info) in calorie_history.items():
        if date == datetime.datetime.today().date().isoformat():
            calories_consumed = food_info[0]
            foods_consumed = food_info[1]
            break

    calorie_counter = CalorieCounter(calories_limit, calories_consumed, foods_consumed, calorie_history)

    print("""Available Commands:
                  \r1. Type "food " + name to add a food you ate.
                  \r2. Type "calories" to view your calories.
                  \r3. Type "date yyyy-dd-mm" to view your calories at particular date.
                  \r4. Type "workout " +  name of the exercise to view your calories burnt during exercising
                  \r5. Type "exit" to exit the app.
                      """)

    while True:
        print(colored("Enter command", 'blue'))
        # print("Enter command")
        text = input("> ")
        if text == "exit":
            calorie_counter.save_data()
            exit_app(calorie_counter.get_calories_history())
        elif "date" in text:
            calorie_counter.print_date_used_calories(text)
            continue
        elif text == "calories":
            print("Today you have consumed %i calories" % calorie_counter.get_calories_consumed())
            calorie_counter.show_foods_eaten()
            continue
        elif "workout" in text:
            calorie_counter.exercise_calories(text)
            continue
        else:
            calorie_counter.find_food(text)


main()
