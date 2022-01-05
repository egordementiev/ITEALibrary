# imports for json
import json
from abc import ABC, abstractmethod


class DataBase(ABC):
    @abstractmethod
    def write_to_db(self, write_info, data_base_title):
        pass

    @abstractmethod
    def read_from_db(self, data_base_title):
        pass


class DataBaseJSON(DataBase):
    def write_to_db(self, write_data, data_base_title):
        with open(data_base_title, 'w') as file:
            json.dump(write_data, file, indent=2)

    def read_from_db(self, data_base_title):
        with open(data_base_title, 'r') as file:
            data = json.load(file)
            return data
