import pandas as pd
import matplotlib.pyplot as plt

com_df = pd.read_csv('communities.csv')
crime_df = pd.read_excel('LGA Offences.xlsx', sheet_name='Table 02')

#filtering the crime stats excel
o_div = crime_df['Offence Division'] == 'B Property and deception offences'
s_div = crime_df['Offence Subdivision'] == 'A50 Robbery'
crimemask = o_div | s_div
filtered = crime_df[crimemask]
grouped = filtered.groupby(['Year', 'Local Government Area'])['Offence Count'].sum().reset_index()

#creating DataFrame of useful data
data = com_df[['LGA', "Holds degree or higher, persons","Holds degree or higher, %"]] # you can add the rows you want to look at here 
cols_to_convert = data.columns[data.columns != 'LGA']
data[cols_to_convert] = data[cols_to_convert].apply(pd.to_numeric, errors='coerce')


sdata = data.sort_values(by='LGA')

#here the data is grouped, use sum for number of people and mean for percentages
gdata = sdata.groupby('LGA').sum().reset_index()
gdata['LGA'] = gdata['LGA'].str.replace(r'\s*\(.*\)', '', regex=True).str.strip()

for year in range(2014, 2024):
    gdata[f'{year} Offence Count'] = None
    sgrouped = grouped[grouped['Year'] == year]

    for index, row in gdata.iterrows():
        lga = row['LGA']
        offence_count = sgrouped.loc[sgrouped['Local Government Area'] == lga, 'Offence Count']
        if not offence_count.empty:
            gdata.at[index, f'{year} Offence Count'] = offence_count.values[0]

print(gdata.info())

