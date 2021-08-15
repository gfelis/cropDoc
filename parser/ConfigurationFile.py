import configparser
import global_vars
import os

def LoadConfigFile():
    config = configparser.ConfigParser()
    configFilePath = os.path.join(os.path.dirname(__file__), 'app.conf')
    config.read(configFilePath)

    global_vars.number_of_clusters = int(config['KML']['number_of_clusters'])
    global_vars.cmap = config['KML']['cmap']
    global_vars.sleep_in_thread = int(config['KML']['sleep_in_thread'])
    global_vars.altitude = int(config['KML']['altitude'])
    global_vars.pRange = int(config['KML']['range'])
    global_vars.kml_destination_path = config['KML']['kml_destination_path']
    global_vars.kml_destination_filename = config['KML']['kml_destination_file']

    global_vars.lg_IP = config['INSTALLATION']['lg_IP']
    global_vars.lg_pass = config['INSTALLATION']['lg_pass']
    global_vars.screen_for_logos = int(config['INSTALLATION']['screen_for_logos'])
    global_vars.logs = config['INSTALLATION']['logs']

    print('Global variables loaded!')