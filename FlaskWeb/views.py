"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from FlaskWeb import app
import pyodbc
import pandas
import numpy as np


def sql():
    server = 'ravenunswpilot.database.windows.net'
    database = 'continuousDataExportDB'
    username = 'ravenadmin'
    password = '''fe'Pc9\C3)_@}'yL'''
    driver= '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    sql = "SELECT * FROM analytics.Measurements ORDER BY timestamp ASC"
    data = pandas.read_sql(sql,cnxn)
    group = data.groupby(['deviceId']).agg(['count'])
    liveval = data.drop_duplicates(['deviceId'], keep='last', inplace=False).reset_index(drop=True)
    liveval = liveval.pivot_table(
            values='numericValue', 
            index=['deviceId', 'timestamp'], 
            columns='measurementDefinition', 
            aggfunc=np.sum)
    return group, liveval



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    group, liveval  = sql()
    table1 = group.to_html(classes=['table', 'table-hover', 'table-bordered', 'thead-dark'], 
           float_format=lambda x: '{0:.3f}'.format(x))
    table2 = liveval.to_html(classes=['table', 'table-hover', 'table-bordered', 'thead-dark'], 
           float_format=lambda x: '{0:.3f}'.format(x))
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        table1 = table1, 
        table2 = table2
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
