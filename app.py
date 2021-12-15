import flask
from flask import Flask, redirect , url_for, render_template, request, jsonify
from flask.wrappers import Response
from numpy import roots
import fetchData
from flask import request, jsonify
import json
import requests
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'img_url':'https://upload.wikimedia.org/wikipedia/en/4/4a/A_Fire_Upon_the_Deep.bookcover.jpg',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'img_url':'https://m.media-amazon.com/images/I/41srw9ZyJrL.jpg',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'img_url':'https://upload.wikimedia.org/wikipedia/en/thumb/a/ac/Dhalgren-bantam-cover.jpg/220px-Dhalgren-bantam-cover.jpg',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]



@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


@app.route('/api/possibleproblem', methods=['GET'])
def api_possibleproblem():
    apidata = fetchData.possibleproblem()
    result = apidata.to_json(orient="table")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)

@app.route('/api/possibleproblemexample', methods=['GET'])
def api_possibleproblememexample():
    apidata = fetchData.possibleproblememexample()
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)

@app.route('/api/diagnostics', methods=['GET'])
def api_diagnostics():
    apidata = fetchData.diagnostics()
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    json_Out = json.dumps(parsed, indent=4)
    res = requests.post('http://127.0.0.1:5000/api/JSONbeautify', json=json_Out)
    return res.json()
    #return json.dumps(parsed, indent=4) 
    #return jsonify(books)

@app.route('/api/treatments', methods=['GET'])
def api_treatments():
    apidata = fetchData.treatments()
    result = apidata.to_json(orient="index")
    parsed = json.loads(result)
    return json.dumps(parsed, indent=4) 
    #return jsonify(books)

@app.route('/api/possibleproblemExplaination', methods=['GET'])
def api_possibleproblemExplaination():
    apidata = fetchData.possibleproblemExplaination()
    result = apidata.to_json(orient="index")
    parsed = json.loads(result)
    return json.dumps(parsed, indent=4) 
    #return jsonify(books)

@app.route('/api/documentation', methods=['GET'])
def api_documentation():
    apidata = fetchData.documentation()
    result = apidata.to_json(orient="index")
    parsed = json.loads(result)
    return json.dumps(parsed, indent=4) 
    #return jsonify(books)

@app.route('/api/testjsonapi', methods=['GET'])
def api_testjsonapi():
    apidata = { "fruit": "Apple", "size": "Large", "color": "Red"}
    json_Out = json.dumps(apidata, indent=4)
    res = requests.post('http://127.0.0.1:5000/api/JSONbeautify', json=json_Out)
    return res.json()
    

@app.route('/api/JSONbeautify', methods = ['POST'])
def api_JSONbeautify():
    result = request.data
    return result

@app.route('/api/possibleproblemexampleparameter', methods=['GET'])
def api_possibleproblememexampleparameter():
    #pproblem = ['Trauma','Alchohol']
    pproblem = request.data
    parsed = json.loads(pproblem)
    reqarr=[]
    #return json.dumps(parsed["Problems"], indent=4)
    for item in parsed['Problems']:
        reqarr.append(item['Source_Problem'])
    
    #return json.dumps(reqarr, indent=4)

    #return pproblem
    apidata = fetchData.possibleproblememexampleparameter(reqarr)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)


@app.route('/api/diagnosticsexampleparameter', methods=['GET'])
def api_diagnosticsexampleparameter():
    diagnose = ['Contusions','Acute Hepatitis','false']
    apidata = fetchData.diagnosticsexampleparameter(diagnose)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)


@app.route('/api/treatmentsexampleparameter', methods=['GET'])
def api_treatmentsexampleparameter():
    treatment = ['Contusions','Acute Hepatitis','false']
    apidata = fetchData.treatmentsexampleparameter(treatment)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)


@app.route('/api/getcomorbiditiesCUI', methods=['GET'])
def api_comorbidities_of_CUI(): 
    #cui_prob_list = ['C1565489', 'C0085762'] 
    pproblem = request.data
    parsed = json.loads(pproblem)
    cui_prob_list=[]
    #return json.dumps(parsed["Problems"], indent=4)
    for item in parsed['CUIs']:
        cui_prob_list.append(item['CUI'])
    #cui_prob_list = pd.read_json(pproblem)
    
    apidata = fetchData.comorbidities_of_CUI(cui_prob_list)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)


@app.route('/api/getproblems', methods=['GET'])
def api_getproblems(): 
    #cui_prob_list = ['C1565489', 'C0085762'] 
    pproblem = request.data
    parsed = json.loads(pproblem)
    cui_prob_list=[]
    #return json.dumps(parsed["Problems"], indent=4)
    for item in parsed['CUIs']:
        cui_prob_list.append(item['CUI'])
    #cui_prob_list = pd.read_json(pproblem)
    
    apidata = fetchData.getproblems(cui_prob_list)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)


@app.route('/api/PotentialComorbidities', methods=['GET'])
def api_PotentialComorbidities(): 
    pproblem = request.data
    parsed = json.loads(pproblem)
    cui_prob_list=[]
    for item in parsed['CUIs']:
        cui_prob_list.append(item['CUI'])
    
    apidata = fetchData.PotentialComorbidities(cui_prob_list)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)

@app.route('/api/LikelyAbnormalLabs', methods=['GET'])
def api_LikelyAbnormalLabs(): 
    pproblem = request.data
    parsed = json.loads(pproblem)
    cui_prob_list=[]
    for item in parsed['CUIs']:
        cui_prob_list.append(item['CUI'])
    
    apidata = fetchData.LikelyAbnormalLabs(cui_prob_list)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)

@app.route('/api/LikelyPrescriptions', methods=['GET'])
def api_LikelyPrescriptions(): 
    pproblem = request.data
    parsed = json.loads(pproblem)
    cui_prob_list=[]
    for item in parsed['CUIs']:
        cui_prob_list.append(item['CUI'])
    
    apidata = fetchData.LikelyPrescriptions(cui_prob_list)
    result = apidata.to_json(orient="records")
    parsed = json.loads(result)
    res = json.dumps(parsed, indent=4) 
    return jsonify(parsed)


@app.route('/api/nodedisplay', methods=['GET'])
def api_nodedisplay():
    apidata = fetchData.nodedisplay()

    html = '<!doctype html><html><head><title>Network | Images With Borders</title>' 
    html = html + '<script type="text/javascript" src="/static/vis.js"></script>'
    html = html + '<script type="text/javascript" src="/static/canvas2svg.js"></script>'
    html = html + '<link href="/static/vis-network.min.css" rel="stylesheet" type="text/css" />'
    html = html + apidata + '</head><body></body></html>'
    
    with open('./templates/test.html', 'w') as f:
        f.write(html)

    return render_template("test.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000) #host="0.0.0.0" will make the page accessable
                            #by going to http://[ip]:5000/ on any computer in 
                            #the network.


#app.run()
#76.251.77.235