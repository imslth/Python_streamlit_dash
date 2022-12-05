import streamlit as st
from .Databased import Base
import datetime


# Функция для заполнения кэша streamlit. Это необходимо, чтобы пользоваться одними переменными во всем коде и на всех
# страницах.
def main():
    # Изначально формируем переменную, которая показывает на какой именно странице мы находимся - это страница о жк
    # или о дилерах. Т.к. у нас одинаковые макеты страниц для всех данных, нам надо знать какие данные передавать на
    # страницу в зависимости от выбора направления - если мы выбираем карты о ЖК, то мы должны передавать координаты
    # именно жилых комплексов и т.д. St.session_state.opinion как раз отвечает за это - этот параметр обычно дальше в
    # коде передается как название таблицы, которую надо выгрузить из БД.
    if st.session_state['Pages_p_Maps Developers'] or st.session_state['Pages_p_Dashboard Developers'] or \
            st.session_state['Pages_p_Reviews Developers'] or st.session_state[
        'Pages_p_Add Developer'] == True:
        st.session_state.option = 'yandex'

    if st.session_state['Pages_p_Maps Dilers'] or st.session_state['Pages_p_Dashboard Dilers'] or st.session_state[
        'Pages_p_Reviews Dilers'] or st.session_state[
        'Pages_p_Add Diler'] == True:
        st.session_state.option = 'dilers_yandex'

    # Здесь реализуется проверка состояния - находимся ли мы еще на странице о ЖК или уже переключились на страницу о
    # дилерах. Также стоит учитывать, что страница dashboard реализована на js и react компонентах, которые за одну
    # загрузку страницы перезагружают её 2-3 раза. Переменная st.session_state.prev_state показывает предыдущее
    # состояние страницы - о чем она была (жк или дилеры), переменная st.session_state.opinion показывает текущую
    # страницу (жк или дилеры). Переменная st.session_state.state показывает количество загрузок страниц одной стадии.


    # При первой загрузке сайта предыдущая стадия равна текущей.
    if 'prev_state' not in st.session_state:
        st.session_state.prev_state = st.session_state.option
        st.session_state.state = 0

    # При дальнейшей работе сайта мы каждый раз проверяем равна ли текущая стадия предыдущей.
    else:
        # Если тип страницы не изменился (страницы о ЖК, например), то мы увеличиваем счетчик количества загрузок
        # одной стадии.
        if st.session_state.prev_state == st.session_state.option:
            st.session_state.state += 1
        # Если тип страницы изменился (с ЖК на дилеров и наоборот), то мы сбрасываем счетчик загрузок страниц.
        if st.session_state.prev_state != st.session_state.option:
            st.session_state.state = 0
        # В конце проверки текущую стадию присваиваем предыдущей.
        st.session_state.prev_state = st.session_state.option

    # Если счетчик загрузок страниц равен 0 (т.е. если сайт открыли впервые или переключили с ЖК на дилеров и обратно),
    # то мы в кэш заносим все данные о ЖК или дилерах (в зависимости от выбранной страницы).
    if st.session_state.state == 0:

        # Функция получения максимальной и минимальной даты в БД по типу выбранной страницы (st.session_state.option
        # показывает загружена страница о ЖК или о дилерах).
        data = Base().min_max_date(table=f'{st.session_state.option}_all')

        # Здесь мы приводим к понятному для datetime виду дату. Скорее всего это можно было бы сделать функцией парсинга
        # даты)
        max_time = datetime.datetime(int(data['max'].split('-')[0]), int(data['max'].split('-')[1]),
                                     int(data['max'].split('-')[2]))

        min_time = datetime.datetime(int(data['min'].split('-')[0]), int(data['min'].split('-')[1]),
                                     int(data['min'].split('-')[2]))


        maxdays = max_time - min_time

        st.session_state.max_time = data['max']

        st.session_state.min_time = data['min']

        # Устанавливаем в кэш постоянную переменную с кол-вом дней между мин и макс датами. Это нужно прежде всего для
        # slider, который мы используем - у него градация идет именно по числам.
        st.session_state.maxdays = maxdays.days

        # Устанавливаем максимальное и минимальное значение слайдера 0 и макс дней (76, например)
        st.session_state.range_slider_min = 0

        st.session_state.range_slider_max = maxdays.days

        # Устанавливаем динамически меняющиеся данные, которые зависят от переключения слайдера. Т.е. даты до и после
        # у нас равны 0 + значения слайдера.
        st.session_state.date_present = min_time + datetime.timedelta(days=st.session_state.range_slider_max)

        st.session_state.date_past = min_time + datetime.timedelta(days=st.session_state.range_slider_min)

        # Загружаем список всех проектов, который зависит от максимальной даты на слайдере! Это нужно для multiselect
        # т.к. он связан со слайдером.
        data_load_project_multiselect = Base().all_project(table=f'{st.session_state.option}_all',
                                                           date_present=st.session_state.date_present.strftime(
                                                               "%Y-%m-%d"))

        # Загружаем список всех проектов, который ни от чего не зависит и показывает список проектов только на сегодня
        # (ну или последний день парсинга)! Это нужно просто для select - он не связан со slider и показывает только
        # последние данные
        data_load_project_select = Base().all_project(table=f'{st.session_state.option}_all',
                                                      date_present=st.session_state.max_time)

        # Заносим инфу о количестве объектов в мониторинге на последнюю дату
        st.session_state.count_obj = len(data_load_project_select['project_present'])

        # Здесь мы инициализируем переменные для работы multiselect. list - полный список всех проектов, который всегда
        # должен отображаться в поле multiselect, address и coordinates - список адресов и координат, которые
        # соответствуют проектам, multiselect - список проектов, которые будут выбраны в самом элементе multiselect.
        # Изначально равен всему списку т.е. по умолчанию в multiselect выбраны все проекты. Потом список multiselect
        # в зависимости от выбранного проекта, будет уменьшаться. Список адресов и координат нужен для сопоставления
        # данных в БД. Дальше мы увидим, что в элементах select и multiselect показываются не только названия проектов,
        # но их адреса. Это вынужденная мера т.к. очень много проектов с одинаковыми названиями. При выборе проекта
        # он сначала ищется в списке адресов и координат и только потом по этим 3ем показателям из БД выгружаются его
        # данные
        st.session_state.list = data_load_project_multiselect['project_present']
        st.session_state.address = data_load_project_multiselect['address_present']
        st.session_state.coordinates = data_load_project_multiselect['coordinates_present']
        st.session_state.multiselect = st.session_state.list

        # Похожая ситуация, как и с multiselect, и с одиночным select. Начальными значениями являются первые элементы в
        # списке о комплексах (ну т.е. нулевые)
        st.session_state.selectlist = data_load_project_select['project_present']
        st.session_state.select = st.session_state.selectlist[0]
        st.session_state.selectaddress = data_load_project_select['address_present']
        st.session_state.selectcoordinates = data_load_project_select['coordinates_present']
        st.session_state.select_coordinates = st.session_state.coordinates[0]
        st.session_state.count_text = data_load_project_select['text_present']

        # Здесь мы выгружаем и устанавливаем в кеш инфу о кол-ве конкурирующих комплексов
        data_load_yandex_related = Base().all_project_related(table=f'{st.session_state.option}_related',
                                                              date_present=st.session_state.date_present.strftime(
                                                                  "%Y-%m-%d")
                                                              )['present']

        st.session_state.count_related_obj = len(data_load_yandex_related)

        st.session_state.number = 0

    # Если происходит повторная загрузка страницы с одним типом (мы перешли из карты дилеров в дашборд дилеров,
    # например), то нам необязательно обновлять все данные в кэше - нужно обновить только самые необходимые.
    if st.session_state.state > 0:
        # Повторно нам надо каждый раз обновлять данные о выбранных датах на слайдере - если этого не делать, то даты
        # всегда будут равны тем, что мы задали вначале - первый и последний день из БД.
        data = Base().min_max_date(table=f'{st.session_state.option}_all')

        min_time = datetime.datetime(int(data['min'].split('-')[0]), int(data['min'].split('-')[1]),
                                     int(data['min'].split('-')[2]))

        st.session_state.max_time = data['max']

        st.session_state.min_time = data['min']

        st.session_state.date_present = min_time + datetime.timedelta(days=st.session_state.range_slider_max)

        st.session_state.date_past = min_time + datetime.timedelta(days=st.session_state.range_slider_min)

        # Также нам надо обновлять всегда список всех проектов. Если этого не делать, то в multiselect при снятии
        # галочки с проекта он будет просто удаляться из списка, а не становиться неактивным.
        data_load_project_multiselect = Base().all_project(table=f'{st.session_state.option}_all',
                                                           date_present=st.session_state.date_present.strftime(
                                                               "%Y-%m-%d"))

        data_load_project_select = Base().all_project(table=f'{st.session_state.option}_all',
                                                      date_present=st.session_state.max_time)

        st.session_state.list = data_load_project_multiselect['project_present']

        st.session_state.selectlist = data_load_project_select['project_present']

        st.session_state.number = 0


if __name__ == '__main__':
    main()
