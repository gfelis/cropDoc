import io
import zipfile
import re
import os

from lxml import etree
from pandas import read_csv, to_numeric

from utils import *

import itertools

#Source code from https://blog.adimian.com/2018/09/04/fast-xlsx-parsing-with-python/

class XLSX:

    sheet_xslt = etree.XML('''
        <xsl:stylesheet version="1.0"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            xmlns:sp="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
            >
            <xsl:output method="text"/>
            <xsl:template match="sp:row">
               <xsl:for-each select="sp:c">
                <xsl:value-of select="parent::*/@r"/> <!-- ROW -->
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@r"/> <!--REMOVEME-->
                <xsl:text>,</xsl:text>
                <xsl:value-of select="@t"/> <!-- TYPE -->
                <xsl:text>,</xsl:text>
                <xsl:value-of select="sp:v/text()"/> <!-- VALUE -->
               <xsl:text>\n</xsl:text>
               </xsl:for-each>
            </xsl:template>
        </xsl:stylesheet>
    ''')

    def __init__(self, file_path):
        self.ns = {
            'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
        }
        self.fh = zipfile.ZipFile(file_path)
        self.shared = self.load_shared()
        self.workbook = self.load_workbook()

    def load_workbook(self):
        # Load workbook
        name = 'xl/workbook.xml'
        root = etree.parse(self.fh.open(name))
        res = {}
        for el in etree.XPath("//ns:sheet", namespaces=self.ns)(root):
            res[el.attrib['name']] = el.attrib['sheetId']
        return res

    def load_shared(self):
        # Load shared strings
        name = 'xl/sharedStrings.xml'
        root = etree.parse(self.fh.open(name))
        res = etree.XPath("/ns:sst/ns:si/ns:t", namespaces=self.ns)(root)
        return {
            str(pos): el.text
            for pos, el in enumerate(res)
        }

    def _parse_sheet(self, root):
        transform = etree.XSLT(self.sheet_xslt)
        result = transform(root)
        df = read_csv(io.StringIO(str(result)),
                      header=None, dtype=str,
                      names=['row', 'cell', 'type', 'value'],
        )
        return df

    def read(self, sheet_name):
        sheet_id = self.workbook[sheet_name]
        sheet_path = 'xl/worksheets/sheet%s.xml' % sheet_id
        root = etree.parse(self.fh.open(sheet_path))
        df = self._parse_sheet(root)

        # First row numbers are filled with nan
        df['row'] = to_numeric(df['row'].fillna(0))

        # Translate string contents
        cond = (df.type == 's') & (~df.value.isnull())
        df.loc[cond, 'value'] = df[cond]['value'].map(self.shared)
        # Add column number and sort rows
        df['col'] = df.cell.str.replace(r'[0-9]+', '')
        df = df.sort_values(by='row')

        # Pivot everything
        df = df.pivot(
            index='row', columns='col', values='value'
        ).reset_index(drop=True).reset_index(drop=True)
        df.columns.name = None  # pivot adds a name to the "columns" array
        # Sort columns (pivot will put AA before B)
        cols = sorted(df.columns, key=lambda x: (len(x), x))
        df = df[cols]
        df = df.dropna(how='all')  # Ignore empty lines
        df = df.dropna(how='all', axis=1)  # Ignore empty cols
        return df

def grouper(n, iterable):
        it = iter(iterable)
        while True:
            chunk = tuple(itertools.islice(it, n))
            if not chunk:
                return
            yield chunk 

def parse(path):
    xlsx = XLSX(path)
    fields_df = xlsx.read('Fields (poligons)')
    locations_df = xlsx.read('Locations (arbres pins)')
    fields = parse_fields(fields_df)
    parse_locations(locations_df, fields)
    return fields

def parse_fields(df):
    
    updated_df = df.drop([df.index[0], df.index[1], df.index[2], df.index[3], df.index[7], df.index[11], df.index[15], df.index[16]])
    updated_df = updated_df.drop(columns='A')

    loc_info = updated_df.iloc[:,:3]
    polygon_info = updated_df.iloc[:,3:]

    loc_info = loc_info.reset_index(drop=True)
    polygon_info = polygon_info.reset_index(drop=True)

    fields = []
    for _, row in loc_info.iterrows():
        field = Field(row['B'])
        field.country = row['C']
        field.region = row['D']
        fields.append(field)       
    
    for i, row in polygon_info.iterrows():
        for point in grouper(3, row.values):
            if (not re.match('-?\d+\'\d+', str(point[0]))) or (not re.match('-?\d+\'\d+', str(point[0]))) or (not re.match('-?\d+\'\d+', str(point[0]))):
                continue
            else:
                longitude = point[0].replace("'", ".")
                latitude = point[1].replace("'", ".")
                altitude = point[2].replace("'", ".")
                fields[i].points.append(Point(longitude, latitude, altitude))
            
    fields_dict = {}
    for item in fields:
        fields_dict[item.name] = item
    return fields_dict

def parse_locations(df, fields):
    updated_df = df.drop([df.index[0]])
    updated_df = updated_df.drop(columns=['A', 'I'])

    for _, row in updated_df.iterrows():
        if(re.match("0", row[3])):
            row[3] = "200'0"
        if (not re.match('-?\d+\'\d+', str(row[1]))) or (not re.match('-?\d+\'\d+', str(row[2]))) or (not re.match('-?\d+\'\d+', str(row[3]))):
                print("Not matching")
                continue
        field_name = row[0]
        if field_name in fields.keys():
            fields[field_name].locations.append(Location(Point(row[1].replace("'", "."), row[2].replace("'", "."), row[3].replace("'", ".")), row[4], row[5]))
        


if __name__ == '__main__':

    # TEST

    p = os.path.sep.join([os.path.dirname(__file__), 'xls/jorge_gil.xlsx'])
    if os.path.exists(p):
        fields = parse(p)
    for field in fields:
        print(fields[field])
        print("")
        print(fields[field].points)
        print("")
        print(fields[field].locations)
        print("=============")
        


    
       

