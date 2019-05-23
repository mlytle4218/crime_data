#!/usr/bin/env python
import csv
import pandas as pd 
import numpy as np 
from scipy.spatial import cKDTree

df_crime = pd.read_csv('Crime_Data_from_2010_to_Present.csv', nrows=10000)
df_zips = pd.read_csv('free-zipcode-database-Primary.csv')

# limit to only CA for speed
df_zips = df_zips.loc[df_zips['State'] == 'CA']

#make new dataframe to make the kdtree possible
df_zips_coords = df_zips[['Lat','Long']]

# make the tree of the zips
tree = cKDTree(df_zips_coords)


#function to get the zip code from lat and long
def get_zip(input):
    lat,long = input.replace('(','').replace(')','').split(',')
    dist,idx = tree.query((lat,long), k=1)
    output = df_zips.iloc[idx,0]
    return output


df_crime['zipcode'] =  df_crime.apply(lambda r : get_zip(r['Location ']), 1)





# Set a new index
df_crime = df_crime.set_index('DR Number')

# Fill Time Occured for conversion
df_crime['Time Occurred'] = df_crime['Time Occurred'].apply (lambda x: str(x).zfill(4))

# Converr the data and time into datetime
df_crime['datetime'] =  df_crime.apply(lambda r : pd.to_datetime(r['Date Occurred'] + ' ' + r['Time Occurred']),1)

# Get rid of huge spaces in Address
df_crime['Address'] = df_crime['Address'].apply (lambda x: " ".join(str(x).split()) )

# Get rid of hug spaces in Cross Street
df_crime['Cross Street'] = df_crime['Cross Street'].apply (lambda x: " ".join(str(x).split()) )



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
            'Crime Code 1',
            'Crime Code 2',
            'Crime Code 3',
            'Crime Code 4',
            'Weapon Description']

# Clean up names for ease
df_crime.rename(index=str,
    columns={
        "DR Number":"dr_number",
        "Crime Code":"crime_code",
        "Crime Code Description":"crime_code_description",
        "Address":"address",
        "Cross Street":"cross_street"},
    inplace=True)

df_crime.drop(to_drop, inplace=True, axis=1)





out = df_crime.head(25)



print(out)


