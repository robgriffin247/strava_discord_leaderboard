import httpx
import os
from dotenv import load_dotenv
import pprint as pp

load_dotenv()


def get_segment_efforts(id):

    content = []

    for page in range(1, 2):

        response = httpx.get(f"https://www.strava.com/api/v3/segment_efforts?segment_id={id}", 
                             headers={"Authorization":f"Bearer {os.getenv('strava_access_token')}"},
                             params={"per_page":5, "page":page})
    
        response.raise_for_status
    
        content = content + response.json()

    return content


#data = get_segment_efforts("4458166")
data = get_segment_efforts("17267489")


effort_ids = [effort["start_date"] for effort in data]
print(len(data))
pp.pprint(effort_ids, indent=2)

