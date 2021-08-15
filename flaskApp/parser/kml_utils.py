import itertools
import os
import parser.global_vars as global_vars
from threading import Thread
from time import sleep, time

def blankKML(id):
    string = "\"echo '<?xml version=\\\"1.0\\\" encoding=\\\"UTF-8\\\"?> \n" + \
        "<kml xmlns=\\\"http://www.opengis.net/kml/2.2\\\"" + \
        " xmlns:gx=\\\"http://www.google.com/kml/ext/2.2\\\"" + \
        " xmlns:kml=\\\"http://www.opengis.net/kml/2.2\\\" " + \
        " xmlns:atom=\\\"http://www.w3.org/2005/Atom\\\">\n" + \
        " <Document id=\\\"slave_" + id + "\\\"> \n" + \
        " </Document>\n" + \
        " </kml>\n' > /var/www/html/kml/slave_" + id + ".kml\""
    return string

def sendKmlToLG(kml_filename):
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" \
        + "cropDoc/flaskApp/" + global_vars.kml_destination_path + kml_filename \
        + " " + global_vars.lg_IP + ":/var/www/html/CD/" + global_vars.kml_destination_filename
    print(command)
    os.system(command)

    # Send Logos
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" \
        + "cropDoc/flaskApp/" + global_vars.kml_destination_path + "slave_" + global_vars.screen_for_logos + ".kml" " " \
        + global_vars.lg_IP + ":/var/www/html/kml/slave_" + global_vars.screen_for_logos + ".kml"
    print(command)
    os.system(command)

    msg = "http:\/\/" + global_vars.lg_IP + ":81\/\CD\/" + global_vars.kml_destination_filename.replace("/", "\/") + "?id=" + str(int(time()*100))
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"sed -i \'1s/.*/" + msg + "/\' /var/www/html/kmls.txt\""
    print(command)
    os.system(command)

def threaded_function():
    files = os.listdir(global_vars.kml_destination_path)
    files = [i for i in files if i.startswith('historic')]
    main = []
    slave = []
    for elem in files:
        if elem.endswith('slave_{}.kml'.format(global_vars.screen_for_colorbar)):
            slave.append(elem)
        else:
            main.append(elem)
    for elem in itertools.cycle(list(zip(main, slave))):
        sleep(global_vars.sleep_in_thread)
        if global_vars.thread == False:
            print("thread finished...exiting")
            break

def startSendKMLThread():
    global_vars.thread = True
    thread = Thread(target = threaded_function)
    thread.name = 'SendKML'
    thread.start()

def stopSendKMLThread():
    global_vars.thread = False
    stopOrbit()

def sendFlyToToLG(lat, lon, altitude, heading, tilt, pRange, duration):
    flyTo = "flytoview=<LookAt>" \
            + "<longitude>" + str(lon) + "</longitude>" \
            + "<latitude>" + str(lat) + "</latitude>" \
            + "<altitude>" + str(altitude) + "</altitude>" \
            + "<heading>" + str(heading) + "</heading>" \
            + "<tilt>" + str(tilt) + "</tilt>" \
            + "<range>" + str(pRange) + "</range>" \
            + "<altitudeMode>relativeToGround</altitudeMode>" \
            + "<gx:altitudeMode>relativeToGround</gx:altitudeMode>" \
            + "<gx:duration>" + str(duration) + "</gx:duration>" \
            + "</LookAt>"

    command = "echo '" + flyTo + "' | sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP + " 'cat - > /tmp/query.txt'"
    print(command)
    os.system(command)

def createRotation(lat, lon, alt, tilt, range1, range2):
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    xml += '\n'+'<kml xmlns="http://www.opengis.net/kml/2.2"'
    xml += '\n'+'xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
    xml += '\n'+'<gx:Tour>'
    xml += '\n\t'+'<name>Orbit</name>'
    xml += '\n\t'+'<gx:Playlist>'
    for i in range(0, range2, 10):
        xml += '\n\t\t'+'<gx:FlyTo>'
        xml += '\n\t\t\t'+'<gx:duration>0.5</gx:duration>'
        xml += '\n\t\t\t'+'<gx:flyToMode>smooth</gx:flyToMode>'
        xml += '\n\t\t\t'+'<LookAt>'
        xml += '\n\t\t\t\t'+'<longitude>'+str(lon)+'</longitude>'
        xml += '\n\t\t\t\t'+'<latitude>'+str(lat)+'</latitude>'
        xml += '\n\t\t\t\t'+'<altitude>'+str(alt)+'</altitude>'
        xml += '\n\t\t\t\t'+'<heading>'+str(i%360)+'</heading>'
        xml += '\n\t\t\t\t'+'<tilt>'+str(tilt)+'</tilt>'
        xml += '\n\t\t\t\t'+'<gx:fovy>35</gx:fovy>'
        xml += '\n\t\t\t\t'+'<range>'+str(range1)+'</range>'
        xml += '\n\t\t\t\t'+'<gx:altitudeMode>relativeToGround</gx:altitudeMode>'
        xml += '\n\t\t\t'+'</LookAt>'
        xml += '\n\t\t'+'</gx:FlyTo>'

    xml += '\n\t'+'</gx:Playlist>'
    xml += '\n'+'</gx:Tour>'
    xml += '\n'+'</kml>'
    return xml

