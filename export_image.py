from qgis.core import (
    QgsProject, QgsCoordinateReferenceSystem, QgsProject, QgsCoordinateTransform, 
    QgsLayoutExporter, QgsCoordinateReferenceSystem, QgsGeometry
    )
import argparse
import os
import shutil
import time
from datetime import datetime
import sys
from info_to_label import Info2Label

## interpreter: C:/OSGEO4W/bin/python-qgis-ltr.bat

FILES = ['Epicenter.DBF', 'Epicenter.ID', 'Epicenter.MAP', 'Epicenter.TAB',
        'Evt1GbsTownLoss.TAB', 'Evt1GbsTownLoss.IND', 'Evt1GbsTownLoss.DBF',
        'ScenarioData.TAB', 'ScenarioData.DBF', 'Evt1GmDmnd.TAB', 'Evt1GmDmnd.DBF']
FILES_NO_CAS = ['Epicenter.DBF', 'Epicenter.ID', 'Epicenter.MAP', 
                'Epicenter.TAB', 'ScenarioData.TAB', 'ScenarioData.DBF']
FILE_DIR = os.path.dirname(__file__)
WORKING_DIR = os.path.join(FILE_DIR, 'export_image_working_dir')
PROJECT_PATH = os.path.join(WORKING_DIR, 'project.qgz')
PROJECT_NO_CAS_PATH = os.path.join(WORKING_DIR, 'project_no_cas.qgz')
IMG_FOLDER = os.path.join(FILE_DIR, 'images')
NO_CAS = False

def main(target_dir, output_dir, dpi):
    from qgis.core import QgsApplication
    if sys.platform == 'win32' or sys.platform == 'win64':
        QgsApplication.setPrefixPath(r'C:/OSGeo4W/apps/qgis-ltr', True)
    elif sys.platform == 'linux':
        QgsApplication.setPrefixPath('/usr', True)
    qgs =  QgsApplication([], False)
    qgs.initQgis()
    project = QgsProject.instance()
    if not check_files(target_dir):
        return False
    update_working_dir(target_dir)
    # remove label.png
    if os.path.exists(os.path.join(FILE_DIR, 'label.png')):
        os.remove(os.path.join(FILE_DIR, 'label.png'))
    get_label()
    year = os.path.basename(os.path.dirname(target_dir))[1:5]
    if NO_CAS:
        project.read(PROJECT_NO_CAS_PATH)
    else:
        project.read(PROJECT_PATH)
    layout_setting(project, year)
    filename_ = os.path.split(target_dir)[-2] + '_' + os.path.split(target_dir)[-1] + '.png'
    filename = os.path.join(output_dir, os.path.split(filename_)[-1])
    export_image(project, filename)
    time.sleep(1)
    qgs.exitQgis()
    time.sleep(1)
    del QgsApplication
    return True
    
def export_image(project, filename):
    layout = project.layoutManager().layoutByName('rosa_line_notify')
    output_path = filename
    setting = QgsLayoutExporter.ImageExportSettings()
    setting.dpi = 300
    exporter = QgsLayoutExporter(layout)
    result = exporter.exportToImage(output_path, setting)
    done = False
    while (not done):
        time.sleep(1)
        if os.path.getsize(output_path) > 1000:
            done = True
    if result == QgsLayoutExporter.Success:
        print(output_path, 'success')

    setting = QgsLayoutExporter.ImageExportSettings()
    setting.dpi = 48
    _path = output_path[:-4] + "_s.jpg"
    result = exporter.exportToImage(_path, setting)
    done = False
    while (not done):
        time.sleep(1)
        if os.path.getsize(output_path) > 1000:
            done = True
    if result == QgsLayoutExporter.Success:
        print(_path, 'success')

def get_label():
    # load project
    project = QgsProject.instance()
    project.read(PROJECT_PATH)
    layer = project.mapLayersByName('ScenarioData')[0]
    label = Info2Label(layer=layer)
    _time = label.main()
    # wait until label.png is created
    while not os.path.exists(os.path.join(FILE_DIR, 'label.png')):
        time.sleep(1)
    return

def layout_setting(project, year):
    layout = project.layoutManager().layoutByName('rosa_line_notify')
    layout.initializeDefaults()
    # set map extent
    _map = layout.itemById('Map 1')
    # has casuality
    if NO_CAS != True:
        town_layer = project.mapLayersByName('推估損失 (鄉鎮市區)')[0]
        layer = project.mapLayersByName('Evt1GbsTownLoss')[0]
        # filter town layer
        towns_to_show = []
        for feature in layer.getFeatures():
            towns_to_show.append(feature['town_code'])
        # int to str
        towns_to_show = [str(i) for i in towns_to_show]
        town_layer.setSubsetString(f"Town_code IN {tuple(towns_to_show)}")
        _extent = town_layer.extent()
        src = QgsCoordinateReferenceSystem(3826)
        dst = QgsCoordinateReferenceSystem(4326)
        tr = QgsCoordinateTransform(src, dst, project)
        extent = QgsGeometry.fromRect(_extent)
        extent.transform(tr)
        _map.zoomToExtent(extent.boundingBox())

    # set label text
    layer = project.mapLayersByName('ScenarioData')[0]
    return

def update_working_dir(target_dir):
    for file in os.listdir(WORKING_DIR):
        if file in FILES:
            os.remove(os.path.join(WORKING_DIR, file))
    
    if NO_CAS != True:
        for file in FILES:
            _path = os.path.join(target_dir, file)
            # move file to project folder
            _new_path = os.path.join(WORKING_DIR, file)
            shutil.copy(_path, _new_path)
    else:
        for file in FILES_NO_CAS:
            _path = os.path.join(target_dir, file)
            # move file to project folder
            _new_path = os.path.join(WORKING_DIR, file)
            shutil.copy(_path, _new_path)

def check_files(dir):
    # check complete
    global NO_CAS
    if not os.path.exists(os.path.join(dir, 'Complete.txt')):
        print("Not complete yet! (No Complete.txt)")
        return False
    with open(os.path.join(dir, 'Complete.txt'), 'r', encoding='utf-8') as f:
        state = str(f.read()).strip()
    if state != '1':
        print(f"Not complete yet! state:{state}")
        return False
    # check if all files exists
    # self.project_path = PROJECT_PATH
    NO_CAS = False
    for file in FILES:
        if not os.path.exists(os.path.join(dir, file)):
            message = \
                f"{file} not found in {dir}, using no casualties project"
            print(message)
            # self.project_path = PROJECT_NO_CAS_PATH
            NO_CAS = True
            break
    for file in FILES_NO_CAS:
        if not os.path.exists(os.path.join(dir, file)):
            message = \
                f"{file} not found in {dir}, please check again"
            print(message)
            return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True)
    parser.add_argument('--output', '-o', type=str, default='default')
    parser.add_argument('--dpi', '-d', type=int, default=300)
    parser.add_argument('--working_dir', '-w', type=str, default='default')
    target_dir = parser.parse_args().input
    output_dir = parser.parse_args().output
    if output_dir == 'default':
        output_dir = IMG_FOLDER
    working_dir = parser.parse_args().working_dir
    if working_dir == 'default':
        working_dir = WORKING_DIR
        # check if project file .qgz exists
    if not os.path.exists(os.path.join(working_dir, 'project.qgz')):
        print("project.qgz not found, please check argument --working_dir")
        print("working_dir:", working_dir)
        exit()
    dpi = parser.parse_args().dpi

    main(target_dir, output_dir, dpi)