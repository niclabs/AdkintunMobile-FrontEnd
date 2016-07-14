from app.data import initial_data_antennas
import urllib.request, json
import codecs
import time

def main():
    file = open('app/data/data_antennas.py', 'w')
    reader = codecs.getreader("utf-8")
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=googleplex&sensor=false"
    response = urllib.request.urlopen(url)
    antennasDICT = json.loads(initial_data_antennas.initial_data_antennas)
    antennas = antennasDICT["antennas"]
    size = len(antennas)

    file.write("data_antennas = [\n")
    for i in range(size):
        if (not (i+1)%200):
            print ("Wrote ",i+1," antennas")
        lat = str(antennas[i]["lat"])
        lon = str(antennas[i]["lon"])
        url = "http://localhost/nominatim/reverse?format=json&lat="+lat+"&lon="+lon+"&zoom=18&addressdetails=1"
        response = urllib.request.urlopen(url)
        data = json.load(reader(response))
        city = "unknown"
        region = "unknown"
        if ('error' not in data):
            if ('state' not in data["address"]):
                print("Searching ",i," in googlemaps")
                url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lon + "&sensor=false"
                response = urllib.request.urlopen(url)
                data = json.load(reader(response))
                for element in data["results"][0]["address_components"]:
                    if element["types"] == ["locality", "political"]:
                        city = element["long_name"]
                    if element["types"] == [ "administrative_area_level_1", "political" ]:
                        region = element["long_name"]
                time.sleep(1)
            elif ('city' in data["address"]):
                city = data["address"]["city"]
            elif ('town' in data["address"]):
                city = data["address"]["town"]
            elif ('village' in data["address"]):
                city = data["address"]["village"]

            if region=="unknown":
                region = data["address"]["state"]

        antennas[i]["city"] = city
        antennas[i]["region"] = region
        result = json.dumps(antennas[i], ensure_ascii=False)
        file.write(result + (",\n" if (i!=size-1) else "]"))
    file.close()



if __name__ == "__main__":
    main()



