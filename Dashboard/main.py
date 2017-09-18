# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

from bokeh.layouts import row, widgetbox
from bokeh.models import Select, Label, TextInput, Label
from bokeh.layouts import layout, column, row, widgetbox
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure
from bokeh.models import DatetimeTickFormatter
from bokeh.themes.theme import Theme
from bokeh.charts import Bar
from random import shuffle
import warnings
import json
import datetime as dt

warnings.filterwarnings('ignore')

# Style 
with open('/home/alvaro/Escritorio/TFM_app/theme.yaml','r') as infile:
    json_data = json.load(infile)


theme_doc = Theme(json=json_data)


# Load data
data = pd.read_csv('tweet_data', sep='\t', header=None, names=['date','lenght_tweet','lenght_mention','lenght_hashtag','politican_party','relevant_person','relevant_user','top_k_word'])


# Add polarity data
data_p = pd.read_csv('tweet_polarity', sep='\t', header=None, names=['pol'])
data['polarity'] = data_p['pol']
data['date'] =pd.to_datetime(data['date'], yearfirst=True)
data = data.set_index('date')

# Make 3 DataFrames (P, N, NEU)
data_P = data.loc[data['polarity'] == 'P']
data_N = data.loc[data['polarity'] == 'N']
data_NEU = data.loc[data['polarity'] == 'NEU']


# Create DataFrame for BarChar 1 (hashtagg and means)
hashtagg_P = data_P['lenght_hashtag'].mean()
hashtagg_N = data_N['lenght_hashtag'].mean()
hashtagg_NEU = data_NEU['lenght_hashtag'].mean()

mention_P = data_P['lenght_mention'].mean()
mention_N = data_N['lenght_mention'].mean()
mention_NEU = data_NEU['lenght_mention'].mean()


values1 = np.array([['Positive', 'Mentions (mean)', str(mention_P)], ['Positive', 'Hashtag (mean)', str(hashtagg_P)], ['Negative','Mentions (mean)',str(mention_N)], ['Negative','Hashtag (mean)',str(hashtagg_N)], ['Neutral', 'Mentions (mean)',str(mention_NEU)], ['Neutral','Hashtag (mean)',str(hashtagg_NEU)]])


df_bar1 = pd.DataFrame(data=values1, columns=['polarity','group','measures'])
df_bar1['measures'] = df_bar1['measures'].apply(pd.to_numeric)


# Plot BarChar1
barchar1 = Bar(df_bar1, label='group', values='measures', group='polarity', legend='top_right', color=['#eb4a5f', '#548ab5', '#7fb414'], plot_height=400, plot_width=400, title='Mean hashtag and mentions')


# Histogram for words per tweet
barchar2 = figure(title="Words per tweet", plot_height=390, plot_width=390)
hist, edges = np.histogram(data['lenght_tweet'].tolist(), bins=50)
hist_words = barchar2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="#797979", line_color="white")

# Group data every 5 min
data_grouped_P = data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()	
data_grouped_P2 = data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()	
data_grouped_N = data_N.groupby([pd.TimeGrouper(freq='5Min')]).count()
data_grouped_NEU = data_NEU.groupby([pd.TimeGrouper(freq='5Min')]).count()

# Add zeros at the end of two DatFrames
A = data_grouped_P2.tail(5)
A['lenght_tweet'] = 0
frames1 = [data_grouped_NEU, A]
frames2 = [data_grouped_N, A]
data_grouped_NEU = pd.concat(frames1)
data_grouped_N = pd.concat(frames2)


# Data to plot
y_P = data_grouped_P.lenght_tweet
x_P = data_grouped_P.index

y_N = data_grouped_N.lenght_tweet
x_N = data_grouped_N.index

y_NEU = data_grouped_NEU.lenght_tweet
x_NEU = data_grouped_NEU.index




### Graph with positive tweets ###
plot_P = figure(title="Positive Tweets •LIVE", plot_height=300, plot_width=1400, x_axis_type='datetime')
r_P = plot_P.line(x_P, y_P, line_color = "#7fb414")
h_P = plot_P.circle(x_P, y_P, fill_color='#7fb414', line_color="#7fb414", size=7)

