from app.models.antenna import Antenna
from app.models.gsm_count import GsmCount
from app.models.carrier import Carrier
from app import db


def build(newZoom, carrier, year, month):
    print("yes")
    if carrier == 0:
        if newZoom < 8:
            data = []
            query = "SELECT region.id, region.lat, region.lon, SUM(gsm_count.quantity) as quantity FROM public.region, public.gsm_count, public.antennas, public.city WHERE gsm_count.antenna_id = antennas.id AND antennas.city_id = city.id AND city.region_id = region.id AND gsm_count.month = %r AND gsm_count.year = %r GROUP BY region.id" % (
                month, year)
            result = db.engine.execute(query)
            for row in result:
                data.append({"lat": 1, "lon": 1, "quantity": row["quantity"]})
            return {"data": data}


def change(lastZoom, newZoom, carrier):
    return {}
