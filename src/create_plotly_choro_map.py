from numpy import log2
import pandas as pd
import plotly.express as px
import chart_studio
import chart_studio.plotly as py
from config import credentials

chart_studio.tools.set_credentials_file(username=credentials.username,
                                        api_key=credentials.api_key)

datafile = '../data/cosmos_download.csv'
df = pd.read_csv(datafile)
df["download_count_log"] = log2(df["download_count"])
print(df.head())

fig = px.choropleth(
    locations=df["country_iso3"],
    color=df["download_count_log"],
    hover_name=df["country"],  # column to add to hover information
    hover_data={"download_count": df["download_count"]},
    color_continuous_scale=px.colors.sequential.YlOrRd,
    projection="natural earth",
)

# fig.update_layout(coloraxis_colorbar=dict(len=0.5,
#                                           title="""Download Count\n(Log Scale)""",
#                                           x=1.1,
#                                           ypad=0,
#                                           xpad=0,
#                                           tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#                                           ticktext=['1', '2', '5', '10', '15', '25', '50', '100', '250', '500',
#                                                     '1000']),
#                   margin=dict(l=0,
#                               r=0,
#                               t=0,
#                               b=0,
#                               pad=0,
#                               ))

fig.show()
# py.plot(fig, filename='COSMOS Download Map', auto_open=True)
