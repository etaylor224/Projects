from flask import Flask, request, render_template, redirect, url_for
from wtforms import Form, StringField, validators
from flask_wtf import FlaskForm
import re
import os
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

app = Flask(__name__)

def google_auth(SCOPES):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def date_grabber(data: str):
    try:
        date_match = re.search(r"\d{1,2}/\d{1,2}/\d{4}", data)
        return date_match.group(0)
    except ValueError:
        return data

def time_grabber(data: str):
    time_match = re.search(r"@*\d{1,2}:\d{2}\s*?(AM|PM|am|pm|Am|Pm)?", data)
    return time_match.group(0).strip().lower()

def date_helper(info: str):
    date = date_grabber(info)
    action = info.split("|")[0]
    if "@" in info:
        time = time_grabber(info).replace("@", "")
    else:
        time = None
    return action, [date, time]

def attendees_helper(emails: str):
    if ";" in emails.strip():
        email_lst = emails.strip().split(";")
    else:
        email_lst = [emails]

    attendees = []

    for entry in email_lst:
        attendees.append({'email': entry.strip()})

    return attendees

def create_google_cal_event(data: dict, address: str, name: str, agent_email: str):
    scope = ['https://www.googleapis.com/auth/calendar']
    creds = google_auth(scope)

    for key in data:
        try:
            date = datetime.strptime(data[key][0], "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            date = data[key][0]

        if len(data[key]) > 1 and data[key][1] != None:
            dt = "T".join(data[key])
            dt_formatted = datetime.strptime(dt, "%m/%d/%YT%I:%M%p").strftime("%Y-%m-%dT%H:%M")

            end_time = (datetime.strptime(dt_formatted, "%Y-%m-%dT%H:%M") + timedelta(minutes=30)).strftime(
                "%Y-%m-%dT%H:%M")
            event = {
                "summary": f"{name} - {key}",
                "description": address,
                "start":
                    {
                        # "dateTime": '2025-03-26T05:00:00-07:00',
                        "dateTime": f"{dt_formatted}:00-05:00",
                        "timeZone": "America/Chicago"
                    },
                "end": {
                    "dateTime": f"{end_time}:00-05:00",
                    "timeZone": "America/Chicago"
                },
                'attendees': attendees_helper(agent_email),
            }
        else:
            event = {
                "summary": "{} - {}".format(name, key),
                "description": address,
                "start":
                    {
                        # "dateTime": '2025-03-26T05:00:00-07:00',
                        "date": f"{date}"
                    },
                "end": {
                    "date": f"{date}"
                },
                'attendees': attendees_helper(agent_email),
            }

        service = build("calendar", "v3", credentials=creds)

        event_create = service.events().insert(calendarId='primary', body=event).execute()

        cal_links = list()
        cal_links.append(event_create.get("htmlLink"))
        #print(f"Created {event_create.get('htmlLink')}")
    return cal_links


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    address = request.form.get('address')
    contract_date = request.form.get('contract_date')
    close_date = request.form.get('close_date')
    email = request.form.get('email')
    buyer_conditions = request.form.getlist('buyer_conditions[]')
    seller_conditions = request.form.getlist('seller_conditions[]')

    print(close_date)

    entries_w_dt = list()

    for entries in buyer_conditions:
        if "@" in entries:
            entries_w_dt.append(entries)

    for entries in seller_conditions:
        if "@" in entries:
            entries_w_dt.append(entries)

    dates_dict = dict()
    for dates in entries_w_dt:
        date_tup = date_helper(dates)
        dates_dict[date_tup[0]] = date_tup[1]

    dates_dict['Contract Date'] = [contract_date]
    dates_dict['Close Date'] = [close_date]
    cal_event = create_google_cal_event(dates_dict, address, name, email)

    return redirect(url_for("index"))

#     return f"""
#         <h1>Submitted!</h1>
#         <p>Name: {name}</p>
#         <p>Address: {address}</p>
#         <p>Contract Date: {contract_date}</p>
#         <p>Close Date: {close_date}</p>
#         <p>Email: {email}</p>
# """

app.run()
