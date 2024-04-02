import json
import csv
import pandas as pd
def convert_json_to_csv(path_to_json):
    with open(path_to_json,"r",encoding="utf-8") as file:
        data=json.load(file)
    with open("data/new_result.csv","w",encoding="utf-8") as csv_file:
        csv_writer=csv.writer(csv_file)
        csv_writer.writerow(['Method Name', 'AST Sequence'])
        for key,value in data.items():
            csv_writer.writerow([key,value[0]])
def logs_to_list(path_to_logs):
    df=pd.read_csv(path_to_logs)
    accuracy=df['accuracy'].tolist()
    loss=df['loss'].tolist()
    return accuracy,loss