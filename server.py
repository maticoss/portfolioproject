from flask import Flask, render_template, url_for, request, redirect
from PIL import Image
import os, datetime, csv

app = Flask(__name__)

current_time = datetime.datetime.now()


@app.route("/")
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def write_to_csv(data):
    file_empty = os.path.getsize('database.csv') == 0
    with open('database.csv', mode='a', newline='') as database:
        header = ['Email', 'Subject', 'Message', 'Time']
        email = data['email']
        subject = data['subject']
        message = data['message']
        time = current_time
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if file_empty:
            csv_writer.writerow(header)
        csv_writer.writerow([email, subject, message, time])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return redirect('/error.html')
    else:
        return 'Something went wrong'
