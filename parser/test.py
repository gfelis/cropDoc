import parser
import os
from ConfigurationFile import *
from GenerateKml import *



if __name__ == '__main__':
    LoadConfigFile()
    p = os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), 'xls/jorge_gil.xlsx'])
    if os.path.exists(p):
        fields = parser.parse(p)
    CreateKML(fields)

    
