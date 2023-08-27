from qgis.core import (
    QgsProject, QgsProject, QgsLayoutExporter
    )
import os
import time
from datetime import datetime
import sys

FILE_DIR = os.path.dirname(__file__)
WORKING_DIR = os.path.join(FILE_DIR, 'export_image_working_dir')
PROJECT_PATH = os.path.join(WORKING_DIR, 'project_demo.qgz')
IMG_FOLDER = os.path.join(FILE_DIR, os.path.pardir, 'images')

def main(output_dir, dpi=300):
    from qgis.core import QgsApplication

    # set QGIS prefix path according to platform
    if sys.platform == 'win32' or sys.platform == 'win64':
        QgsApplication.setPrefixPath(r'C:/OSGeo4W/apps/qgis-ltr', True)
    if os.getenv('QGIS_PREFIX_PATH'):
        QgsApplication.setPrefixPath(os.getenv('QGIS_PREFIX_PATH'), True)
    # create a reference to the QgsApplication, set gui enabled to False
    qgs =  QgsApplication([], False)
    qgs.initQgis()
    # load project
    project = QgsProject.instance()
    project.read(PROJECT_PATH)

    filename = os.path.join(output_dir, datetime.now().strftime("%Y%m%d_%H%M%S") + '.png')
    export_image(project, filename, dpi)
    # add a delay to ensure the project is closed before exiting the script
    time.sleep(1)
    qgs.exitQgis()
    time.sleep(1)
    del QgsApplication
    return True
    
def export_image(project, filename, dpi):
    # get fist layout or alternative layout by name: layout = project.layoutManager().layoutByName('layout_name')
    layout = project.layoutManager().layouts()[0]
    output_path = filename
    # set image export settings
    setting = QgsLayoutExporter.ImageExportSettings()
    setting.dpi = dpi
    exporter = QgsLayoutExporter(layout)
    result = exporter.exportToImage(output_path, setting)
    time.sleep(1)
    if result == QgsLayoutExporter.Success:
        print(output_path, 'success')
    else:
        print(result)

if __name__ == '__main__':
    main(IMG_FOLDER, 300)