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

def create_google_cal_event(data:dict, address:str, name:str, agent_email:str):

    scope = ['https://www.googleapis.com/auth/calendar']
    creds = google_auth(scope)

    for key in data:
        date = datetime.strptime(data[key][0], "%m/%d/%Y").strftime("%Y-%m-%d")

        if len(data[key]) > 1 and data[key][1] != None:
            dt = "T".join(data[key])
            dt_formatted = datetime.strptime(dt, "%m/%d/%YT%I:%M%p").strftime("%Y-%m-%dT%H:%M")

            end_time = (datetime.strptime(dt_formatted, "%Y-%m-%dT%H:%M") + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M")
            event = {
                "summary": f"{name} - {key}",
                "description": address,
                "start":
                    {
                        #"dateTime": '2025-03-26T05:00:00-07:00',
                        "dateTime": f"{dt_formatted}:00-05:00",
                        "timeZone": "America/Chicago"
                    },
                "end": {
                    "dateTime": f"{end_time}:00-05:00",
                    "timeZone": "America/Chicago"
                    },
                'attendees': [
                    {'email': agent_email},
                ],
            }
        else:
            event = {
                "summary": "{} - {}".format(name, key),
                "description": address,
                "start":
                    {
                        #"dateTime": '2025-03-26T05:00:00-07:00',
                        "date": f"{date}"
                    },
                "end": {
                    "date": f"{date}"
                    },
                'attendees': [
                    {'email': agent_email},
                ],
            }

        service = build("calendar", "v3", credentials=creds)

        event_create = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Created {event_create.get('htmlLink')}")
    return

def scope_change():
    if os.path.exists("token.json"):
        os.remove("token.json")
    return

def date_grabber(data:str):
    date_match = re.search(r"\d{1,2}/\d{1,2}/\d{4}", data)
    return date_match.group(0)

def time_grabber(data:str):
    time_match = re.search(r"@*\d{1,2}:\d{2}\s*?(AM|PM|am|pm|Am|Pm)?", data)
    return time_match.group(0).strip().lower()

def date_helper(info:str):

    date = date_grabber(info)
    action = info.split("|")[0]
    if "@" in info:
        time = time_grabber(info).replace("@", "")
    else:
        time = None
    return action, [date, time]

def main():

    name = input("Enter the agent name how you want them displayed: ")
    address = input("What is the address: ")
    contract_date = input("Enter the contract date: ")
    close_date = input("Enter the close date: ")
    buyer_conditions = input("Enter any and all Buyer Conditions/Contingencies with Deadlines seperated by semicolon (;) use the following"
                        "format EX. 'Deposit/Escrow Deposit | Deadline Date: 3/22/2025 @8:06pm'\n Enter: ")

    seller_conditions = input("Enter any and all Seller Conditions/Contingencies with Deadlines seperated by semicolon (;) use the following"
                        "format EX. 'Closing Date 4/15/2025: This is the date on which the sale will be finalized, and the property will be transferred to the buyer. '\n Enter: ")

    agent_emails = input("Enter any/all emails to receive notification reminders separated by semicolon (;), "
                         "ex. john@email.com;doe@email.com : ")

    entries_w_dt = list()

    if ";" in buyer_conditions:
        buyer_splt = buyer_conditions.split(";")
        buyer_cond = "\n".join(buyer_splt)
    else:
        buyer_cond = buyer_conditions

    if ";" in seller_conditions:
        seller_splt = seller_conditions.split(";")
        seller_cond = "\n".join(seller_splt)
    else:
        seller_cond = seller_conditions

    for entries in buyer_splt:
        if "Deposit/Escrow Deposit" in entries:
            depo_date = date_grabber(entries)
            entries_w_dt.append(entries)
        else:
            if "@" in entries:
                entries_w_dt.append(entries)

    dates_dict = dict()
    for dates in entries_w_dt:
        date_tup = date_helper(dates)
        dates_dict[date_tup[0]] = date_tup[1]

    dates_dict['Contract Date'] = [contract_date]
    dates_dict['Close Date'] = [close_date]
    try:
        create_google_cal_event(dates_dict, address)
    except RefreshError:
        scope_change()
        create_google_cal_event(dates_dict, address, name, agent_emails)

