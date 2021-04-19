import sys, os, re
import glob
import zipfile
import shutil
import math
import xml.etree.ElementTree as ET
import Common

OUTPUT_FILENAME = "user_fix.csv"


def unzip_kmz_file(filename):
    dirname = filename.replace(".kmz", "_kmz")
    print("Unzipping '%s' -> '%s'"%(filename, dirname))
    with zipfile.ZipFile(filename, 'r') as zip_file:
        zip_file.extractall(dirname)
    return dirname

def unzip_kmz_files():
    dirs = []
    filenames = glob.glob('**/*.kmz', recursive=True)
    for filename in filenames:
        dirname = unzip_kmz_file(filename)
        dirs.append(dirname)
    return dirs

def remove_dirs(dirs):
    for d in dirs:
        print("Removing '%s'"%d)
        shutil.rmtree(d)

def parse_kml(kml_filename):
    print("Parsing '%s'"%kml_filename)
    pois = []
    root = ET.parse(kml_filename).getroot()
    xmlns = re.findall("({.*?})", root.tag)[0]
    for placemark in root.iter(xmlns + "Placemark"):
        name = placemark.find(xmlns + "name").text
        name = name.replace("\n", " ")
        polygon = placemark.find(".//" + xmlns + "Polygon")
        if polygon != None: # Only interested in single point elements
            continue
        if placemark.find(".//" + xmlns + "longitude") != None:
            long = placemark.find(".//" + xmlns + "longitude").text
            lat = placemark.find(".//" + xmlns + "latitude").text
        elif placemark.find(".//" + xmlns + "coordinates") != None:
            coordinates = placemark.find(".//" + xmlns + "coordinates").text
            long = coordinates.split(",")[0]
            lat = coordinates.split(",")[1]
        pois.append(Common.Poi(kml_filename, name, float(lat), float(long)))
    print("Parsed %d POIs"%len(pois))
    return pois

def parse_kmls(all_kml_filenames):
    pois = []
    for kml_filename in all_kml_filenames:
        pois = pois + parse_kml(kml_filename)
    return pois



# MAIN

try:
    arg = sys.argv[1]
except:
    arg = "."
path = Common.get_path(arg)

if os.path.isdir(path):
    temp_kmz_dirs = unzip_kmz_files()
    all_kml_filenames = glob.glob('**/*.kml', recursive=True)
    pois = parse_kmls(all_kml_filenames)
    out_filename = os.path.basename(path) + ".csv"
else:
    if path[-4:] == ".kmz":
        kmz_dirname = unzip_kmz_file(path)
        temp_kmz_dirs = [kmz_dirname]
        all_kml_filenames = glob.glob(kmz_dirname + '/*.kml', recursive=True)
        pois = parse_kmls(all_kml_filenames)
    elif path[-4:] == ".kml":
        pois = parse_kml(path)
    else:
        print("Error - filename '%s' must be .kml or .kmz"%path)
        sys.exit(-1)               
    out_filename = os.path.splitext(path)[0] + ".csv"
out_filename = out_filename.replace(" ", "_")

print("%d total POIs"%len(pois))

if 'temp_kmz_dirs' in globals():
    remove_dirs(temp_kmz_dirs)

pois = Common.filter_duplicates(pois)

print("%d total POIs after filtering"%len(pois))

Common.write_csv(out_filename, pois)


