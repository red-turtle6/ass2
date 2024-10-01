import pandas as pd
import matplotlib.pyplot as plt
year = 2023 # put year that you want
crime_data  = 'Rate per 100,000 population' # put name of column u want to analysed
element = 'Holds degree or higher, %' # put what data is being analysed

com_df = pd.read_csv('communities.csv')
crime_df = pd.read_excel('LGA Offences.xlsx', sheet_name='Table 01')

crime_df = crime_df[crime_df['Year'] == year]

# alphabetical to add the data
crime_df = crime_df.sort_values(by='Local Government Area')

# Strip whitespace from the relevant columns
crime_df['Local Government Area'] = crime_df['Local Government Area'].str.strip()
com_df['Community Name'] = com_df['Community Name'].str.strip()

# Initialize a new column in com_df to hold matching data from crime_df
com_df['Crime Data'] = None  # Or any other relevant column name

# Loop through each Local Government Area and assign data
for area in crime_df['Local Government Area']:
    # Check if the area is in the Community Name and assign data
    mask = com_df['Community Name'].str.contains(area, case=False, na=False)
    com_df.loc[mask, 'Crime Data'] = crime_df[crime_df['Local Government Area'] == area][crime_data].values[0]

com_df_cleaned = com_df.dropna()



# Create a scatter plot
plt.figure(figsize=(8, 6))  # Optional: set the figure size
plt.scatter(com_df_cleaned[element], com_df_cleaned['Crime Data'], color='blue', marker='o')  # You can customize color and marker

# Add titles and labels
plt.title('crime rate vs level of education')
plt.xlabel(element)
plt.ylabel(crime_data)

# Show grid
plt.grid(True)

# Display the plot
plt.show()


