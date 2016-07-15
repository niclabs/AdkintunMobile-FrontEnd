region_codes = {
    15: "Región de Arica y Parinacota",
    1: "Región de Tarapacá",
    2: "Región de Antofagasta",
    3: "Región de Atacama",
    4: "Región de Coquimbo",
    5: "Región de Valparaíso",
    6: "Región del Libertador General Bernardo O'Higgins",
    7: "Región del Maule",
    8: "Región del Biobío",
    9: "Región de la Araucanía",
    14: "Región de los Ríos",
    10: "Región de Los Lagos",
    11: "Región Aysén del General Carlos Ibáñez del Campo",
    12: "Región de Magallanes y de la Antártica Chilena",
    13: "Región Metropolitana"
}

def get_region_name_by_id(region_id):
    return region_codes.get(region_id)

inv_map = {v: k for k, v in region_codes.items()}

def get_region_code_by_name(region_name):
    for key in inv_map.keys():
        if key.lower() in region_name.lower():
            return inv_map.get(key)
    return "error"

