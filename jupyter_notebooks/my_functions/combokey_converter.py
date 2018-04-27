"""A frustrating quality with working with csv files is their implicit handling of values

When a csv file is saved, it tries to guess what the type of the value of a cell -- ordinarily this fairly helpful and we probably don't notice it, but when your files have very large numbers (e.g. the combokey in these files), the values are read in scientific notation and are truncated, losing precision.  This is especially problematic, as we want to use the combokey as a primary key to join together the nces and crdc datasets.

The way this code works is by taking the leaid and schid of each school and concatenates them togther in the following format:  '=1233456712345'

This way, we force the csv file to read the values as text, rather than 'very large numbers that need to be truncated'
"""
import pandas as pd
import numpy as np

def convert(dataFrame, leaid, schid):
    """
    inputs:
            dataFrame:  pandas.DataFrame that contains the leaid and schid columns to be converted
             leaid and schid:    names of the columns in the file that correspond to each

    returns:
            a pandas.Series with concatenated leaid and schid values (to be saved in the 'combokey' column)
    """
    
    leaid_temp = dataFrame[leaid].apply(lambda x: str(x).zfill(7))
    schid_temp = dataFrame[schid].apply(lambda x: str(x).zfill(5) + "'")

    return "='" + leaid_temp + schid_temp

def test_convert():
    crdc_1516 = pd.read_csv(r'../../filtered_data/00_crdc_1516_initial.csv', 
                        dtype = {'LEAID':np.object})

    test = convert(crdc_1516, 'LEAID', 'SCHID')
    print(test.head())

if __name__ == '__main__':
    test_convert()