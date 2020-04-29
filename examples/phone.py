from region_search.lookup import RegionLookupFactory
from region_search.phone.lookup import PhoneRegionLookupFactory


def client_code(factory: RegionLookupFactory):
    region_lookup = factory.create_region_lookup("phone.dat")
    print(region_lookup.lookup("13812341234"))
    region_lookup.get_dat_msg()


if __name__ == '__main__':
    lookup_factory = PhoneRegionLookupFactory()
    client_code(lookup_factory)
