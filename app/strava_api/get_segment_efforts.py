import httpx
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta
from strava_api.get_tokens import refresh_token
import pandas as pd

load_dotenv()


def get_segment_efforts(id=17267489):

    content = []
    access_token = refresh_token()

    # TODO - resolve pagination; currently works for <=200 effort segments
    for page in range(1, 2):

        response = httpx.get(f"{os.getenv('strava_api_address')}segment_efforts?segment_id={id}", 
                             headers={"Authorization":f"Bearer {access_token}"},
                             params={"per_page":200, "page":page})
    
        response.raise_for_status
    
        content = content + response.json()

    output = {
        'segment_name': content[0]["name"],
        'effort_count': len(content),
        'efforts': pd.DataFrame({
            'effort_date': [effort["start_date"] for effort in content],
            'days_since': [(datetime.now() - datetime.strptime(effort["start_date"], "%Y-%m-%dT%H:%M:%SZ")).days for effort in content],
            'seconds': [effort["elapsed_time"] for effort in content],
            'time': [str(timedelta(seconds=effort["elapsed_time"]))  for effort in content]
        })
    }

    output["all_time_best"] = output["efforts"]["time"][0]
    output["90_day_best"] = output["efforts"].loc[output["efforts"]["days_since"]<=90]["time"].iloc[0]

    return output