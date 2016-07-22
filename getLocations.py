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
            print ("Wrote ",i," antennas")
        lat = str(antennas[i]["lat"])
        lon = str(antennas[i]["lon"])
        url = "http://localhost/nominatim/reverse?format=json&lat="+lat+"&lon="+lon+"&zoom=18&addressdetails=1"
        city = "unknown"
        region = "unknown"
        try:
            response = urllib.request.urlopen(url)
            data = json.load(reader(response))
            if ('error' not in data):
                if ('city' in data["address"]):
                    city = data["address"]["city"]
                elif ('town' in data["address"]):
                    city = data["address"]["town"]
                elif ('village' in data["address"]):
                    city = data["address"]["village"]
                else:
                    region = data["address"]["state"]
                    raise UnknownCityError()

                region = data["address"]["state"]
        except:
            print("Searching ", i, " in googlemaps")
            url = "http://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat + "," + lon + "&sensor=false"
            response = urllib.request.urlopen(url)
            data = json.load(reader(response))
            if data["status"]=="OK":
                found = False
                for element in data["results"][0]["address_components"]:
                    if element["types"] == ["locality", "political"]:
                        city = element["long_name"]
                        found = True
                    if ["administrative_area_level_3", "political" ] and not found:
                        city = element["long_name"]
                    if element["types"] == ["administrative_area_level_1", "political"]:
                        region = element["long_name"]
            time.sleep(1)
        antennas[i]["city"] = city
        antennas[i]["region"] = region
        result = json.dumps(antennas[i], ensure_ascii=False)
        file.write(result + (",\n" if (i!=size-1) else "]"))
    file.close()

class UnknownCityError(Exception):
    pass


if __name__ == "__main__":
    main()



