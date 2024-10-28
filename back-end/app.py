import requests
import base64
from flask import Flask, request, jsonify
import webbrowser
import os
from dotenv import load_dotenv

load_dotenv()

# Microsoft Graph API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = 'common'
SCOPE = 'Calendars.ReadWrite offline_access'
REDIRECT_URI = 'http://localhost:5001/getToken'
CLIENT_ID = os.getenv("CLIENT_ID")

# Companies House API credentials
input_company = input('Company House No: ')
company_number = input_company
api_key = os.getenv("API_KEY")
encoded_api_key = base64.b64encode(f"{api_key}:".encode()).decode()

# Flask app initialization
app = Flask(__name__)

# Authorization URL for Microsoft login
def get_authorization_code():
    auth_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'response_mode': 'query',
        'scope': SCOPE
    }
    webbrowser.open(f"{auth_url}?{requests.compat.urlencode(params)}")

# Exchange authorization code for access token
def get_access_token(authorization_code):
    token_url = f'https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token'
    token_data = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'scope': SCOPE
    }
    token_response = requests.post(token_url, data=token_data)
    return token_response.json().get('access_token')

# Create events using Microsoft Graph API
def create_graph_event(access_token, event_data):
    events_url = "https://graph.microsoft.com/v1.0/me/events"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(events_url, headers=headers, json=event_data)
    if response.status_code == 201:
        print("Event created successfully.")
    else:
        print(f"Failed to create event: {response.status_code}, {response.text}")

# Get company deadlines and create calendar events
def get_company_deadlines_and_create_events(access_token):
    url = f'https://api.company-information.service.gov.uk/company/{company_number}'
    headers = {"Authorization": f"Basic {encoded_api_key}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        company_data = response.json()

        # Extract deadlines
        company_name = company_data.get('company_name', 'Not available')
        accounts_data = company_data.get('accounts', {})
        confirmation_data = company_data.get('confirmation_statement', {})

        next_accounts = accounts_data.get('next_made_up_to', 'Not available')
        accounts_deadline = accounts_data.get('next_due', 'Not available')
        confirmation_statement_due_date = confirmation_data.get('next_due', 'Not available')
        next_confirmation_statement_made_up_to = confirmation_data.get('next_made_up_to', 'Not available')

        # Create events for each deadline
        if next_accounts != 'Not available':
            event_data = {
                "subject": f"Next Accounts Made Up To for {company_name}",
                "start": {"dateTime": next_accounts, "timeZone": "UTC"},
                "end": {"dateTime": next_accounts, "timeZone": "UTC"},
            }
            create_graph_event(access_token, event_data)

        if accounts_deadline != 'Not available':
            event_data = {
                "subject": f"Accounts Deadline for {company_name}",
                "start": {"dateTime": accounts_deadline, "timeZone": "UTC"},
                "end": {"dateTime": accounts_deadline, "timeZone": "UTC"},
            }
            create_graph_event(access_token, event_data)

        if next_confirmation_statement_made_up_to != 'Not available':
            event_data = {
                "subject": f"Next Confirmation Statement Made Up To for {company_name}",
                "start": {"dateTime": next_confirmation_statement_made_up_to, "timeZone": "UTC"},
                "end": {"dateTime": next_confirmation_statement_made_up_to, "timeZone": "UTC"},
            }
            create_graph_event(access_token, event_data)

        if confirmation_statement_due_date != 'Not available':
            event_data = {
                "subject": f"Next Confirmation Statement Due for {company_name}",
                "start": {"dateTime": confirmation_statement_due_date, "timeZone": "UTC"},
                "end": {"dateTime": confirmation_statement_due_date, "timeZone": "UTC"},
            }
            create_graph_event(access_token, event_data)

        print("Company deadlines input as calendar events.")
    else:
        print(f"Failed to retrieve company data: {response.status_code}, {response.text}")
        
@app.route('/get_events', methods=['GET'])  # Highlighted new endpoint
def get_events():
    # Here you can implement the logic to retrieve events, for example, from a database or in-memory storage
    # This is a placeholder for demonstration purposes
    events = [
        {"name": "Next Accounts Made Up To", "date": "2024-10-30"},
        {"name": "Accounts Deadline", "date": "2024-11-05"}
    ]
    return jsonify(events)  # Highlighted returning events in JSON format

# Flask route to handle token
@app.route('/getToken')
def get_token():
    authorization_code = request.args.get('code')
    access_token = get_access_token(authorization_code)
    if access_token:
        get_company_deadlines_and_create_events(access_token)
        return "Events created successfully!", 200
    else:
        return "Failed to obtain access token.", 400
    

# Main function to run the app
if __name__ == '__main__':
    get_authorization_code()
    app.run(port=5001)
