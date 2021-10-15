from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from googleapiclient.discovery import build
from flask import make_response

import pprint

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:thisisSparta!@srv-captain--look-database/mydatabase?authSource=admin"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/db"
mongo = PyMongo(app)




@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        new_user = {
            "username":"",
            "password":"",
        }
        

        new_user["username"] = request.form.get("username")
        new_user["password"] = request.form.get("password")
        confirmPassword = request.form.get('confirmPassword')
        
        # if the user successfully confirms their password
        if new_user["password"] == confirmPassword:
            # find if the user exists in the database
            # if the user exists, route them to log in
            if mongo.db.user.count_documents({"username": new_user["username"]}) == 1:
                return render_template('login.html', **{
                    'username': new_user["username"],
                })
            # if the user is not, put them in the database
            else :
                mongo.db.user.insert(new_user)
                return render_template('registered.html', **{
                    'username': new_user["username"],
                })
        else :
            pass
    else :
        return render_template('404.html')

@app.route('/handleLoggedInUser', methods = ['POST'])
def handleLoggedInUser():
    # check the post data
    # return logged in page
    user = {
        'username' : "",
        'password' : "" 
    }

    user["username"] = request.form.get("username")
    user["password"] = request.form.get("password")

    print(user["username"])
    print(user["password"])

    # find the username in the datatbase
    username_object = mongo.db.user.find({"username": user["username"]})

    # get the user object
    user_object = username_object.next()

    if user_object["password"] == user["password"] and user_object["username"] == user["username"]:
        return render_template('registered.html', **{
                'username': user_object["username"],
        })
    else :
        pass

    

@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        user = {
            "username": "",
            "password": ""
        }

        
        user["username"] = request.form.get("username2")
        user["password"] = request.form.get("password2")
        # print(user["username"])
        # print(user["password"])

        # find the username in the database
        username_object = mongo.db.user.find({"username": user["username"]})
        # get the user object
        user_object = username_object.next()
        # if the password matches the object password
        if user_object["password"] == user["password"] and user_object["username"] == user["username"]:
            # take the user to registered
            # print(user_object["username"], user_object["password"])
            resp = make_response(render_template('registered.html', **{
                'username': user_object["username"],
            }))
            resp.set_cookie('username', user["username"])
            resp.set_cookie('password', user["password"])
            return resp
        else :
            return("nothing yet")
    else :
        return render_template('404.html')


@app.route('/response', methods=['GET','POST'])
def getResponse():
    
    if request.method == 'POST':
        search = request.form.get("response")
        
        service = build("customsearch", "v1", 
            developerKey="AIzaSyDgzp6gO1foZqVJNifc_mPrG0CXmi5mv0Q")

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
    else :
        return render_template('404search.html')




if __name__ == '__main__':
    app.run(host="localhost",debug=True)