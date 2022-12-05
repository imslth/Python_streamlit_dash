from pathlib import Path
from typing import Optional
import streamlit.components.v1 as components

frontend_dir = Path(__file__).parent.absolute()
_component_func = components.declare_component(
    "custom_grid", path=str(frontend_dir)
)



# Это полная библиотека https://github.com/aalteirac/streamlit_highcharts. Изначально здесь не был подключен js скрипт
# по генерации wordcloud. Я добавил этот скрипт и занес библиотеку с этими изменениями к себе. Все возможные диаграммы,
# которые можно отобразить - https://www.highcharts.com/. Хотя может здесь и не добавлены все js скрипты.


def custom_grid(
        options=None,
        height=410,
        key: Optional[str] = None,
):
    """
    Add a descriptive docstring
    """
    component_value = _component_func(
        options=options, key=key, height=height
    )

    return component_value

