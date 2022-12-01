from pathlib import Path
from typing import Optional
import streamlit.components.v1 as components

frontend_dir = Path(__file__).parent.absolute()
_component_func = components.declare_component(
    "custom_grid", path=str(frontend_dir)
)


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

# def main():
#     st.write("## Example")
#     selSample=st.selectbox("Choose a sample",[SAMPLE,SAMPLE2,SAMPLE3,SAMPLE4,SAMPLE5,SAMPLE6,SAMPLE7,SAMPLE8,SAMPLE9,SAMPLE10],format_func=lambda x: str(x["title"]["text"])
# )
#     value = streamlit_highcharts(selSample,640)
#     with st.expander("Show code...",expanded=False):
#         st.code(str(selSample).replace("},","},\r\n"),language="python")


# if __name__ == "__main__":
#     main()
