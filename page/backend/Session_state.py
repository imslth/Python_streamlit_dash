import streamlit as st
from .Databased import Base
import datetime


def main():

    if st.session_state['Pages_p_Maps Developers'] or st.session_state['Pages_p_Dashboard Developers'] or \
            st.session_state['Pages_p_Reviews Developers'] or st.session_state[
        'Pages_p_Add Developer'] == True: st.session_state.option = 'yandex'
    if st.session_state['Pages_p_Maps Dilers'] or st.session_state['Pages_p_Dashboard Dilers'] or st.session_state[
        'Pages_p_Reviews Dilers'] or st.session_state[
        'Pages_p_Add Diler'] == True: st.session_state.option = 'dilers_yandex'

    data = Base().min_max_date()

    max_time = datetime.datetime(int(data['max'].split('-')[0]), int(data['max'].split('-')[1]),
                                 int(data['max'].split('-')[2]))

    min_time = datetime.datetime(int(data['min'].split('-')[0]), int(data['min'].split('-')[1]),
                                 int(data['min'].split('-')[2]))

    maxdays = max_time - min_time

    if "max_time" not in st.session_state:
        st.session_state.max_time = data['max']
    st.session_state.max_time = data['max']

    if "min_time" not in st.session_state:
        st.session_state.min_time = data['min']
    st.session_state.min_time = data['min']

    if "maxdays" not in st.session_state:
        st.session_state.maxdays = maxdays.days
    st.session_state.maxdays = maxdays.days

    if "range_slider_min" not in st.session_state:
        st.session_state.range_slider_min = 0

    if "range_slider_max" not in st.session_state:
        st.session_state.range_slider_max = maxdays.days

    date_present = min_time + datetime.timedelta(days=st.session_state.range_slider_max)

    date_past = min_time + datetime.timedelta(days=st.session_state.range_slider_min)

    st.session_state.date_present = date_present

    st.session_state.date_past = date_past

    data_load_project = Base().all_project(table=f'{st.session_state.option}_all',
                                           date_present=st.session_state.date_present.strftime("%Y-%m-%d"))

    if 'count_obj' not in st.session_state:
        st.session_state.count_obj = len(data_load_project['present'])

    st.session_state.count_obj = len(data_load_project['present'])

    st.session_state.list = data_load_project['present']

    st.session_state.address = data_load_project['address_present']

    st.session_state.multiselect = st.session_state.list

    st.session_state.select = st.session_state.list[0]

    data_load_yandex_related = Base().all_project_related(table=f'{st.session_state.option}_related',
                                                          date_present=st.session_state.date_present.strftime(
                                                              "%Y-%m-%d"),
                                                          )['present']

    if 'count_related_obj' not in st.session_state:
        st.session_state.count_related_obj = len(data_load_yandex_related)
    st.session_state.count_related_obj = len(data_load_yandex_related)

    if 'number' not in st.session_state:
        st.session_state.number = 0


if __name__ == '__main__':
    main()
