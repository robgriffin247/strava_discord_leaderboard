import httpx
import os
from dotenv import load_dotenv

load_dotenv()


def get_athlete():

    response = httpx.get("https://www.strava.com/api/v3/athlete", 
                         headers={"Authorization":f"Bearer {os.getenv('strava_access_token')}"})
    
    response.raise_for_status
    
    content = response.content

    return content
