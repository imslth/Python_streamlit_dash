import streamlit as st
from .Databased import Base
import datetime


def main():
    if st.session_state['Pages_p_Maps Developers'] or st.session_state['Pages_p_Dashboard Developers'] or \
            st.session_state['Pages_p_Reviews Developers'] or st.session_state[
        'Pages_p_Add Developer'] == True:
        st.session_state.option = 'yandex'
    if st.session_state['Pages_p_Maps Dilers'] or st.session_state['Pages_p_Dashboard Dilers'] or st.session_state[
        'Pages_p_Reviews Dilers'] or st.session_state[
        'Pages_p_Add Diler'] == True:
        st.session_state.option = 'dilers_yandex'

    if 'prev_state' not in st.session_state:
        st.session_state.prev_state = st.session_state.option
        st.session_state.state = 0
    else:

        if st.session_state.prev_state == st.session_state.option:
            st.session_state.state += 1
        if st.session_state.prev_state != st.session_state.option:
            st.session_state.state = 0
        st.session_state.prev_state = st.session_state.option

    if st.session_state.state == 0:
        data = Base().min_max_date(table=f'{st.session_state.option}_all')

        max_time = datetime.datetime(int(data['max'].split('-')[0]), int(data['max'].split('-')[1]),
                                     int(data['max'].split('-')[2]))

        min_time = datetime.datetime(int(data['min'].split('-')[0]), int(data['min'].split('-')[1]),
                                     int(data['min'].split('-')[2]))

        maxdays = max_time - min_time

        st.session_state.max_time = data['max']

        st.session_state.min_time = data['min']

        st.session_state.maxdays = maxdays.days

        st.session_state.range_slider_min = 0

        st.session_state.range_slider_max = maxdays.days

        st.session_state.date_present = min_time + datetime.timedelta(days=st.session_state.range_slider_max)

        st.session_state.date_past = min_time + datetime.timedelta(days=st.session_state.range_slider_min)


        data_load_project_multiselect = Base().all_project(table=f'{st.session_state.option}_all',
                                               date_present=st.session_state.date_present.strftime("%Y-%m-%d"))

        data_load_project_select = Base().all_project(table=f'{st.session_state.option}_all',
                                               date_present=st.session_state.max_time)

        st.session_state.count_obj = len(data_load_project_select['project_present'])

        st.session_state.list = data_load_project_multiselect['project_present']
        st.session_state.address = data_load_project_multiselect['address_present']
        st.session_state.coordinates = data_load_project_multiselect['coordinates_present']
        st.session_state.multiselect = st.session_state.list





        st.session_state.selectlist = data_load_project_select['project_present']
        st.session_state.select = st.session_state.selectlist[0]
        st.session_state.selectaddress = data_load_project_select['address_present']
        st.session_state.selectcoordinates = data_load_project_select['coordinates_present']
        st.session_state.select_coordinates = st.session_state.coordinates[0]
        st.session_state.count_text = data_load_project_select['text_present']

        data_load_yandex_related = Base().all_project_related(table=f'{st.session_state.option}_related',
                                                              date_present=st.session_state.date_present.strftime(
                                                                  "%Y-%m-%d")
                                                              )['present']

        st.session_state.count_related_obj = len(data_load_yandex_related)

        st.session_state.number = 0

    if st.session_state.state > 0:
        data = Base().min_max_date(table=f'{st.session_state.option}_all')

        min_time = datetime.datetime(int(data['min'].split('-')[0]), int(data['min'].split('-')[1]),
                                     int(data['min'].split('-')[2]))

        st.session_state.max_time = data['max']

        st.session_state.min_time = data['min']

        st.session_state.date_present = min_time + datetime.timedelta(days=st.session_state.range_slider_max)

        st.session_state.date_past = min_time + datetime.timedelta(days=st.session_state.range_slider_min)

        data_load_project_multiselect = Base().all_project(table=f'{st.session_state.option}_all',
                                               date_present=st.session_state.date_present.strftime("%Y-%m-%d"))

        data_load_project_select = Base().all_project(table=f'{st.session_state.option}_all',
                                               date_present=st.session_state.max_time)


        st.session_state.list = data_load_project_multiselect['project_present']

        st.session_state.selectlist = data_load_project_select['project_present']



if __name__ == '__main__':
    main()
