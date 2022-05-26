import json
import pandas as pd

class BMIcalculator:
    def __init__(self):
        with open('bmi_data.json') as bmi_table:
            df_bmi = json.load(bmi_table)
        self.table = pd.json_normalize(df_bmi)

    def bmi_calculator(self, mass, height):
        bmi = (mass/(height/100)**2)
        bmi = round(bmi,2)
        return bmi
    
    def bmi_range(self,bmi):
        table = self.table  
        try:
            record = table.iloc[(table['BmiRange']-bmi).abs().argsort()[:1]] #finding bmi withing a specific range
            data = {
                "BMICategory":record["BMICategory"].iat[0],       #finding category record for bmi range using table 1
                "HealthRisk" :record["HealthRisk"].iat[0]   #finding health risk record for bmi range using table 1
            }
        except Exception as e:
            data = {
                "BMICategory": "No data",       
                "HealthRisk" : "No Data"   
            }
        return data
