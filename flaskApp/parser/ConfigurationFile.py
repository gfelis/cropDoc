import configparser
import parser.global_vars as global_vars
import os

def LoadConfigFile():
    config = configparser.ConfigParser()
    configFilePath = os.path.join(os.path.dirname(__file__), 'app.conf')
    config.read(configFilePath)

    global_vars.kml_destination_path = config['KML']['kml_destination_path']
    global_vars.kml_destination_filename = config['KML']['kml_destination_file']

    global_vars.lg_IP = config['INSTALLATION']['lg_IP']
    global_vars.lg_pass = config['INSTALLATION']['lg_pass']
    global_vars.screen_for_logos = int(config['INSTALLATION']['screen_for_logos'])
    global_vars.screen_for_statistics = config['INSTALLATION']['screen_for_statistics']

    print('Global variables loaded!')