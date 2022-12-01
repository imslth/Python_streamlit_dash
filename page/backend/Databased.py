import sqlite3
import os
import streamlit as st


class Base:

    def __init__(self):
        self.urls = list()
        self.result_past = list()
        self.result_present = list()
        self.result = list()
        self.address_past = list()
        self.address_present = list()
        BASE_DIR = os.path.dirname(__file__)
        DB_DIR = os.path.join(BASE_DIR, 'DB/base.db')
        self.conn = sqlite3.connect(DB_DIR, check_same_thread=False)

    def create_new_url(self, table, url):
        table = f'{table}_url'
        cursor = self.conn.cursor()
        cursor.execute(
            f'INSERT INTO "{table}" (url) VALUES(?)',
            (url,))
        self.conn.commit()
        self.conn.close()


    def create_new_items(self, table=None, context=None):
        cursor = self.conn.cursor()
        keys = str(list(context.keys()))[1:-1]
        values = list(context.values())
        str_get = f'INSERT INTO "{table}" ({keys}) VALUES ({("?," * len(values))[:-1]})'

        if len(values) == 7:
            data_get = (
                [values[0], values[1], values[2], values[3], values[4], values[5], values[6]])
            cursor.execute(str_get, data_get)
            self.conn.commit()

        if len(values) == 8:
            for i in range(len(values[0])):
                data_get = (
                    [values[0][i], values[1][i], values[2][i], values[3][i], values[4][i], values[5][i], values[6][i],
                     values[7][i]])
                cursor.execute(str_get, data_get)
                self.conn.commit()

        if len(values) == 6:
            for i in range(len(values[0])):
                data_get = ([values[0][i], values[1][i], values[2][i], values[3][i], values[4][i], values[5][i]])
                cursor.execute(str_get, data_get)
                self.conn.commit()

        if len(values) == 10:
            for i in range(len(values[0])):
                data_get = (
                    [values[0][i], values[1][i], values[2][i], values[3][i], values[4][i], values[5][i], values[6][i],
                     values[7][i], values[8][i], values[9][i]])
                cursor.execute(str_get, data_get)
                self.conn.commit()


    def read_all(self, table,
                 date_present, project, date_past=None):
        cursor_past = self.conn.cursor()
        cursor_present = self.conn.cursor()
        for item in project:
            info_past = cursor_past.execute(f'SELECT * FROM "{table}" WHERE now=? AND project=?',
                                            ([date_past, item]))
            info_present = cursor_present.execute(f'SELECT * FROM "{table}" WHERE now=? AND project=?',
                                                  ([date_present, item]))
            past = info_past.fetchall()
            present = info_present.fetchall()
            for items in past:
                self.result_past.append(items)
            for items in present:
                self.result_present.append(items)
        self.conn.close()
        content = {'past': self.result_past, 'present': self.result_present}
        return content

    def min_max_date(self, table='yandex_all'):
        cursor_min = self.conn.cursor()
        cursor_max = self.conn.cursor()
        info_min = cursor_min.execute(f'SELECT now FROM "{table}" ORDER BY now ASC LIMIT 1')
        info_max = cursor_max.execute(f'SELECT now FROM "{table}" ORDER BY now DESC LIMIT 1')
        result_min = info_min.fetchall()
        result_max = info_max.fetchall()
        self.conn.close()
        result_min = result_min[0][0]
        result_max = result_max[0][0]
        content = {'min': result_min, 'max': result_max}
        return content

    def all_project(self, table, date_past=None,
                    date_present=None):
        cursor_past = self.conn.cursor()
        cursor_present = self.conn.cursor()
        info_past = cursor_past.execute(f'SELECT project,address FROM "{table}" WHERE now=?', ([date_past]))
        info_present = cursor_present.execute(f'SELECT project,address FROM "{table}" WHERE now=?', ([date_present]))
        past = info_past.fetchall()
        present = info_present.fetchall()
        self.conn.close()
        for project in past:
            self.address_past.append(project[1])
            self.result_past.append(project[0])
        for project in present:
            self.address_present.append(project[1])
            self.result_present.append(project[0])
        content = {'past': self.result_past, 'present': self.result_present, 'address_past': self.address_past,
                   'address_present': self.address_present}
        return content

    def all_project_related(self, table,
                            date_present, date_past=None):
        cursor_past = self.conn.cursor()
        cursor_present = self.conn.cursor()
        info_past = cursor_past.execute(f'SELECT related_project FROM "{table}" WHERE now=?', ([date_past]))
        info_present = cursor_present.execute(f'SELECT related_project FROM "{table}" WHERE now=?', ([date_present]))
        past = info_past.fetchall()
        present = info_present.fetchall()
        self.conn.close()
        for project in past:
            self.result_past.append(project[0])
        for project in present:
            self.result_present.append(project[0])
        content = {'past': self.result_past, 'present': self.result_present}
        return content

    def maps(self, date_present):
        cursor_all = self.conn.cursor()
        cursor_related = self.conn.cursor()
        table_all = f"{st.session_state.option}_all"
        table_related = f"{st.session_state.option}_related"
        info_all = cursor_all.execute(f'SELECT project,coordinates,address,rating FROM "{table_all}" WHERE now=?',
                                      ([date_present]))
        info_related = cursor_related.execute(
            f'SELECT project,related_project,related_coordinates,related_rating FROM "{table_related}" WHERE now=?',
            ([date_present]))
        content_all = info_all.fetchall()
        content_related = info_related.fetchall()
        content = {'all': content_all, 'related': content_related}
        return content

    def all_rating(self, table='yandex_all', project=None):
        cursor = self.conn.cursor()
        info = cursor.execute(f'SELECT rating,now FROM "{table}" WHERE project=?', ([project]))
        content = info.fetchall()
        self.conn.close()
        return content

    def rating_related(self, table, project=None):
        cursor = self.conn.cursor()
        info = cursor.execute(f'SELECT related_project,related_rating,now FROM "{table}" WHERE project=?', ([project]))
        content = info.fetchall()
        self.conn.close()
        return content

    def count_all_votes_reviews(self, table, project=None):
        cursor = self.conn.cursor()
        info = cursor.execute(f'SELECT count_text,count_vote,now FROM "{table}" WHERE project=?', ([project]))
        content = info.fetchall()
        self.conn.close()
        return content

    def reviews(self, table, project, date_present):
        cursor = self.conn.cursor()
        info = cursor.execute(f'SELECT reviews_text FROM "{table}" WHERE project=? AND now=?',
                              ([project, date_present]))
        content = info.fetchall()
        self.conn.close()
        return content

    def read_count_reviews(self, table, project=None):
        cursor = self.conn.cursor()
        info = cursor.execute(
            f'SELECT aspect_positive,aspect_neutral,aspect_negative,now FROM "{table}" WHERE project=?', ([project]))
        content = info.fetchall()
        self.conn.close()
        return content

    def read_url(self,table):
        table = f'{table}_url'
        cursor = self.conn.cursor()
        info = cursor.execute(
            f'SELECT url FROM "{table}"')
        content = list()
        for item in info.fetchall():
            content.append(item[0])
        self.conn.close()
        return content

