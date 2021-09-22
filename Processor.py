#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dateutil
import pandas as pd


# defining methods for shortening

def shorten(obj):
    obj.rename(columns = {'East Coast (PADD 1) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD1',
                     'Midwest (PADD 2) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD2',
                     'Gulf Coast (PADD 3) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD3',
                     'Rocky Mountain (PADD 4) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD4', 
                     'West Coast (PADD 5) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD5',
                    'Total US Refinery Net Input of Crude Oil':'TotalPADD'
                    }, inplace=True)
    
def unshorten(obj):
    obj.rename(columns = {'PADD1':'(PADD 1) Refinery and Blender Net Input of Crude Oil',
                     'PADD2':'(PADD 2) Refinery and Blender Net Input of Crude Oil',
                    'PADD3': '(PADD 3) Refinery and Blender Net Input of Crude Oil',
                   'PADD4':  '(PADD 4) Refinery and Blender Net Input of Crude Oil', 
                   'PADD5':  '(PADD 5) Refinery and Blender Net Input of Crude Oil',
                  'TotalPADD':  'Total US Refinery Net Input of Crude Oil'
                    }, inplace=True)

# In[2]:


# reading excel
df = pd.read_excel('PET_PNP_INPT_A_EPC0_YIR_MBBL_M.xls',sheet_name = 'Data 1', index_col=0)


# In[3]:


# Removing non PADD columns
df = df.loc[:,df.loc['Sourcekey'].str.contains('MCRRIP') | df.loc['Sourcekey'].str.contains('MCRRIUS1')  ]


# In[4]:


# setting column name for date 

df = df.rename(columns=df.iloc[1]).drop(df.index[0])
df = df.iloc[1:].reset_index().rename(columns= {'Back to Contents':'Date'})


# In[5]:


# removing older data than Jan 2016
df = df[df.Date > dateutil.parser.parse("2016-01-01")]

# extracting month and year 
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year
df['Quarter'] = df['Date'].dt.to_period('Q')


# In[6]:


# shortening the column names
df.rename(columns = {'East Coast (PADD 1) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD1',
                     'Midwest (PADD 2) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD2',
                     'Gulf Coast (PADD 3) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD3',
                     'Rocky Mountain (PADD 4) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD4', 
                     'West Coast (PADD 5) Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'PADD5',
                    'U.S. Refinery and Blender Net Input of Crude Oil (Thousand Barrels)':'TotalPADD'
                    }, inplace=True)



# In[7]:


# reordering columns

order = [8,9,7,2,3,4,5,6,1] # setting column's order
df = df[[df.columns[i] for i in order]]



# In[8]:


df1 = df.groupby('Quarter')['PADD1', 'PADD2', 'PADD3', 'PADD4', 'PADD5', 'TotalPADD'].sum()


# In[9]:


unshorten(df1)



# In[10]:


df2 = df.groupby('Year')['PADD1', 'PADD2', 'PADD3', 'PADD4', 'PADD5', 'TotalPADD'].sum()


# In[11]:


unshorten(df2)



# In[12]:


# All units in thousand barrels
unshorten(df)

df.to_csv(r'Monthly.csv', index = False)
df1.to_csv(r'Quarterly.csv')
df2.to_csv(r'Annual.csv')

