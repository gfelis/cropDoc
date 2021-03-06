# -*- coding: utf-8 -*-

# Import libraries
from lxml import etree
from PIL import Image, ImageDraw, ImageFont
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
import parser.global_vars as global_vars
import os
import parser.utils as utils

def GetCoords(field):
    string = ''
    for point in field.points:
        string += '{},{}\n'.format(point.longitude, point.latitude)
    string += '{},{}\n'.format(field.points[0].longitude, field.points[0].latitude)
    return string

def CreateLogosKML():
    kml = KML.kml(
        KML.Document(
            KML.Folder(
                KML.ScreenOverlay(
                    KML.name('Logos'),
                    KML.Icon(KML.href('http://lg1:81/CD/Logos.png')),
                    KML.overlayXY(x="0", y="1", xunits="fraction", yunits="fraction"),
                    KML.screenXY(x="0.02", y="0.9", xunits="fraction", yunits="fraction"),
                    KML.rotationXY(x="0", y="0", xunits="fraction", yunits="fraction"),
                    KML.size(x="0.5", y="0.5", xunits="fraction", yunits="fraction")
                )
            )
        )
    )
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, global_vars.kml_destination_path)

    if os.path.exists(path):
        f = open(path + 'slave_{}.kml'.format(global_vars.screen_for_logos), "w")
    else:
        raise ValueError(path)
    out = etree.tostring(kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()

    command = "sshpass -p {} scp $HOME/cropDoc/flaskApp/static/logos/Logos.png {}:/var/www/html/CD/Logos.png".format(global_vars.lg_pass, global_vars.lg_IP)
    print(command)
    os.system(command)

def save_stats_as_img(field):
        img = Image.new('RGB', (1100, 1400), color = 'white')

        n_healthy, n_ill, n_doubt = 0, 0, 0

        for location in field.locations:
            if float(location.diagnose) < 30:
                n_healthy += 1
            elif float(location.diagnose) < 60:
                n_doubt += 1
            else:
                n_ill += 1

        info = '\n'+'FIELD STATISTICS'+'\n'
        info += '__________________________________'+'\n\n\n'
        info += 'Field name: ' + f'{field.name}\n'
        info += 'Country: ' + f'{field.country}\n'
        info += 'Region: ' + f'{field.region}\n'
        info += 'Number of samples: ' + f'{len(field.locations)}\n'
        info += 'Percentage of healthy: ' + f'{n_healthy/len(field.locations) * 100}%\n'
        info += 'Percentage of unclear: ' + f'{n_doubt/len(field.locations) * 100}% \n'
        info += 'Percentage of ill: ' + f'{n_ill/len(field.locations) * 100}% \n'
        print(info)

        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("Phetsarath_OT.ttf", 40)
        d.text((70,70), info, fill=(0,0,0), font=font)
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "static/images/stats.png")
        img.save(path)

def createStatisticsKML():
    info_kml = 'slave_' + str(global_vars.screen_for_statistics) + '.kml'
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    xml += '<kml xmlns="http://www.opengis.net/kml/2.2" '
    xml += 'xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:atom="http://www.w3.org/2005/Atom">'
    xml += '\n\t'+'<Document>'
    xml += '\n\t\t'+'<Folder>'
    xml += '\n\t\t\t'+'<ScreenOverlay>'
    xml += '\n\t\t\t\t'+'<name>Stats</name>'
    xml += '\n\t\t\t\t'+'<Icon>'
    xml += '\n\t\t\t\t\t'+'<href>http://lg1:81/CD/stats.png</href>'
    xml += '\n\t\t\t\t'+'</Icon>'
    xml += '\n\t\t\t\t'+'<overlayXY x="0" y="1" xunits="fraction" yunits="fraction"/>'
    xml += '\n\t\t\t\t'+'<screenXY x="0" y="1" xunits="fraction" yunits="fraction"/>'
    xml += '\n\t\t\t\t'+'<rotationXY x="0" y="0" xunits="fraction" yunits="fraction"/>'
    xml += '\n\t\t\t\t'+'<size x="0" y="0" xunits="fraction" yunits="fraction"/>'
    xml += '\n\t\t\t'+'</ScreenOverlay>'
    xml += '\n\t\t'+'</Folder>'
    xml += '\n\t'+'</Document>'
    xml += '\n'+'</kml>'
    
    
    print(info_kml)
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, global_vars.kml_destination_path)

    if os.path.exists(path):
        f = open(path + 'slave_{}.kml'.format(global_vars.screen_for_statistics), "w")
    else:
        raise ValueError(path)
    f.write(xml)
    f.close()

def getDiagnoseColor(diagnosis):
    if 0 < float(diagnosis) and float(diagnosis) < 30:
        return "5014F00A"
    elif float(diagnosis) < 60:
        return "501478FA"
    else:
        return "501400FA"

def CreateFieldKML(field: utils.Field) -> None:
    kml = KML.kml(
        KML.Document(
            KML.Folder(
                KML.name('Fields'))
            )
        )

    filename = global_vars.kml_destination_filename

    
    print(field)
    kml.Document.Folder.append(
        KML.Placemark(
            KML.name(field.name),
            KML.Style(
            KML.PolyStyle(
                KML.color('#188804'),
                KML.outline(1)
                )
            ),
            KML.Polygon(
                KML.outerBoundaryIs(
                    KML.LinearRing(
                        KML.coordinates(GetCoords(field))
                    ),
                    KML.extrude(1),
                    KML.altitudeMode("relativeToGround")
                )
            ),
            KML.Style(
                KML.PolyStyle(
                    KML.color("ff0000ff"),
                    KML.outline(1)
                )
            )
        )
    )

    for location in field.locations:
        color = getDiagnoseColor(location.diagnose)
        kml.Document.Folder.append(
            KML.Placemark(
                KML.name(location.image),
                KML.description("Diagnose: " + location.diagnose),
                KML.Style(
                    KML.BalloonStyle(
                        KML.bgColor(color)
                    ),    
                ),
                GX.balloonVisibility(1),
                KML.Point(
                    KML.coordinates(str(location.coord.longitude) + ',' + location.coord.latitude)
                )
            )
        )

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, global_vars.kml_destination_path)
   
    if os.path.exists(path):
        f = open(path + filename, "w")
    else:
        raise ValueError(path)
    out = etree.tostring(kml, pretty_print=True).decode("utf-8")
    f.write(out)
    f.close()

def CreateKMLS(field):
    CreateFieldKML(field)
    createStatisticsKML()
