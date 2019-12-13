#!/usr/bin/env python
# coding: utf-8

# In[7]:


import sys
import os
sys.path.append('')
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



file_path = globals()["__file__"]



#File path for client sector profile view
sector_profile_view_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(filepath)))),
                                       "data/client/new_sector_profile_view_shortlisted_clients.csv")
product_profile_view_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(filepath)))),
                                       "data/client/new_product_profile_view_shortlisted_clients.csv")
shortlisted_client_profile_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(filepath)))),
                                       "data/client/shortlisted_client_profile.csv")



#To retrieve client unique IDS
def get_client_ids():
    client_s = pandas.read_csv(sector_profile_view_file)
    return list(client_s["idn_party"].unique())




#Retrieve sector view for a given client.
def get_client_sectors(client_id):
    sectors = pandas.read_csv(sector_profile_view_file)
    client_sector = sectors[sectors["idn_party"] == client_id]
    return client_sector



#Retrieve product view for a given client.
def get_client_products(client_id):
    products = pandas.read_csv(product_profile_view_file)
    client_product = products[products["idn_party"] == client_id]
    return client_product



#To retrieve shortlisted full profile having product, sector and location info
def client_profile(client_id):
    sector_profile_df = pandas.read_csv(sector_profile_view_file)
    product_profile_df = pandas.read_csv(product_profile_view_file)
    shortlisted_client_profile = pandas.read_csv(shortlisted_client_profile_file)
    shortlisted_client_profile = shortlisted_client_profile[shortlisted_client_profile["idn_party"] == client_id]
    return shortlisted_client_profile, sector_profile_df, product_profile_df





