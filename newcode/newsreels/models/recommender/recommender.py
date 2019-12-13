#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import json
sys.path.append()
import dslib
import dslib.setup()
dslib.setup.load_env()
import ms.version
import argparse
import logging
import itertools
import pandas as pd
import re
sys.getdefaultencoding()
import argparse
import json
import csv
ms.version.addpkg("fuzzywuzzy","0.17.0")
import fuzzywuzzy as fw
from fuzzywuzzy import fuzz, process
import os
import numpy as np

file_path = globals()["__file__"]





def get_news_profile(news_article, products_list, sectors_list, location_list, column_mapping):
    #create a df in the same format as client profiles
    column_all = list(column_mapping['original_list'].values)
    column_all.insert(0, 'article_name')
    df = pd.DataFrame(columns=columns_all)
    #for art_nm in news_article['article_name'].unique()
    for art_nm in news_article.keys():
        sectors = {}
        products = {}
        locations = {}
        news_art = news_article[art_nm]
        df_sectors = news_art[(news_art['_type'].isin(['IndustryTerm']))].reset_index()
        df_sectors_topics = news_art[(news_art['_typeGroup'].isin(['topics']))].reset_index()
        df_products = news_art[(news_art['_type'].isin(['Company']))].reset_index()
        df_locations = news_art[(news_art['_type'].isin(['City'])) | (news_art['_type'].isin(['ProvinceOrState']))].reset_index()

        #get relevence and relevant tags of refinitiv into dictionary
        for i in df_sectors.index:
            sectors[df_sectors['name'][i]] = df_sectors['relevence'][i]
        for i in df_sectors_topics.index:
            sectors[df_sectors_topics['name'][i].replace("_"," ").replace("Business", "")] = df_sectors_topics['score'][i]            
        for i in df_products.index:
            products[df_sectors['name'][i]] = df_products['relevence'][i]
        for i in df_locations.index:
            locations[df_locations['name'][i]] = df_locations['relevence'][i]
            
        #apply fuzzy matching & store in dictionaries
        sector_dict ={}
        product_dict = {}
        location_dict = {}
        for sector in sectors.keys():
            match = process.extractOne(sector, sectors_list)
            if match[1] > 70:
                sector_dict[match[0]] = sector
        for product in products.keys():
            match = process.extractOne(product, products_list)
            if match[1] > 70:
                product_dict[match[0]] = product
        for location in locations.keys():
            match = process.extractOne(location, location_list)
            if match[1] > 70:
                location_dict[match[0]] = location   
                
        #Create a dictionary with matched tags
        df_dict = {}
        df_dict1 = {}
        for i in product_dict.keys():
            df_dict[i] = products.get(product_dict.get(i))
        for i in sector_dict.keys():
            df_dict[i] = sectors.get(sector_dict.get(i))
        for i in location_dict.keys():
            df_dict[i] = locations.get(location_dict.get(i))  
            
            
        for i in df_dict.keys():
            new_key = column_mapping.loc[column_mapping['refined_list'] == i].iloc[0]['original_list']
            df_dict[i] = new_key
            
        for old, new in df_dict1.items():
            df_dict[new] = df_dict.pop(old)
            
        df2 = pd.DataFrame(data=None, columns = df.columns)
        df2 = df2.append(pd.series(), ignore_index=True)
        
        for i in df_dict.keys():
            for col in df2.columns:
                if (col == i):
                    df2.loc[0, col] = np.float32(df_dict.get(i))
        df2['article_name'] = art_nm
        df2 = df2.fillna(0.0)
        df = df.append(df2)
    return df



#This function Create one time static list sector, product, location_list and column mapping
def createFeaturelist(sector_profile_df, product_profile_df):
    sectors = sector_profile_df['sector'].unique()
    sectors = [str(a) for a in sectors]
    char_list = ['LTD', 'INC', 'CORP', 'HLDG', 'CO', 'GROUP', '&', '  '," ",'INFORMATION', 'SERVICES']
    sectors_list = [a.strip() for a in sectors]
    for i, v in enumerate(sectors_list):
        sectors_lis[i] = re.sub("|".join(char_list), "", v)
    products = product_profile_df['nme_scy'].unique()
    products = [str(a) for a in products]
    products_list = [a.strip() for a in products]
    for i, v in enumerate(products_list):
        products_list[i] = re.sub("|".join(char_list), "", v)
    state = product_profile_df['txt_st_desc'].unique()
    city = product_profile_df['nme_city'].unique()
    original_loc = [str(a) for a in state] + [str(a) for a in city]
    location_list = [str(a).strip() for a in state] + [str(a).strip() for a in city]
    original_loc = [x for x in original_loc if x !='nan']
    location_list = [x for x in location_list if x != 'nan']
    refined_list = sectors_list + products_list + location_list
    original_list = sectors + products + original_loc
    d = {'refined_list' : refined_list, 'original_list':original_list}
    column_mapping = pd.DataFrame(d, columns = ['refined_list', 'original_list'])
    return sectors_list, products_list, location_list, column_mapping
                                                        
                                               
    
    






