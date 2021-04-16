import re
import pandas as pd
import pycountry
from sqlalchemy import create_engine

engine = create_engine('postgresql://serenay@localhost/cosmos')

input_path = "/Users/serenay/Documents/work/engagement_lead/COSMOS-request-dashboard/research/notebooks/data" \
             "/COSMOS_Requests.csv"

df_requests = pd.read_csv(input_path)

# Null rows are deleted from 'Email' column
df_requests = df_requests[~df_requests["Email"].isnull()]

# regex patterns
regex_patterns_path = "../data/country_regex_patterns.csv"
df_country_patterns = pd.read_csv(regex_patterns_path)


def match_country_pattern(email, df):
    """ returns a country name when it is matched with the regex pattern.

    Parameters
    ----------
    df
    email
    """
    for index, row in df.iterrows():
        if re.search(row['regex_pattern'], email):
            return row['country_name']


# Create 'country_name' for countries, we found from emails.
df_requests["country_name"] = df_requests["Email"].apply(lambda x: match_country_pattern(x, df_country_patterns))

# Create a csv file for null rows country_names column has.
# This file was created to figure out how many countries was written in the spreadsheet
# before we determined the regex pattern from emails.
temp_path = "/Users/serenay/Documents/work/engagement_lead/COSMOS-request-dashboard/research/notebooks/data" \
            "/temp.csv"
df_requests[df_requests["country_name"].isnull()].to_csv(temp_path)

# Drop duplicated Emails
df_missing_countries = pd.read_csv(temp_path).drop_duplicates(subset="Email",
                                                              ignore_index=True)

# Select only two columns
df_missing_countries = df_missing_countries[["Email", "Country"]]

# Joined two df on email key column.
temp_joined_df = df_requests.merge(df_missing_countries, on='Email', how='left')

# Combine two columns (country_name and country_y) into one (country_name_new)
temp_joined_df['country_name_new'] = temp_joined_df["country_name"].combine_first(temp_joined_df["Country_y"])

# Dropped unnecessary columns from dataframe
dropped_temp_joined_df = temp_joined_df.drop(columns=['Counry', 'Country_x', 'Domain'])

# dropped_temp_joined_df.to_csv('clean.csv')

# Replace null rows with NaN from country_name_new column to able to insert them to the database.
dropped_temp_joined_df.loc[dropped_temp_joined_df["country_name_new"].isnull(), 'country_name_new'] = 'NaN'

dropped_temp_joined_df.to_sql('requests', engine, schema="cosmos")

