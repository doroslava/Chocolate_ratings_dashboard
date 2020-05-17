import pandas as pd
import plotly.graph_objs as go
import country_converter as coco
import numpy as np


def cleandata(dataset, keep_columns = ['CompanyLocation', 'Rating'], rating_treshold = 4.0):
    """Clean choco data for a visualization dashboard

    Keeps selected columns in keep_columns variable and observations which have chocolate       ratings more than specified treshold value
    Tidys-up column names, values of cells and removes NaNs
    Outputs the results to a csv file

    Args:
        dataset (str): name of the csv data file

    Returns:
        df (data frame): cleaned dataframe

    """ 
    
    df = pd.read_csv(dataset)
    
    
    #Remove all spaces and lines from the column names.
    
    tmp_cols = [i.replace('\n',' ') for i in df.columns] 
    tmp_cols[0] = tmp_cols[0].replace(u'\xa0', u' ')
    tmp_cols = [i.replace(' ','') for i in tmp_cols] 
    df.columns = tmp_cols
    
    # Keep only the columns of interest. 
    
    df = df[df["Rating"] >= rating_treshold]    
    df = df[keep_columns]
        
    #Manually correct all obvious mistakes in country spelling. 
    
    df = df.replace("Domincan Republic","Dominican Republic")
    df = df.replace("Hawaii","United States")
    df = df.replace("Cost Rica, Ven","Costa Rica, Venezuela")
    df = df.replace("Niacragua","Nicaragua")
    df = df.replace("Eucador","Ecuador")
    df = df.replace("Mad., Java, PNG","Madagascar, Java, Papua New Guinea")
    df = df.replace(r'^Ven\,',"Venezuela", regex=True)
    df = df.replace("Amsterdam","Netherlands")
    df = df.replace("Scotland","United Kingdom")
    df = df.replace("Wales","United Kingdom")
    
    #Apply country_convert to convert all "non-standardized" country names if possible.
    
    if "BroadBeanOrigin" in df.columns:
        cleaned_country_names = coco.convert(names = list(df["BroadBeanOrigin"]), to = 'name_short')
        df["BroadBeanOrigin"] = cleaned_country_names
        df["BroadBeanOrigin"] = df.BroadBeanOrigin.astype(str).str.replace('\[|\]|\'', '')
    
    
    if "CompanyLocation" in df.columns:
        cleaned_country_names = coco.convert(names = list(df["CompanyLocation"]), to = 'name_short')
        df["CompanyLocation"] = cleaned_country_names
    
    if "CocoaPercent" in df.columns:    
        df["CocoaPercent"] = df["CocoaPercent"].str.strip("%").astype('float') / 100
    
    #Replace all blank spaces with NaNs.
    
    df = df.replace(r'^\s*$', np.nan, regex = True)
    df = df.replace(r'^not found$', np.nan, regex = True)
    
    #Remove all rows with NaNs.
    df = df.dropna()
    
    return df
        

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # First chart plots number of top-rated chocolates produced in each country. 
    
    graph_one = []  
    
    df = cleandata("data/flavors_of_cacao.csv", keep_columns = ["CompanyLocation"])
    
    graph_one.append(
      go.Bar(
      x = df.CompanyLocation.value_counts().keys().tolist(),
      y = df.CompanyLocation.value_counts().tolist(),
      )
    )

    layout_one = dict(title = 'Company location for the best rated chocolates',
                yaxis = dict(title = 'Number of top-rated chocolates'),
                )

   # Second chart plots number of beans from top-rated chocolates per each origin country.     
    graph_two = []
    
    df = cleandata("data/flavors_of_cacao.csv", keep_columns = ["BroadBeanOrigin"])
    
    bean_origin_list = df.BroadBeanOrigin.str.split(", ").apply(pd.Series,1).stack()
    
    graph_two.append(
      go.Bar(
      x = bean_origin_list.value_counts().keys().tolist(),
      y = bean_origin_list.value_counts().tolist(),
      )
    )

    layout_two = dict(title = 'Bean origin for the best rated chocolates',
                yaxis = dict(title = 'Number of top-rated chocolates'),
                )


# Third chart plots percent of Cocoa and Chocolate rating.
    graph_three = []
    
    df = cleandata("data/flavors_of_cacao.csv", keep_columns = ["CocoaPercent","Rating"], rating_treshold = 1.0)
    
    graph_three.append(
      go.Scatter(
      x = [i for i in df["CocoaPercent"]],
      y = [i for i in df["Rating"]],
      mode = 'markers'
      )
    )

    layout_three = dict(title = 'Chocolate rating and cocoa percent',
                xaxis = dict(title = 'Cocoa percent %'),
                yaxis = dict(title = 'Chocolate rating')
                       )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))

    return figures