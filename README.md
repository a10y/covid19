COVID-19 Pandas Analysis
------------------------

* NYTimes COVID case data from GitHub, pulled on Sunday 29 March, 2020: https://github.com/nytimes/covid-19-data/blob/master/us-counties.csv
* Hospital data pulled from Homeland Infrastructure Foundation-Level Data, DHS: https://hifld-geoplatform.opendata.arcgis.com/datasets/hospitals

## Running

Make sure you have the following packages installed:

* pandas
* numpy

```
python covid.py
```

Output is US counties where number of confirmed COVID cases in the 2 weeks before March 29, 2020 outstrips the number of total hospital beds by 5x
