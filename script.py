import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# Use glob to sort the csv_files into a single path
csv_files = glob.glob('states*.csv')

# Loop through the csv_files and sort them into temporary dataframes
temp_dfs = []
for file in csv_files:
    temp_df = pd.read_csv(file)
    temp_dfs.append(temp_df)

# Concatenate the list of dataframes into a single dataframe
us_census = pd.concat(temp_dfs, axis = 0)
#print(us_census.head(5))

# Change income into a workable datatype (numeric)
us_census['Income'] = us_census['Income'].str.replace('$', '', regex = True)
us_census['Income'] = pd.to_numeric(us_census['Income'])

# Separate GenderPop into two columns Gender and Population
gen_split = us_census['GenderPop'].str.split('_', expand = True)
gen_split[0] = gen_split[0].replace('M', '', regex = True)
gen_split[1] = gen_split[1].replace('F', '', regex = True)
#print(gen_split)

# Create the two new columns and remove the old 'GenderPop' column in us_census dataframe
us_census['Male Population'] = gen_split[0]
us_census['Female Population'] = gen_split[1]
us_census = us_census.drop('GenderPop', axis = 1)

# Convert the new columns into the numeric datatype
us_census['Male Population'] = pd.to_numeric(us_census['Male Population'])
us_census['Female Population'] = pd.to_numeric(us_census['Female Population'])

# Fill in any Null values within the population columns with estimates from TotalPop
us_census = us_census.fillna(value={
  'Female Population': us_census['TotalPop'] - us_census['Male Population']
})

# Drop all duplicate data entries
us_census = us_census.drop_duplicates('State')
#print(us_census.head(5))

# Create a scatterplot showing the relation of Female Population and Income
#plt.scatter(us_census['Female Population'], us_census['Income'])
#plt.show()

# Clean all race data for analysis (Remove symbols and convert to numeric)
us_census['Hispanic'] = us_census['Hispanic'].str.replace('%', '', regex = True)
us_census['Hispanic'] = pd.to_numeric(us_census['Hispanic'])
#
us_census['White'] = us_census['White'].str.replace('%', '', regex = True)
us_census['White'] = pd.to_numeric(us_census['White'])
#
us_census['Black'] = us_census['Black'].str.replace('%', '', regex = True)
us_census['Black'] = pd.to_numeric(us_census['Black'])
#
us_census['Native'] = us_census['Native'].str.replace('%', '', regex = True)
us_census['Native'] = pd.to_numeric(us_census['Native'])
#
us_census['Asian'] = us_census['Asian'].str.replace('%', '', regex = True)
us_census['Asian'] = pd.to_numeric(us_census['Asian'])
#
us_census['Pacific'] = us_census['Pacific'].str.replace('%', '', regex = True)
us_census['Pacific'] = pd.to_numeric(us_census['Pacific'])
#

# Fill Null values within Pacific column with the us_census average
us_census = us_census.fillna(value={
  'Pacific': us_census['Pacific'].mean()
})

# Create a histogram for each of the races in the us_census
def hist_factory(df, column):
  plt.hist(df[column], edgecolor = 'black')
  plt.title(column)
  plt.xlabel('Percent % of Population')
  plt.ylabel('Number of States')
  plt.show()
  plt.cla()

hist_factory(us_census, 'Hispanic')
hist_factory(us_census, 'White')
hist_factory(us_census, 'Black')
hist_factory(us_census, 'Native')
hist_factory(us_census, 'Asian')
hist_factory(us_census, 'Pacific')
print(us_census)