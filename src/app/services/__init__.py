from __future__ import print_function

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.app.utils import generate_jwt
from datetime import datetime, timedelta


CLIENT_SECRETS_FILENAME = os.getenv('GOOGLE_CLIENT_SECRETS')

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "openid",
    'https://www.googleapis.com/auth/contacts.readonly',
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email"
]

def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                client_config=json.loads(CLIENT_SECRETS_FILENAME), scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('people', 'v1', credentials=creds)
      
        contacts_service = service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,
            personFields='emailAddresses').execute()
        connections = contacts_service.get('connections', [])
        
        user_service = service.people().get(resourceName='people/me', personFields='names,emailAddresses').execute()
        username = user_service.get('names')[0].get('displayName')
        useremail = user_service.get('emailAddresses')[0].get('value')
        payload = {
            'name': username,
            'email': useremail,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        token = generate_jwt(payload)
        user_infos = {
            'profile': {
                'name': username,
                'email': useremail,
                'token': token
                }}

        domains = set([])
        emails = set([])
        for person in connections:
            person_emails = person.get('emailAddresses', [])
            if person_emails:
                for email in person_emails:
                    value = email.get('value')
                    domain = value.split('@')[-1]
                    domains.add(domain)
                    emails.add(value)
        domains_dict = {}
        for domain in domains:
            same_domains = []
            for email in emails:
                email_domain = email.split('@')[-1]
                if email_domain == domain:
                    same_domains.append(email)
            domains_dict[domain] = same_domains
        user_infos['contacts'] = domains_dict
        return user_infos
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()