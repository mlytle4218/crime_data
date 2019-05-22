#!/usr/bin/env python
import csv
import pandas as pd 
import numpy as np 

df_crime = pd.read_csv('Crime_Data_from_2010_to_Present.csv', nrows=10000)
df_zips = pd.read_csv('free-zipcode-database-Primary.csv')
df_zips = df_zips.loc[df_zips['State'] == 'CA']
# df_zips = df_zips.set_index('Zipcode')
df_zips_coords = df_zips[['Lat','Long']]
print(df_zips.head())




from scipy.spatial import cKDTree

tree = cKDTree(df_zips_coords)
dist,idx = tree.query((33.9328,-118.2621), k=1)

print idx

print(df_zips.iloc[idx,0])

# df_crime = pd.read_csv('data.csv', nrows=10000)
# print(df_crime.head())
# print(df_crime.loc[0])

# out = df_crime['Crime Code 4'].value_counts()
# print(df_crime.keys())




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


# split up Location into lat and lon
df_crime['lat'] = df_crime['Location '].apply(lambda x: str(x).replace('(','').split(',')[0] )
df_crime['lon'] = df_crime['Location '].apply(lambda x: str(x).replace(')','').split(',')[1] )


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
# print(df_crime.isna().sum())
# print("crime_code nulls: " + str(df_crime.crime_code.isnull().sum()))
# print("address nulls: " + str(df_crime.Address.isnull().sum()))
# print("crime_code_description nulls: " + str(df_crime.crime_code_description.isnull().sum()))
# print("cross_street nulls: " + str(df_crime.cross_street.isnull().sum()))
# print("datetime nulls: " + str(df_crime.datetime.isnull().sum()))
# print("lat nulls: " + str(df_crime.lat.isnull().sum()))
# print("lon nulls: " + str(df_crime.lon.isnull().sum()))



#from https://stackoverflow.com/questions/48836567/pandas-compare-multiple-column-values-from-different-frames-of-different-lengths




out = df_crime.head(25)

# df_crime.to_csv('data_gps.csv')


# print(out)



# def get_data_from_csv(csv_file):
#     with open(csv_file, 'r') as file:
#         return list(csv.DictReader(file))



# # csv_dict = get_data_from_csv('Crime_Data_from_2010_to_Present.csv')

# count = 0
# with open('Crime_Data_from_2010_to_Present.csv') as f:
#     for line in f:
#         count += 1
#         if count > 10:
#             break
#         print(line.split()[6])


