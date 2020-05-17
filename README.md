# Chocolate ratings dashboard

Test dashboard for chocolate ratings data set, based on course from Udacity Data Scientist Nanodegree. Dahboard is available at https://lit-garden-88296.herokuapp.com/. 

## Data

The analyzed data includes Chocolate Bar Ratings dataset from kaggle (https://www.kaggle.com/rtatman/chocolate-bar-ratings). I want to thank authors for providing this data set.

## Local deployment

To deploy localy, first clone the repository to your local computer. 

Then, change to the app directory.

`cd chocoapp`

Activate virtual environment. 

In Windows system:

`chocoenv\Scripts\activate.bat`

In Linux system:

`source chocoenv/bin/activate`

In the chocoapp.py, un-comment the second line. 

> app.run(host='localhost', port=5000, debug=True)

Run the application:

`python chocoapp.py`

You can view the dashboard in the browser. 

> http://localhost:5000/

