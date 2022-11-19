from flask import Blueprint, request, redirect, render_template, url_for
from flask_login import login_required, current_user
from . import connect_db
import ibm_db
from .models import User, DailyIntake, Meal
from .extApis import getNutritionData, getFoodName

views = Blueprint('views', __name__)
conn = connect_db()


@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    sql = "SELECT * FROM USERS WHERE ID = '" + str(current_user.id) + "'"
    stmt = ibm_db.exec_immediate(conn, sql)
    result = ibm_db.fetch_assoc(stmt)
    user = User(result['ID'], result['EMAIL'], result['FIRSTNAME'], result['LASTNAME'], result['PASSWORDHASH'], result['DOB'], result['GENDER'], result['HEIGHT'], result['WEIGHT'], result['WEIGHTGOAL'])
    return render_template("dashboard.html", user=user)

@views.route('/add-meal', methods=['GET', 'POST'])
@login_required
def add_meal():
    if request.method == 'POST':
        type = request.form.get('inputtype')
        date = request.form.get('date')
        print(type, date)
        if type == 'foodname':
            foodname = request.form.get('foodname')
            calories, fat, carbs, protein = getNutritionData(foodname)
            sql = "INSERT INTO MEALS (USERID, DATE, MEALNAME, CALORIES, CARBOHYDRATES, PROTEINS, FAT) VALUES ('" + str(current_user.id) + "', '" + str(date) + "', '" + str(foodname) + "', '" + str(calories) + "', '" + str(carbs) + "', '" + str(protein) + "', '" + str(fat) + "')"
            stmt = ibm_db.exec_immediate(conn, sql)
            # create or update daily intake
            sql = "SELECT * FROM DAILYINTAKE WHERE USERID = '" + str(current_user.id) + "' AND DATE = '" + str(date) + "'"
            stmt = ibm_db.exec_immediate(conn, sql)
            result = ibm_db.fetch_assoc(stmt)
            if result:
                # update
                sql = "UPDATE DAILYINTAKE SET CALORIES = CALORIES + '" + str(calories) + "', CARBOHYDRATES = CARBOHYDRATES + '" + str(carbs) + "', PROTEINS = PROTEINS + '" + str(protein) + "', FAT = FAT + '" + str(fat) + "' WHERE USERID = '" + str(current_user.id) + "' AND DATE = '" + str(date) + "'"
                stmt = ibm_db.exec_immediate(conn, sql)
            else:
                # create
                sql = "INSERT INTO DAILYINTAKE (USERID, DATE, CALORIES, CARBOHYDRATES, PROTEINS, FAT) VALUES ('" + str(current_user.id) + "', '" + str(date) + "', '" + str(calories) + "', '" + str(carbs) + "', '" + str(protein) + "', '" + str(fat) + "')"
                stmt = ibm_db.exec_immediate(conn, sql)
            return redirect(url_for('views.reports'))
        elif type == 'image':
            image = request.form.get('image')
            print(image)
            foodname = getFoodName(image)
            calories, fat, carbs, protein = getNutritionData(foodname)
            sql = "INSERT INTO MEALS (USERID, DATE, MEALNAME, CALORIES, CARBOHYDRATES, PROTEINS, FAT) VALUES ('" + str(current_user.id) + "', '" + str(date) + "', '" + str(foodname) + "', '" + str(calories) + "', '" + str(carbs) + "', '" + str(protein) + "', '" + str(fat) + "')"
            stmt = ibm_db.exec_immediate(conn, sql)
            sql = "SELECT * FROM DAILYINTAKE WHERE USERID = '" + str(current_user.id) + "' AND DATE = '" + str(date) + "'"
            stmt = ibm_db.exec_immediate(conn, sql)
            result = ibm_db.fetch_assoc(stmt)
            if result:
                # update
                sql = "UPDATE DAILYINTAKE SET CALORIES = CALORIES + '" + str(calories) + "', CARBOHYDRATES = CARBOHYDRATES + '" + str(carbs) + "', PROTEINS = PROTEINS + '" + str(protein) + "', FAT = FAT + '" + str(fat) + "' WHERE USERID = '" + str(current_user.id) + "' AND DATE = '" + str(date) + "'"
                stmt = ibm_db.exec_immediate(conn, sql)
            else:
                # create
                sql = "INSERT INTO DAILYINTAKE (USERID, DATE, CALORIES, CARBOHYDRATES, PROTEINS, FAT) VALUES ('" + str(current_user.id) + "', '" + str(date) + "', '" + str(calories) + "', '" + str(carbs) + "', '" + str(protein) + "', '" + str(fat) + "')"
                stmt = ibm_db.exec_immediate(conn, sql)
            return redirect(url_for('views.reports'))
    return render_template("add_food.html", user=current_user)

        
