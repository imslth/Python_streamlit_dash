import sqlite3
import os

import pandas
import streamlit as st


# класс для выгрузки/загрузки из БД
class Base:

    def __init__(self):
        self.text_past = list()
        self.text_present = list()
        self.uniq_past = list()
        self.uniq_present = list()
        self.coordinates_present = list()
        self.coordinates_past = list()
        self.project_present = list()
        self.project_past = list()
        self.urls = list()
        self.result_past = list()
        self.result_present = list()
        self.result = list()
        self.address_past = list()
        self.address_present = list()
        BASE_DIR = os.path.dirname(__file__)
        DB_DIR = os.path.join(BASE_DIR, 'DB/base.db')
        self.conn = sqlite3.connect(DB_DIR, check_same_thread=False)

    # функция для добавления новой ссылки в таблицу с url
    def create_new_url(self, table, url):
        table = f'{table}_url'
        cursor = self.conn.cursor()
        cursor.execute(
            f'INSERT INTO "{table}" (url) VALUES(?)',
            (url,))
        self.conn.commit()
        self.conn.close()

    # Функция для добавления данных в остальные таблицы. В зависимости от количества элементов данные записываются
    # в определенную таблицу. Перед записью в каждой таблице происходит проверка наличия данных в этой таблице.
    # Чаще всего проверка осуществляется по координатам объекта и дате добавления. Опционально добавляются остальные
    # элементы (текст и т.д.). Все таблицы каждый день записывают новые данные, исключением является только таблица
    # с отзывами - там данные добавляются только при обнаружении новых отзывов и данные не привязаны к дате.
    def create_new_items(self, table, context):
        cursor = self.conn.cursor()
        keys = str(list(context.keys()))[1:-1]
        values = list(context.values())
        str_get = f'INSERT INTO "{table}" ({keys}) VALUES ({("?," * len(values))[:-1]})'

        if len(values) == 7:
            check = cursor.execute(f'SELECT * FROM "{table}" WHERE coordinates=? AND now=?', ([values[1], values[6]]))
            check_list = check.fetchall()
            if check_list:
                pass
            else:
                data_get = (
                    [values[0], values[1], values[2], values[3], values[4], values[5], values[6]])
                cursor.execute(str_get, data_get)
                self.conn.commit()

        if len(values) == 8:
            for i in range(len(values[0])):
                check = cursor.execute(f'SELECT * FROM "{table}" WHERE aspect_text=? AND coordinates=? AND now=?',
                                       ([values[0][i], values[6][i], values[7][i]]))
                check_list = check.fetchall()
                if check_list:
                    pass
                else:
                    data_get = (
                        [values[0][i], values[1][i], values[2][i], values[3][i], values[4][i], values[5][i],
                         values[6][i],
                         values[7][i]])
                    cursor.execute(str_get, data_get)
                    self.conn.commit()

        if len(values) == 6:
            for i in range(len(values[0])):
                check = cursor.execute(
                    f'SELECT * FROM "{table}" WHERE coordinates=? AND related_coordinates=? AND now=?',
                    ([values[1][i], values[3][i], values[5][i]]))
                check_list = check.fetchall()
                if check_list:
                    pass
                else:
                    data_get = ([values[0][i], values[1][i], values[2][i], values[3][i], values[4][i], values[5][i]])
                    cursor.execute(str_get, data_get)
                    self.conn.commit()

        if len(values) == 10:
            for i in range(len(values[0])):
                check = cursor.execute(f'SELECT * FROM "{table}" WHERE reviews_text=? AND coordinates=? ',
                                       ([values[0][i], values[8][i]]))
                check_list = check.fetchall()
                if check_list:
                    pass
                else:
                    data_get = (
                        [values[0][i], values[1][i], values[2][i], values[3][i], values[4][i], values[5][i],
                         values[6][i],
                         values[7][i], values[8][i], values[9][i]])
                    cursor.execute(str_get, data_get)
                    self.conn.commit()

    # Функция для считывания всех данных с любой таблицы. Есть несколько версий - где происходит проверка по
    # наличию координат в таблице и без неё. Здесь выгружаются данные по двум датам одновременно - было и стало.
    def read_all(self, table,
                 date_present, project, date_past=None, coordinates=None):
        cursor_past = self.conn.cursor()
        cursor_present = self.conn.cursor()
        for item in project:
            if coordinates:
                info_past = cursor_past.execute(f'SELECT * FROM "{table}" WHERE now=? AND project=? AND coordinates=?',
                                                ([date_past, item, coordinates]))
                info_present = cursor_present.execute(
                    f'SELECT * FROM "{table}" WHERE now=? AND project=? AND coordinates=?',
                    ([date_present, item, coordinates]))
            else:
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
        self.uniq_past = list(set(self.result_past))
        self.uniq_present = list(set(self.result_present))
        content = {'past': self.uniq_past, 'present': self.uniq_present}
        return content

    # Функция выгрузки крайних дат с БД. По этим датам мы определяем временной промежуток в slider.
    def min_max_date(self, table):
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

    # Функция для выгрузки названия всех проектов с БД. Данные нужны для отображения их в Select.
    def all_project(self, table, date_past=None,
                    date_present=None):
        cursor_past = self.conn.cursor()
        cursor_present = self.conn.cursor()
        info_past = cursor_past.execute(f'SELECT project,address,coordinates,count_text FROM "{table}" WHERE now=?',
                                        ([date_past]))
        info_present = cursor_present.execute(
            f'SELECT project,address,coordinates,count_text FROM "{table}" WHERE now=?',
            ([date_present]))
        past = list(set(info_past.fetchall()))
        present = list(set(info_present.fetchall()))
        self.conn.close()
        for project in past:
            self.coordinates_past.append(project[2])
            self.address_past.append(project[1])
            self.project_past.append(project[0])
            self.text_past.append(project[3])
        for project in present:
            self.coordinates_present.append(project[2])
            self.address_present.append(project[1])
            self.project_present.append(project[0])
            self.text_present.append(project[3])
        content = {'project_past': self.project_past, 'project_present': self.project_present,
                   'address_past': self.address_past, 'text_past': self.text_past,
                   'address_present': self.address_present, 'coordinates_past': self.coordinates_past,
                   'coordinates_present': self.coordinates_present, 'text_present': self.text_present}
        return content

    # Функция для выгрузки названия всех конкурентных комплексов
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

    # Функция для выгрузки данных только для отображения карты. Здесь нам необходимы только название проекта, координаты
    # и рейтинг объекта
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

    # Функция для выгрузки данных о рейтинге объекта в определенную дату
    def all_rating(self, table, project, coordinates):
        cursor = self.conn.cursor()
        info = cursor.execute(f'SELECT rating,now FROM "{table}" WHERE project=? AND coordinates=?',
                              ([project, coordinates]))
        result = info.fetchall()
        self.conn.close()
        temp = list(set(result))
        df = pandas.DataFrame(temp, columns=['rating', 'date'])
        df = df.sort_values(by=['date'])
        content = df.values.tolist()
        return content

    # Функция для выгрузки данных о рейтинге конкурирующих объектов
    def rating_related(self, table, project, coordinates, date_present):
        cursor = self.conn.cursor()
        info = cursor.execute(
            f'SELECT related_project,related_rating,now FROM "{table}" WHERE project=? AND coordinates=? AND now=?',
            ([project, coordinates, date_present]))
        result = info.fetchall()
        self.conn.close()
        return result

    # Функция для выгрузки данных об кол-ве текстов и оценок о проекте
    def count_all_votes_reviews(self, table, project, coordinates):
        cursor = self.conn.cursor()
        info = cursor.execute(f'SELECT count_text,count_vote,now FROM "{table}" WHERE project=? AND coordinates=?',
                              ([project, coordinates]))
        content = info.fetchall()
        self.conn.close()
        return content

    # Функция для выгрузки отзывов о проекте
    def reviews(self, table, project, coordinates):
        cursor = self.conn.cursor()
        info = cursor.execute(f'SELECT reviews_text FROM "{table}" WHERE project=? AND coordinates=?',
                              ([project, coordinates]))
        content = info.fetchall()
        self.conn.close()
        return content

    # Функция для выгрузки всех данных из таблицы отзывов (отзывы, дата публикации, кол-во лайков, дизлайков и т.д.)
    def reviews_all(self, table, project, coordinates):
        cursor = self.conn.cursor()
        info = cursor.execute(f'SELECT * FROM "{table}" WHERE project=? AND coordinates=?',
                              ([project, coordinates]))
        content = info.fetchall()
        self.conn.close()
        return content

    # Функция для выгрузки данных об кол-ве текстов и их тематик по проекту
    def read_count_reviews(self, table, project, coordinates):
        cursor = self.conn.cursor()
        info = cursor.execute(
            f'SELECT aspect_positive,aspect_neutral,aspect_negative,now FROM "{table}" WHERE project=? AND coordinates=?',
            ([project, coordinates]))
        content = info.fetchall()
        self.conn.close()
        return content

    # Функция для выгрузки ссылок для парсинга
    def read_url(self, table):
        table = f'{table}_url'
        cursor = self.conn.cursor()
        info = cursor.execute(
            f'SELECT url FROM "{table}"')
        content = list()
        for item in info.fetchall():
            content.append(item[0])
        self.conn.close()
        return content
