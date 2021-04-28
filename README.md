# FlightSimCSVTools
A set of command line Python scripts to help manage .csv files used in flight simulation for maintaining POIS. As used by Little Navmap, Plan-G and Avitab.

The scripts may be run on Windows or Linux. Or bash for Windows.

## Installation
Install python3.

If installing python on Windows, ensure that python is added to PATH in the appropriate installation dialog.

The scripts use the simplekml library. To install use :

```
% pip install simplekml
```

If you have both python2 and python3, use pip3 to install simplekml

When running the scripts, ensure python3 is being used. For a system in which python3 is the only version installed, "python" can probably be used. For a system which has more than one version installed, "python3" is more likely.

## Running

### KML2FlightSimCSV
```
% python KML2FlightSimCSV [arg]
```
If arg is a file, the script will convert it to a .csv file. The input file must be .kml or .kmz.

If arg is a directory, the script will parse all kml and kmz files recursively   found in that directory. 

If arg is omitted, the current directory is selected as the input directory.

Once all POIs have been parsed, any duplicates are filtered out. 

The output .csv file is given a name derived from the input file or directory name and is written to the same location as the input file or directory.

### FlightSimCSV2KML
```
% python FlightSimCSV2KML [arg]
```
If arg is a file, the script will convert it to a .kml file. The input file must be a .csv file, formatted as described in LittleNavMap or PlanG documentation.

If arg is a directory, the script will parse all .csv files recursively found in that directory. 

If arg is omitted, the current directory is selected as the input directory.

Once all POIs have been parsed, any duplicates are filtered out. 

The output .kml file is given a name derived from the input file or directory name and is written to the same location as the input file or directory.

### MergeCSV

```
% python MergeCSV primaryCSVFile newDataCSVFile
```

The use-case for this script is where new POIs is a .csv are required to be merged into existing primary POIs, without duplicates. The script does not perform the actual merge, but classifies all new POIs into one of 4 types : existing, renamed, new and query. 4 new .csv files are created containing the items for each respective class. It is then up to the user to cut'n'paste from these files into the primary POI database.

The classification is implemented by comparing the name of a new POI and its distance from, all existing primary POIs. 

POIs classified as "existing" are very near an existing primary POI with an identical name match. They should not be added to the primary database.

POIs classified as "renamed" are very near an existing primary POI with some similar words in the name. They require the user to decide whether to keep the version in the primary .csv or the new .csv.

POIs classified as "new" have a completely different name and are not near any existing POI. They can usually just be added directly to the primary data.

POIs classified as "query" don't fall into any of the previous categories. They will be near another POI, but unclear whether renamed. They require the user to decide whether to merge.

A merge_report file is also generated, which should help the user understand how classifications were decided for each of the new candidate POIs.

## Issues and Troubleshooting

The scripts are a work in progress and do have room for improvement. Please refer to the github project page for known issues or plans for improvement.

Please report any other issues or enhancement requests on the github project page.




