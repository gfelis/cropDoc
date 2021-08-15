# -*- coding: utf-8 -*-

# Import libraries
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
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

def CreateFieldsKML(field: utils.Field) -> None:
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
            KML.Style(
            KML.PolyStyle(
                KML.color('#188804'),
                KML.outline(10)
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
                    KML.outline(10)
                )
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

def CreateKML(fields):
    CreateFieldsKML(fields)
    CreateLogosKML()
