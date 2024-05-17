import httpx
import os
from dotenv import load_dotenv

from strava_api.get_tokens import refresh_token

load_dotenv()

def get_activities(one_page=False):

    activities = []
    activities_on_page = 200
    page = 0

    access_token = refresh_token()["access_token"]

    while activities_on_page==200:
        page += 1
        
        print(f"Getting page {page}")
        
        response = httpx.get(f"{os.getenv('strava_api_address')}athlete/activities",
                            headers={"Authorization":f"Bearer {access_token}"},
                            params={"page":page, "per_page":200},
                            timeout=60
                            )
        
        response.raise_for_status
        
        if one_page:
            activities_on_page = 0
        else:
            activities_on_page = len(response.json())

        activities = activities + response.json()



    return activities

