from flask.templating import render_template
from app import app
from flask import request, redirect, session
from app.controllers import predikController, authController, dosenController, chatController

@app.route("/")
def index():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/masuk")
    return render_template('beranda.html')

@app.route("/pindai")
def pindai():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/masuk")
    return dosenController.getAllDosenPredik()

@app.route('/masuk', methods=['GET'])
def masuk():
    return render_template('login.html')

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/listdosen")
def listdosen():
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/masuk")
    return dosenController.getAlldosenHistori()

@app.route("/result/<id>")
def result(id):
    return predikController.getHistoryByDosen(id)



@app.route('/dosen', methods=['GET', 'POST'])
def dosen():
    if request.method == 'GET':
        return dosenController.getAlldosen()
    else:
        return dosenController.createDosen()

@app.route('/dosen/<id>', methods=['GET', 'PUT', 'DELETE'])
def dosenDetail(id):
    if request.method == 'GET':
        return dosenController.getDosenById(id)
    elif request.method == 'PUT':
        return dosenController.updateDosen(id)
    elif request.method == 'DELETE':
        return dosenController.deleteDosen(id)

@app.route('/signup', methods=['POST'])
def signUp():
    if request.method == 'GET':
        print("melihat semua user")
    elif request.method == 'POST':
        return authController.signUp()


@app.route('/signin', methods=['POST'])
def signIn():
    return authController.signIn()

@app.route('/user/<id>', methods=['GET', 'PUT'])
def userDetails(id):
    if(request.method == 'GET'):
        return authController.getUser(id)
    if(request.method == 'PUT'):
        return authController.updateUser(id)

@app.route('/predict', methods=['POST'])
def predict():
    return predikController.result()



@app.route("/chat")
def home():
    return render_template("chatbot.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatController.chatbot_response(userText)


