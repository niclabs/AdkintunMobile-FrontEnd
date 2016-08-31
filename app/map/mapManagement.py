from app.models.antenna import Antenna
from app.models.gsm_count import GsmCount
from app.models.carrier import Carrier
from app import db

points = [8, 11]


def build(newZoom, carrier, bounds):
    if carrier == 0:
        if newZoom <= 8:
            type = "Región"
            query1 = "SELECT region.id, region.name, region.lat, region. lon, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND city.region_id = region.id GROUP BY region.id;"

            query2 = "SELECT region.id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND city.region_id = region.id GROUP BY region.id, gsm_count.network_type;"

            return getData(query1, query2, type)
        elif newZoom <= 11:
            type = "Ciudad"
            query1 = "SELECT city.id, city.name, city.lat, city.lon, SUM(gsm_count.quantity) as quantity FROM public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND city.lat IS NOT NULL AND city.lon IS NOT NULL GROUP BY city.id;"

            query2 = "SELECT city.id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id GROUP BY city.id, gsm_count.network_type;"

            return getData(query1, query2, type)
        else:
            type = "Antena"
            query1 = "SELECT antennas.id as id, antennas.id as name, antennas.lat, antennas.lon, SUM(gsm_count.quantity) as quantity FROM public.antennas, public.gsm_count WHERE gsm_count.antenna_id = antennas.id AND antennas.lat > %r AND antennas.lon > %r AND antennas.lat < %r AND antennas.lon < %r GROUP BY antennas.id;" % (
                bounds["sw"]["lat"], bounds["sw"]["lon"], bounds["ne"]["lat"], bounds["ne"]["lon"])
            query2 = "SELECT antennas.id as id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.antennas, public.gsm_count WHERE gsm_count.antenna_id = antennas.id AND antennas.lat > %r AND antennas.lon > %r AND antennas.lat < %r AND antennas.lon < %r GROUP BY antennas.id, gsm_count.network_type;" % (
                bounds["sw"]["lat"], bounds["sw"]["lon"], bounds["ne"]["lat"], bounds["ne"]["lon"])
            return getData(query1, query2, type, "cluster")

    else:
        if newZoom <= 8:
            type = "Región"
            query1 = "SELECT region.id, region.name, region.lat, region.lon, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND gsm_count.carrier_id = %r AND city.region_id = region.id  GROUP BY region.id;" % carrier

            query2 = "SELECT region.id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND gsm_count.carrier_id = %r AND city.region_id = region.id GROUP BY region.id, gsm_count.network_type;" % carrier
            return getData(query1, query2, type)
        elif newZoom <= 11:
            type = "Ciudad"
            query1 = "SELECT city.id, city.name, city.lat, city.lon, SUM(gsm_count.quantity) as quantity FROM public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND gsm_count.carrier_id = %r AND city.lat IS NOT NULL AND city.lon IS NOT NULL GROUP BY city.id;" % carrier

            query2 = "SELECT city.id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND gsm_count.carrier_id= %r GROUP BY city.id, gsm_count.network_type;" % carrier
            return getData(query1, query2, type)
        else:
            type = "Antena"
            query1 = "SELECT antennas.id as id, antennas.id as name, antennas.lat, antennas.lon, SUM(gsm_count.quantity) as quantity FROM public.antennas, public.gsm_count WHERE gsm_count.antenna_id = antennas.id AND gsm_count.carrier_id = %r AND antennas.lat > %r AND antennas.lon > %r AND antennas.lat < %r AND antennas.lon < %r GROUP BY antennas.id;" % (
                carrier, bounds["sw"]["lat"], bounds["sw"]["lon"], bounds["ne"]["lat"], bounds["ne"]["lon"])
            query2 = "SELECT antennas.id as id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.antennas, public.gsm_count WHERE gsm_count.antenna_id = antennas.id AND gsm_count.carrier_id = %r AND antennas.lat > %r AND antennas.lon > %r AND antennas.lat < %r AND antennas.lon < %r GROUP BY antennas.id, gsm_count.network_type;" % (
                carrier, bounds["sw"]["lat"], bounds["sw"]["lon"], bounds["ne"]["lat"], bounds["ne"]["lon"])
            return getData(query1, query2, type, "cluster")


def change(lastZoom, newZoom, lastCarrier, newCarrier, bounds):
    if lastCarrier != newCarrier:
        return build(newZoom, newCarrier, bounds)
    size = len(points)
    for i in range(size):
        if (lastZoom <= points[i] and newZoom > points[i]) or (lastZoom > points[i] and newZoom <= points[i]):
            return build(newZoom, newCarrier, bounds)
    return {"action": "noChange"}


def getData(sqlQuery, sqlQuery2, type, action="change"):
    data = {}
    locations = {}
    query = sqlQuery
    result = db.engine.execute(query)
    for row in result:
        locations[row["id"]] = {"lon": row["lon"], "lat": row["lat"], "quantity": row["quantity"],
                                "name": row["name"]}
        data[row["id"]] = {}
    query = sqlQuery2
    result = db.engine.execute(query)
    for row in result:
        data[row["id"]][row["type"]] = row["quantity"]
    return {"data": data, "locations": locations, "type": type, "action": action}
