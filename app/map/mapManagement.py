from app.models.antenna import Antenna
from app.models.gsm_count import GsmCount
from app.models.carrier import Carrier
from app import db


def build(newZoom, carrier):
    if carrier == 0:
        if newZoom < 8:
            type = "Región"
            query1 = "SELECT region.id, region.name, region.lat, region. lon, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND city.region_id = region.id GROUP BY region.id;"


            query2 = "SELECT region.id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND city.region_id = region.id GROUP BY region.id, gsm_count.network_type;"

            return getData(query1, query2, type)
        elif newZoom < 12:
            type = "Ciudad"
            query1 = "SELECT city.id, city.name, city.lat, city.lon, SUM(gsm_count.quantity) as quantity FROM public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND city.lat IS NOT NULL AND city.lon IS NOT NULL GROUP BY city.id;"


            query2 = "SELECT city.id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id GROUP BY city.id, gsm_count.network_type;"

            return getData(query1, query2, type)
    else:
        if newZoom < 8:
            type = "Región"
            query1 = "SELECT region.id, region.name, region.lat, region. lon, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.carriers, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND antennas.carrier_id = carriers.id AND carriers.id = %r AND city.region_id = region.id  GROUP BY region.id;" % carrier

            query2 = "SELECT region.id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.carriers, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND antennas.carrier_id = carriers.id AND carriers.id = %r AND city.region_id = region.id GROUP BY region.id, gsm_count.network_type;" % carrier
            return getData(query1, query2, type)
        elif newZoom < 12:
            type = "Ciudad"
            query1 = "SELECT city.id, city.name, city.lat, city.lon, SUM(gsm_count.quantity) as quantity FROM public.gsm_count, public.antennas, public.carriers, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.carrier_id = carriers.id AND antennas.city_id = city.id AND carriers.id = %r AND city.lat IS NOT NULL AND city.lon IS NOT NULL GROUP BY city.id;" % carrier

            query2 = "SELECT city.id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.gsm_count, public.antennas, public.carriers, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.carrier_id = carriers.id AND antennas.city_id = city.id AND carriers.id = %r GROUP BY city.id, gsm_count.network_type;" % carrier
            return getData(query1, query2, type)



def change(lastZoom, newZoom, carrier):
    if lastZoom < 8 and newZoom < 8:
        return {"action": "notChange"}
    elif lastZoom < 8 and newZoom >= 8:
        return build(newZoom, carrier)
    elif lastZoom >= 8 and newZoom >= 8:
        return {"action": "notChange"}
    elif lastZoom >= 8 and newZoom < 8:
        return build(newZoom, carrier)


def getData(sqlQuery, sqlQuery2, type):
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
    return {"data": data, "locations": locations, "type": type, "action": "change"}
