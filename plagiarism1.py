import plotly.express as px
df = px.data.gapminder().query("year == 2007").query("continent == 'Asia'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig = px.pie(df, values='pop', names='country', title='Population of people affected with covid')
fig.show()

