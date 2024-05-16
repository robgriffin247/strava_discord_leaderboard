import pprint as pp

from strava_api.get_athlete_details import get_athlete_details
from strava_api.get_segment_efforts import get_segment_efforts

#pp.pprint(get_athlete_details(), indent=2)
pp.pprint(get_segment_efforts(window=30, since="2024-01-01"), indent=2)

    
