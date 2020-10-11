# list of datasets
# https://api.census.gov/data.html
# to get variable for datasets click on "variables"
# to get examples for of requests click on "examples"

# get your key using the following website:
# https://api.census.gov/data/key_signup.html

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from geopy.geocoders import Nominatim
import numpy as np
import json

state_input = input('Choose a state: ').title()

geolocator = Nominatim(user_agent="my-apps")

plt.style.use('seaborn-colorblind')

#add you API key
YOUR_KEY = ''

data = requests.get(
    'https://api.census.gov/data/2018/acs/acs5/profile?get='  
    + 'NAME,'       # State, County 
    + 'DP03_0063E&' # Average Income
    + 'DP04_0001E&' # Population Estimate 
    + 'DP02_0057E&' # Enrolled in college
    + 'DP02_0092E&' # Foreigner
    + 'DP02_0150E&' # Computer/Internet Use
    + 'DP03_0095E&' # Has Health Insurance
    + 'DP05_0002E&' # Male Population
    + 'DP05_0003E&' # Female Population
    + 'DP02_0016E&' # Average family size
    + 'for=county:*&in=state:*'     
    + '&key=' + YOUR_KEY)

data = data.text

x = json.loads(data)
headers = x[0]
data = x[1:]

df = pd.DataFrame(data, columns=headers)

df['state'] = df['NAME'].str.split(', ').str[1]
df['county'] = df['NAME'].str.split(',').str[0]

df = df[df['state'] == state_input]

#replacing value due to API not recognizing original value
if state_input == 'California':
    df['NAME'] = df['NAME'].replace('San Francisco County, California', 
                                    'San Francisco, California')

df['city_coord'] = df['NAME'].apply(geolocator.geocode)
df = df.dropna(subset=['city_coord'])
df['longitude'] = df['city_coord'].apply(lambda x: x.latitude)
df['latitude'] = df['city_coord'].apply(lambda x: x.longitude)

df = df.drop(['NAME','city_coord'], axis=1) 

df.columns = ['Average_Income','Population_Estimate','Enrolled_College',
              'Foreigner','Computer_Internet_Use','Health_Insurance',
              'Male_Pop','Female_Pop','Average_Family_Size','State','County',
              'Longitude','Latitude']

int_columns = df.columns.to_list()[:8]
df[int_columns] = df[int_columns].astype(int)

df['Average_Family_Size'] = df['Average_Family_Size'].astype(float)

# Average Income vs Population Estimate
plt.show(df.plot(kind ="scatter", 
                 x = 'Latitude', 
                 y = 'Longitude' ,
                 title = "Estimated Population vs. Average Income in "+ state_input,
                 figsize = (10,7),
                 alpha = .6,
                 s=df['Average_Income']*.005,
                 c=df['Foreigner'],
                 cmap = plt.get_cmap('jet'),
                 colorbar=True))
 
#male to female population
plt.show(df.plot(kind ="scatter", 
                 x = 'Latitude', 
                 y = 'Longitude' ,
                 title = "Estimated Male to Female Population in "+ state_input,
                 figsize = (10,7),
                 alpha = .6,
                 s=df['Male_Pop']*.005,
                 c=df['Female_Pop'],
                 cmap = plt.get_cmap('jet'),
                 colorbar=True))

#population vs people who has access to internet
plt.show(df.plot(kind ="scatter", 
                 x = 'Latitude', 
                 y = 'Longitude' ,
                 title = "Estimated Population vs Internet Access in "+ state_input,
                 figsize = (10,7),
                 alpha = .6,
                 s=df['Population_Estimate']*.005,
                 c=df['Computer_Internet_Use'],
                 cmap = plt.get_cmap('jet'),
                 colorbar=True))
