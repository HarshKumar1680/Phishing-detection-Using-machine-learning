#importing required libraries
from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import webbrowser
from threading import Timer
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            url = request.form["url"]
            obj = FeatureExtraction(url)
            x = np.array(obj.getFeaturesList()).reshape(1,30) 

            y_pred = gbc.predict(x)[0]
            y_pro_phishing = gbc.predict_proba(x)[0,0]
            y_pro_non_phishing = gbc.predict_proba(x)[0,1]
            
            # Determine prediction and probability
            if y_pred == 1:
                pred = "SAFE"
                probability = y_pro_non_phishing * 100
            else:
                pred = "UNSAFE"
                probability = y_pro_phishing * 100
                
            return render_template('index.html', 
                                prediction=pred,
                                probability=round(probability, 2),
                                url=url,
                                xx=round(y_pro_non_phishing, 2))
        except Exception as e:
            return render_template('index.html', 
                                error=f"Error analyzing URL: {str(e)}",
                                xx=-1)
            
    return render_template("index.html", xx=-1)

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)