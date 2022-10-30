import numpy as np
from flask import Flask, render_template, request, redirect, jsonify
from markupsafe import escape
import pickle
import inputScript   #inputScript file - to analyze the URL

app = Flask(__name__)

model = pickle.load(open("/home/ana/ana/web-phishing-detection/phishing_website.pkl","rb"))

# user-inputs the URL in this page
@app.route('/')
def predict():
    return render_template("index.html")

#  fetches given URL and passes to inputScript
@app.route('/predict',methods=["POST"])
def y_predict():
    url = request.form['url']
    check_predic = inputScript.main(url)
    predic = model.predict(check_predic)
    # print(predic)

    result = predic[0]
    if(result==1):
        pred = "You are safe!! This is a Legimate Website :)"
    else:
        pred = "You are in a wrong site. Be Cautious :("

    return render_template("index.html", pred_text = '{}'.format(pred), url = url)

#  takes ip parameters from URL by inputScript and returns the predictions
@app.route('/predict_api', methods = ['POST'])
def predict_api():

    data = request.get_json(force = True)
    predic = model.y_predict([np.array(list(data.values()))])
    result = predic[0]
    return jsonify(result)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)
