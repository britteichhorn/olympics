#!/usr/bin/env python
# coding: utf-8

# # Import packages
# 
# 

# In[2]:


#pip install session-info


# In[3]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import streamlit as st

import session_info
session_info.show()


# # Load data 

# In[48]:


##https://www.kaggle.com/arjunprasadsarkhel/2021-olympics-in-tokyo
athletes = pd.read_excel('Athletes.xlsx')
coaches = pd.read_excel('Coaches.xlsx')
entries_gender = pd.read_excel('EntriesGender.xlsx')
medals = pd.read_excel('Medals.xlsx')
teams = pd.read_excel('Teams.xlsx')


# # Barplot with dropdown
# 

# In[ ]:


fig = go.Figure()
#Make a bar plot for each color of a medal
for medal in ['Gold','Silver', 'Bronze']:
    fig.add_trace(go.Bar(x = medals['Team/NOC'], y = medals[medal]))
#Make the dropdown buttons
    dropdown_buttons = [
    {'label':'Gold medals','method':'update', 'args':[{'visible':[True, False, False]},{'title':'Gold medals'}]},
    {'label':'Silver medals', 'method':'update','args':[{'visible':[False,True,False]},{'title': 'Silver medals'}]},
    {'label':'Bronze medals', 'method':'update','args':[{'visible':[False,False,True]},{'title': 'Bronze medals'}]}]
#add the dropdown to the figure
fig.update_layout({'updatemenus':[{'type':'dropdown','x':1.3, 'y':0.5, 'showactive':True, 'active':0, 
                                   'buttons': dropdown_buttons}]})
#show the plot in streamlit
st.plotly_chart(fig)


# # Bar plot with slider

# In[ ]:


fig = px.histogram(athletes,title="Number of participants per discipline", x="Discipline", 
                   color='Discipline',animation_frame="NOC", 
                   animation_group="Discipline").update_xaxes(categoryorder='total descending')
fig.update_layout(height=800, width=1000, bargap=0.1, bargroupgap=0.1, xaxis = dict(
tickfont = dict(size=13)),yaxis = dict(
tickfont = dict(size=13)))
fig["layout"].pop("updatemenus")
st.plotly_chart(fig)


# # Bar plot with the number of athletes for each discipline

# In[ ]:


fig = px.histogram(athletes, x='Discipline', color='Discipline', labels={'x':'total_bill', 'y':'count'})

fig.update_layout(title='Discipline', title_x=0.5)
st.plotly_chart(fig)


# # Map with the number of coaches for each country

# In[ ]:


coaches_NOC = coaches.groupby('NOC')['Discipline'].count()


# In[ ]:


fig = go.Figure(data=go.Choropleth(
locations = coaches_NOC.keys(),
locationmode = 'country names',
z = coaches_NOC,
text = coaches_NOC.keys(),
colorscale = 'viridis',
autocolorscale=False,
reversescale=True,
marker_line_color='darkgray',
marker_line_width=0.5,
colorbar_title = 'Disciplines',
))
#Give the figure a title and change the size
fig.update_layout(title = 'The amount of Coaches every country participated in ', title_x = 0.5,)
st.plotly_chart(fig)



# # Bar plot with the number of disciplines for each country

# In[ ]:


#Make a copy
teams_temp = teams.copy()


# In[ ]:


#Delete the rows with the same discipline and NOC
teams_data = teams_temp.drop_duplicates(subset=['Discipline', 'NOC'])


# In[ ]:


#Group by per discipline and NOC en count them together
teams_Dis_Noc = teams_data.groupby('Discipline')['NOC'].count()


# In[ ]:


fig = px.bar(teams_Dis_Noc)
#Give a title and add a label to the y-axis
fig.update_layout(title = 'The amount of countries participating in each Discipline', title_x = 0.5,
yaxis_title = 'Countries', showlegend=False
)
st.plotly_chart(fig)


# # Map with the number of disciplines for each country

# In[ ]:


#Group by per NOC and discipline and count them together
teams_Noc_Dis = teams_data.groupby('NOC')['Discipline'].count()


# In[ ]:


fig = go.Figure(data=go.Choropleth(
locations = teams_Noc_Dis.keys(),
locationmode = 'country names',
z = teams_Noc_Dis,
text = teams_Noc_Dis.keys(),
colorscale = 'viridis',
autocolorscale=False,
reversescale=True,
marker_line_color='darkgray',
marker_line_width=0.5,
colorbar_title = 'Disciplines',
))#Give the figure a title and change the size
fig.update_layout(title = 'The amount of Disciplines every country participated in ', title_x = 0.5,
)
st.plotly_chart(fig)


# # Pie chart with checkbox for the number of medals for each country

# In[ ]:


st.title('Medals')
check = st.checkbox('Total medals') #Checkbox for the total medals per country
if check: #if the checkbox is checked
    #making the pie with total for each team
    fig = px.pie(medals, values = 'Total', names = 'Team/NOC', title = 'Total of medals for each country') 
    #Put the percent with the country inside the pie
    fig.update_traces(textposition = 'inside', textinfo = 'percent+label' )
    st.plotly_chart(fig)

check2 = st.checkbox('Gold medals') #Checkbox for the number of gold medals per country
if check2:
    fig = px.pie(medals, values = 'Gold', names = 'Team/NOC', title = 'Gold of medals for each country')
    fig.update_traces(textposition = 'inside', textinfo = 'percent+label' )
    st.plotly_chart(fig)
          
check3 = st.checkbox('Silver medals') #Checkbox for the number of silver medals per country
if check3:
    fig = px.pie(medals, values = 'Silver', names = 'Team/NOC', title = 'Silver of medals for each country')
    fig.update_traces(textposition = 'inside', textinfo = 'percent+label' )
    st.plotly_chart(fig)
    
check4 = st.checkbox('Bronze medals') #Checkbox for the number of bronze medals per country
if check4:
    fig = px.pie(medals, values = 'Total', names = 'Team/NOC', title = 'Bronze of medals for each country')
    fig.update_traces(textposition = 'inside', textinfo = 'percent+label' )
    st.plotly_chart(fig)

