from region_search.ip.lookup import IPRegionLookupFactory
from region_search.lookup import RegionLookupFactory


def client_code(factory: RegionLookupFactory):
    region_lookup = factory.create_region_lookup("ip.dat")
    print(region_lookup.lookup("180.76.76.76"))
    region_lookup.get_dat_msg()


if __name__ == '__main__':
    lookup_factory = IPRegionLookupFactory()
    client_code(lookup_factory)
