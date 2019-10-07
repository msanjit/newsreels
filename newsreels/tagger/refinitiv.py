# TAGGER MODULE - Intelligent Tagging using Refinitiv API
# tag(url=None,api_key=None,content=None,headType="text/raw")
# url = "https://api.thomsonreuters.com/permid/calais"
# api_key = "1tuJRbkEEOJ5SyERevb9pk5oDDVjQ4AQ"

# INPUT PARAMETERS - 
    # url : refinitiv url
    # api_key : refinitiv api token
    # content : news article (text)
    # headType="text/raw" (for text data)
# OUTPUT - 
    # entity_tags : Dictionary
        # entity_tags['topic']          
        #entity_tags['region']
        #entity_tags['organization']
        #entity_tags['person']
        #entity_tags['industry']
        #entity_tags['market_index']
        #entity_tags['currency']
     

        
#Import required libraries
import requests
import json


# tagger function
def tag(url=None,api_key=None,content=None,headType="text/raw"):   
    # Open Calais/hosted Intelligent Tagging
    token = api_key
    #url = "https://api.thomsonreuters.com/permid/calais"
    payload = contentText.encode('utf8')
    #Provide the Output format Desired -- Mandatory Headers
    headers = {
        'Content-Type': headType,
        'X-AG-Access-Token': token,
        'outputformat': "application/json"
        }
    TRITResponse = requests.request("POST", url, data=payload, headers=headers)
    #Json Format
    TRITJsonResponse = TRITResponse.json()
    return entities_extraction(TRITJsonResponse) 


