#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import logging


class Database:
    __dbms = 'sqlite'

    def __init__(self, database=None):
        self.__conn = None

        self.__param = {
            'database': database
            # 'timeout': None,
            # 'detect_types': None,
            # 'isolation_level': None,
            # 'check_same_thread': None,
            # 'factory': None,
            # 'cached_statements': None,
            # 'uri': None
        }

    def get_connection(self):
        '''
        :return:
        '''
        if (self.__conn == None):
            try:
                self.__conn = sqlite3.connect(**self.__param)
                return self.__conn
            except Exception as e:
                logging.error("Db error while getting connection: {}".format(e))
                raise e
        else:
            return self.__conn

    def close_connection(self):
        if (self.__conn != None):
            self.__conn.close()
            return 0
        return 1

    def commit(self):
        if (self.__conn != None):
            self.__conn.commit()
            return 0
        return 1

    def insert(self, table, columns, data):
        '''
        :param table:
        :param columns:
        :param data: list of records
        :return:
        '''
        conn = self.get_connection()
        cur = conn.cursor()
        sql = 'INSERT INTO {} ({}) VALUES ({});'.format(table, ', '.join(columns),
                                                        str('?, ' * columns.__len__())[:-2])
        for row in data:
            try:
                cur.execute(sql,row)
            except Exception as e:
                logging.error("Db error while trying insert {}: {}".format(row, e))
                pass

    def get(self, table, where=None):
        '''
        :param table:
        :param where:
        :return:
        '''
        conn = self.get_connection()
        cur = conn.cursor()
        where_sql, row = self.parse_where(where)
        sql = 'SELECT * FROM {} {};'.format(table, where_sql)
        cur.execute(sql, row)
        return cur.fetchall()

    def execute(self, sql):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def update(self, table, columns, data, where):
        '''
        :param table:
        :param columns:
        :param data:
        :param where:
        :return:
        '''
        set_sql, set_row = self.parse_set(columns=columns, data=data)
        where_sql, where_row = self.parse_where(where=where)
        row = (*set_row, *where_row)
        conn = self.get_connection()
        cur = conn.cursor()
        sql = 'UPDATE {} {} {};'.format(table, set_sql, where_sql)
        cur.execute(sql, row)

    @staticmethod
    def parse_where(where=None):
        '''
        :param where:
        :return:
        '''
        if where is None:
            return '', ''
        else:
            row = []
            sql = 'WHERE {} {} {} AND {}'
            for k, v in where.items():
                sql = sql.format(k,
                                 'LIKE' if (str(v).__contains__('%') or str(v).__contains__('_')) else '=',
                                 '?',
                                 '{} {} {} AND {}')
                row.append(v)
            sql = sql[:-len(' AND {} {} {} AND {}')]
            return sql, (*row,)

    @staticmethod
    def parse_set(columns, data):
        '''
        :param columns:
        :param data:
        :return:
        '''
        if columns is None or data is None:
            return '', ''
        else:
            sql = 'SET {} = {}, {}'
            row = []
            for i in range(columns.__len__()):
                sql = sql.format(columns[i], '?', '{} = {}, {}')
                row.append(data[i])
            sql = sql[:-len(', {} = {}, {}')]
            return sql, (*row,)
