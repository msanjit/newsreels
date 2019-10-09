import refinitiv
import fuzzywuzzy
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 

def getRelevantNewsArticles(news_articles,client_data):
    client_tags=getClientProfile(client_data)
    news_relevance_list=[]
    
    for news in news_articles:
        news_relevance={}
        news_relevance['id']=news['id']
        news_tags=getNewstagswithRelevance(news['text'])
        matching_choices=news_tags.keys()
        total_relevance_of_article=0.0
        for tag in client_tags:
    
            match=process.extractOne(tag, matching_choices)
            if match[1]>70:
                news_tag_relevance=float(news_tags[match[0]])
                total_relevance_of_article=total_relevance_of_article+(match[1]/100)*(news_tag_relevance)
           
            
        news_relevance['relevance']=total_relevance_of_article
        news_relevance_list.append(news_relevance)
    return sorted(news_relevance_list, key = lambda x : x['relevance'],reverse=True)

def getClientProfile(client_data):
    client_tags=[]
    for key in client_data.keys():
        client_tags.append(client_data[key])
    return client_tags

#captures all news tags and relevance in dict
def getNewstagswithRelevance(data):
    result=refinitiv.tag(url='https://api.thomsonreuters.com/permid/calais',api_key='1tuJRbkEEOJ5SyERevb9pk5oDDVjQ4AQ',content=data)
    #bring all the details in one array
    news_tags={}
    for key in result.keys():
        for val in result[key]:
            if 'relevance' in val.keys():
                news_tags[val['name']]=val['relevance']
            else:
                news_tags[val['name']]=val['score']
    return news_tags