total = len(data_P) + len(data_N) + len(data_NEU)

x_bottom = int(dt.datetime(2016, 6, 14, 0, 0).timestamp() * 1e3)
x_top = int(dt.datetime(2016, 6, 14, 2, 35).timestamp() * 1e3)

label_P = Label(x_units = 'screen', y_units = 'screen', x=100, y=180, text='%.2f' % ((len(data_P)/total)*100) + '%', text_font_size='50pt', text_color='white')
plot_P.add_layout(label_P)

### Graph with negative tweets ###
plot_N = figure(title="Negative Tweets •LIVE", plot_height=350, plot_width=1400, x_axis_type='datetime', x_range=(x_bottom, x_top))
r_N = plot_N.line(x_N, y_N, line_color = "#eb4a5f")
h_N = plot_N.circle(x_N, y_N, fill_color='#eb4a5f', line_color="#eb4a5f", size=7)

label_N = Label(x_units = 'screen', y_units = 'screen', x=100, y=230, text='%.2f' % ((len(data_N)/total)*100) + '%', text_font_size='50pt', text_color='white')
plot_N.add_layout(label_N)

### Graph with neutral tweets ###
plot_NEU = figure(title="Neutral Tweets •LIVE", plot_height=300, plot_width=1400, x_axis_type='datetime', x_range=(x_bottom, x_top))
r_NEU = plot_NEU.line(x_NEU, y_NEU, line_color = "#548ab5")
h_NEU = plot_NEU.circle(x_NEU, y_NEU, fill_color='#548ab5', line_color="#548ab5", size=7)

label_NEU = Label(x_units = 'screen', y_units = 'screen', x=100, y=180, text='%.2f' % ((len(data_NEU)/total)*100) + '%', text_font_size='50pt', text_color='white')
plot_NEU.add_layout(label_NEU)

