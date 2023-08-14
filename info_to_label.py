import os
from datetime import datetime
import matplotlib.pyplot as plt

class Info2Label:
    """Get teles info from QgsLayer and draw it to a label 
    with white background and black text
    """

    def __init__(self, layer, year=None):
        self.layer = layer
        self.year = year
        self.label = plt.figure(figsize=(17,2.1))
        self.ax = self.label.add_subplot()
        self.ax.axis([0, 170, 1, 3.7])
        self.ax.axis('off')
        ## use microsoft jhenghei font
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
        self.infos = {}

    def main(self):
        self.get_info()
        _time = self.draw_label()
        self.save_label()
        return _time

    def get_info(self):
        """Get teles info from QgsLayer"""
        for feature in self.layer.getFeatures():
            if feature['Name'] == 'SmsDateTime2':
                self.infos['SmsDateTime1'] = feature['Value']
                self.infos['SmsDateTime2'] = datetime.strptime(self.infos['SmsDateTime1'], '%m/%d_%H:%M').strftime('%m/%d %H:%M')
                if self.year:
                    self.infos['SmsDateTime2'] = self.year + '/' + self.infos['SmsDateTime2']
            elif feature['Name'] == 'SmsEpicLoc':
                self.infos['SmsEpicLoc'] = feature['Value']
            elif feature['Name'] == 'SmsRespLevel':
                self.infos['SmsRespLevel'] = feature['Value']
            elif feature['Name'] == 'SmsEpicX':
                self.infos['SmsEpicX'] = feature['Value']
            elif feature['Name'] == 'SmsEpicY':
                self.infos['SmsEpicY'] = feature['Value']
            elif feature['Name'] == 'SmsDepth':
                self.infos['SmsDepth'] = feature['Value']
            elif feature['Name'] == 'SmsMag':
                self.infos['SmsMag'] = feature['Value']
        
        self.infos['coordinate'] = f"{self.infos['SmsEpicX']}°E, {self.infos['SmsEpicY']}°N"

    def draw_text(self, text, x, y, **kwargs):
        """Draw text on label"""
        self.ax.text(x, y, text, fontsize=28, **kwargs)

    def draw_label(self):
        """Draw label with white background and black text"""
        self.draw_text('發生時間:', 0, 3, weight='bold')
        self.draw_text(self.infos['SmsDateTime2'], 25, 3)
        self.draw_text('地震震央:', 0, 2, weight='bold')
        self.draw_text(self.infos['SmsEpicLoc'], 25, 2)
        self.draw_text('動員層級:', 0, 1, weight='bold')
        self.draw_text(self.infos['SmsRespLevel'], 25, 1)
        self.draw_text('地震規模:', 95, 3, weight='bold')
        self.draw_text(self.infos['SmsMag'], 120, 3)
        self.draw_text('震央座標:', 95, 2, weight='bold')
        self.draw_text(self.infos['coordinate'], 120, 2)
        self.draw_text('震源深度:', 95, 1, weight='bold')
        self.draw_text(self.infos['SmsDepth'] + 'km', 120, 1)
        if self.year:
            return datetime.strptime(self.year + '/' + self.infos['SmsDateTime1'], '%Y/%m/%d_%H:%M')
        else:
            return datetime.strptime(self.infos['SmsDateTime1'], '%m/%d_%H:%M')

    def save_label(self):
        """Save label to png file"""
        path = os.path.join(os.path.dirname(__file__), 'label.png')
        self.label.savefig(path, bbox_inches='tight', pad_inches = 0)

if __name__ == '__main__':
    from qgis.core import QgsApplication, QgsVectorLayer
    QgsApplication.setPrefixPath(r'C:/OSGeo4W/apps/qgis-ltr', True)
    qgs =  QgsApplication([], False)
    qgs.initQgis()
    layer = QgsVectorLayer(r'C:\Users\olove\Downloads\AutoRun\D20221003\E0425\ScenarioData.TAB', 'teles', 'ogr')
    info2label = Info2Label(layer)
    info2label.get_info()
    info2label.draw_label()
    info2label.save_label()