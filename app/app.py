import pprint as pp

from strava_api.athletes import get_athlete_details
from strava_api.segments import get_segment_efforts
from strava_api.activities import get_activities, get_activity

#pp.pprint(get_athlete_details(), indent=2)

#print(get_activities(True))
print(get_activity(12158727257))

#pp.pprint(get_segment_efforts(window=30, since="2024-01-01"), indent=2)
#pp.pprint(get_segment_efforts(id=2228703), indent=2)

    


