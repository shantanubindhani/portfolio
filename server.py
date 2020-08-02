from flask import Flask, render_template, url_for, request, redirect
import csv


app = Flask(__name__)


def save_data(data):
    with open("database.csv", mode='a') as dbs:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]

        csv_writer = csv.writer(dbs, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/')
def home():
    return render_template("./index.html")


@app.route('/<page_name>')
def page(page_name):
    return render_template(f"./{page_name}")


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":

        try:    
            data = request.form.to_dict()
            save_data(data)
            print(data)
            return redirect("/form_submited.html")
        except:
            return "server was unable to get your data, Try again!."
    else:
        return "something went wrong"
