"""
parent class for DB api

Author: Shaya Weissberg
"""

from SharedUtils.DBUtils.wrapper import Wrapper


class DBUtilsAPI:

    def __init__(self, DBname, TABLE_NAME, TABLE_COLUMNS, CREATE_TABLE_STRING):
        self.wrapper = Wrapper(DBname)
        self.TABLE_NAME = TABLE_NAME
        self.TABLE_COLUMNS = TABLE_COLUMNS
        self.CREATE_TABLE_STRING = CREATE_TABLE_STRING

    def __delete__(self, instance):
        self.wrapper.__delete__(instance)

    def create_table(self):
        self.wrapper.create_table(self.TABLE_NAME, self.CREATE_TABLE_STRING)

    def reset(self):
        self.wrapper.drop_table(self.TABLE_NAME)
        self.create_table()

    def save(self, values):
        self.wrapper.insert(self.TABLE_NAME, self.TABLE_COLUMNS, values)

    def get_all_table(self) -> list:
        return self.wrapper.select('*', self.TABLE_NAME, '1 IS NOT NULL') #TODO: do it better

    def get_all_where(self, condition) -> list:
        return self.wrapper.select('*', self.TABLE_NAME, condition)

    def get_column(self, column) -> list:
        return self.wrapper.select(column, self.TABLE_NAME, '1 IS NOT NULL') #TODO: do it better

    def get(self, result, condition) -> list:
        return self.wrapper.select(result, self.TABLE_NAME, condition)






