from math import isnan
from dash import Dash, html, dcc, Output, Input, State, callback_context
import pandas as pd
import plotly.express as px
from plotly.basedatatypes import BaseFigure
import dash_bootstrap_components as dbc
from db import DB

data_set: DB = DB()
app: Dash = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.CYBORG])
app.title="CS 411: Final Project"
background_color: str = "rgb(17,17,17)"
view_options: list = [s.upper() for s in ["University Publications Over Time", "University Number of Faculty With Atleast N-Publications", "Faculty Page", "Top Faculty Results Based On Keywords", "Top Publication Results Based On Keywords", "University Faculty Type Distribution"]]
view_options_title_color= ["pink", "yellow", "#66fcf1", "lightgreen", "#efe2ba", "#ffca80"]


widgets = [
            [html.Button(html.H5(view_options[0], style={"textAlign":"center", "color":view_options_title_color[0], "fontWeight":"bold", "margin":"0"}), view_options[0], 0, style={"margin":"auto", "display": "block", "border":"none", "backgroundColor":"transparent", "marginTop":"1%", "marginBottom":"0"}), html.Div(id="graph1", style={"margin":"1%", "marginTop":"0"})],
            [html.Button(html.H5(view_options[1].replace("N-", f"{0}-"), "title2", style={"textAlign":"center", "color":view_options_title_color[1], "fontWeight":"bold", "margin":"0"}), view_options[1], style={"margin":"auto", "display": "block", "border":"none", "backgroundColor":"transparent"}), dcc.Slider(1, 1, 1, value=1, id="number_of_min_publications_slider"), html.Div(id="graph2")],
            [
                html.Button(html.H5(view_options[2], style={"textAlign":"center", "fontWeight":"bold", "margin":"0", "color":view_options_title_color[2]}), view_options[2], 0, style={"margin":"auto", "display": "block", "border":"none", "backgroundColor":"transparent"}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("EDIT FACULTY MENU", style={"textAlign":"center", "color":view_options_title_color[2], "fontWeight":"bold"})),
                        dbc.ModalBody(html.Table(html.Tbody(
                            [
                                html.Tr([html.Td("POSITION:", style={"paddingRight":"1%", "color":"white", "fontWeight":"bold", "textAlign":"right", "minWidth": "150px"}), html.Td(dcc.Input(id="edit_position_input"))]),
                                html.Tr([html.Td("EMAIL ADDRESS:", style={"paddingRight":"1%", "color":"white", "fontWeight":"bold", "textAlign":"right"}), html.Td(dcc.Input(id="edit_email_input", type="text"))]),
                                html.Tr([html.Td("PHONE NUMBER:", style={"paddingRight": "1%", "color":"white", "fontHeight":"bold", "textAlign":"right"}), html.Td(dcc.Input(id="edit_phone_input", type="text"))]),
                                html.Tr([html.Td("RESEARCH AREA:", style={"paddingRight":"1%", "color":"white", "fontHeight":"bold", "textAlign":"right"}), html.Td(dcc.Input (id="edit_research_input", type="text"))])
                            ]))),
                        dbc.ModalFooter([html.Div(dbc.Button("Submit", "edit_modal_submit", "ms-auto", n_clicks=0, style={"background":"green", "borderColor":"green", "borderRadius":"10px"}), style={}), html.Div(dbc.Button("Submit", "edit_modal_close", "ms-auto", n_clicks=0, style={"background":"red", "borderColor":"red", "borderRadius":"10px"}), style={})])
                    ], "edit_modal", size="lg", is_open=False),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("ADD FACULTY MENU", style={"textAlign":"center", "color":view_options_title_color[2], "fontWeight": "bold"})), 
                        dbc.ModalBody(html.Table(html.Tbody(
                            [
                                html.Tr([html.Td("FACULTY NAME:", style={"paddingRight":"1%", "color":"white", "fontWeight":"bold", "textAlign":"right", "minWidth": "150px"}), html.Td(dcc.Input(id="add_name_input"))]),
                                html.Tr([html.Td("POSITION:", style={"paddingRight":"1%", "color":"white", "fontWeight":"bold", "textAlign":"right"}), html.Td(dcc.Input(id="add_position_input", type="text"))]),
                                html.Tr([html.Td("EMAIL ADDRESS:", style={"paddingRight":"1%", "color":"white", "fontWeight":"bold", "textAlign":"right"}), html.Td(dcc.Input(id="add_email_input", type="text"))]),
                                html.Tr([html.Td("PHONE NUMBER:", style={"paddingRight":"1%", "color": "white", "fontWeight":"bold", "textAlign":"right"}), html.Td(dcc.Input(id="add_phone_input", type="text"))]),
                                html.Tr([html.Td("UNIVERSITY:", style={"paddingRight":"1%", "color": "white", "fontWeight":"bold", "textAlign":"right"}), html.Td(dcc.Dropdown(data_set.Affiliation_df["Affiliation_name"], "", id="add_university_input"))]),
                                html.Tr([html.Td("RESEARCH AREA:", style={"paddingRight":"1%", "color":"white", "fontWeight": "bold", "textAlign": "right"}), html.Td(dcc.Input(id="add_research_input", type="text"))]),
                                html.Tr([html.Td("PHOTO URL:", style={"paddingRight":"1%", "color": "white", "fontWeight":"bold", "textAlign":"right"}), html.Td(dcc.Input(id="add_photo_input", type="text"))])
                            ]))),
                        dbc.ModalFooter([html.Div(dbc.Button("Submit", "add_modal_submit", "ms-auto", style={"background": "green", "borderColor":"green", "borderRadius":"10px"}, n_clicks=0), style={}), html.Div(dbc.Button("Submit", "add_modal_close", "ms-auto", n_clicks=0, style={"background":"red", "borderColor":"red", "borderRadius":"10px"}), style={})])
                    ], "add_modal", size="lg", is_open=False),
                html.Table([html.Tbody([html.Tr(
                    [
                        html.Td(dcc.Dropdown(clearable=False, id="Faculty_name_dropdown"), style={"width": "100%", "paddingRight":"10%", "paddingLeft":"50px", "color":"black"}),
                        html.Td(html.Button(html.Img(src="https://img.icons8.com/nolan/512/edit--v1.png", height=40, width=40), id="edit_button", n_clicks=0, style={"background":background_color, "borderRadius":"20px"}), style={"minWidth": ""}),
                        html.Td(html.Button(html.Img(src="https://img.icons8.com/plasticine/512/000000/filled-trash.png", height=40, width=40), id="delete_button", n_clicks=0, style={"background":background_color, "borderRadius":"20px"}), style={"minWidth": ""}),
                        html.Td(html.Button(html.Img(src="https://img.icons8.com/color/512/eeeeee/add--vi.png", height=40, width=40), id="add_button", n_clicks=0, style={"background":background_color, "borderRadius":"20px"}), style={"minWidth": ""})
                    ])])], style={"marginTop":"2%", "marginBottom":"2%", "textAlign":"center"}),
                html.Div(html.Div(id="faculty_info", style={"display": "flex", "flexDirection": "row"}), "faculty_info_wrapper")
            ],
            [html.Button(html.H5(view_options[3], style={"textAlign":"center", "color":view_options_title_color[3], "fontWeight":"bold", "margin":"0"}), view_options[3], 0, style={"margin":"auto", "display": "block", "border":"none", "backgroundColor":"transparent"}), dcc.Dropdown(id="faculty_Keywords_dropdown", style={"textAlign":"center", "color":"black", "paddingLeft":"10%", "paddingRight":"10%", "marginTop":"2%"}), html.Div(id="chart1")],
            [html.Button(html.H5(view_options[4], style={"textAlign":"center", "color":view_options_title_color[4], "fontWeight":"bold", "margin":"0"}), view_options[4], 0, style={"margin":"auto", "display": "block", "border":"none", "backgroundColor":"transparent"}), dcc.Dropdown(id="publication_Keywords_dropdown", style={"textAlign":"center", "color":"black", "paddingLeft":"10%", "paddingRight":"10%", "marginTop":"2%"}), html.Div(id="chart2")],
            [html.Button(html.H5(view_options[5], style={"textAlign":"center", "color":view_options_title_color[5], "fontWeight":"bold", "margin":"0"}), view_options[5], 0, style={"margin":"auto", "display": "block", "border":"none", "backgroundColor":"transparent", "marginTop":"1%"}), html.Div(id="graph3")] 
         ]



