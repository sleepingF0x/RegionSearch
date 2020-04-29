from abc import ABC, abstractmethod


class RegionLookup(ABC):
    @abstractmethod
    def lookup(self, info):
        pass

    @staticmethod
    @abstractmethod
    def csv2dat(csv_path, columns, csv_version, dat_path):
        pass

    @abstractmethod
    def get_dat_msg(self):
        pass


class RegionLookupFactory(ABC):
    @abstractmethod
    def create_region_lookup(self, db_path):
        pass
