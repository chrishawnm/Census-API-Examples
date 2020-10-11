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

#end user to choose a state in the United States
state_input = input('Choose a state: ').title()

#need for geopy api
geolocator = Nominatim(user_agent="my-apps")

#for heatmap
plt.style.use('seaborn-colorblind')

#add you API key
YOUR_KEY = ''

#api request 
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

#converting data to readable format (it converts it to a string)
data = data.text

#converts it to a list of list
x = json.loads(data)

#retrieving the header and then the body for pandas dataframe
headers = x[0]
data = x[1:]

#convert lists to pandas dataframe 
df = pd.DataFrame(data, columns=headers)

#splitting column into state and county
df['state'] = df['NAME'].str.split(', ').str[1]
df['county'] = df['NAME'].str.split(',').str[0]

#based on the state the end user has chose this will filter the dataset 
df = df[df['state'] == state_input]

#replacing value due to API not recognizing original value
if state_input == 'California':
    df['NAME'] = df['NAME'].replace('San Francisco County, California', 
                                    'San Francisco, California')

#retrieving lon and lat to be graphed on heatmap
print('Retrieving longitude and latitude please wait...')
df['city_coord'] = df['NAME'].apply(geolocator.geocode)
df = df.dropna(subset=['city_coord'])
df['longitude'] = df['city_coord'].apply(lambda x: x.latitude)
df['latitude'] = df['city_coord'].apply(lambda x: x.longitude)
print('Finished retrieving longituden and latitude')

#removing columns that are no longer needed
df = df.drop(['NAME','city_coord'], axis=1) 

# renaming columns
df.columns = ['Average_Income','Population_Estimate','Enrolled_College',
              'Foreigner','Computer_Internet_Use','Health_Insurance',
              'Male_Pop','Female_Pop','Average_Family_Size','State','County',
              'Longitude','Latitude']

#converting the first eight columns in the dataframe to int
int_columns = df.columns.to_list()[:8]
df[int_columns] = df[int_columns].astype(int)

#converting column to a float
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
 
print('Graphs have been completed!')
