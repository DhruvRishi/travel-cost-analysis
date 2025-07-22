#Libraries imported
import pandas as pd
import matplotlib.pyplot as plt

#Loading csv file into a dataframe
df = pd.read_csv("B:\\Project_python\\Travel\\data\\Travel details dataset.csv", index_col=0)

#Data Exploration
print(df.head())
print(df.shape)
print(df[df.isnull().any(axis=1)])
print(df.dtypes)

#Converting date columns to datetime
df['Start date'] = pd.to_datetime(df['Start date'])
df['End date'] = pd.to_datetime(df['End date'])

# Define cleaning function
def clean_currency(column):
    return (
        column.astype(str)                          # Ensure all values are string
        .str.replace(',', '', regex=False)          # Remove commas (e.g. 1,200 → 1200)
        .str.replace('$', '', regex=False)          # Remove dollar signs
        .str.replace('USD', '', regex=False)        # Remove 'USD'
        .str.strip()                                # Remove leading/trailing whitespace
    )

# Apply cleaning function to the relevant columns
df['Transportation cost'] = clean_currency(df['Transportation cost'])
df['Accommodation cost']  = clean_currency(df['Accommodation cost'])

# Convert cleaned strings to numeric (float); invalid parsing becomes NaN
df['Transportation cost'] = pd.to_numeric(df['Transportation cost'], errors='coerce')
df['Accommodation cost']  = pd.to_numeric(df['Accommodation cost'], errors='coerce')

#Data Cleaning
df = df.drop([72,128])                         #Trip 82 and 128 are missing all values so we drop them
df.loc[83,"Transportation type"] = "Unknown"   #Trip 83 had two columns with missing values
df.loc[83,"Transportation cost"] = 0           #Trip 83 had two columns with missing values

print(df[df.isnull().any(axis=1)])             #Rechecking for Null Values
print (df.duplicated().sum())                  #Checking for duplicates

#Total Cost Column for further analysis
df['Total cost'] = df['Transportation cost'] + df['Accommodation cost']

#Average Transportation Cost
avg_transport_cost = df['Transportation cost'].mean()
print (f"\nThe average transport cost is ${avg_transport_cost:,.2f}")

#Average Accommodation Cost
avg_accommodation_cost = df['Accommodation cost'].mean()
print(f"The average accommodation cost is ${avg_accommodation_cost:,.2f}")

#Top 5 Visited Destinations
top_5 = df["Destination"].value_counts().head(5)
print(f"\nThe top 5 destinations are: {top_5}")

#Top 5 Used Accommodation Types
top_accom = df['Accommodation type'].value_counts().head(5)
print(f"\nThe top 5 accommodations are: {top_accom}")

#Top 5 Common Transportation Types
top_transport = df['Transportation type'].value_counts().head(5)
print(f"\nThe top 5 transportation types are: {top_transport}")


#Age Distribution of Travelers
traveler_mean_age = int(df['Traveler age'].mean())
print(f"\nThe average age of a traveler is: {traveler_mean_age}")
travel_common_age = int(df['Traveler age'].mode()[0])
print(f"\nThe most common age of a traveler is: {travel_common_age}")

#Traveler Gender Distribution
traveler_gen = df['Traveler gender'].value_counts()
print(f"\nThe gender distribution of travelers is: {traveler_gen}")

#Top 5 Most Expensive Trips
Exp_Trip = df.sort_values(by='Total cost', ascending=False).head(5)
print (f"\nThe top 5 exp trips are: {Exp_Trip}")

#Average Cost by Destination
average_cost_dest= df.groupby(['Destination'])['Total cost'].mean().sort_values(ascending=False)
print(f"\nThe average cost of destinations are: {average_cost_dest}")
