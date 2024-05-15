import httpx
import os
from dotenv import load_dotenv
import datetime
import pandas as pd

load_dotenv()


def get_segment_efforts(id):

    content = []

    # TODO - resolve pagination
    for page in range(1, 2):

        response = httpx.get(f"https://www.strava.com/api/v3/segment_efforts?segment_id={id}", 
                             headers={"Authorization":f"Bearer {os.getenv('strava_access_token')}"},
                             params={"per_page":200, "page":page})
    
        response.raise_for_status
    
        content = content + response.json()

    output = {
        'segment_name': content[0]["name"],
        'efforts': len(content),
        'data': pd.DataFrame({
            'effort_date': [effort["start_date"] for effort in content],
            'seconds': [effort["elapsed_time"] for effort in content],
            'times': [str(datetime.timedelta(seconds=effort["elapsed_time"]))  for effort in content]
        }),
    }

    return output
    

