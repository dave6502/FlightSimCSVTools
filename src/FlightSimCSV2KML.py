import sys, os, re
import glob
import zipfile
import shutil
import math
import xml.etree.ElementTree as ET
import Common
from pprint import pprint

try:
    import simplekml
except:
    print("Please install the python simplekml library")
    sys.exit(-1)

def parse_csvs(all_csv_filenames):
    pois = []
    for csv_filename in all_csv_filenames:
        pois = pois + Common.parse_csv(csv_filename)
    return pois

def write_kml(filename, pois):
    kml = simplekml.Kml()
    for poi in pois:
        kml.newpoint(name=poi.name, coords=[(poi.long, poi.lat)])
    kml.save(filename)


# MAIN

try:
    arg = sys.argv[1]
except:
    arg = "."
path = Common.get_path(arg)

if os.path.isdir(path):
    all_csv_filenames = glob.glob('**/*.csv', recursive=True)
    pois = parse_csvs(all_csv_filenames)
    out_filename = os.path.basename(path) + ".kml"
else:
    if path[-4:] != ".csv":
        print("Error - filename '%s' must be .csv"%path)
        sys.exit(-1)
    pois = Common.parse_csv(path)
    out_filename = os.path.splitext(path)[0] + ".kml"
out_filename = out_filename.replace(" ", "_")

print("%d total POIs"%len(pois))

pois = Common.filter_duplicates(pois)

print("%d total POIs after filtering"%len(pois))

write_kml(out_filename, pois)


