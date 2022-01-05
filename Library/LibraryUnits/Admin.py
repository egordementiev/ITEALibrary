class Admin:
    def __init__(self, name: str, surname: str, user_id: int, add_by=None):
        self.__name = name
        self.__surname = surname
        self.__user_id = user_id
        self.__add_by = add_by

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_add_by(self):
        return self.__add_by

    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_name(self, name):
        self.__name = name

    def set_surname(self, surname):
        self.__surname = surname

    def __repr__(self):
        if self.__add_by:
            return f'{self.__name} {self.__surname}, id = {self.__user_id} | added by {self.__add_by}'
        else:
            return f'{self.__name} {self.__surname}, id = {self.__user_id} | added by Main Admin'
