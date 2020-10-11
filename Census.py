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

state_input = input('Choose a state: ').title()

geolocator = Nominatim(user_agent="my-apps")

plt.style.use('seaborn-colorblind')

#add you API key
YOUR_KEY = ''

data = requests.get(
    'https://api.census.gov/data/2018/acs/acs5/profile?get='  +
    'NAME,DP03_0063E&DP04_0001E&for=county:*&in=state:*'     +
    '&key=' + YOUR_KEY)

data = data.text
x = ast.literal_eval(data)

headers = x[0]
data = x[1:]

df = pd.DataFrame(data,columns=headers) 

df['state'] = df['NAME'].str.split(', ').str[1]
df['county'] = df['NAME'].str.split(',').str[0]

df = df[df['state'] == state_input]

df['city_coord'] = df['NAME'].apply(geolocator.geocode)
df = df.dropna(subset=['city_coord'])
df['longitude'] = df['city_coord'].apply(lambda x: x.latitude)
df['latitude'] = df['city_coord'].apply(lambda x: x.longitude)

df = df.drop(['NAME','city_coord'], axis=1) 

df.columns = ['Average_Income','Population_Estimate','State','County',
              'Longitude','Latitude']

df['Average_Income'] = df['Average_Income'].astype(int)
df['Population_Estimate'] = df['Population_Estimate'].astype(int)

plt.show(df.plot(kind ="scatter", 
                 x = 'Latitude', 
                 y = 'Longitude' ,
                 label = "Reported Average Income of "+ state_input,
                 figsize = (7,7),
                 alpha = .6,
                 s=df['Average_Income']*.005))