app.layout = html.Div([
    dbc.Modal([dbc.ModalHeader(dbc.ModalTitle(id="enlarge_widget_title"), close_button=True), dbc.ModalBody(id="enlarge_widget_body")], "enlarge_widget", size="xl", is_open=False, centered=True),
    html.Div([html.Div(style={"margin":"auto", "flex": 4}, children=[dcc.Dropdown(data_set.Affiliation_df["Affiliation_name"], "", True, False, id="Affiliation_name_dropdown", style={"textAlign":"center", "color":"black", "margin": "auto", "paddingLeft":"5%"})]), html.Div(html.Img(src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1200px-No_image_available.svg.png", id="Affiliation_photo", height=95, width=150, style={"display":"block", "margin":"auto", "background":"white", "border":"2px solid grey", "borderRadius":"20px"}), style={"flex": 1, "paddingLeft":"1%"})], style={"display": "flex", "flexDirection": "row", "margin":"auto", "paddingTop":"5px", "paddingBottom":"5px"}), 
    html.Table(html.Tbody(
        [html.Tr([
                    html.Td(html.Div(widgets[0], style={"border":"5px solid red", "borderRadius":"20px", "margin":"auto", "background":background_color, "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px", "paddingBottom":"5px"}), 
                    html.Td(html.Div(widgets[1], style={"padding":"1%", "border":"5px solid yellow", "borderRadius":"20px", "background":background_color, "margin":"auto", "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px", "paddingBottom":"5px"}),
                    html.Td(html.Div(widgets[2], style={"padding":"1%", "margin":"auto", "border":"5px solid darkorange", "borderRadius":"20px", "background":background_color, "height": "420px"}), style={"paddingLeft":"5px", "paddingRight":"5px", "paddingBottom":"5px"})
                ]),
         html.Tr([
                    html.Td(html.Div(widgets[3], style={"padding":"1%", "margin":"auto", "border":"5px solid blue", "borderRadius":"20px", "background":background_color, "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px"}),
                    html.Td(html.Div(widgets[4], style={"padding":"1%", "margin":"auto", "border":"5px solid #269699", "borderRadius":"20px", "background":background_color, "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px"}),
                    html.Td(html.Div(widgets[5], style={"border":"5px solid #BF40BF", "borderRadius":"20px", "margin":"auto", "background":background_color, "height":"420px"}), style={"paddingLeft":"5px", "paddingRight":"5px"}), 
                ])
        ]
    ), style={"tableLayout": "fixed", "width": "100%", "height": "100%"}),
    html.H6(id="faculty_info_widget_change_trigger", style={"visibility":"hidden"})
], style={"background":"rgb(6,6,6)", "margin":0, "padding":0, "width":"100%", "height":"100%", "top":"0px", "left":"0px", "zIndex":"1000"})



#CALLBACKS
@app.callback([Output("Affiliation_photo", "src"), Output("Affiliation_photo", "alt"), Output("graph1", "children"), Output("graph3", "children"), Output("number_of_min_publications_slider", "value"), Output("faculty_Keywords_dropdown", "options"), Output("faculty_Keywords_dropdown", "value"), Output("publication_Keywords_dropdown", "options"), Output("publication_Keywords_dropdown", "value"), Output("faculty_info_widget_change_trigger", "children")],
               Input("Affiliation_name_dropdown", "value"))
def update_view(university_names):
    if university_names is None or university_names == "" or len(university_names) == 0: 
        return ("https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1200px-No_image_available.svg.png", "", [], [], 1, [], "", [], "", "")
    university_names = [university_names] if isinstance(university_names, str) else university_names
    df1: pd.DataFrame = (data_set.Publication_df[data_set.Publication_df ["Year"] > 0][["Publication_id", "Year"]]
                                 .join(data_set.Publish_df[["Publication_id","Faculty_id"]].set_index("Publication_id"), on="Publication_id")
                                 .join(data_set.Faculty_df[["Faculty_id","Affiliation_id"]].set_index("Faculty_id"), on="Faculty_id")
                                 .join(data_set.Affiliation_df[["Affiliation_id","Affiliation_name"]].set_index("Affiliation_id"), on="Affiliation_id")[["Year", "Affiliation_name"]])
    fig1: BaseFigure = px.bar(df1[df1["Affiliation_name"].isin(university_names)].value_counts().rename_axis(["Year","University"]).reset_index(name="Number of Publication(s)"), x="Year", y="Number of Publication(s)", height=370, template="plotly_dark", color="University", barmode="group")
    fig1.update_layout(plot_bgcolor="#23252F", font = {"family": "courier"}, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    df2: pd.DataFrame = (data_set.Affiliation_df[data_set.Affiliation_df["Affiliation_name"].isin(university_names) ][["Affiliation_id"]]
                                 .join(data_set.Faculty_df[["Faculty_id","Affiliation_id"]].set_index("Affiliation_id"), on="Affiliation_id")
                                 .join(data_set.Publish_df.set_index("Faculty_id"), on="Faculty_id"))[["Faculty_id", "Publication_id"]]
    faculty_keywords: list = list(data_set.Keyword_df[data_set.Keyword_df["Keyword_id"].isin(list(df2[["Faculty_id"]].join(data_set.Faculty_keyword_df[["Keyword_id", "Faculty_id"]].set_index("Faculty_id"), on="Faculty_id")["Keyword_id"]))]["Keyword_name"])
    publication_keywords: list = list(data_set.Keyword_df[data_set.Keyword_df["Keyword_id"].isin(list(df2[["Publication_id"]].join(data_set.Publication_keyword_df[["Keyword_id", "Publication_id"]].set_index("Publication_id"), on="Publication_id")["Keyword_id"]))]["Keyword_name"])
    df2: pd.DataFrame = (data_set.Affiliation_df[data_set. Affiliation_df["Affiliation_name"].isin(university_names)][["Affiliation_id","Affiliation_name"]]
                                 .join(data_set.Faculty_df[["Affiliation_id", "Position"]].set_index("Affiliation_id"), on="Affiliation_id"))[["Affiliation_name","Position"]]
    positions: list = df2["Position"].unique()
    graph3_data: dict = {"Position": positions}
    graph3_data.update({u: [len (df2[((df2["Affiliation_name"] == u) & (df2["Position"]== p))]) for p in positions] for u in university_names})
    fig2: BaseFigure = px.bar(pd.DataFrame(graph3_data), y="Position", x=university_names, template= "plotly_dark", height=350) 
    fig2.update_layout(plot_bgcolor="#23262F", font = {"family":"courier"})
    return (data_set.Affiliation_df[data_set.Affiliation_df["Affiliation_name"] == university_names[-1]]["Affiliation_photoUrl"].iloc[0], 
            university_names[-1],
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            1,
            faculty_keywords,
            "" if len(faculty_keywords) == 0 else faculty_keywords[0], 
            publication_keywords,
            "" if len(publication_keywords) == 0 else publication_keywords[0],
            "")


@app.callback([Output("enlarge_widget_body", "children"), Output("enlarge_widget", "is_open"), Output("enlarge_widget_title", "children"), Output("enlarge_widget_title", "style")],
              [Input(view, "n_clicks") for view in view_options],
              [State("enlarge_widget", "is_open"), State("graph1", "children"), State("graph2", "children"), State("faculty_info_wrapper", "children"), State("chart1", "children"), State("chart2", "children"), State("graph3", "children")]) 
def enlarge_widget(v1, v2, v3, v4, v5, V6, enlarge_widget_is_open: bool, graph1_c, graph2_c, faculty_info_c, chart1_c, chart2_c, graph3_c):
    try:
        idx: int=view_options.index([p["prop_id"] for p in callback_context.triggered][0][:-9])
        modal_widget = graph3_c
        if idx == 0: modal_widget = graph1_c
        if idx == 1: modal_widget = graph2_c
        if idx == 2:
            del faculty_info_c["props"]["id"]
            modal_widget = faculty_info_c
        if idx == 3: modal_widget = chart1_c
        if idx == 4: modal_widget = chart2_c
        return (modal_widget, True, view_options[idx], {"fontheight":"bold", "color":view_options_title_color[idx]}) 
    except ValueError: return ([], False, "", {})



@app.callback([Output("graph2", "children"), Output("title2", "children"), Output("number_of_min_publications_slider", "max"), Output("number_of_min_publications_slider", "marks")], 
               Input("number_of_min_publications_slider", "value"),
              [State("Affiliation_name_dropdown", "value"), State("number_of_min_publications_slider", "max"), State("number_of_min_publications_slider", "marks")])
def generate_graph_for_university_faculty_with_atleast_n_publications(num_publications: int, university_names, max_slider: int, marks_slider: dict):
    university_names = [university_names] if isinstance(university_names, str) else university_names
    if len(university_names) == 0: return ([], view_options[1], 1, {})
    num_publications_by_each_faculty_id: pd.DataFrame = data_set.Publish_df["Faculty_id"].value_counts().rename_axis("Faculty_id").reset_index(name="num_publications")
    df2: pd.DataFrame = (num_publications_by_each_faculty_id[num_publications_by_each_faculty_id["num_publications"] >= num_publications]
                                                            .join(data_set.Faculty_df[["Faculty_id", "Affiliation_id"]].set_index("Faculty_id"), on="Faculty_id")
                                                            .join(data_set.Affiliation_df[data_set.Affiliation_df["Affiliation_name"].isin(university_names)][["Affiliation_id", "Affiliation_name"]].set_index("Affiliation_id"), on="Affiliation_id")[["Affiliation_name"]]
                                                            .value_counts().rename_axis("University name(s)").reset_index(name=f"Number of Faculty with {num_publications} or more publication(s)")
                                                            .sort_values(by=[f"Number of Faculty with {num_publications} or more publication(s)"], ascending=True))
    fig2: BaseFigure = px.bar(df2, x=f"Number of Faculty with {num_publications} or more publication(s)", y="University name(s)", height=2000*(len(df2.index)+8)/len(data_set.Affiliation_df.index), template="plotly_dark")
    fig2.update_layout(plot_bgcolor="#23262f", font={"family": "courier"})
    graph_out = dcc.Graph(figure=fig2)
    try: max_pub: int = int((data_set.Affiliation_df[data_set.Affiliation_df["Affiliation_name"].isin(university_names)]
                                     .join(data_set.Faculty_df[["Faculty_id","Affiliation_id"]].set_index("Affiliation_id"), on="Affiliation_id")
                                     .join(num_publications_by_each_faculty_id.set_index("Faculty_id"), on="Faculty_id")["num_publications"]).max())
    except ValueError:
        max_pub: int = 1
        graph_out = []

    return (graph_out,
            view_options[1].replace("N-", f"{num_publications}-"),
            max_pub,
            {i: {"label":str(i), "style": {"color": "#f50"}} for i in range(1, max_pub, max_pub//10)} if max_slider != max_pub else marks_slider)



@app.callback(Output("chart1", "children"),
              Input("faculty_Keywords_dropdown","value"),
              State("Affiliation_name_dropdown", "value"))
def generate_table_by_keyword_faculty (keyword: str, university_names):
    university_names = [university_names] if isinstance(university_names, str) else university_names
    if len(university_names) == 0: return []
    df1: pd.DataFrame = (data_set.Affiliation_df[data_set.Affiliation_df["Affiliation_name"].isin(university_names)][["Affiliation_id","Affiliation_name"]]
                               .join(data_set.Faculty_df[["Faculty_id","Affiliation_id"]].set_index("Affiliation_id"), on="Affiliation_id")
                               .join(data_set.Faculty_keyword_df.set_index("Faculty_id"), on="Faculty_id")
                               .join(data_set.Keyword_df.set_index("Keyword_id"), on="Keyword_id"))[["Affiliation_name","Faculty_score","Keyword_name"]]
    df1: pd.DataFrame = df1[df1["Keyword_name"] == keyword][["Affiliation_name","Faculty_score"]]
    fig1: BaseFigure = px.pie(values=[df1[df1["Affiliation_name"]==u]["Faculty_score"].sum() for u in university_names], names=university_names, template="plotly_dark", height=300)
    fig1.update_layout(plot_bgcolor="#23262F", font={"family": "courier"})
    return dcc.Graph(figure=fig1)



@app.callback(Output("chart2", "children"), 
              Input("publication_Keywords_dropdown", "value"), 
              State("Affiliation_name_dropdown", "value"))
def generate_table_by_keyword_publication(keyword: str, university_names):
    university_names = [university_names] if isinstance(university_names, str) else university_names
    if len(university_names) == 0: return []
    df2: pd.DataFrame = (data_set.Affiliation_df[data_set.Affiliation_df["Affiliation_name"].isin(university_names)][["Affiliation_id","Affiliation_name"]]
                                 .join(data_set.Faculty_df[["Faculty_id", "Affiliation_id"]].set_index("Affiliation_id"), on="Affiliation_id")
                                 .join(data_set.Publish_df.set_index("Faculty_id"), on="Faculty_id")
                                 .join(data_set.Publication_keyword_df.set_index("Publication_id"), on="Publication_id")
                                 .join(data_set.Publication_df[["Publication_id","Title","Year"]].set_index("Publication_id"), on="Publication_id")
                                 .join(data_set.Keyword_df.set_index("Keyword_id"), on="Keyword_id"))[["Affiliation_name","Publication_score","Keyword_name"]]
    df2: list = df2[df2["Keyword_name"] == keyword][["Affiliation_name", "Publication_score"]]
    fig2: BaseFigure = px.pie(values=[df2[df2["Affiliation_name"]==u]["Publication_score"].sum() for u in university_names], names=university_names, template="plotly_dark", height=300)
    fig2.update_layout(plot_bgcolor="#232621", font={"family": "courier"})
    return dcc.Graph(figure=fig2)



@app.callback([Output("faculty_info", "children"), Output ("edit_modal", "is_open"), Output ("add_modal", "is_open"), Output ("Faculty_name_dropdown","options"), Output("Faculty_name_dropdown", "value")],
              [Input("faculty_info_widget_change_trigger", "children"), Input("Faculty_name_dropdown", "value"), Input("delete_button", "n_clicks"), Input("edit_button", "n_clicks"), Input("add_button", "n_clicks"), Input("edit_modal_close", "n_clicks"), Input("edit_modal_submit", "n_clicks"), Input("add_modal_close", "n_clicks"), Input("add_modal_submit", "n_clicks")],
              [State("edit_modal", "is_open"), State("add_modal", "is_open"), State("edit_position_input", "value"), State("edit_email_input", "value"), State("edit_phone_input", "value"), State("edit_research_input", "value"), State("add_name_input", "value"), State("add_position_input", "value"), State("add_email_input", "value"), State("add_phone_input", "value"), State("add_research_input", "value"), State("add_university_input", "value"), State("add_photo_input", "value"), State("Affiliation_name_dropdown", "value")])
def generate_faculty_page(change_trigger, faculty_name: str, del_btn: int, edit_btn: int, add_btn: int, edit_close_btn: int, edit_submit_btn: int, add_close_btn: int, add_submit_btn: int, edit_is_open: bool, add_is_open: bool, edit_pos_val, edit_email_val, edit_phone_val, edit_research_val, add_name_val, add_pos_val, add_email_val, add_phone, add_research_val, add_university, add_photo, university_names):
    if len(university_names) == 0: return ([], False, False, [], "")
    callback_id: list = [p["prop_id"] for p in callback_context.triggered][0]
    if "delete_button" in callback_id:
        if faculty_name == "" or faculty_name is None: return ([], False, False, [], "")
        faculty_id: int = data_set.Faculty_df[data_set.Faculty_df["Faculty_name"] == faculty_name].iloc[0,:]["Faculty_id"]
        data_set.Faculty_keyword_df = (data_set.Faculty_keyword_df[data_set.Faculty_keyword_df["Faculty_id"] != faculty_id])
        data_set.Publish_df = (data_set.Publish_df[data_set.Publish_df["Faculty_id"] != faculty_id])
        data_set.Faculty_df = (data_set.Faculty_df[data_set.Faculty_df["Faculty_id"] != faculty_id]) 
        faculties: list = list(data_set.Affiliation_df[data_set.Affiliation_df["Affiliation_name"].isin(university_names)][["Affiliation_id"]]
                                       .join(data_set.Faculty_df[["Faculty_name", "Affiliation_id"]].set_index("Affiliation_id"), on="Affiliation_id")["Faculty_name"])
        fac_data_frame: pd.DataFrame = data_set.Faculty_df[data_set.Faculty_df["Faculty_name"] == faculties[0]]
        if len(fac_data_frame) == 0: return ([], False, False, [], "")
        fac_data: pd.Series = fac_data_frame.iloc[0,:]
        faculty_name = faculties[0]
    else:
        if "edit_button" in callback_id: edit_is_open = True
        elif "edit_modal_close" in callback_id: edit_is_open = False 
        elif "add_button" in callback_id: add_is_open = True
        elif "add_modal_close" in callback_id: add_is_open = False
        elif "add_modal_submit" in callback_id:
            recs: list = data_set.Faculty_df.to_records(index=False).tolist()
            recs.append((data_set.Faculty_df["Faculty_id"].max()+1, "" if add_name_val is None else add_name_val, "" if add_pos_val is None else add_pos_val, "" if add_research_val is None else add_research_val, "" if add_email_val is None else add_email_val))
            data_set.Faculty_df = pd.DataFrame.from_records(recs, columns=data_set.Faculty_df.columns)
            add_is_open = False
        elif "edit_nodal_submit" in callback_id:
            rows = data_set.Faculty_df[data_set.Faculty_df["Faculty ame"] == faculty_name].index
            data_set.Faculty_df.loc[rows, "Position"] = "" if edit_pos_val is None else edit_pos_val
            data_set.Faculty_df.loc[rows, "Phone_Number"] = "" if edit_phone_val is None else edit_phone_val 
            data_set.Faculty_df.loc[rows, "Email"] = "" if edit_email_val is None else edit_email_val
            data_set.Faculty_df.loc[rows, "Email"] = "" if edit_email_val is None else edit_email_val
            data_set. Faculty_df.loc[rows, "Research_interest"] = "" if edit_research_val is None else edit_research_val
            edit_is_open = False
        faculties: list = list(data_set.Affiliation_df[data_set.Affiliation_df["Affiliation_name"].isin(university_names)][["Affiliation_id"]]
                                       .join(data_set.Faculty_df[["Faculty_name", "Affiliation_id"]].set_index("Affiliation_id"), on="Affiliation_id")["Faculty_name"])
        faculty_name = ("" if len(faculties) == 0 else faculties[0]) if faculty_name is None or faculty_name == "" else faculty_name
        fac_data_frame: pd.DataFrame = data_set.Faculty_df[data_set.Faculty_df["Faculty_name"] == faculty_name]
        if len(fac_data_frame) == 0: return ([], False, "add_button" in callback_id, [], "")
        fac_data: pd.Series  = fac_data_frame.iloc[0,:]
    labels: list = ["FACULTY NAME:", "POSITION:", "EMAIL ADDRESS:", "PHONE NUMBER:", "RESEARCH AREA", "PUBLICATIONS:", "UNIVERSITY:"]
    data: list = [("--" if not isinstance(fac_data[l], str) and isnan(fac_data[l]) else fac_data[l]) for l in ["Faculty_name", "Position", "Email", "Phone_Number", "Research_interest"]] + [len(data_set.Publish_df[data_set.Publish_df["Faculty_id"] == fac_data["Faculty_id"]])]
    try: data.append(data_set.Affiliation_df[data_set.Affiliation_df["Affiliation_id"] == fac_data["Affiliation_id"]]["Affiliation_name"].iloc[0])
    except: data.append("--")
    return ([html.Img(src=fac_data["Faculty_photoUrl"], alt=faculty_name, height=300, width=240, style={"display":"block", "margin":"auto", "borderRadius":"20px", "padding":"10px", "flex":1}), html.Table([html.Tbody([html.Tr([html.Td(l), html.Td(d)]) for (l, d) in zip(labels, data)])])],
            edit_is_open,
            add_is_open,
            faculties,
            faculty_name)



if __name__ == "__main__": app.run_server(debug=True)
