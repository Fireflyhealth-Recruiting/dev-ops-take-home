from datetime import date

import jsonrpclib
from flask import Flask, redirect, render_template, request, session, url_for
from markupsafe import escape

app = Flask(__name__)

client = jsonrpclib.ServerProxy('http://0.0.0.0:8000/api')


@app.template_filter('date_to_string')
def timestamp_to_datetime(datestring):
    return date.fromisoformat(datestring).strftime('%a, %B %-d, %Y')


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    params = dict(request.form)
    action = params.pop('action', None)
    owner = params.pop('owner', '')
    notes = params.pop('notes', None)
    admin = bool(params.pop('admin', False))
    appointments = []
    error = None

    try:
        if action == 'create-appointment':
            client.appointments.register(
                datestring=params['date'], owner=owner, notes=notes)
    except jsonrpclib.AppError as e:
        error = e.args[0][1]

    try:
        appointments = client.appointments.list()
        if not admin:
            appointments = [
                appointment for appointment in appointments if appointment['owner'] == owner]

        if action == 'cancel-appointments':
            remove = []
            for i, appointment in enumerate(appointments):
                if params.get(str(appointment['date'])) == 'on':
                    if admin or appointment['owner'] == owner:
                        client.appointments.cancel(appointment['date'])
                        remove.append(i)
            for i in reversed(remove):
                appointments.pop(i)
    except jsonrpclib.AppError as e:
        error = e.args[0][1]

    return render_template(
        "index.html",
        appointments=appointments,
        admin=admin,
        owner=owner,
        error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
