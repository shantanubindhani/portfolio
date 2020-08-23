from flask import Flask, render_template, url_for, request, redirect
import csv
import smtplib
import datetime

s = None

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

@app.route('/admin')
def admin():
    return redirect("https://www.pythonanywhere.com")

@app.route('/<page_name>')
def page(page_name):
    return render_template(f"./{page_name}")

def send_alert(data):
    global s
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    my_email = "mail.sender.codewithshan@gmail.com"
    mypwd = "thisiscodewithshan"

    client = data["email"]

    users = ["coder.shantanu@gmail.com", client]

    messages = [f"Someone is trying to contact you shan :\n email : {client}\n subject : {data['subject']}\n message : {data['message']}",
                "Hello this is Shantanu Bindhani, \nTHANK YOU for contacting me, \n I will be contacting you shortly through the G-MAIL :\n coder.shantanu@gmail.com."]

    sub = ["New client.", "Thank You."]

    date = datetime.datetime.now().strftime( "%d|%m|%Y %H:%M" )

    try:
        s.login(my_email, mypwd)
    except:
        print("=======[  Error loging in ....  ]=======")


    def msg(receiver_email_id, subject, message):
        global s
        print(message)
        msg = f"From: BOT <{my_email}>\nTo: {receiver_email_id}\nSubject: {subject}\nDate: {date}\n\n{message}"
        s.sendmail(f"BOT <{my_email}>", receiver_email_id, msg)

    try:
        msg(users[0], sub[0], messages[0])
    except:
        print("error sending message to admin.")
    try:
        msg(users[1], sub[1], messages[1])
    except:
        print("error sending message to client.")

    s.quit()


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":

        try:
            data = request.form.to_dict()
            save_data(data)
            send_alert(data)

            return redirect("/form_submited.html")
        except:
            return "server was unable to get your data, Try again!."
    else:
        return "something went wrong"