# Def update function (widgets)
def update(attrname, old, new):
    per = character.value.lower()
    par = pol_par.value.lower()
    pal = k_w.value.lower()
    if par != 'all' and per != 'all' and pal != '':

        # Plot sentiment
        new_data_P = data_P.loc[(data_P['relevant_person'].str.contains(per)==True) & (data_P['politican_party'].str.contains(par)==True) & (data_P['top_k_word'].str.contains(pal)==True)]
        dg_P = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_N = data_N.loc[(data_N['relevant_person'].str.contains(per)==True) & (data_N['politican_party'].str.contains(par)==True) & (data_N['top_k_word'].str.contains(pal)==True)]
        dg_N = new_data_N.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_NEU = data_NEU.loc[(data_NEU['relevant_person'].str.contains(per)==True) & (data_NEU['politican_party'].str.contains(par)==True) & (data_NEU['top_k_word'].str.contains(pal)==True)]
        dg_NEU = new_data_NEU.groupby([pd.TimeGrouper(freq='5Min')]).count()

        # Add last elem
        dg_P2 = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()
        AUX = dg_P2.tail(5)
        AUX['lenght_tweet'] = 0

        fr1 = [dg_NEU, A]
        fr2 = [dg_N, A]

        dg_NEU = pd.concat(fr1)
        dg_N = pd.concat(fr2)

        r_NEU.data_source.data['x'] = dg_NEU.index
        r_NEU.data_source.data['y'] = dg_NEU.lenght_tweet
        h_NEU.data_source.data['x'] = dg_NEU.index
        h_NEU.data_source.data['y'] = dg_NEU.lenght_tweet

        r_N.data_source.data['x'] = dg_N.index
        r_N.data_source.data['y'] = dg_N.lenght_tweet
        h_N.data_source.data['x'] = dg_N.index
        h_N.data_source.data['y'] = dg_N.lenght_tweet

        r_P.data_source.data['x'] = dg_P.index
        r_P.data_source.data['y'] = dg_P.lenght_tweet
        h_P.data_source.data['x'] = dg_P.index
        h_P.data_source.data['y'] = dg_P.lenght_tweet

        # Histogram
        frames = [new_data_N, new_data_P, new_data_NEU]
        new_data_his = pd.concat(frames)
        hist, edges = np.histogram(new_data_his['lenght_tweet'].tolist(), bins=50)
        hist_words.data_source.data['top'] = hist

	# Percentages
        label_P.text = '%.2f' % ((len(new_data_P)/total)*100) + '%'
        label_N.text = '%.2f' % ((len(new_data_N)/total)*100) + '%'
        label_NEU.text = '%.2f' % ((len(new_data_NEU)/total)*100) + '%'


    elif par != 'all' and per != 'all':

        # Plot sentiment
        new_data_P = data_P.loc[(data_P['relevant_person'].str.contains(per)==True) & (data_P['politican_party'].str.contains(par)==True)]
        dg_P = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()

        new_data_N = data_N.loc[(data_N['relevant_person'].str.contains(per)==True) & (data_N['politican_party'].str.contains(par)==True)]
        dg_N = new_data_N.groupby([pd.TimeGrouper(freq='5Min')]).count()

        new_data_NEU = data_NEU.loc[(data_NEU['relevant_person'].str.contains(per)==True) & (data_NEU['politican_party'].str.contains(par)==True)]
        dg_NEU = new_data_NEU.groupby([pd.TimeGrouper(freq='5Min')]).count()

        # Add last elem
        dg_P2 = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()
        AUX = dg_P2.tail(5)
        AUX['lenght_tweet'] = 0

        fr1 = [dg_NEU, A]
        fr2 = [dg_N, A]

        dg_NEU = pd.concat(fr1)
        dg_N = pd.concat(fr2)

        r_NEU.data_source.data['x'] = dg_NEU.index
        r_NEU.data_source.data['y'] = dg_NEU.lenght_tweet
        h_NEU.data_source.data['x'] = dg_NEU.index
        h_NEU.data_source.data['y'] = dg_NEU.lenght_tweet

        r_N.data_source.data['x'] = dg_N.index
        r_N.data_source.data['y'] = dg_N.lenght_tweet
        h_N.data_source.data['x'] = dg_N.index
        h_N.data_source.data['y'] = dg_N.lenght_tweet

        r_P.data_source.data['x'] = dg_P.index
        r_P.data_source.data['y'] = dg_P.lenght_tweet
        h_P.data_source.data['x'] = dg_P.index
        h_P.data_source.data['y'] = dg_P.lenght_tweet

        # Histogram
        frames = [new_data_N, new_data_P, new_data_NEU]
        new_data_his = pd.concat(frames)
        hist, edges = np.histogram(new_data_his['lenght_tweet'].tolist(), bins=50)
        hist_words.data_source.data['top'] = hist

	# Percentages
        label_P.text = '%.2f' % ((len(new_data_P)/total)*100) + '%'
        label_N.text = '%.2f' % ((len(new_data_N)/total)*100) + '%'
        label_NEU.text = '%.2f' % ((len(new_data_NEU)/total)*100) + '%'


    elif par != 'all' and pal != '':

        # Plot sentiment
        new_data_P = data_P.loc[(data_P['top_k_word'].str.contains(pal)==True) & (data_P['politican_party'].str.contains(par)==True)]
        dg_P = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_N = data_N.loc[(data_N['top_k_word'].str.contains(pal)==True) & (data_N['politican_party'].str.contains(par)==True)]
        dg_N = new_data_N.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_NEU = data_NEU.loc[(data_NEU['top_k_word'].str.contains(pal)==True) & (data_NEU['politican_party'].str.contains(par)==True)]
        dg_NEU = new_data_NEU.groupby([pd.TimeGrouper(freq='5Min')]).count()

        # Add last elem
        dg_P2 = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()
        AUX = dg_P2.tail(5)
        AUX['lenght_tweet'] = 0

        fr1 = [dg_NEU, A]
        fr2 = [dg_N, A]

        dg_NEU = pd.concat(fr1)
        dg_N = pd.concat(fr2)

        r_NEU.data_source.data['x'] = dg_NEU.index
        r_NEU.data_source.data['y'] = dg_NEU.lenght_tweet
        h_NEU.data_source.data['x'] = dg_NEU.index
        h_NEU.data_source.data['y'] = dg_NEU.lenght_tweet

        r_N.data_source.data['x'] = dg_N.index
        r_N.data_source.data['y'] = dg_N.lenght_tweet
        h_N.data_source.data['x'] = dg_N.index
        h_N.data_source.data['y'] = dg_N.lenght_tweet

        r_P.data_source.data['x'] = dg_P.index
        r_P.data_source.data['y'] = dg_P.lenght_tweet
        h_P.data_source.data['x'] = dg_P.index
        h_P.data_source.data['y'] = dg_P.lenght_tweet

        # Histogram
        frames = [new_data_N, new_data_P, new_data_NEU]
        new_data_his = pd.concat(frames)
        hist, edges = np.histogram(new_data_his['lenght_tweet'].tolist(), bins=50)
        hist_words.data_source.data['top'] = hist

	# Percentages
        label_P.text = '%.2f' % ((len(new_data_P)/total)*100) + '%'
        label_N.text = '%.2f' % ((len(new_data_N)/total)*100) + '%'
        label_NEU.text = '%.2f' % ((len(new_data_NEU)/total)*100) + '%'


    elif pal != '' and per != 'all':

        # Plot sentiment
        new_data_P = data_P.loc[(data_P['top_k_word'].str.contains(pal)==True) & (data_P['relevant_person'].str.contains(per)==True)]
        dg_P = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()

        new_data_N = data_N.loc[(data_N['top_k_word'].str.contains(pal)==True) & (data_N['relevant_person'].str.contains(per)==True)]
        dg_N = new_data_N.groupby([pd.TimeGrouper(freq='5Min')]).count()

        new_data_NEU = data_NEU.loc[(data_NEU['top_k_word'].str.contains(pal)==True) & (data_NEU['relevant_person'].str.contains(per)==True)]
        dg_NEU = new_data_NEU.groupby([pd.TimeGrouper(freq='5Min')]).count()

        # Add last elem
        dg_P2 = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()
        AUX = dg_P2.tail(5)
        AUX['lenght_tweet'] = 0

        fr1 = [dg_NEU, A]
        fr2 = [dg_N, A]

        dg_NEU = pd.concat(fr1)
        dg_N = pd.concat(fr2)

        r_NEU.data_source.data['x'] = dg_NEU.index
        r_NEU.data_source.data['y'] = dg_NEU.lenght_tweet
        h_NEU.data_source.data['x'] = dg_NEU.index
        h_NEU.data_source.data['y'] = dg_NEU.lenght_tweet

        r_N.data_source.data['x'] = dg_N.index
        r_N.data_source.data['y'] = dg_N.lenght_tweet
        h_N.data_source.data['x'] = dg_N.index
        h_N.data_source.data['y'] = dg_N.lenght_tweet

        r_P.data_source.data['x'] = dg_P.index
        r_P.data_source.data['y'] = dg_P.lenght_tweet
        h_P.data_source.data['x'] = dg_P.index
        h_P.data_source.data['y'] = dg_P.lenght_tweet

        # Histogram
        frames = [new_data_N, new_data_P, new_data_NEU]
        new_data_his = pd.concat(frames)
        hist, edges = np.histogram(new_data_his['lenght_tweet'].tolist(), bins=50)
        hist_words.data_source.data['top'] = hist

	# Percentages
        label_P.text = '%.2f' % ((len(new_data_P)/total)*100) + '%'
        label_N.text = '%.2f' % ((len(new_data_N)/total)*100) + '%'
        label_NEU.text = '%.2f' % ((len(new_data_NEU)/total)*100) + '%'



    elif par != 'all':

        # Plot sentiment
        new_data_P = data_P.loc[data_P['politican_party'].str.contains(par)==True]
        dg_P = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_N = data_N.loc[data_N['politican_party'].str.contains(par)==True]
        dg_N = new_data_N.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_NEU = data_NEU.loc[data_NEU['politican_party'].str.contains(par)==True]
        dg_NEU = new_data_NEU.groupby([pd.TimeGrouper(freq='5Min')]).count()

        # Add last elem
        dg_P2 = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()
        AUX = dg_P2.tail(5)
        AUX['lenght_tweet'] = 0

        fr1 = [dg_NEU, A]
        fr2 = [dg_N, A]

        dg_NEU = pd.concat(fr1)
        dg_N = pd.concat(fr2)

        r_NEU.data_source.data['x'] = dg_NEU.index
        r_NEU.data_source.data['y'] = dg_NEU.lenght_tweet
        h_NEU.data_source.data['x'] = dg_NEU.index
        h_NEU.data_source.data['y'] = dg_NEU.lenght_tweet

        r_N.data_source.data['x'] = dg_N.index
        r_N.data_source.data['y'] = dg_N.lenght_tweet
        h_N.data_source.data['x'] = dg_N.index
        h_N.data_source.data['y'] = dg_N.lenght_tweet

        r_P.data_source.data['x'] = dg_P.index
        r_P.data_source.data['y'] = dg_P.lenght_tweet
        h_P.data_source.data['x'] = dg_P.index
        h_P.data_source.data['y'] = dg_P.lenght_tweet

        # Histogram
        frames = [new_data_N, new_data_P, new_data_NEU]
        new_data_his = pd.concat(frames)
        hist, edges = np.histogram(new_data_his['lenght_tweet'].tolist(), bins=50)
        hist_words.data_source.data['top'] = hist

	# Percentages
        label_P.text = '%.2f' % ((len(new_data_P)/total)*100) + '%'
        label_N.text = '%.2f' % ((len(new_data_N)/total)*100) + '%'
        label_NEU.text = '%.2f' % ((len(new_data_NEU)/total)*100) + '%'


    elif pal != '':

        # Plot sentiment
        new_data_P = data_P.loc[data_P['top_k_word'].str.contains(pal)==True]
        dg_P = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_N = data_N.loc[data_N['top_k_word'].str.contains(pal)==True]
        dg_N = new_data_N.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_NEU = data_NEU.loc[data_NEU['top_k_word'].str.contains(pal)==True]
        dg_NEU = new_data_NEU.groupby([pd.TimeGrouper(freq='5Min')]).count()

        # Add last elem
        dg_P2 = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()
        AUX = dg_P2.tail(5)
        AUX['lenght_tweet'] = 0

        fr1 = [dg_NEU, A]
        fr2 = [dg_N, A]

        dg_NEU = pd.concat(fr1)
        dg_N = pd.concat(fr2)

        r_NEU.data_source.data['x'] = dg_NEU.index
        r_NEU.data_source.data['y'] = dg_NEU.lenght_tweet
        h_NEU.data_source.data['x'] = dg_NEU.index
        h_NEU.data_source.data['y'] = dg_NEU.lenght_tweet

        r_N.data_source.data['x'] = dg_N.index
        r_N.data_source.data['y'] = dg_N.lenght_tweet
        h_N.data_source.data['x'] = dg_N.index
        h_N.data_source.data['y'] = dg_N.lenght_tweet

        r_P.data_source.data['x'] = dg_P.index
        r_P.data_source.data['y'] = dg_P.lenght_tweet
        h_P.data_source.data['x'] = dg_P.index
        h_P.data_source.data['y'] = dg_P.lenght_tweet

        # Histogram
        frames = [new_data_N, new_data_P, new_data_NEU]
        new_data_his = pd.concat(frames)
        hist, edges = np.histogram(new_data_his['lenght_tweet'].tolist(), bins=50)
        hist_words.data_source.data['top'] = hist

	# Percentages
        label_P.text = '%.2f' % ((len(new_data_P)/total)*100) + '%'
        label_N.text = '%.2f' % ((len(new_data_N)/total)*100) + '%'
        label_NEU.text = '%.2f' % ((len(new_data_NEU)/total)*100) + '%'


    elif per != 'all':

        # Plot sentiment
        new_data_P = data_P.loc[data_P['relevant_person'].str.contains(per)==True]
        dg_P = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_N = data_N.loc[data_N['relevant_person'].str.contains(per)==True]
        dg_N = new_data_N.groupby([pd.TimeGrouper(freq='5Min')]).count()


        new_data_NEU = data_NEU.loc[data_NEU['relevant_person'].str.contains(per)==True]
        dg_NEU = new_data_NEU.groupby([pd.TimeGrouper(freq='5Min')]).count()

        # Add last elem
        dg_P2 = new_data_P.groupby([pd.TimeGrouper(freq='5Min')]).count()
        AUX = dg_P2.tail(5)
        AUX['lenght_tweet'] = 0

        fr1 = [dg_NEU, A]
        fr2 = [dg_N, A]

        dg_NEU = pd.concat(fr1)
        dg_N = pd.concat(fr2)

        r_NEU.data_source.data['x'] = dg_NEU.index
        r_NEU.data_source.data['y'] = dg_NEU.lenght_tweet
        h_NEU.data_source.data['x'] = dg_NEU.index
        h_NEU.data_source.data['y'] = dg_NEU.lenght_tweet

        r_N.data_source.data['x'] = dg_N.index
        r_N.data_source.data['y'] = dg_N.lenght_tweet
        h_N.data_source.data['x'] = dg_N.index
        h_N.data_source.data['y'] = dg_N.lenght_tweet

        r_P.data_source.data['x'] = dg_P.index
        r_P.data_source.data['y'] = dg_P.lenght_tweet
        h_P.data_source.data['x'] = dg_P.index
        h_P.data_source.data['y'] = dg_P.lenght_tweet

        # Histogram
        frames = [new_data_N, new_data_P, new_data_NEU]
        new_data_his = pd.concat(frames)
        hist, edges = np.histogram(new_data_his['lenght_tweet'].tolist(), bins=50)
        hist_words.data_source.data['top'] = hist

	# Percentages
        label_P.text = '%.2f' % ((len(new_data_P)/total)*100) + '%'
        label_N.text = '%.2f' % ((len(new_data_N)/total)*100) + '%'
        label_NEU.text = '%.2f' % ((len(new_data_NEU)/total)*100) + '%'

    else:

	# Plot sentiment
        r_P.data_source.data['x'] = data_grouped_P.index
        r_P.data_source.data['y'] = data_grouped_P.lenght_tweet
        h_P.data_source.data['x'] = data_grouped_P.index
        h_P.data_source.data['y'] = data_grouped_P.lenght_tweet

        r_N.data_source.data['x'] = data_grouped_N.index
        r_N.data_source.data['y'] = data_grouped_N.lenght_tweet
        h_N.data_source.data['x'] = data_grouped_N.index
        h_N.data_source.data['y'] = data_grouped_N.lenght_tweet

        r_NEU.data_source.data['x'] = data_grouped_NEU.index
        r_NEU.data_source.data['y'] = data_grouped_NEU.lenght_tweet
        h_NEU.data_source.data['x'] = data_grouped_NEU.index
        h_NEU.data_source.data['y'] = data_grouped_NEU.lenght_tweet


        # Histogram
        hist, edges = np.histogram(data['lenght_tweet'].tolist(), bins=50)
        hist_words.data_source.data['top'] = hist

	# Percentages
        label_P.text = '%.2f' % ((len(data_P)/total)*100) + '%'
        label_N.text = '%.2f' % ((len(data_N)/total)*100) + '%'
        label_NEU.text = '%.2f' % ((len(data_NEU)/total)*100) + '%'
       




character = Select(title='Political', value='All', options=["All" ,"Rajoy", "Sanchez", "Iglesias", "Rivera"])
pol_par = Select(title='Politic Party', value='All', options=["All" ,"PP", "PSOE", "Podemos", "Ciudadanos"])
k_w = TextInput(value='', title='Keywords')



for widget in [character, pol_par, k_w]:
    widget.on_change('value', update)


layout = layout([
    [row(column(widgetbox(character, pol_par, k_w),barchar1,barchar2), column(plot_P, plot_NEU, plot_N))],
])


curdoc().theme = theme_doc
curdoc().add_root(layout)
curdoc().title = "Twitter Debate13J"
