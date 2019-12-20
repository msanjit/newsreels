import logging
import datetime
import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery
from elasticsearch import Elasticsearch
import json
import random
import azure.cosmos.cosmos_client as cosmos_client
import refinitive_config


#Create and configure logger
logging.basicConfig(filename="refinitive.log", format='%(asctime)s - %(message)s', level=logging.INFO, filemode='w')
#Creating an object
logger = logging.getLogger()


class RefinitiveNewsAPI(object):
    def __init__(self):
        self.index_name = refinitive_config.index_name
        self.cred = service_account.Credentials.from_service_account_info(refinitive_config.personal_cred)
        self.bigquery_client = bigquery.Client(project=refinitive_config.proj, credentials=self.cred)
        # Creating Elasticsearch connection through api gateway
        self.es_cred = Elasticsearch(
                            host=refinitive_config.ELASTICSEARCH_HOST,
                            port=443,
                            headers={'X-api-key': refinitive_config.ELASTICSEARCH_API_KEY},
                            use_ssl=True,
                            timeout=30
                        )
        self.cosmosdb_client = cosmos_client.CosmosClient(refinitive_config.cosmos_endpoint, {'masterKey': refinitive_config.cosmos_primarykey})

    def cosmosdb(self, data):
        self.cosmosdb_client.UpsertItem("dbs/" + refinitive_config.cosmos_database_id + "/colls/" + refinitive_config.container_id, data)

    def show_stats(self, index, doc_type, field):
        '''Show basic statistics for a specific index'''
        res = es.search(index=index, doc_type=doc_type, body={
            "aggs": {
                "date_stats": {"stats":{"field": field } }
            }
        })
        print("Count: %d\nEarliest: %s\nLatest: %s"%(res['aggregations']['date_stats']['count'],res['aggregations']['date_stats']['min_as_string'],res['aggregations']['date_stats']['max_as_string']))


    def news_elastic_to_df(self, res):
        '''takes a json object (result from elasticsearch query)
        from news archive and returns a dataframe'''
        res_df = None
        res_df = pd.DataFrame.from_dict([
            {'body': i['_source']['data']['body'],
             'mimeType': i['_source']['data']['mimeType'],
             'dt2_strt_news': i['_source']['data']['firstCreated'].split('T')[0],
             'versionCreated': i['_source']['data']['versionCreated'],
             # 'dt2_strt_news': i['_source']['data']['firstCreated'].split(' ')[0]
             }
            for i in res['hits']['hits']
        ])
        return res_df


    def news_elastic_to_json(self, res):
        '''takes a json object (result from elasticsearch query)
        from news archive and returns a dataframe'''
        res_json = None
        res_json = [
            {'body': i['_source']['data']['body'],
             'mimeType': i['_source']['data']['mimeType'],
             'dt2_strt_news': i['_source']['data']['firstCreated'].split('T')[0],
             'versionCreated': i['_source']['data']['versionCreated'],
             # 'dt2_strt_news': i['_source']['data']['firstCreated'].split(' ')[0]
             }
            for i in res['hits']['hits']
        ]
        return res_json

    def get_news_id(self, start_date):
        end_date = start_date + datetime.timedelta(days = 1)
        query_news_id = " SELECT NEWS.id FROM `tr-data-workbench.TRNA.news` AS NEWS LEFT JOIN \
                        `tr-data-workbench.TRNA.scores` AS SCORES ON NEWS.id = SCORES.id \
                            WHERE NEWS.feedTimestamp BETWEEN '" + str(start_date) + "' AND '" + str(end_date) + "' "
        df_news_ids = self.bigquery_client.query(query_news_id).to_dataframe()
        return df_news_ids

    def get_all_news_metadata(self, start_date):
        end_date = start_date + datetime.timedelta(days=1)
        query_news_metadata = "SELECT NEWS.*, SCORES.* EXCEPT (amerTimestamp, apacTimestamp, emeaTimestamp, id) FROM \
           `tr-data-workbench.TRNA.news` AS NEWS LEFT JOIN `tr-data-workbench.TRNA.scores` AS SCORES ON NEWS.id = SCORES.id \
            WHERE NEWS.feedTimestamp BETWEEN '" + str(start_date) + "' AND '" + str(end_date) + "' "
        df_news_metadata = self.bigquery_client.query(query_news_metadata).to_dataframe().to_json(orient='records')
        df_news_metadata = json.loads(df_news_metadata)
        return df_news_metadata




    def get_news_metadata(self, news_id):

        sql_qry = "SELECT NEWS.*, SCORES.* EXCEPT (amerTimestamp, apacTimestamp, emeaTimestamp, id) \
            FROM `tr-data-workbench.TRNA.news` AS NEWS LEFT JOIN `tr-data-workbench.TRNA.scores` AS SCORES " \
            "ON NEWS.id = SCORES.id WHERE NEWS.id = '" + news_id + "'"
        # trna_df_all_updates = pandas_gbq.read_gbq(sql_qry, project_id="tr-data-workbench", credentials=self.cred, dialect='standard')
        trna_df_all_updates = json.loads(self.bigquery_client.query(sql_qry).to_dataframe())
        print("trna_df_all_updates", trna_df_all_updates)
        return trna_df_all_updates


    def get_newsbody(self, news_id):
        print("news_id *****************", news_id)
        res = None
        news_df = None
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "data.id": {
                                    "query": news_id
                                }
                            }
                        }
                    ]
                }
            }
        }
        res = self.es_cred.search(index=self.index_name, body=query)
        print ("res",res)
        news_df = self.news_elastic_to_json(res)
        print("news_df", news_df)
        return news_df

    def generatenews_json(self, date_list):
        print("mydates", mydates)
        for date in date_list[:5]:
            print("date", str(date))
            df_news_metadatas = self.get_all_news_metadata(date)
            for df_news_metadata in df_news_metadatas:
                print("df_news_metadata", df_news_metadata)

                news_id = df_news_metadata['id']
                print("news_id", news_id)
                news_body_df = refinitive.get_newsbody(news_id)
                print("news_body_df", news_body_df)
                # df_news_metadata.update(news_body_df[0])
                # self.cosmosdb(df_news_metadata)

if __name__ == "__main__":
    refinitive = RefinitiveNewsAPI()
    startdate = '2017-10-31'
    enddate =  '2017-11-01'

    mydates = pd.date_range(startdate, enddate).tolist()
    print ("mydates",mydates)
    refinitive.generatenews_json(mydates)
    # for date in mydates[:1]:
    #     print("date",str(date))
    #     df_news_ids = refinitive.get_news_id(date)
    #     for df_news_id in df_news_ids['id']:
    #         print("df_news_id", df_news_id)
    #         trna_df_all_updates = refinitive.get_news_metadata(df_news_id)
    #
    #         news_body_df = refinitive.get_newsbody(df_news_id)
    #         new_all_df = pd.concat([trna_df_all_updates, news_body_df], axis=1)
    #         new_all_json = json.loads(new_all_df.to_json(orient='records'))
    #
    #         print("new_all_json ***", type(new_all_json))
    #         print ("*********111111***********")
    #         refinitive.cosmosdb(new_all_json[0])
    #         break
    #     print("df_news_ids", str(len(df_news_ids)))