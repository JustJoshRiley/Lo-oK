from flask import Flask, request, render_template

from googleapiclient.discovery import build

from flask import jsonify

import pprint

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:thisisSparta!@srv-captain--look-database/mydatabase?authSource=admin"
# app.config["MONGO_URI"] = "mongodb://root:thisisSparta!@srv-captain--look-database:27017/mydatabase?authSource=admin"



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/response', methods=['GET', 'POST'])
def getResponse():
    
    if request.method == 'POST':
        search = request.form.get("response")
        print(search)
        
        service = build("customsearch", "v1", 
            developerKey="AIzaSyDmMPBhep_IvCp1W0XiD_O0Pf36WSWsWT8")

        res = service.cse().list(
            q=search, 
            cx='3150098a9e3b71586').execute()

        newDict = []

        for response in res['items']:
            
            result = {
                "title" : response['title'],
                "url" : response['link'],
                "description" : response['snippet']
            }

            newDict.append(result)
            
        print(newDict)

        return render_template('results.html', newDict=newDict)


if __name__ == '__main__':
    app.run(host="localhost",debug=True)