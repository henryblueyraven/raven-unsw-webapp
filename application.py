from flask import Flask, render_template
import pyodbc
import pandas
import numpy as np
app = Flask(__name__)

def sql():
    server = 'unswsmartsash.database.windows.net'
    database = 'continuousDataExportDB'
    username = 'ravenadmin'
    password = '''fe'Pc9\C3)_@}'yL'''
    driver= '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    sql = "SELECT * FROM analytics.Measurements WHERE NOT deviceTemplate = 'None' ORDER BY timestamp ASC"
    data = pandas.read_sql(sql,cnxn)
    group = data.groupby(['deviceId']).agg(['count'])
    data['measurementDefinition'] = [x.split('.0/')[1] for x in data['measurementDefinition']]
    liveval = data.drop_duplicates(['deviceId', 'measurementDefinition'], keep='last', inplace=False).reset_index(drop=True)
    liveval = liveval.pivot_table(
            values='numericValue', 
            index=['deviceId', 'timestamp'], 
            columns='measurementDefinition', 
            aggfunc=np.sum)
    return group, liveval

@app.route("/")
def analysis():
    group, liveval  = sql()
    table1 = group.to_html(classes=['table', 'table-hover', 'table-bordered', 'thead-dark'], 
           float_format=lambda x: '{0:.3f}'.format(x))
    table2 = liveval.to_html(classes=['table', 'table-hover', 'table-bordered', 'thead-dark'], 
           float_format=lambda x: '{0:.3f}'.format(x))
    return render_template("index.html", data=table1, data2=table2)