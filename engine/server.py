import crypt
from collections import namedtuple
from datetime import date, timedelta
from random import sample

from flask import Flask
from flask_jsonrpc import JSONRPC
from flask_jsonrpc.exceptions import OtherError

app = Flask(__name__)
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)

Appointment = namedtuple("Appointment", ("date", "owner", "notes"))


def initialize_appointments(n=5):
    today = date.today()
    appointments = {}
    for offset in sample(range(n*4), n):
        appt_date = today + timedelta(days=offset)
        appt = Appointment(
            owner='hodor',
            date=appt_date.isoformat(),
            notes=None
        )
        appointments[appt.date] = appt
    return appointments

APPOINTMENTS = initialize_appointments()

@jsonrpc.method("appointments.register")
def register_appointment(datestring, owner, notes=None):
    date.fromisoformat(datestring)
    if datestring in APPOINTMENTS:
        raise ValueError("This time is already taken")
    appointment = Appointment(date=datestring, owner=owner, notes=notes)
    APPOINTMENTS[datestring] = appointment
    return appointment._asdict()


@jsonrpc.method("appointments.list")
def list_appointments():
    return [appointment._asdict()
            for appointment in sorted(APPOINTMENTS.values())]


@jsonrpc.method("appointments.cancel")
def cancel_appointment(datestring):
    date.fromisoformat(datestring)
    if datestring not in APPOINTMENTS:
        raise ValueError("Appointment does not exist!")
    del APPOINTMENTS[datestring]
    return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
