from strava_api.get_tokens import refresh_token
import httpx
import os 

class Athlete:

    # Constructor
    def __init__(self, id):
        self.id = id
        self.bio = {}
        self.activities = []

    # Call to strava API to 
    # ... get athlete details for athlete bio (name, location etc.) to allow output controls on these attributes
    def get_bio(self):
        access_token = refresh_token()["access_token"]

        response = httpx.get(f"{os.getenv('strava_api_address')}athletes/{self.id}",
                            headers={"Authorization":f"Bearer {access_token}"}
                            )
    
        response.raise_for_status
    
        content = response.json()

        self.bio = {
            "name":f"{content['firstname']} {content['lastname']}",
            "username": content['username'],
            "sex": content['sex'],
            "weight": content['weight'],
            "country": content['country'],
        }
    
    # ... get athlete activities
    def get_activities(self, per_page=2):
        self.activities = []
        page = 0
        on_page = per_page

        access_token = refresh_token()["access_token"]

        while on_page==per_page and page<2: # added to limit number of requests and time taken for dev
            page += 1
            
            print(f"Getting actvities, page {page}")
            
            response = httpx.get(f"{os.getenv('strava_api_address')}athlete/activities",
                                headers={"Authorization":f"Bearer {access_token}"},
                                params={"page":page, "per_page":per_page},
                                timeout=60
                                )
            
            response.raise_for_status
            
            on_page = len(response.json())

            self.activities = self.activities + response.json()



