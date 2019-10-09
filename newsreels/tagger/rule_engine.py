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
        print('news_id',news['id'])
        print('matching_choices',matching_choices)
        total_relevance_of_article=0.0
        for tag in client_tags:
    
            match=process.extractOne(tag, matching_choices)
            print(match)
            if match[1]>70:
                news_tag_relevance=float(news_tags[match[0]])
                print(type(match[1]/100))
                print(type(news_tag_relevance))
                total_relevance_of_article=total_relevance_of_article+(match[1]/100)*(news_tag_relevance)
            else:
                print('didnot contribute to article relvance', match[0])
            print(type(process.extractOne(tag, choices)))
        news_relevance['relevance']=total_relevance_of_article
        news_relevance_list.append(news_relevance)
        print(total_relevance_of_article)
        
    return sorted(relevance_list, key = lambda x : x['relevance'],reverse=True)
	
def getClientProfile(client_data):
    client_tags=[]
    for key in client_data.keys():
        print(client_data[key])
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
                print(val['name'],val['relevance'])
                news_tags[val['name']]=val['relevance']
            else:
                print(val['name'],val['score'])
                news_tags[val['name']]=val['score']

    print(news_tags)
    return news_tags
	
if __name__ == '__main__':
    news_articles=[]
news_article={}
news_article['id']="article_123"
news_article['text']="""Hong Kong’s embattled leader Carrie Lam said on Tuesday her administration had no plans to use colonial-era emergency powers to introduce new laws, after a long weekend of violent protests saw widespread defiance of a ban on face masks.
    Despite the violence, and the first interaction between Chinese troops stationed in the territory and the protesters, Lam said Hong Kong was equipped to handle the situation on its own, as it braced for more demonstrations through the week.
    Lam’s comments came as the Asian financial hub got back to work after the weekend, with its metro rail system only partially functioning and authorities warning residents they may have trouble commuting due to widespread vandalism of infrastructure.
    Speaking at a weekly news conference, Lam said tourist numbers had fallen sharply and the impact on the city’s third quarter economic data of the protests, which have been going on for about four months, would “surely be very bad”.
    She appealed to property developers and landlords to offer relief to retailers whose businesses had been hit. 
    “For the first six days of October, during the so-called Golden Week holiday, visitors visiting Hong Kong plunged over 50%,” she said. Retail, catering, tourism and hotels had been severely hit, with some 600,000 people affected, she added.
    The protests, which show no sign of abating, pose the biggest popular challenge to Chinese President Xi Jinping since he came to power in 2012 and are Hong Kong’s thorniest political crisis since Britain returned it to China in 1997.
    What started as opposition to a now-withdrawn extradition bill has grown into a pro-democracy movement against what is seen as Beijing’s increasing grip on the city, which protesters say undermines a “one country, two systems” formula promised when Hong Kong returned to Chinese rule in 1997.
    China dismisses such accusations, saying foreign governments, including Britain and the United States, have fanned anti-China sentiment.
    U.S. President Donald Trump said on Monday that if anything bad happened in Hong Kong it would be bad for the U.S.-China trade talks.
    And an increasing number of U.S. lawmakers voiced anger on Monday over the National Basketball Association’s response to a Houston Rockets official’s tweet backing the protests.
    Lam, who has said she must serve both the central government and the people of Hong Kong, was in Beijing last week for Oct. 1 National Day celebrations but said she did not meet any central government officials to discuss “business”.
    Asked under what circumstances she would call upon Beijing for help to quell the protests, Lam said Hong Kong should be able to find solutions on its own to manage the crisis.
    “I cannot tell you categorically now under what circumstances we will do extra things, including ... calling on the central government to help,” she said.updating
    On Sunday, personnel inside a People’s Liberation Army barracks in the territory issued warnings to protesters who had shined laser pointers at the building. It was the first time the Chinese military had engaged with the demonstrators.
    On Friday, Lam invoked the emergency powers for the first time in more than 50 years to outlaw face masks, which protesters have used to shield their identities.
    But the move inflamed demonstrations over the weekend and thousands took to the streets wearing masks in defiance. Rallies  deteriorated into running clashes with police firing tear gas and charging with batons to disperse protesters across the city.
    Two teenage protesters have been shot and wounded, one in the chest and the other in the leg, during skirmishes with police in some of the recent violence.
    ATMs, Chinese banks and scores of shops were vandalized during protests over the long weekend. Many restaurants and malls closed early over what is typically a very busy holiday period.
    Hong Kong’s metro, which carries about 5 million passengers a day, said on Tuesday some stations would not open for service because damaged facilities needed to be repaired. Train service would also end at 8 p.m. (1200 GMT), more than four hours earlier than normal.
    MTR was forced to shut down in an unprecedented move after arson attacks on Friday night and only partially operated during the weekend, with protesters again setting stations ablaze and destroying ticketing machines. The closures largely paralyzed transportation.
    Lam said it was too early to say whether the mask ban would be ineffective and urged youth not to participate in what she called political actions.
    The anti-mask law is also applicable in schools and universities, with the Education Bureau asking secondary schools to inform how many students wear masks to school on Tuesday, the first day of classes since the ban was implemented.
    Lam, who is due to give a policy address next week, said it would not be the “usual comprehensive” address due to her team’s preoccupation with the situation. She did not elaborate."""
	news_article1={}
	news_article1['id']="article_456"
	news_article1['text']="""
	The beauty of being a private company is you get to make up your own value when you've run out of investors to pump in 
	more cash. Vice is paying about $400 million of mostly stock for Refinery, a digital media company focused on women's fashion, 
	beauty and entertainment. The only two companies that needed to agree on value with this deal are Vice and Refinery29. 
	Perhaps Vice thinks Refinery29 is actually worth $100 million and Refinery29 thinks Vice is worth $900 million. That's OK. 
	They just agreed to publicly inflate each other by 4x. The stock isn't traded on a public exchange. 
	At this point, while the relative values are meaningful, the overall value is virtually meaningless. I live in florida, and texas was my birth place. 
	I am very much interested in Morgan Stanley's stocks.
	"""
	news_articles.append(news_article1)
	news_articles.append(news_article)
	client_data={'residence':'Illinois', 'top1':'morgan','top2':'Davis new york Venture','top3':'ishare core high dividend etf','top4':'ishare select high dividend etf','top5':'fulton FinL corp PA'}
	relevance_list=getRelevantNewsArticles(news_articles,client_data)
	print('relevance_list',relevance_list)
