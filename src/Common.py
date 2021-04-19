import math
import sys
import os
import csv

class Poi:

    def __init__(self, filename, name, lat, long):
        self.filename = filename
        self.name = name
        # Ideally, if comma in name, surround with quotes, but PlanG doesn't support
        #self.name = self.name.replace(',', " ")
        try:
            check_lat_float = float(lat)
            check_long_float = float(long)
        except:
            print("ERROR: lat = '%s', long = '%s' ?\n"%(lat, long))
            sys.exit(-1)
        self.lat = lat
        self.long = long

    def __repr__(self):
        #return ("%s %s %s %s"%(self.name, self.lat, self.long, self.filename))
        return ("%s %s %s"%(self.name, self.lat, self.long))

    def to_csv(self):
        name = self.name
        if ',' in name:
            name = '"' + name + '"'
        return ("POI,%s,,%s,%s,,,,%s"%(name, self.lat, self.long, self.filename))

    def distance_from(self, other):
        R = 6371000; # earth radius in meters
        phi1 = float(self.lat) * math.pi / 180.0;
        phi2 = float(other.lat) * math.pi / 180.0;
        deltaPhi = (float(other.lat) - float(self.lat)) * math.pi / 180.0;
        deltaLambda = (float(other.long) - float(self.long)) * math.pi / 180.0;
        a = math.sin(deltaPhi / 2.0) * math.sin(deltaPhi / 2.0) + \
               math.cos(phi1) * math.cos(phi2) * \
               math.sin(deltaLambda / 2.0) * math.sin(deltaLambda / 2.0);
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
        return R * c;



def get_path(arg):
    # ToDo - tidy this up.
    # get_path doesn't really describe what it does internally
    # and it has side effects of changing working dir which isn't ideal
    if sys.version_info.major < 3:
        print("Error - Requires python 3")
        sys.exit(-1)
    
    path = os.path.abspath(arg)
    if not os.path.exists(path):
        print("Error - path '%s' does not exist"%path)
        sys.exit(-1)
        
    if os.path.isdir(path):
        print("Processing directory %s"%path)
        os.chdir(path)
    else:
        dirname = os.path.dirname(path)
        os.chdir(dirname)
        if dirname == "":
            dirname = "."
        print("Processing file %s"%path)

    print("Working dir now '%s'"%os.getcwd())
    return path


def filter_duplicates(pois):
    filtered_pois = []
    for poi in pois:
        remove = False
        for other in filtered_pois:
            distance = poi.distance_from(other)
            if distance < 50 and (poi.name == other.name):
                print("Removing duplicate %s"%poi)
                remove = True
            if distance < 20:
                print("Removing co-located POI %s"%poi)
                print(" - keeping POI %s"%other)
                remove = True
        if not remove:
            filtered_pois.append(poi)
    return filtered_pois

def parse_csv(csv_filename, preserve_description_field=False):
    print("Parsing '%s'"%csv_filename)
    pois = []
    with open(csv_filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row == []:
                continue
            try:
                name = row[1]
                lat = row[3]
                long = row[4]
                description_field = row[8]
            except:
                print("Couldn't parse '%s'"%row)
                print(sys.exc_info()[0])
                sys.exit(-1)
            if not preserve_description_field:
                description_field = csv_filename
            pois.append(Poi(description_field, name, lat, long))
    print("Parsed %d POIs"%len(pois))
    return pois

def write_csv(filename, pois):
    with open(filename, 'w', encoding="utf-8") as file:
        abs_filename = os.path.join(os.getcwd(), filename)
        print("Writing to '%s'"%abs_filename)
        for poi in pois:
            file.write(poi.to_csv() + "\n")