# Function that takes in a JSON Response and extracts the required entities.
# It returns a dictionary where each Key [Entity Type] is a list of dictionaries. 
def entities_extraction(TRITJsonResponse):
    entity_tags={}
    topics_list=[]
    geographical_list=[]
    organizations_list=[]
    industries_list=[]
    persons_list=[]
    currencies_list=[]
    market_indexes=[]

    #Read each entity from JSON Response and extract relevant tags
    for entity in TRITJsonResponse:
        for info in TRITJsonResponse[entity]:
            topics={}
            geography={}
            organizations={}
            persons={}
            industries={}
            currencies={}
            market_index={}

            #Topics
            if(info=='_typeGroup' and str(TRITJsonResponse[entity][info])=='topics'):
                for companyinfo in (TRITJsonResponse[entity]):
                    if(companyinfo in ['_type','name','confidencelevel','score','relevance','permid']):
                        topics[companyinfo]=str(TRITJsonResponse[entity][companyinfo])
            if topics:
                topics_list.append(topics)


            #Geographical Locations
            if((info=='_type' and str(TRITJsonResponse[entity][info]) in ['Country','City','Continent','Region','ProvinceOrState'])):
                for companyinfo in (TRITJsonResponse[entity]):
                    if(companyinfo in ['_type','name','confidencelevel','score','relevance','permid']):
                        geography[companyinfo]=str(TRITJsonResponse[entity][companyinfo])
                    if(companyinfo=='resolutions'):
                        if('permid' in TRITJsonResponse[entity][companyinfo][0]):  
                            geography['permid']=str(TRITJsonResponse[entity][companyinfo][0]['permid'])
                        if('id' in TRITJsonResponse[entity][companyinfo][0]):  
                            geography['id']=str(TRITJsonResponse[entity][companyinfo][0]['id'])
                        if('score' in TRITJsonResponse[entity][companyinfo][0]):  
                            geography['score']=str(TRITJsonResponse[entity][companyinfo][0]['score'])
                        if('ticker' in TRITJsonResponse[entity][companyinfo][0]):
                            geography['ticker']=str(TRITJsonResponse[entity][companyinfo][0]['ticker'])
            if geography:
                geographical_list.append(geography)

            #Company
            if((info=='_type' and str(TRITJsonResponse[entity][info]) in ['Company','Organization'])):
                for companyinfo in (TRITJsonResponse[entity]):
                    if(companyinfo in ['_type','name','confidencelevel','score','relevance','permid']):
                        organizations[companyinfo]=str(TRITJsonResponse[entity][companyinfo])
                    if(companyinfo=='resolutions'):
                        if('permid' in TRITJsonResponse[entity][companyinfo][0]):  
                            organizations['permid']=str(TRITJsonResponse[entity][companyinfo][0]['permid'])
                        if('id' in TRITJsonResponse[entity][companyinfo][0]):  
                            organizations['id']=str(TRITJsonResponse[entity][companyinfo][0]['id'])
                        if('score' in TRITJsonResponse[entity][companyinfo][0]):  
                            organizations['score']=str(TRITJsonResponse[entity][companyinfo][0]['score'])
                        if('ticker' in TRITJsonResponse[entity][companyinfo][0]):
                            organizations['ticker']=str(TRITJsonResponse[entity][companyinfo][0]['ticker'])
            if organizations:
                organizations_list.append(organizations)


            #Industries
            if((info=='_type' and str(TRITJsonResponse[entity][info])=='IndustryTerm')):
                for companyinfo in (TRITJsonResponse[entity]):
                    if(companyinfo in ['_type','name','confidencelevel','score','relevance','permid']):
                        industries[companyinfo]=str(TRITJsonResponse[entity][companyinfo])
                    if(companyinfo=='resolutions'):
                        if('permid' in TRITJsonResponse[entity][companyinfo][0]):  
                            industries['permid']=str(TRITJsonResponse[entity][companyinfo][0]['permid'])
                        if('id' in TRITJsonResponse[entity][companyinfo][0]):  
                            industries['id']=str(TRITJsonResponse[entity][companyinfo][0]['id'])
                        if('score' in TRITJsonResponse[entity][companyinfo][0]):  
                            industries['score']=str(TRITJsonResponse[entity][companyinfo][0]['score'])
                        if('ticker' in TRITJsonResponse[entity][companyinfo][0]):
                            industries['ticker']=str(TRITJsonResponse[entity][companyinfo][0]['ticker'])    
            if industries:
                industries_list.append(industries)

            #Persons
            if((info=='_type' and str(TRITJsonResponse[entity][info])=='Person')):
                companies=[]
                for companyinfo in (TRITJsonResponse[entity]):
                    if(companyinfo in ['_type','name','confidencelevel','score','relevance','permid']):
                        persons[companyinfo]=str(TRITJsonResponse[entity][companyinfo])
                    if(companyinfo=='resolutions'):
                        if('permid' in TRITJsonResponse[entity][companyinfo][0]):  
                            persons['permid']=str(TRITJsonResponse[entity][companyinfo][0]['permid'])
                        if('id' in TRITJsonResponse[entity][companyinfo][0]):  
                            persons['id']=str(TRITJsonResponse[entity][companyinfo][0]['id'])
                        if('score' in TRITJsonResponse[entity][companyinfo][0]):  
                            persons['score']=str(TRITJsonResponse[entity][companyinfo][0]['score'])
                        if('ticker' in TRITJsonResponse[entity][companyinfo][0]):
                            persons['ticker']=str(TRITJsonResponse[entity][companyinfo][0]['ticker'])
            if persons:
                persons_list.append(persons)

            #Market Indexes
            if((info=='_type' and str(TRITJsonResponse[entity][info])=='MarketIndex')):
                for companyinfo in (TRITJsonResponse[entity]):
                    if(companyinfo in ['_type','name','confidencelevel','score','relevance','permid']):
                        market_index[companyinfo]=str(TRITJsonResponse[entity][companyinfo])
                    if(companyinfo=='resolutions'):
                        if('permid' in TRITJsonResponse[entity][companyinfo][0]):  
                            market_index['permid']=str(TRITJsonResponse[entity][companyinfo][0]['permid'])
                        if('id' in TRITJsonResponse[entity][companyinfo][0]):  
                            market_index['id']=str(TRITJsonResponse[entity][companyinfo][0]['id'])
                        if('score' in TRITJsonResponse[entity][companyinfo][0]):  
                            market_index['score']=str(TRITJsonResponse[entity][companyinfo][0]['score'])
                        if('ticker' in TRITJsonResponse[entity][companyinfo][0]):
                            market_index['ticker']=str(TRITJsonResponse[entity][companyinfo][0]['ticker'])
                if market_index:
                    market_indexes.append(market_index)


            #Currencies
            if((info=='_type' and str(TRITJsonResponse[entity][info])=='Currency')):
                for companyinfo in (TRITJsonResponse[entity]):
                    if(companyinfo in ['_type','name','confidencelevel','score','relevance','permid']):
                        currencies[companyinfo]=str(TRITJsonResponse[entity][companyinfo])
                    if(companyinfo=='resolutions'):
                        if('permid' in TRITJsonResponse[entity][companyinfo][0]):  
                            currencies['permid']=str(TRITJsonResponse[entity][companyinfo][0]['permid'])
                        if('id' in TRITJsonResponse[entity][companyinfo][0]):  
                            currencies['id']=str(TRITJsonResponse[entity][companyinfo][0]['id'])
                        if('score' in TRITJsonResponse[entity][companyinfo][0]):  
                            currencies['score']=str(TRITJsonResponse[entity][companyinfo][0]['score'])
                        if('ticker' in TRITJsonResponse[entity][companyinfo][0]):
                            currencies['ticker']=str(TRITJsonResponse[entity][companyinfo][0]['ticker'])
                if currencies:
                    currencies_list.append(currencies)


    entity_tags['topic']=topics_list            
    entity_tags['region']=geographical_list
    entity_tags['organization']=organizations_list
    entity_tags['person']=persons_list
    entity_tags['industry']=industries_list
    entity_tags['market_index']=market_indexes
    entity_tags['currency']=currencies_list
    
    return entity_tags
