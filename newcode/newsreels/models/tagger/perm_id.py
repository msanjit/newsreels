#!/usr/bin/env python
# coding: utf-8

# In[27]:


import sys
import json
sys.path.append("")
import dslib
dslib.setup.load_env()
certify - Dependency for requests.
ms.version.addpkg("certifi","2019.6.16")
import requests


def get_permid_response(url=None, api_key=None, proxies=None):
    proxies = {"http" : "http://proxy-app.ms.com:8080", "https" : "https://proxy-app.ms.com:8080"} if proxies is None else proxies
    api_key = "1tuJRbkEEOJ5SyERevb9pk5oDDVjQ4AQ" if api_key is None else api_key
    headers = {'Accept' : "application/ld+json", 'x-ag-access-token': "1tuJRbkEEOJ5SyERevb9pk5oDDVjQ4AQ"}
    trit_response = requests.request("GET", url, headers=headers, proxies=proxies)
    
    #convert the response to a json object.
    trit_json_response = json.loads(trit_response.content.decode('utf-8'))
    
    return trit_json_response


def parse_permid_entity(url):
    trit_response = get_permid_response(url)
    permid_dict = {}
    permid_detail_dict = {}
    organization_detail_dict = {}
    primary_instrument = {}
    primary_quote = {}
    
    
    if "tr-common:hasPermId" in trit_response:        
        organization_detail_dict["PermID"] = trit_response["tr-common:hasPermId"]
        
    if "hasHoldingClassification" in trit_response:
        organization_detail_dict["Public"] = 'Yes' if 'tr-org:publiclyHeld' in trit_response['hasHoldingClassification'] else 'No'
    if "hasActivityStatus" in trit_response:
        organization_detail_dict["Status"] = 'Active' if 'tr-org:statusActive' in trit_response['hasActivityStatus'] else 'Not Active'  
    if "hasIPODate" in trit_response:
        organization_detail_dict["IPO Date"] = trit_response['hasIPODate'].split('T')[0]  
    if "hasLatestOrganizationFoundedDate" in trit_response:
        organization_detail_dict["Latest Date of Incorporation"] = trit_response['hasLatestOrganizationFoundedDate'].split('T')[0]    
    if "tr-org:hasLEI" in trit_response:
        organization_detail_dict["LEI"] = trit_response['tr-org:hasLEI']
    if "hasPrimaryBusinessSector" in trit_response:
        organization_detail_dict["Primary Industry"] = get_permid_response(trit_response['hasPrimaryBusinessSector'])['prefLabel']
    if "hasPrimaryIndustryGroup" in trit_response:
        organization_detail_dict["Primary Business Sector"] = get_permid_response(trit_response['hasPrimaryIndustryGroup'])['prefLabel']
    if "hasPrimaryEconomicSector" in trit_response:
        organization_detail_dict["Primary Economic Sector"] = get_permid_response(trit_response['hasPrimaryEconomicSector'])['prefLabel'] 
    if "isDomiciledIn" in trit_response:
        organization_detail_dict["Domiciled In"] = trit_response['isDomiciledIn']
    if "isIncorporatedIn" in trit_response:
        organization_detail_dict["Incorporated In"] = trit_response['isIncorporatedIn']
    if "hasURL" in trit_response:
        organization_detail_dict["Website"] = trit_response['hasURL'] 
    if "mdass:HeadquartersAddress" in trit_response:
        organization_detail_dict["HQ Address"] = trit_response['mdass:HeadquartersAddress'] 
    if "tr-org:hasHeadQuartersPhoneNumber" in trit_response:
        organization_detail_dict["HQ Phone"] = trit_response['tr-org:hasHeadQuartersPhoneNumber'] 
    if "mdass:RegisteredAddress" in trit_response:
        organization_detail_dict["Registered Address"] = trit_response['mdass:RegisteredAddress'] 
    if "mdass:RegisteredAddress" in trit_response:
        organization_detail_dict["Registered Address"] = trit_response['mdass:RegisteredAddress']          
    if "vcard:organization-name" in trit_response:
        organization_detail_dict["Organization Name"] = trit_response['vcard:organization-name']   
        
    if "hasPrimaryInstrument" in trit_response:
        hasPrimaryInstrument = get_permid_response(trit_response['hasPrimaryInstrument'])
        if 'tr-common:hasName' in hasPrimaryInstrument:
            primary_instrument['Instrument Name'] = hasPrimaryInstrument['tr-common:hasName']
        if 'hasAssetClass' in hasPrimaryInstrument:
            hasAssetClass = get_permid_response(hasPrimaryInstrument['hasAssetClass'])
            if 'skos:prefLabel' in hasAssetClass:
                primary_instrument['Instrument Type'] = hasAssetClass['skos:prefLabel']
    if "hasOrganizationPrimaryQuote" in trit_response:
        hasOrganizationPrimaryQuote = get_permid_response(trit_response['hasOrganizationPrimaryQuote'])
        if 'tr-fin:hasRic' in hasOrganizationPrimaryQuote:
            primary_quote['RIC'] = hasOrganizationPrimaryQuote['tr-fin:hasRic']
        if 'tr-fin:hasExchangeTicker' in hasOrganizationPrimaryQuote:
            primary_quote['Ticker'] = hasOrganizationPrimaryQuote['tr-fin:hasExchangeTicker']
        if 'tr-fin:hasMic' in hasOrganizationPrimaryQuote:
            primary_quote['MIC'] = hasOrganizationPrimaryQuote['tr-fin:hasMic']
        if 'tr-fin:hasExchangeCode' in hasOrganizationPrimaryQuote:
            primary_quote['Exchange'] = hasOrganizationPrimaryQuote['tr-fin:hasExchangeCode']     
    permid_detail_dict.update(organization_detail_dict)
    permid_detail_dict.update(primary_instrument)
    permid_detail_dict.update(primary_quote)
    permid_dict['OrganizationDetails'] = organization_detail_dict
    permid_dict['Primary Instrument'] = primary_instrument
    permid_dict['Primary Quote'] = primary_quote
    print ("permid_detail_dict",permid_dict)
    return permid_detail_dict


# In[56]:


if __name__ == "__main__":
    parse_permid_entity('https://permid.org/1-4295907168')






