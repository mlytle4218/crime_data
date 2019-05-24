#!/usr/bin/env python
import csv
import pandas as pd 
import numpy as np 
from scipy.spatial import cKDTree
from tqdm import tqdm
import time

from dask import dataframe as dd
from dask.multiprocessing import get
from multiprocessing import cpu_count
nCores = cpu_count()
start  = time.time()
print('Read in csv files')
df_crime = dd.read_csv('Crime_Data_from_2010_to_Present.csv',assume_missing=True)
# df_crime = pd.read_csv('Crime_Data_from_2010_to_Present.csv')
df_zips = dd.read_csv('free-zipcode-database-Primary.csv')
end = time.time()
print(end-start)

# limit to only CA for speed
df_zips = df_zips.loc[df_zips['State'] == 'CA']

#make new dataframe to make the kdtree possible
df_zips_coords = df_zips[['Lat','Long']]

# make the tree of the zips
print('Create Zip tree')
tree = cKDTree(df_zips_coords)


#function to get the zip code from lat and long
def get_zip(input):
    lat,long = input.replace('(','').replace(')','').split(',')
    dist,idx = tree.query((lat,long), k=1)
    output = df_zips.iloc[idx,0]
    return output


# df_crime['zipcode'] =  df_crime.apply(lambda r : get_zip(r['Location ']), 1)


#replace the column names with friendlier titles
cols = []
for title in df_crime.columns:
    cols.append(title.lower().replace(' ','_'))

df_crime  = df_crime.rename(columns=dict(zip(df_crime.columns,cols)))



df_crime.date_occurred = df_crime.date_occurred.astype("M8[us]")
print(df_crime.head())

print(type(df_crime.date_occurred))


# Set a new index
print('Set a new index')
# df_crime = df_crime.set_index('dr_number')

# Fill Time Occured for conversion
print('Format Time Occurred')
tqdm.pandas()

def z_fill(input):
    output  = str(input).zfill(4)
    return output


# result = df_crime.time_occurred.map_partitions(z_fill, meta=df_crime)
# df_crime.time_occurred = str(df_crime.time_occurred).zfill(4)
# print df_crime.head()



# df_crime['Time Occurred'] =dd.from_pandas(df_crime,npartitions=nCores).map_partitions(
#     lambda df : df.apply(lambda x: str(x).zfill(4))
# ).compute(scheduler='threads')
# df_crime['Time Occurred'] = df_crime['Time Occurred'].progress_apply(lambda x: str(x).zfill(4))
# df_crime['time_occurred'] = df_crime['time_occurred'].apply(lambda x: str(x).zfill(4))

print df_crime.head()
print('finished new')

# ddf = dd.from_pandas(df_crime,npartitions=nCores)
# ddf['']




# Converr the data and time into datetime
print('Create datetime')
# df_crime['datetime'] =  df_crime.apply(lambda r : pd.to_datetime(r['date_occurred'] + ' ' + r['time_occurred']),axis=1)
# df_crime[';datetime'] = pd.to_datetime(df_crime.date_occurred + " " + df_crime.time_occurred)
# df_crime.date_occurred + df_crime.time_occurred.astype('timedelta64[m]')


# meta = ('datetime', pd.Timestamp)
# df_crime.datetime.map_partitions(pd.to_datetime)
def dt(row):
    return pd.to_datetime(row['date_occurred'])



# Get rid of huge spaces in Address
# df_crime['Address'] = df_crime['Address'].apply (lambda x: " ".join(str(x).split()) )

# Get rid of hug spaces in Cross Street
# df_crime['Cross Street'] = df_crime['Cross Street'].apply (lambda x: " ".join(str(x).split()) )



#list to drop later if not needed
to_drop = ['Date Reported',
            'Area ID',
            'Area Name',
            'Reporting District',
            'Victim Age',
            'Victim Sex',
            'Victim Descent',
            'Weapon Used Code',
            'Status Code',
            'Status Description',
            'Date Occurred',
            'Time Occurred',
            'Location ',
            'MO Codes',
            'Premise Code',
            'Premise Description',
            # 'Crime Code 1',
            # 'Crime Code 2',
            # 'Crime Code 3',
            # 'Crime Code 4',
            'Weapon Description',
            'Address',
            'Cross Street']



df_crime.drop(to_drop, inplace=True, axis=1)





out = df_crime.head(25)



print(out)


