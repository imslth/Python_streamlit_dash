from streamlit_elements import mui
import streamlit as st
from .MuiGraphs import MuiGraphs

# Класс для генерации редактируемого и перетаскиваемого окна на базе react, а именно https://mui.com/.
# Взято и чуть упрощено из https://github.com/okld/streamlit-elements.
class Mui:
    def __init__(self):
        pass

    # При вызове мы заносим в кэш инфу о полученном ключе, который связываем с созданным окном.
    def __call__(self, key, name, content=None):
        if f'{key}_st' not in st.session_state:
            st.session_state[f'{key}_st'] = 0

        # Функция смены темы отображения фона окон. Если нажата кнопка, то мы меняем для определенного окна (на котором
        # нажата кнопка) переменную. В дальнейшем почти везде в css свойствах стоит проверка на значение этого параметра
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
                               # Про вот такую проверку я говорил выше.
                               'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                               'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526",
                           }, dark_switcher=True):
                mui.Typography(name, sx={"flex": 1})

                # В окне устанавливаем кнопку в виде меняющейся иконки. При нажатии мы меняем параметр темы для этого
                # окна.
                if st.session_state[f'{key}_st'] == 0:
                    mui.IconButton(mui.icon.LightMode, sx={"color": "#ffc107"}, onClick=func_state)

                else:
                    mui.IconButton(mui.icon.DarkMode, sx={"color": "#252526"}, onClick=func_state)

            # Проверяем полученный ключ окна и вызываем функцию отображения графиков внутри этого окна.
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

