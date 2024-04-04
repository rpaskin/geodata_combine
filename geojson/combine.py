import json
import os

def ensure_right_hand_rule(geometry):
    def is_clockwise(ring):
        # Calculate the area under the curve.
        total = 0
        for i in range(len(ring) - 1):
            x1, y1 = ring[i]
            x2, y2 = ring[i + 1]
            total += (x2 - x1) * (y2 + y1)
        return total > 0

    def enforce_orientation(ring, clockwise):
        # Reverse ring orientation if necessary.
        if is_clockwise(ring) != clockwise:
            ring.reverse()
        return ring

    if geometry['type'] == 'Polygon':
        geometry['coordinates'][0] = enforce_orientation(geometry['coordinates'][0], clockwise=True)
        for i in range(1, len(geometry['coordinates'])):
            geometry['coordinates'][i] = enforce_orientation(geometry['coordinates'][i], clockwise=False)

    elif geometry['type'] == 'MultiPolygon':
        for p in range(len(geometry['coordinates'])):
            geometry['coordinates'][p][0] = enforce_orientation(geometry['coordinates'][p][0], clockwise=True)
            for i in range(1, len(geometry['coordinates'][p])):
                geometry['coordinates'][p][i] = enforce_orientation(geometry['coordinates'][p][i], clockwise=False)

    return geometry

def combine_geojson_files(directory_path):
    region_geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    geojson_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]

    for file_name in geojson_files:
        file_path = os.path.join(directory_path, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                if data['type'] == 'FeatureCollection':
                    for feature in data['features']:
                        feature['geometry'] = ensure_right_hand_rule(feature['geometry'])
                    region_geojson['features'].extend(data['features'])
                elif data['type'] == 'Feature':
                    data['geometry'] = ensure_right_hand_rule(data['geometry'])
                    region_geojson['features'].append(data)
                else:
                    print(f"File {file_name} does not contain a valid GeoJSON Feature or FeatureCollection")
        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

    with open('combined_region.geojson', 'w', encoding='utf-8') as outfile:
        json.dump(region_geojson, outfile, ensure_ascii=False, indent=4)

    print(f"Combined GeoJSON file created with {len(region_geojson['features'])} features.")

# Replace 'path_to_your_geojson_files' with the path to the directory containing your GeoJSON files
combine_geojson_files('/mnt/d/ronnie/Projects/geodata-br/geojson')
