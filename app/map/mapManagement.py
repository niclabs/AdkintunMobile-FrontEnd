from app.models.antenna import Antenna
from app.models.gsm_count import GsmCount
from app.models.carrier import Carrier
from app import db


def build(newZoom, carrier, year, month):
    print("yes")
    if carrier == 0:
        if newZoom:
            data = {}
            regions = {}
            query = "SELECT region.id, region.name, region.lat, region. lon, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND city.region_id = region.id AND gsm_count.month = %r AND gsm_count.year = %r GROUP BY region.id;" % (
                month, year)
            result = db.engine.execute(query)
            for row in result:
                regions[row["id"]] = {"lon": row["lon"], "lat": row["lat"], "quantity": row["quantity"], "name": row["name"]}
                data[row["id"]] = {}
            query = "SELECT region.id, gsm_count.network_type as type, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND city.region_id = region.id AND gsm_count.month = %r AND gsm_count.year = %r GROUP BY region.id, gsm_count.network_type;" % (
                month, year)
            result = db.engine.execute(query)
            for row in result:
                data[row["id"]][row["type"]] = row["quantity"]
            return {"dataRegion": data, "regions": regions}


def change(lastZoom, newZoom, carrier):
    return {}
