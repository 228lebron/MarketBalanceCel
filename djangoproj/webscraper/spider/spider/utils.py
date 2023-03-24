brand_mapping = {
            'GIGADEV': 'GigaDevice',
            'GigaDevice®': 'GigaDevice',
        }


def map_brand_name(brand_name):
    return brand_mapping.get(brand_name, brand_name)