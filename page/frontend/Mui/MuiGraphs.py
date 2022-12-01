from streamlit_elements import mui, nivo
import streamlit as st


class MuiGraphs:

    def __init__(self):

        self.themes = {
            "dark": {
                "background": "#252526",
                "textColor": "#FAFAFA",
                "tooltip": {
                    "container": {
                        "background": "#3F3F3F",
                        "color": "FAFAFA",
                    }
                }
            },
            "light": {
                "background": "#FFFFFF",
                "textColor": "#31333F",
                "tooltip": {
                    "container": {
                        "background": "#FFFFFF",
                        "color": "#31333F",
                    }
                }
            }
        }

    def Multiselect(self, key):
        with mui.Box(sx={"flex": 1, "minHeight": 0,
                         "padding": "5px 15px 5px 15px",
                         "borderBottom": 1,
                         "borderColor": "divider",
                         'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                         'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526", }):

            def handle_change(event, newValue):
                for item in st.session_state.address:
                    if item in newValue.props.children:
                        value = newValue.props.children.replace(item, '')[:-2]
                if value in st.session_state.multiselect:
                    st.session_state.multiselect.remove(value)
                else:
                    st.session_state.multiselect.append(value)

            temp = list()
            num = list()

            for i in range(len(st.session_state.list)):
                temp.append(mui.MenuItem(f'{st.session_state.list[i]}, {st.session_state.address[i]}', value=i,
                                         variant="outlined"))
                if st.session_state.list[i] in st.session_state.multiselect:
                    num.append(i)

            ITEM_HEIGHT = 48
            ITEM_PADDING_TOP = 8
            MenuProps = {
                'PaperProps': {
                    'style': {
                        'maxHeight': ITEM_HEIGHT * 4 + ITEM_PADDING_TOP,
                        'width': 250,
                        'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526",
                        'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF"
                    },
                },
            }

            with mui.Box():
                mui.Typography('Выберете нужные проекты')
                mui.FormControl(
                    mui.InputLabel('', id="demo-simple-select-label", sx={
                        "borderColor": "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526",
                        'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526", }),
                    mui.Select(
                        temp,
                        labelId="demo-multiple-name-label",
                        id="demo-multiple-name",
                        multiple=True,
                        onChange=handle_change,
                        value=num,
                        MenuProps=MenuProps,
                        sx={
                            "borderBottom": 1,
                            "borderColor": "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526",
                            'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526",
                        }
                    ),
                    fullWidth=False,
                    sx={'width': '100%', 'margin-top': '3%'}, variant="standard")

    def RangeSlider(self, key):
        with mui.Box(sx={"flex": 1, "minHeight": 0,
                         "padding": "5px 15px 5px 15px",
                         "borderBottom": 1,
                         "borderColor": "divider",
                         'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                         'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526", }):
            def handle_change(event, value):
                st.session_state.range_slider_max = value[1]
                st.session_state.range_slider_min = value[0]

            with mui.Grid():
                mui.Slider(defaultValue=([st.session_state.maxdays, 0]),
                           max=st.session_state.maxdays,
                           min=0,
                           step=1,
                           orientation='horizontal',
                           valueLabelDisplay="off",
                           onKeyDown='preventHorizontalKeyboardNavigation',
                           onChangeCommitted=handle_change,
                           sx={'width': '60%', 'margin-left': '20%', 'margin-top': '10%',
                               'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526",
                               },
                           )

                with mui.Box(sx={"flex": 1, "minHeight": 0, "padding": "5px 15px 5px 15px",
                                 'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                                 'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526"}):
                    mui.Grid(
                        mui.Grid(
                            mui.Typography(st.session_state.date_past.strftime("%Y-%m-%d"), sx={
                                'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                                'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526", },
                                           align="center"),
                            xs=6
                        ),
                        mui.Grid(
                            mui.Typography(st.session_state.date_present.strftime("%Y-%m-%d"), sx={
                                'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                                'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526", },
                                           align="center"),
                            xs=6,
                        ),
                        container=True,
                        spacing=1,
                    )

    def Table(self, content, key):
        with mui.Box(sx={"flex": 1, "minHeight": 0}):
            mui.DataGrid(
                columns=content['col'],
                rows=content['rows'],
                pageSize=6,
                experimentalFeatures={'newEditingApi': True},
                rowsPerPageOptions=[5],
                checkboxSelection=True,
                disableSelectionOnClick=True,
                sx={
                    'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                    'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526",
                }
            )

    def Bar(self, content, key):
        with mui.Box(sx={'flex': 1, 'minHeight': 0}):
            nivo.Bar(
                data=content['x'],
                keys=content['y'],
                indexBy="country",
                margin={'top': 50, 'right': 50, 'bottom': 50, 'left': 60},
                padding=0.2,
                innerPadding=2,
                valueScale={'type': 'linear'},
                indexScale={'type': 'band', 'round': True},
                colors={'scheme': 'nivo'},
                theme=self.themes["dark" if st.session_state[f'{key}_st'] == 0 else "light"],
                borderColor={'theme': 'background'},
                axisTop=None,
                axisRight=None,
                borderRadius=15,
                axisBottom={
                    'tickSize': 5,
                    'tickPadding': 5,
                    'tickRotation': 0,
                    'legend': '',
                    'legendPosition': 'middle',
                    'legendOffset': 32
                },
                axisLeft={
                    'tickSize': 5,
                    'tickPadding': 5,
                    'tickRotation': 0,
                    'legend': '',
                    'legendPosition': 'middle',
                    'legendOffset': -40
                },
                enableGridY=False,
                labelSkipWidth=10,
                labelSkipHeight=12,
                labelTextColor={
                    'from': 'color',
                    'modifiers': [
                        [
                            'darker',
                            1.6
                        ]
                    ]
                },
                motionConfig="molasses",
                role="application",
                isFocusable=True)

    def Select(self, key):
        with mui.Box(sx={"flex": 1, "minHeight": 0,
                         "padding": "5px 15px 5px 15px",
                         "borderBottom": 1,
                         "borderColor": "divider",
                         'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                         'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526", }):

            def handle_change(event, newValue):
                for item in st.session_state.address:
                    if item in newValue.props.children:
                        value = newValue.props.children.replace(item, '')[:-2]
                st.session_state.select = value

            temp = list()

            for i, item in enumerate(st.session_state.list):
                temp.append(mui.MenuItem(f'{st.session_state.list[i]}, {st.session_state.address[i]}', value=i))

            ITEM_HEIGHT = 48
            ITEM_PADDING_TOP = 8
            MenuProps = {
                'PaperProps': {
                    'style': {
                        'maxHeight': ITEM_HEIGHT * 4 + ITEM_PADDING_TOP,
                        'width': 250,
                    },
                },
            }

            with mui.Box():
                mui.Typography('Выберете один проект')
                mui.FormControl(
                    mui.Select(
                        temp,
                        labelId="demo-simple-select-label",
                        defaultValue=0,
                        id="demo-simple-select",
                        variant="standard",
                        onChange=handle_change,
                        MenuProps=MenuProps,
                        sx={
                            "borderBottom": 1,
                            "borderColor": "divider",
                            'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526", }
                    ),
                    fullWidth=False,
                    sx={'width': '100%', 'margin-top': '3%'})

    def RadianBar(self, content, key):
        with mui.Box(sx={"flex": 1, "minHeight": 0}):
            nivo.RadialBar(
                data=content,
                theme=self.themes["dark" if st.session_state[f'{key}_st'] == 0 else "light"],
                valueFormat=">-.2f",
                padding=0.4,
                cornerRadius=2,
                margin={'top': 40, 'right': 120, 'bottom': 40, 'left': 40},
                radialAxisStart={'tickSize': 5, 'tickPadding': 5, 'tickRotation': 0},
                circularAxisOuter={'tickSize': 5, 'tickPadding': 12, 'tickRotation': 0},
                legends=[
                    {
                        'anchor': 'right',
                        'direction': 'column',
                        'justify': False,
                        'translateX': 50,
                        'translateY': 0,
                        'itemsSpacing': 6,
                        'itemDirection': 'left-to-right',
                        'itemWidth': 100,
                        'itemHeight': 15,
                        'itemTextColor': '#999',
                        'symbolSize': 18,
                        'symbolShape': 'square',
                        'effects': [
                            {
                                'on': 'hover',
                                'style': {
                                    'itemTextColor': '#000'
                                }
                            }
                        ]
                    }
                ])

    def Line(self, content, key):
        with mui.Box(sx={"flex": 1, "minHeight": 0}):
            nivo.Line(
                data=content,
                margin={'top': 50, 'right': 200, 'bottom': 20, 'left': 50},
                yFormat=" >-.2f",
                axisTop=None,
                axisRight=None,
                axisBottom=None,
                curve="cardinal",
                xScale={'type': 'point'},
                yScale={
                    'type': 'linear',
                    'min': 'auto',
                    'max': 'auto',
                    'stacked': False,
                    'reverse': False
                },
                theme=self.themes['dark' if st.session_state[f'{key}_st'] == 0 else 'light'],
                axisLeft={
                    'orient': 'left',
                    'tickSize': 5,
                    'tickPadding': 5,
                    'tickRotation': 0,
                    'legend': '',
                    'legendOffset': -40,
                    'legendPosition': 'middle'
                },
                enableGridX=False,
                enableGridY=False,
                pointSize=2,
                pointColor={'theme': 'background'},
                pointBorderWidth=1,
                pointBorderColor={'from': 'serieColor'},
                pointLabelYOffset=-12,
                enableCrosshair=False,
                enableArea=False,
                enableSlices="x",
                lineWidth=4,
                useMesh=True,
                legends=[
                    {
                        'anchor': 'right',
                        'direction': 'column',
                        'justify': False,
                        'translateX': 100,
                        'translateY': 0,
                        'itemsSpacing': 0,
                        'itemDirection': 'left-to-right',
                        'itemWidth': 80,
                        'itemHeight': 20,
                        'itemOpacity': 0.75,
                        'symbolSize': 12,
                        'symbolShape': 'circle',
                        'symbolBorderColor': 'rgba(0, 0, 0, .5)',
                        'effects': [
                            {
                                'on': 'hover',
                                'style': {
                                    'itemBackground': 'rgba(0, 0, 0, .03)',
                                    'itemOpacity': 1
                                }
                            }
                        ]
                    }
                ])


    def Calendar(self, content, key):
        with mui.Box(sx={"flex": 1, "minHeight": 0}):
            nivo.Calendar(data=content,
                          from_=st.session_state.min_time,
                          to_=st.session_state.max_time,
                          theme=self.themes["dark" if st.session_state[f'{key}_st'] == 0 else "light"],
                          emptyColor="#eeeeee",
                          colors=['#61cdbb', '#97e3d5', '#e8c1a0', '#f47560'],
                          margin={'top': 0, 'right': 0, 'bottom': 0, 'left': 25},
                          yearSpacing=40,
                          monthBorderColor="#ffffff",
                          dayBorderWidth=2,
                          monthSpacing=10,
                          dayBorderColor="#ffffff",
                          direction="horizontal",
                          legends=[
                              {
                                  'anchor': 'bottom-right',
                                  'direction': 'row',
                                  'translateY': 36,
                                  'itemCount': 4,
                                  'itemWidth': 42,
                                  'itemHeight': 36,
                                  'itemsSpacing': 14,
                                  'itemDirection': 'right-to-left'
                              }
                          ])

    def Reviews(self, content, key):

        with mui.Box(sx={"flex": 1, "minHeight": 0, "padding": "5px 15px 5px 15px",
                         'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                         'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526"}):
            mui.Grid(
                mui.Grid(
                    mui.Typography('Рейтинг', align="center"),
                    mui.Rating(name="disabled", value=content['Rating'], size="large",
                               sx={'margin-top': '5%', 'margin-left': '10%'},
                               align="center", readOnly=True),
                    mui.Typography('Опубликовано', sx={'margin-top': '10%'}, align="center"),
                    mui.Typography(content['Date'], align="center"),
                    mui.Typography('Кол-во лайков', sx={'margin-top': '10%'}, align="center"),
                    mui.Typography(content['Like'], align="center"),
                    mui.Typography('Кол-во дизлайков', sx={'margin-top': '10%'}, align="center"),
                    mui.Typography(content['Dislike'], align="center"),
                    xs=4,
                    sx={'margin-top': '10%'}
                ),
                mui.Grid(
                    mui.Accordion(
                        mui.AccordionSummary(
                            mui.Typography('Текст отзыва', sx={'flexShrink': 0}),
                            expandIcon=mui.icon.ArrowDropDown,
                            ariacontrols="panel1a-content",
                            id="panel1a-header",
                            TransitionProps={'unmountOnExit': True}),
                        mui.AccordionDetails(
                            mui.InputBase(
                                value=content['Reviews'],
                                id="standard-textarea",
                                sx={'margin-top': '0%', 'margin-left': '0%', 'ml': 1, 'flex': 1,
                                    'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526"},
                                InputProps={'readOnly': True},
                                multiline=True,
                                minRows=2,
                                maxRows=8,
                                label='Текст отзыва',
                                fullWidth=True,
                                variant="standard", )),
                        sx={'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                            'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526"},
                        defaultExpanded=True),
                    mui.Accordion(
                        mui.AccordionSummary(
                            mui.Typography('Текст официального ответа', sx={'flexShrink': 0}),
                            expandIcon=mui.icon.ArrowDropDown,
                            ariacontrols="panel1a-content",
                            id="panel1a-header",
                            TransitionProps={'unmountOnExit': True}),
                        mui.AccordionDetails(
                            mui.InputBase(
                                value=content['OrgText'],
                                id="standard-textarea1",
                                sx={'margin-top': '0%', 'margin-left': '0%', 'ml': 1, 'flex': 1,
                                    'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526"},
                                InputProps={'readOnly': True},
                                multiline=True,
                                minRows=2,
                                maxRows=8,
                                label='Текст отзыва',
                                fullWidth=True,
                                variant="standard", )),
                        sx={'background': "#252526" if st.session_state[f'{key}_st'] == 0 else "#FFFFFF",
                            'color': "#FFFFFF" if st.session_state[f'{key}_st'] == 0 else "#252526"}),
                    xs=7,
                    sx={'margin-top': '10%', 'margin-left': '5%'}
                ),
                container=True,
                spacing=2,
            )
