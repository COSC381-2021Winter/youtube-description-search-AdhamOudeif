import sys
import os
import config
import json
from googleapiclient.discovery import build
# pylint: disable=maybe-no-member

api_key = config.api_key
cse_id = config.cse_id
service = build("youtube", "v3", developerKey=api_key)

def mSearch(query_term, max_page_count):
    def get_video_info(video_id):
        result = service.videos().list(part='snippet', id=video_id).execute()
        try:
            return result['items'][0]
        except:
            return None
    
    def get_video_list(search_results):
        video_list = []
        for item in search_results['items']:
            video_id = item['id']['videoId']
            video_info = get_video_info(video_id)
            if video_info:
                video_list.append(video_info)
        
        return video_list

    results = []
    count=1
    index_name="music_search_"+query_term+".json"
    if os.path.exists(index_name):
        with open(index_name) as f:
              results = json.load(f)
    else:
        
        tempResults=service.search().list(q=query_term, part="snippet",type="video",maxResults=50,videoCategoryId=10).execute()
        video_list=get_video_list(tempResults)
        results.extend(video_list)
        while tempResults['nextPageToken']!='' and count < max_page_count:
            token=tempResults['nextPageToken']
            tempResults=service.search().list(q=query_term, part="snippet",type="video",maxResults=50,pageToken=token,videoCategoryId=10).execute()
            video_list=get_video_list(tempResults)
            results.extend(video_list)
            count+=1
        fileName="music_search_"+query_term+".json"
        with open(fileName,'w',encoding='utf-8')as f:
            json.dump(results,f,ensure_ascii=False,indent=4)
    return results

    pageCounter=0
    resultList=[]
    results = service.search().list(part="snippet", type="video", maxResults=50, q=query_term, videoCategoryId=10).execute()
    video_list = get_video_list(results)
    resultList.extend(video_list)
    nextPage=results.get('nextPageToken',None)

    while nextPage and (pageCounter < max_page_count):
        results = service.search().list(part="snippet", type="video", maxResults=50, pageToken=nextPage, q=query_term, videoCategoryId=10).execute()
        video_list = get_video_list(results)
        resultList.extend(video_list)

        pageCounter = pageCounter + 1
        nextPage=results.get('nextPageToken',None)
    
    with open('music_search_' + query_term + '.json', 'w', encoding='utf-8') as f:
        json.dump(resultList, f, ensure_ascii=False, indent=4)

    
    return resultList


if __name__ == '__main__':
    arg1 = sys.argv[0]

    if len(sys.argv) == 2:
        query_term = sys.argv[1]
       
        print("query: " + query_term)

        resultList = mSearch(query_term, 1)
        with open('music_search_' + query_term + '.json', 'w', encoding='utf-8') as f:
            json.dump(resultList, f, ensure_ascii=False, indent=4)

        
    else:
        print("usage: " + arg1 + " [search_term]")
