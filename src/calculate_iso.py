import pandas as pd
import pycountry
from sqlalchemy import create_engine

engine = create_engine('postgresql://serenay@localhost/cosmos')


def convert_country_iso3(country):
    """converts country name to country codes

    Parameters
    ----------
    country : object
    """
    try:
        iso3 = pycountry.countries.get(name=country).alpha_3
    except AttributeError:
        iso3 = "Other"
    return iso3


# Add iso3 column for graph.
df_db = pd.read_sql("SELECT country_name_new FROM requests", engine)

geo_df_db = df_db['country_name_new'].value_counts().reset_index()
geo_df_db.columns = ["country", "download_count"]
geo_df_db["country_iso3"] = geo_df_db["country"].apply(lambda x: convert_country_iso3(x))
geo_df_db.columns = ["country", "download_count", "country_iso3"]
geo_df_db.to_csv("../data/cosmos_download.csv")
