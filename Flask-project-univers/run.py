from flask import Flask, render_template, request, url_for, redirect
import csv
import random
import datetime
app = Flask(__name__)


def make_bold(function):
    def wrapper_function():
        return f"<b>{function()}</b>"

    return wrapper_function


@app.route("/")
# @make_bold
# def my_home():
#     return '<p>My paragraph</p>' \
#            '<p>Another paragraph</p>'

# hit enter outside p tag
def my_home():
    random_number = random.randint(1,9)
    return render_template('index.html', num =random_number)

@app.route("/<int:number>")
def go_to_specific(number):
    return render_template("specific.html")

@app.route("/<string:page_name>")
def my_project(page_name):
    year=datetime.datetime.now().year
    company="Acoptex.lt"
    return render_template(page_name,company_name=company,current_year=year)


def write_to_txt_file(data):
    with open('database.txt', mode='a') as database:
        full_name = data['full-name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{full_name},{email},{subject},{message}')


def write_to_csv_file(data):
    with open('database.csv', mode='a', newline="") as database2:
        full_name = data['full-name']
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([full_name, email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            name = data['full-name'].upper()
            # write_to_txt_file(data)
            write_to_csv_file(data)
            # print(data)
            return render_template('/thank-you.html', name=name)
        except:
            return 'did not save to database'
    else:
        return 'something went wrong. try again'
