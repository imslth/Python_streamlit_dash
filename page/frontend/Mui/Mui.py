from streamlit_elements import mui
import streamlit as st
from .MuiGraphs import MuiGraphs


class Mui:
    def __init__(self):
        pass

    def __call__(self, key, name, content=None):
        if f'{key}_st' not in st.session_state:
            st.session_state[f'{key}_st'] = 0

        def func_state():
            if st.session_state[f'{key}_st'] == 0:
                st.session_state[f'{key}_st'] = 1
            else:
                st.session_state[f'{key}_st'] = 0

        with mui.Paper(key=key,
                       sx={"display": "flex", "flexDirection": "column", "borderRadius": 3,
                           "overflow": "hidden", },
                       elevation=1):
            with mui.Stack(className='draggable', alignItems="center", direction="row",
                           spacing=1,
                           sx={
                               "padding": "5px 15px 5px 15px",
                               "borderBottom": 1,
                               "borderColor": "divider",
                               'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                               'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526",
                           }, dark_switcher=True):
                mui.Typography(name, sx={"flex": 1})

                if st.session_state[f'{key}_st'] == 0:
                    mui.IconButton(mui.icon.LightMode, sx={"color": "#ffc107"}, onClick=func_state)

                else:
                    mui.IconButton(mui.icon.DarkMode, sx={"color": "#252526"}, onClick=func_state)

            if key == 'slider': MuiGraphs().RangeSlider(key)
            if key == 'multiselect': MuiGraphs().Multiselect(key)
            if key == 'table': MuiGraphs().Table(content, key)
            if key == 'bar_rating': MuiGraphs().Bar(content, key)
            if key == 'bar_reviews': MuiGraphs().Bar(content, key)
            if key == 'select': MuiGraphs().Select(key)
            if key == 'radian_reviews': MuiGraphs().RadianBar(content, key)
            if key == 'line_reviews': MuiGraphs().Line(content, key)
            if key == 'line_rating': MuiGraphs().Line(content, key)
            if key == 'reviews_calendar': MuiGraphs().Calendar(content, key)
            if key == 'votes_calendar': MuiGraphs().Calendar(content, key)
            if key == 'reviews_like': MuiGraphs().Reviews(content, key)
            if key == 'reviews_dislike': MuiGraphs().Reviews(content, key)
            if key == 'pie_related': MuiGraphs().Pie(content, key)
            if key == 'network': MuiGraphs().Network(content, key)
