import sys
import config
import json
from googleapiclient.discovery import build

api_key = config.api_key
cse_id = config.cse_id
service = build("youtube", "v3", developerKey=api_key)

def search(query_term, max_page_count):
    pageCounter=0
    resultList=[]
    results = service.search().list(part="snippet", maxResults=50, q=query_term).execute()
    resultList.extend(results['items'])
    nextPage=results.get('nextPageToken',None)

    while nextPage and (pageCounter < max_page_count):
        results = service.search().list(part="snippet", maxResults=50, pageToken=nextPage, q=query_term).execute()
        resultList.extend(results['items'])

        pageCounter = pageCounter + 1
        nextPage=results.get('nextPageToken',None)

    
        return resultList
if __name__ == '__main__':
    arg1 = sys.argv[0]

    if len(sys.argv) == 2:
        query_term = sys.argv[1]
       
        print("query: " + query_term)

        resultList = search(query_term, 1)
        with open('youtube_search_' + query_term + '.json', 'w', encoding='utf-8') as f:
            json.dump(resultList, f, ensure_ascii=False, indent=4)

        
    else:
        print("usage: " + arg1 + " [search_term]")
