# Strava Segments Leaderboard to Discord

### Aim 

Use the Strava API to collect effort counts and PR times for segments on Strava for associated users, then generate a leaderboard generating bot in discord.



### Components

- Code to extract best times and effort counts for connected athletes on a given segment, including all time, sliding window (e.g. last 90 days) and efforts since (e.g. since January 1st 2024). This data will be used to generate a leaderboard.
  - Status: The `get_segment_efforts()` function is limited by pagination issues - currently working on lifting all efforts via activities.
- Strava authorization to other athletes.
  - Status: App has been approved for multiple users, need to get users to authorize to allow testing.
- Code to push leaderboards to Discord on request.
  - Status: Not started.



### Setup

1. Create Strava App (Strava > Settings > My API Application)

1. Get authorization code
  1. Get your client ID and client secret from the Strava My API Application page, and add to a .env file
  1. Exchange your client id into this url; note the scope=`activity:read_all` grants access to all activity data including hidden start/finishes etc. ([read more](https://developers.strava.com/docs/authentication/)).
  `http://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all`
  1. Follow the link and authorize the app
  1. Copy the authorization code from the url you are directed to and store in the .env file

1. Exchange the authorization code for access and refresh tokens

    ```python
    def get_tokens():
        response = httpx.post("https://www.strava.com/oauth/token?",
                              data={
                                  "client_id": os.getenv("strava_client_id"),
                                  "client_secret": os.getenv("strava_client_secret"),
                                  "code": os.getenv("strava_authorization_code"),
                                  "grant_type": "authorization_code"
                              }

        return response.json()

    print(get_tokens())
    ```
  
1.  Store the access and refresh tokens in the .env file



### Making a request

The following code makes a request to get the details of the authorized athlete. Read about all available endpoints [here](https://developers.strava.com/docs/reference/).

```python
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
```

I have stored the api address in the .env file in case the address changes in the future; the current address is *https://www.strava.com/api/v3/*. Note that the function will also make a request to refresh the access token every time it is run, even if the token is not expired; I will add functionality to check expiration to reduce excess requests. 

The response will look a bit like this:

```json
{ 'badge_type_id': 1,
  'bio': 'Instagram - Griffinevo3782',
  'city': 'Vänersborg',
  'country': 'Sweden',
  'created_at': '2012-08-27T17:11:15Z',
  'firstname': 'Robert',
  ...
}  
```

Pagination will probably be needed to return all activities by the user:

```python
import httpx
import os
from dotenv import load_dotenv

from strava_api.get_tokens import refresh_token

load_dotenv()

def get_activities():

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
        
        activities_on_page = len(response.json())

        activities = activities + response.json()

    return activities
```