from database.dao import DAO

class Model:
    def __init__(self):

        pass

    def get_date_range(self):
        return DAO.get_date_range()

