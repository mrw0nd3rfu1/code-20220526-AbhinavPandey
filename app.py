import logging
import json
import os

from flask import Flask, render_template, Response, request, redirect, url_for

from BMIcalc import BMIcalculator

app = Flask(__name__)

bmi = BMIcalculator()

# @app.route('/')
# def index():
#     return render_template("index.html")

@app.route('/', methods = ['GET','POST'])
def read_file():
    results = []
    count = 0

    #reading the sample data
    with open('data.json') as f:
        bmi_data = json.load(f)

    #storing value in a dict
    for data in bmi_data:         
        weight = data["WeightKg"]
        height = data["HeightCm"]
        gender = data["Gender"]

        #using BMIcalc class to calculate bmi
        # using formula (mass/(height/100)**2)
        final_bmi = bmi.bmi_calculator(weight,height)

        #calculating range from BMIcalc 
        range = bmi.bmi_range(final_bmi)

        #calculate no. of overweight pople
        if range['BMICategory'] == 'Overweight':
            count+=1

        recordData = {
            "Gender":gender,
            "WeightKg":weight,
            "HeightCm":height,
            "Bmi":final_bmi,
        }
        
        #merging the data
        data = {**recordData, **range}  
        results.append(data)

    #adding total overweight count and the bmi with categories
    response_obj = {
    'status': 'success',
    'results': results,
    'total_overweight':count
    }

    #return the above object to the flask application
    return render_template('index.html',response_obj=response_obj)

# creating a user input function so that we can calculate bmi of any user
@app.route('/user_input', methods = ['GET','POST'])
def user_input():
    if request.method == 'GET':
        return render_template('user_input.html')
    
    # getting the data from the form
    if request.method == "POST":

        results = []
        count = 0
        output = request.form.to_dict()
        
        weight = output["WeightKg"]
        height = output["HeightCm"]
        gender = output["Gender"]

        #using BMIcalc class to calculate bmi
        # using formula (mass/(height/100)**2)
        final_bmi = bmi.bmi_calculator(int(weight),int(height))

        #calculating range from BMIcalc 
        range = bmi.bmi_range(final_bmi)

        recordData = {
            "Gender":gender,
            "WeightKg":weight,
            "HeightCm":height,
            "Bmi":final_bmi,
        }
        
        #merging the data
        data = {**recordData, **range}  
        results.append(data)

        #adding total overweight count and the bmi with categories
        user_obj = {
        'status': 'success',
        'results': results,
        }

        #return the above object to the flask application
        return render_template('data.html', user_obj = user_obj)
    

if __name__ == "__main__":
    app.run(debug=False)
