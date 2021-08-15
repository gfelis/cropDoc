from PIL import Image, ImageDraw, ImageFont
import os

def save_stats_as_img(path):
        img = Image.new('RGB', (1100, 1400), color = 'white')

        info = '\n'+'FIELD STATISTICS'+'\n'
        info += '__________________________________'+'\n\n\n'
        #info += 'TIMESTAMP:'+f'{dict_stats["Last refresh"]}'+'\n\n'
        print(info)

        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("NotoSans-SemiCondensedMedium.ttf", 40)
        d.text((70,70), info, fill=(0,0,0), font=font)
        img.save(path)

if __name__ == '__main__':
    #ConfigurationFile.LoadConfigFile()
    #p = os.path.sep.join([os.path.dirname(os.path.abspath(__file__)), 'xls/jorge_gil.xlsx'])
    #if os.path.exists(p):
    #    fields = parser.parse(p)
    #GenerateKml.CreateKML(fields['Campo de Gracia'])
    #kml_utils.sendKmlToLG(global_vars.kml_destination_filename)
    #kml_utils.flyToField(fields['Campo de Gracia'], 1440)
    
    save_stats_as_img('image.png')


    