def generateOrbitFile(content, path):
    with open(path, 'w') as file1:
        file1.write(content)

def sendOrbitToLG():
    command = "sshpass -p " + global_vars.lg_pass + " scp $HOME/" \
        + "cropDoc/flaskApp/" + global_vars.kml_destination_path + "orbit.kml " + global_vars.lg_IP + ":/var/www/html/CD/orbit.kml"
    print(command)
    os.system(command)

    msg = "http:\/\/" + global_vars.lg_IP + ":81\/\CD\/" + "orbit.kml"  + "?id=" + str(int(time()*100))

    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " \"sed -i \'2s/.*/" + msg + "/\' /var/www/html/kmls.txt\""

    print(command)
    os.system(command)

def startOrbit():
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP + " \'echo \'playtour=Orbit\' > /tmp/query.txt\'"
    print(command)
    os.system(command)

def stopOrbit():
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP + " \'echo \'exittour=true\' > /tmp/query.txt\'"
    print(command)
    os.system(command)

def doRotation(latitude, longitude, altitude, pRange, range2):
    kml = createRotation(latitude, longitude, altitude, 45, pRange, range2)
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, global_vars.kml_destination_path, 'orbit.kml')
    generateOrbitFile(kml, path)
    sendOrbitToLG()
    sleep(1)
    startOrbit()

def flyToField(field, range2):
    sendFlyToToLG(field.centroid.latitude, field.centroid.longitude, 150, 0, 45, 600, 2)
    sleep(6)
    doRotation(field.centroid.latitude, field.centroid.longitude, 150, 600, range2)

def cleanMainKML():
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP + " \"echo ' ' > /var/www/html/kmls.txt\""
    print(command)
    os.system(command)

    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP + " \"echo ' ' >> /var/www/html/kmls.txt\""
    print(command)
    os.system(command)

def cleanSecundaryKML():
    for i in range(2,6):
        string = blankKML(str(i))
        command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
            + " " + string
        print(command)
        os.system(command)

def removeCDFolder():
    command = "sshpass -p " + global_vars.lg_pass + " ssh " + global_vars.lg_IP \
        + " rm -rf /var/www/html/CD"
    print(command)
    os.system(command)

def cleanKMLFiles():
    cleanMainKML()
    cleanSecundaryKML()


def cleanAllKMLFiles():
    cleanMainKML()
    cleanSecundaryKML()
    removeCDFolder()

def setLogo():
    kml = '<kml xmlns=\\\"http://www.opengis.net/kml/2.2\\\" xmlns:atom=\\\"http://www.w3.org/2005/Atom\\\" xmlns:gx=\\\"http://www.google.com/kml/ext/2.2\\\">'
    kml += '\n ' + '<Document>'
    kml += '\n  ' + '<Folder>'
    kml += '\n   ' + '<name>Logos</name>'
    kml += '\n   ' + '<ScreenOverlay>'
    kml += '\n    ' + '<name>Logo</name>'
    kml += '\n    ' + '<Icon>'
    kml += '\n     ' + '<href>http://lg1:81/CD/Logos.png</href>'
    kml += '\n    ' + '</Icon>'
    kml += '\n    ' + '<overlayXY x=\\\"0\\\" y=\\\"1\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
    kml += '\n    ' + '<screenXY x=\\\"0.02\\\" y=\\\"0.98\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
    kml += '\n    ' + '<rotationXY x=\\\"0\\\" y=\\\"0\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
    kml += '\n    ' + '<size x=\\\"0.65\\\" y=\\\"0.2\\\" xunits=\\\"fraction\\\" yunits=\\\"fraction\\\"/>'
    kml += '\n   ' + '</ScreenOverlay>'
    kml += '\n  ' + '</Folder>'
    kml += '\n ' + '</Document>'
    kml += '\n' + '</kml>'

    logos_file_target = '/var/www/html/kml/slave_{}.kml'.format(global_vars.screen_for_logos)

    command = "sshpass -p {} ssh {} echo \"'{}' > {}\"".format(global_vars.lg_pass, global_vars.lg_IP, kml, logos_file_target)
    print(command)
    os.system(command)

def resetView():
    sendFlyToToLG(40.77, -3.6, 0, 0, 5, 10000000, 1.2)
    setLogo()
