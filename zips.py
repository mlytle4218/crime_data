#!/usr/bin/env python
import csv
import pandas as pd 
import numpy as np 

df = pd.read_csv('free-zipcode-database-Primary.csv')
df_new = df.loc[df['State'] == 'CA']
print(df_new.head(25))