import json
import os

def combine_geojson_files(directory_path):
    # Initialize an empty FeatureCollection
    region_geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    # List all GeoJSON files in the provided directory
    geojson_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

    # Loop through each file
    for file_name in geojson_files:
        file_path = os.path.join(directory_path, file_name)
        with open(file_path, 'r') as file:
            # Load GeoJSON data from file
            data = json.load(file)

            # Check if the data is a FeatureCollection
            if data['type'] == 'FeatureCollection':
                # Add each feature to the new FeatureCollection
                region_geojson['features'].extend(data['features'])
            elif data['type'] == 'Feature':
                # Add the feature directly to the new FeatureCollection
                region_geojson['features'].append(data)
            else:
                print(f"File {file_name} does not contain a valid GeoJSON Feature or FeatureCollection")

    # Save the combined GeoJSON to a new file
    with open('combined_region.geojson', 'w') as outfile:
        json.dump(region_geojson, outfile, indent=4)

    print(f"Combined GeoJSON file created with {len(region_geojson['features'])} features.")

# Replace 'path_to_your_geojson_files' with the path to the directory containing your GeoJSON files
combine_geojson_files('/mnt/d/ronnie/Projects/geodata-br/geojson')
