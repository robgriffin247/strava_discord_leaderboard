import httpx
import os
from dotenv import load_dotenv, set_key, find_dotenv

load_dotenv()

def get_tokens():
    response = httpx.post("https://www.strava.com/oauth/token?",
                          data={
                              "client_id": os.getenv("strava_client_id"),
                              "client_secret": os.getenv("strava_client_secret"),
                              "code": os.getenv("strava_authorization_code"),
                              "grant_type": "authorization_code"
                          })

    return response.json()


def refresh_token():
    response = httpx.post("https://www.strava.com/oauth/token?",
                          data={
                              "client_id": os.getenv('strava_client_id'),
                              "client_secret": os.getenv('strava_client_secret'),
                              "refresh_token": os.getenv('strava_refresh_token'),
                              "grant_type": "refresh_token"
                          })
    
    return response.json()
