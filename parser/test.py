import parser
import os
import ConfigurationFile
import GenerateKml
import kml_utils
import global_vars



if __name__ == '__main__':
    ConfigurationFile.LoadConfigFile()
    p = os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), 'xls/jorge_gil.xlsx'])
    if os.path.exists(p):
        fields = parser.parse(p)
    GenerateKml.CreateKML(fields['Campo de Gracia'])
    #kml_utils.sendKmlToLG("CropDoc_Demo.kml")
    kml_utils.sendKmlToLG(global_vars.kml_destination_filename)
    kml_utils.flyToField(fields['Campo de Gracia'], 1440)
    
