import httpx
import os
from dotenv import load_dotenv

from datetime import datetime, timedelta

from strava_api.get_tokens import refresh_token
from strava_api.get_athlete_details import get_athlete_details
import pandas as pd

load_dotenv()


def get_segment_efforts(id=17267489, window=90, since="1970-01-01"):

    content = []
    access_token = refresh_token()

    athlete_details = get_athlete_details()
    
    # TODO - resolve pagination; currently works for <=200 effort segments
    for page in range(1, 2):

        response = httpx.get(f"{os.getenv('strava_api_address')}segment_efforts?segment_id={id}", 
                             headers={"Authorization":f"Bearer {access_token}"},
                             params={"per_page":200, "page":page})
    
        response.raise_for_status
    
        content = content + response.json()

    output = {
        'athlete_name': f"{athlete_details['firstname']} {athlete_details['lastname']}",
        'athlete_id': athlete_details['id'],
        'segment_name': content[0]["name"],
        'segment_id': content[0]["segment"]["id"],
        'effort_count_all_time': len(content),
        'efforts': pd.DataFrame({
            'effort_id': [effort["id"] for effort in content],
            'effort_datetime': [datetime.strptime(effort["start_date"], "%Y-%m-%dT%H:%M:%SZ") for effort in content],
            'activity_id': [effort["activity"]["id"] for effort in content],
            'days_since': [(datetime.now() - datetime.strptime(effort["start_date"], "%Y-%m-%dT%H:%M:%SZ")).days for effort in content],
            'seconds': [effort["elapsed_time"] for effort in content],
            'time': [str(timedelta(seconds=effort["elapsed_time"]))  for effort in content]
        })
    }

    output["best_all_time"] = output["efforts"]["time"][0]
    output["best_window"] = output["efforts"].loc[output["efforts"]["days_since"]<=window]["time"].iloc[0]
    output["best_since"] = output["efforts"].loc[output["efforts"]["effort_datetime"]>=datetime.strptime(f"{since}T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")]["time"].iloc[0]
    
    output["effort_count_window"] = len(output["efforts"].loc[output["efforts"]["days_since"]<=window])
    output["effort_count_since"] = len(output["efforts"].loc[output["efforts"]["effort_datetime"]>=datetime.strptime(f"{since}T00:00:00Z", "%Y-%m-%dT%H:%M:%SZ")])
    
    output["most_efforts_in_one_activity"] = output["efforts"].groupby("activity_id").size().max()

    return output