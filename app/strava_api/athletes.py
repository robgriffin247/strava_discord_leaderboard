import httpx
import os
from dotenv import load_dotenv
from strava_api.get_tokens import refresh_token

load_dotenv()

def get_athlete_details():

    access_token = refresh_token()["access_token"]

    response = httpx.get(f"{os.getenv('strava_api_address')}athlete",
                        headers={"Authorization":f"Bearer {access_token}"}
                        )
    
    response.raise_for_status
    
    content = response.json()

    return content