@views.route('/add-custom-meal', methods=['GET', 'POST'])
@login_required
def add_custom_meal():
    if request.method == 'POST':
        mealName = request.form.get('name')
        date = request.form.get('date')
        calories = request.form.get('calories')
        carbs = request.form.get('carbs')
        fat = request.form.get('fats')
        protein = request.form.get('proteins')
        print(mealName, calories, carbs, fat, protein)
        sql = "INSERT INTO MEALS (USERID, DATE, MEALNAME, CALORIES, CARBOHYDRATES, PROTEINS, FAT) VALUES ('" + str(current_user.id) + "', '" + str(date) + "', '" + str(mealName) + "', '" + str(calories) + "', '" + str(carbs) + "', '" + str(protein) + "', '" + str(fat) + "')"
        stmt = ibm_db.exec_immediate(conn, sql)

        # create or update daily intake
        sql = "SELECT * FROM DAILYINTAKE WHERE USERID = '" + str(current_user.id) + "' AND DATE = '" + str(date) + "'"
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_assoc(stmt)
        if result:
            # update
            sql = "UPDATE DAILYINTAKE SET CALORIES = CALORIES + '" + str(calories) + "', CARBOHYDRATES = CARBOHYDRATES + '" + str(carbs) + "', PROTEINS = PROTEINS + '" + str(protein) + "', FAT = FAT + '" + str(fat) + "' WHERE USERID = '" + str(current_user.id) + "' AND DATE = '" + str(date) + "'"
            stmt = ibm_db.exec_immediate(conn, sql)
        else:
            # create
            sql = "INSERT INTO DAILYINTAKE (USERID, DATE, CALORIES, CARBOHYDRATES, PROTEINS, FAT) VALUES ('" + str(current_user.id) + "', '" + str(date) + "', '" + str(calories) + "', '" + str(carbs) + "', '" + str(protein) + "', '" + str(fat) + "')"
            stmt = ibm_db.exec_immediate(conn, sql)
        return redirect(url_for('views.reports'))
    return render_template("custom_meals.html", user=current_user)

@views.route('/reports')
@login_required
def reports():
    sql = "SELECT * FROM DAILYINTAKE WHERE USERID = '" + str(current_user.id) + "' ORDER BY DATE DESC FETCH FIRST 10 ROWS ONLY"
    stmt = ibm_db.exec_immediate(conn, sql)
    result = ibm_db.fetch_assoc(stmt)
    reports = []
    while result:
        print(result)
        reports.append(DailyIntake(result['ID'], result['DATE'], result['CALORIES'], result['PROTEINS'], result['CARBOHYDRATES'], result['FAT'], result['USERID']))
        result = ibm_db.fetch_assoc(stmt)
    return render_template("reports.html", user=current_user, reports=reports)

@views.route('/get-day-report')
@login_required
def get_day_report():
    date = request.args.get('date')
    sql = "SELECT * FROM DAILYINTAKE WHERE USERID = '" + str(current_user.id) + "' AND DATE = '" + str(date) + "'"
    stmt = ibm_db.exec_immediate(conn, sql)
    result = ibm_db.fetch_assoc(stmt)
    if result:
        report = DailyIntake(result['ID'], result['DATE'], result['CALORIES'], result['PROTEINS'], result['CARBOHYDRATES'], result['FAT'], result['USERID'])
        sql = "SELECT * FROM MEALS WHERE USERID = '" + str(current_user.id) + "' AND DATE = '" + str(date) + "'"
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_assoc(stmt)
        meals = []
        while result:
            meals.append(Meal(result['ID'], result['USERID'], result['DATE'], result['MEALNAME'], result['CALORIES'], result['CARBOHYDRATES'], result['PROTEINS'], result['FAT']))
            result = ibm_db.fetch_assoc(stmt)
        return render_template("day_report.html", user=current_user, report=report, meals=meals)
    else:
        return render_template("day_report.html", user=current_user)

# @views.route('/daily-intake')
# @login_required
# def daily_intake():
#     # Fetch the user's daily intake over the last 7 days
#     sql = "SELECT * FROM DAILYINTAKE WHERE USERID = '" + str(current_user.id) + "' ORDER BY DATE DESC FETCH FIRST 7 ROWS ONLY"
#     stmt = ibm_db.exec_immediate(conn, sql)
#     result = ibm_db.fetch_assoc(stmt)
#     dailyIntake = []
#     while result:
#         dailyIntake.append(DailyIntake(result['ID'], result['USERID'], result['DATE'], result['CALORIES'], result['CARBS'], result['FAT'], result['PROTEIN']))
#         result = ibm_db.fetch_assoc(stmt)
#     return render_template("daily-intake.html", user=current_user, dailyIntake=dailyIntake)
