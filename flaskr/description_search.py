from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID 
from whoosh.analysis import StemmingAnalyzer
from whoosh.lang.porter import stem 
from whoosh.qparser import QueryParser
from whoosh import scoring

import os

def create_whoosh_index(video_list, index_name):
    # Schema definition: 
    schema = Schema(id=ID(stored=True),
                    title=TEXT(stored=True),
                    description=TEXT(analyzer=StemmingAnalyzer(), stored=True))

    # create a folder to store the index
    if not os.path.exists(index_name):
        os.mkdir(index_name)

    index = create_in(index_name, schema)
    writer = index.writer()

    for video_item in video_list:
        video_id = video_item['id']
        video_title = video_item['snippet']['title']
        video_description = video_item['snippet']['description']
        writer.add_document(id=video_id, title=video_title, description=video_description)

    writer.commit()

def query_on_whoosh(index_name, query_str):
    query_str = stem(query_str)
    index = open_dir(index_name)
    with index.searcher(weighting=scoring.Frequency) as searcher:
        query = QueryParser("description", index.schema).parse(query_str)
        results = searcher.search(query, limit=None)

        formatted_results = []
        for result in results:
            d = {}
            d['url'] = "https://www.youtube.com/watch?v=" + result['id']
            d['snippet'] = {}
            d['snippet']['title'] = result['title']
            d['snippet']['description'] = result.highlights('description')
            d['id'] = {}
            d['id']['videoId'] = result.score
            formatted_results.append(d)

    return formatted_results