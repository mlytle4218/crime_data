#!/usr/bin/env python
import csv
import pandas as pd 
import numpy as np 
from scipy.spatial import cKDTree

import pandas as pd
import numpy as np
from tqdm import tqdm


 

#for progress bar so I know where the damn thing has gotten to.
tqdm.pandas()

# df_crime = pd.read_csv('Crime_Data_from_2010_to_Present.csv', nrows=100000)
df_crime = pd.read_csv('Crime_Data_from_2010_to_Present.csv')
df_zips = pd.read_csv('free-zipcode-database-Primary.csv')

print('creating lat and long')

df_crime['lat'] = df_crime.progress_apply(lambda r : str(r['Location ']).replace('(','').split(',')[0].strip(), axis=1 )
df_crime['lon'] = df_crime.progress_apply(lambda r : str(r['Location ']).replace(')','').split(',')[1].strip(), axis=1 )


df_crime.lat = df_crime.lat.astype(float)
df_crime.lon = df_crime.lon.astype(float)
df_crime = df_crime[df_crime.lat != 0]
df_crime = df_crime[df_crime.lon != 0]


lat_min = float(df_crime.lat.min())
lat_max = float(df_crime.lat.max())
lon_min = float(df_crime.lon.min())
lon_max = float(df_crime.lon.max())

print lat_min
print lat_max
print lon_min
print lon_max

# >>> print lat_min
# 33.3427
# >>> print lat_max
# 34.7907
# >>> print lon_min
# -118.8279
# >>> print lon_max
# -117.6596
# >>> 


# >>> df_crime.datetime.min()
# Timestamp('2010-01-01 00:01:00')
# >>> df_crime.datetime.max()
# Timestamp('2019-04-17 18:30:00')






# limit to only CA for speed
df_zips = df_zips.loc[df_zips['State'] == 'CA']

#make new dataframe to make the kdtree possible
df_zips_coords = df_zips[['Lat','Long']]

# make the tree of the zips
tree = cKDTree(df_zips_coords)



#rename column titles for consistency
cols = []
for each in df_crime.columns:
    cols.append(each.lower().strip().replace(' ','_'))

#acutally rename columns titles 
df_crime.columns = cols




#function to get the zip code from lat and long
def get_zip(lat,long):
    # lat,long = input.replace('(','').replace(')','').split(',')
    dist,idx = tree.query((lat,long), k=1)
    output = df_zips.iloc[idx,0]
    return output

#for progress bat so I know where the damn thing has gotten to.
tqdm.pandas()
# run zip function to get nearest neighbor
print('getting zip codes')
df_crime['zipcode'] =  df_crime.progress_apply(lambda r : get_zip(r['lat'],r['lon']), axis=1)




# Set a new index
# df_crime = df_crime.set_index('dr_number')

# Converr the data and time into datetime
print('creating datetime')
df_crime['datetime'] =  df_crime.progress_apply(lambda r : pd.to_datetime(r['date_occurred'] + ' ' + str(r['time_occurred']).zfill(4)),axis=1)

# Get rid of huge spaces in Address
# df_crime['Address'] = df_crime['Address'].apply (lambda x: " ".join(str(x).split()) )

# Get rid of hug spaces in Cross Street
# df_crime['Cross Street'] = df_crime['Cross Street'].apply (lambda x: " ".join(str(x).split()) )





to_keep = [
    'crime_code_1',
    'crime_code_2',
    'crime_code_3',
    'crime_code_4',
    'crime_code_description']

# remove the ones we want to keep from the cols list
for keep in to_keep:
    cols.remove(keep)


# df_crime.drop(cols, inplace=True, axis=1)

# print(df_crime.head(25))
# df_crime.to_csv('out.csv', encoding='utf-8', index=False)

