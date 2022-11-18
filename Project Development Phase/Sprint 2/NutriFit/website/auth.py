from flask import Blueprint, render_template, request, flash, redirect, url_for
import ibm_db
import sendgrid
import os
from sendgrid.helpers.mail import *
from .models import User
from . import connect_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

conn = connect_db()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        sql = "SELECT * FROM USERS WHERE EMAIL = '" + email + "'"
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_assoc(stmt)
        user = User(result['ID'], result['EMAIL'], result['FIRSTNAME'], result['LASTNAME'], result['PASSWORDHASH'], result['DOB'], result['GENDER'], result['HEIGHT'], result['WEIGHT'], result['WEIGHTGOAL'])
        if result:
            if check_password_hash(user.passwordHash, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        dob = request.form.get('dob')
        gender = request.form.get('sex')
        height = request.form.get('height')
        weight = request.form.get('weight')
        weightGoal = request.form.get('weightGoal')
        password1 = request.form.get('password')
        password2 = request.form.get('password2')

        print(email, first_name, last_name, dob, gender, height, weight, weightGoal, password1, password2)
        print(password1, password2)
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Add user to database if email check passes
            sql = "SELECT * FROM USERS WHERE EMAIL = '" + email + "'"
            stmt = ibm_db.exec_immediate(conn, sql)
            result = ibm_db.fetch_assoc(stmt)
            if result:
                flash('Email already exists.', category='error')
            else:
                sql = "INSERT INTO USERS (EMAIL, FIRSTNAME, LASTNAME, PASSWORDHASH, GENDER, DOB, HEIGHT, WEIGHT, WEIGHTGOAL) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                stmt = ibm_db.prepare(conn, sql)
                ibm_db.bind_param(stmt, 1, email)
                ibm_db.bind_param(stmt, 2, first_name)
                ibm_db.bind_param(stmt, 3, last_name)
                ibm_db.bind_param(stmt, 4, generate_password_hash(password1, method='sha256'))
                ibm_db.bind_param(stmt, 5, gender)
                ibm_db.bind_param(stmt, 6, dob)
                ibm_db.bind_param(stmt, 7, height)
                ibm_db.bind_param(stmt, 8, weight)
                ibm_db.bind_param(stmt, 9, weightGoal)
                ibm_db.execute(stmt)
                flash('Account created!', category='success')
                message = Mail(
                    from_email='',
                    to_emails=email,
                    subject='Welcome to NutriFit!',
                    html_content='<strong>Thank you for signing up for NutriFit! We hope you enjoy your experience with us.</strong>')
                try:
                    sg = sendgrid.SendGridAPIClient('')
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print(e.message)
                return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)
