import sys, os, re
import glob
import shutil
import math
import xml.etree.ElementTree as ET
import Common
from pprint import pprint

def get_string_match_score(primary_name, new_name):
    if (primary_name == new_name):
        return 100
    #else:
    #    return 0
    primary_name = primary_name.lower().split()
    new_name = new_name.lower().split()
    dont_match = [",", "-", "st", "of", "and", "the", "bridge", "tower", "castle", "stadium", "lighthouse", "church", 
        "cathedral", "pier", "abbey", "airport", "park", "national", "street", "road", "hall", "museum"
        "transmitter", "transmitting", "mast", "station", "railway", "centre", "library", "building",
        "viaduct", "rock", "hill", "palace", "north", "east", "south", "west", "old", "house", "power",
        "fort", "city", "monument", "bank", "court"]
    for remove_word in dont_match:
        if remove_word in primary_name:
            primary_name.remove(remove_word)
        if remove_word in new_name:
            new_name.remove(remove_word)
    if primary_name == [] or new_name == []:
        return 0
    matching_words = list(set(primary_name) & set(new_name))
    return (len(matching_words) * 99) / len(new_name)

# MAIN

try:
    primary_file = sys.argv[1]
    new_data_file = sys.argv[2]
except:
    print("Usage : PrimaryFile.csv NewDataFile.csv")
    sys.exit(-1)
    
working_dir = os.getcwd()
primary_file = Common.get_path(primary_file)
os.chdir(working_dir)
new_data_file = Common.get_path(new_data_file)

if primary_file[-4:] != ".csv" or new_data_file[-4:] != ".csv" :
    print("Error - Both filenames must be .csv")
    sys.exit(-1)
    
primary_pois = Common.parse_csv(primary_file, preserve_description_field = True)
new_candidate_pois = Common.parse_csv(new_data_file, preserve_description_field = True)

if False: 
    Common.write_csv(primary_file.replace(".", "_check."), primary_pois)
    Common.write_csv(new_data_file.replace(".", "_check."), new_candidate_pois)

existing_pois = []
query_pois = []
new_pois = []
renamed_pois = []

merge_report = open(re.sub("\..*", "_merge_report.txt", new_data_file),"w")

for new_poi in new_candidate_pois:
    merge_report.write(str(new_poi) + "\n")
    exact_match = False
    partial_match = False
    renamed = False
    for primary_poi in primary_pois:
        # merge_report.write(primary_poi)  
        distance = int(primary_poi.distance_from(new_poi))
        name_match_score = get_string_match_score(primary_poi.name, new_poi.name)
        if (distance >= 100) and (name_match_score == 0):
            # > 100m away and completely different name, so ignore
            continue
        if (distance >= 10000) and (name_match_score <  50):
            # > 10km away and fairly different name, so ignore
            continue
        if (distance < 1) and (name_match_score == 100):
            exact_match = True
            break
        if (distance < 1) and (name_match_score < 100):
            renamed = True
            merge_report.write("%3d%% %7dm %sn"%(name_match_score,distance, repr(primary_poi)))
            break
        partial_match = True
        merge_report.write("%3d%% %7dm %s\n"%(name_match_score,distance, repr(primary_poi)))
    if exact_match:
        merge_report.write("-> exists\n")
        existing_pois.append(new_poi)
    elif partial_match:
        merge_report.write("-> query\n")
        query_pois.append(new_poi)
    elif renamed:
        merge_report.write("-> renamed\n")
        renamed_pois.append(new_poi)
    else:
        merge_report.write("-> new\n")
        new_pois.append(new_poi)
    merge_report.write("\n")
 
Common.write_csv(new_data_file.replace(".", "_existing."), existing_pois)
Common.write_csv(new_data_file.replace(".", "_query."), query_pois)
Common.write_csv(new_data_file.replace(".", "_new."), new_pois)
Common.write_csv(new_data_file.replace(".", "_renamed."), renamed_pois)

