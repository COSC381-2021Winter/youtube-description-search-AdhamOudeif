from flask import Flask, request, render_template
from youtube import search
from description_search import create_whoosh_index
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
    username = request.args.get('name')
    if not username or not username.strip():
        username = "World"

    return render_template("index.html", name="Hello " + username)

@app.route("/query")
def query():
    arg = request.args.get('q')
    if not arg or not arg.strip():
        return render_template("query.html")
    
    index_name = "whoosh_index" + arg

    results = search(arg, 1)
    create_whoosh_index(results, index_name)

    return render_template("query.html", data=results)
