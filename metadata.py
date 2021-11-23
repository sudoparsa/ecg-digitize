import os
import json
import copy

metadata_path = 'metadata\\50-3            _200805140933-jpg.json'
path = 'C:\\Users\\Parsa\\Desktop\\ECG\\final\\ECG_Record\\'
out_path = path + '.paperecg\\'
if not os.path.isdir(out_path):
    os.mkdir(out_path)

if not os.path.isfile(metadata_path):
    print('Warning: No metadata file found!')
else:
    with open(metadata_path) as metadata_json:
        metadata = json.load(metadata_json)
        files = os.listdir(path)
        for file_name in files:
            if os.path.isfile(path + file_name):
                data = copy.deepcopy(metadata)
                data['image']['name'] = file_name
                data['image']['directory'] = path
                name, extension = file_name.split('.')
                outfile = open(out_path + name + '-' + extension + '.json', 'w')
                json.dump(data, outfile)
                outfile.close()