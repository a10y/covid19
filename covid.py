import pandas as pd
import numpy as np
import datetime
import os

########################
# Utility transforms
########################
def weeknum(dt):
    return datetime.date.fromisoformat(dt).isocalendar()[1]

#####################
# Data loading
#####################
hospitals = pd.read_csv(
        os.path.join(os.curdir, "hospitals.csv"),
)
cases = pd.read_csv(
        os.path.join(os.curdir, "cases_by_county.csv"),
)

#####################
# Data cleaning
#####################

# FIPS is integral
cases = cases.dropna()
cases['fips'] = cases['fips'].apply(int)

# Drop hospitals with unknown bed counts
hospitals.dropna()
hospitals['COUNTYFIPS'] = hospitals['COUNTYFIPS'].apply(lambda x: int(x) if x != 'NOT AVAILABLE' else -1)
hospitals = hospitals[hospitals['BEDS'] >= 0]

# Get total beds for each county
county_beds = hospitals.groupby(['COUNTYFIPS'])['BEDS'].sum()

# Extract week number for time tracking
cases['week'] = cases['date'].apply(weeknum)

# Keep most recent 2 weeks of data
cases_last2w = cases[cases['week'] >= 11]
cases_last2w = pd.merge(cases_last2w, county_beds, left_on='fips', right_index=True)

cases_last2w_by_county = cases_last2w.groupby(['state', 'county']).agg({
    'cases': np.sum,
    'deaths': np.sum,
    'BEDS': np.max,
})
cases_last2w_by_county['ratio'] = cases_last2w_by_county['cases'] / cases_last2w_by_county['BEDS']

at_risk_counties = cases_last2w_by_county[cases_last2w_by_county['ratio'] > 5]
print(at_risk_counties.sort_values('ratio', ascending=False))
