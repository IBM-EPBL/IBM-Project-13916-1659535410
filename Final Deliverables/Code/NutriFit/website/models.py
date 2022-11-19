from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin):
    def __init__(self, id, email, first_name, last_name, passwordHash, dob, gender, height, weight, weightGoal):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.gender = gender
        self.height = height
        self.weight = weight
        self.weightGoal = weightGoal
        self.passwordHash = passwordHash

    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_dob(self):
        return self.dob

    def get_gender(self):
        return self.gender

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight

    def get_weightGoal(self):
        return self.weightGoal

    def get_passwordHash(self):
        return self.passwordHash


class DailyIntake():
    def __init__(self, id, date, calories, protein, carbs, fat, userId):
        self.id = id
        self.date = date
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat
        self.userId = userId

    def get_id(self):
        return self.id

    def get_date(self):
        return self.date

    def get_calories(self):
        return self.calories

    def get_protein(self):
        return self.protein

    def get_carbs(self):
        return self.carbs

    def get_fat(self):
        return self.fat

    def get_userId(self):
        return self.userId

class Meal():
    def __init__(self, id, userId, date, mealName, calories, carbs, protein, fat):
        self.id = id
        self.mealName = mealName
        self.userId = userId
        self.date = date
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat

    def get_id(self):
        return self.id

    def get_date(self):
        return self.date

    def get_mealName(self):
        return self.mealName

    def get_calories(self):
        return self.calories

    def get_protein(self):
        return self.protein

    def get_carbs(self):
        return self.carbs

    def get_fat(self):
        return self.fat

    def get_userId(self):
        return self.userId

    def getString(self):
        return self.mealName + " " + str(self.calories) + " " + str(self.carbs) + " " + str(self.protein) + " " + str(self.fat)