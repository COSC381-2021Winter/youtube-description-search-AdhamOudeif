from flask import Flask, request, render_template
from youtube import search
from musicSearch import mSearch
from description_search import create_whoosh_index, query_on_whoosh
#print("The variable _name_: ")
#print(_name_)

#_name_ is a special variable in python
#it can either be "_main_" or the name of the script
app = Flask(__name__) # the name of the script


#The request handler

#listens to /
#example: google.com/
#example: google.com/search

@app.route("/")
def index(): #The method name doesn't matter to Flask


    return render_template("index.html")

@app.route("/query", methods=['GET', 'POST'])
def query():
    arg = request.args.get('q')
    if not arg or not arg.strip():
        arg = request.args.get('m')
    
    else:
        index_name = "whoosh_index" + arg

        if request.method == 'GET':
            results = search(arg, 1)
            create_whoosh_index(results, index_name)
            return render_template("query.html", query_term=arg, data=results)
        
        if request.method == 'POST':
            # request sent by search bar on query page
            search_term = request.form['description_search']
            results = query_on_whoosh(index_name, search_term)
            return render_template("description.html", query_term=arg, data=results, search_t=search_term)

@app.route("/music_query", methods=['GET', 'POST'])
def mquery():
    arg = request.args.get('m')
    if not arg or not arg.strip():
        return render_template("music_query.html")
        
    else:
        index_name = "whoosh_index" + arg

        if request.method == 'GET':
            results = mSearch(arg, 1)
            create_whoosh_index(results, index_name)
            return render_template("music_query.html", query_term=arg, data=results)
            
        if request.method == 'POST':
            # request sent by search bar on query page
            search_term = request.form['musicSearch']
            results = query_on_whoosh(index_name, search_term)
            return render_template("music_desc_search.html", query_term=arg, data=results, search_t=search_term)
