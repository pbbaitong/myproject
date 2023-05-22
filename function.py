from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

import pandas as pd
import streamlit as st

import plotly.graph_objects as go
import base64

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)
            
    modification_container = st.container()
    
    column_list = df.columns.to_list()
    column_list.remove('ชื่อจริง')
    column_list.remove('นามสกุล')
    
    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", column_list)
        
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            
            if is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
                    
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]            
            
            
            
            # Treat columns with < 10 unique values as categorical
            elif is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                if column == 'โรคประจำตัว':
                    user_cat_input = right.multiselect(f"Values for {column}", ['ความดันโลหิต', 'ไขมันในเลือดสูง', 'เบาหวาน', 'ลิ้นหัวใจรั่ว โรคหัวใจ', 'ไตวาย ภาวะไตอักเสบ', 'โลหิตจาง มะเร็งเม็ดเลือด', 'หอบหืด จมูกอักเสบ', 'อื่น ๆ'])
                else:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique()
                    )
                user_cat_input = '|'.join(user_cat_input)
                # st.write(str(user_cat_input))
                df = df[df[column].astype(str).str.contains(user_cat_input, regex=True)]
                # df = df[df[column].isin(user_cat_input)]


            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

def format_congenital(congenital):
    # --- HT ---
    ht = 1 if 'ความดันโลหิต' in congenital else 0
    
    # --- DLP ---
    dlp = 1 if 'ไขมันในเลือดสูง' in congenital else 0
    
    # --- DM ---
    dm = 1 if 'เบาหวาน' in congenital else 0
    
    # --- HEART ---
    heart = 1 if 'ลิ้นหัวใจรั่ว โรคหัวใจ' in congenital else 0
    
    # --- KIDNEY ---
    kidney = 1 if 'ไตวาย ภาวะไตอักเสบ' in congenital else 0
    
    # --- BLOOD ---
    blood = 1 if 'โลหิตจาง มะเร็งเม็ดเลือด' in congenital else 0
    
    # --- BREATHE ---
    breathe = 1 if 'หอบหืด จมูกอักเสบ' in congenital else 0
    
    # --- OTHERS ---
    others = 1 if 'อื่น ๆ' in congenital else 0
    
    return (ht, dlp, dm, heart, kidney, blood, breathe, others)

def horizontal_chart(top_labels, x_data, y_data):
    top_labels = top_labels

    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)']

    x_data = x_data

    y_data = y_data

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
            for xd, yd in zip(x_data, y_data):
                fig.add_trace(go.Bar(
                    x=[xd[i]], y=[yd],
                    orientation='h',
                    # marker=dict(
                        # color=colors[i],
                        # line=dict(color='rgb(248, 248, 249)', width=1)
                    # )
                ))

    fig.update_layout(
    xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
    ),
    yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.7, 1]
    ),
    barmode='stack',
    # paper_bgcolor='rgb(248, 248, 255)',
    # plot_bgcolor='rgb(248, 248, 255)',
    margin=dict(l=100, r=10, t=40, b=0),
    showlegend=False,
    height=200
    )
    
    fig.update_yaxes(automargin='left+top')

    annotations = []

    for yd, xd in zip(y_data, x_data):
            # labeling the y-axis
            annotations.append(dict(xref='paper', yref='y',
                                    x=0.1, y=yd,
                                    xanchor='right',
                                    text=str(yd),
                                    font=dict(family='Anuphan', size=14),
                                    showarrow=False, align='right'))
            # labeling the first percentage of each bar (x_axis)
            annotations.append(dict(xref='x', yref='y',
                                    x=xd[0] / 2, y=yd,
                                    text=str(f'{xd[0]:.2f}') + '%',
                                    font=dict(family='Anuphan', size=14,
                                            color='rgb(248, 248, 255)'),
                                    showarrow=False))
            # labeling the first Likert scale (on the top)
            if yd == y_data[-1]:
                annotations.append(dict(xref='x', yref='paper',
                                        x=xd[0]/2, y=1.1,
                                        text=top_labels[0],
                                        font=dict(family='Anuphan', size=14,
                                                    color='rgb(0, 0, 0)'),
                                        showarrow=False))
            space = xd[0]
            for i in range(1, len(xd)):
                # labeling the rest of percentages for each bar (x_axis)
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i]/2), y=yd,
                                        text=str(f'{xd[i]:.2f}') + '%',
                                        font=dict(family='Anuphan', size=14,
                                                    color='rgb(248, 248, 255)'),
                                        showarrow=False))
                # labeling the Likert scale
                if yd == y_data[-1]:
                    annotations.append(dict(xref='x', yref='paper',
                                            x=space + (xd[i]/2), y=1.1,
                                            text=top_labels[i],
                                            font=dict(family='Anuphan', size=14,
                                                        color='rgb(67, 67, 67)'),
                                            showarrow=False))
                space += xd[i]

    fig.update_layout(annotations=annotations)
    return fig

def show_header():
    file_ = open("images/logo.png", "rb")
    contents = file_.read()
    logo_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    
    file_ = open("images/name.jpg", "rb")
    contents = file_.read()
    name_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    
    file_ = open("images/kmutt_logo.png", "rb")
    contents = file_.read()
    kmutt_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    
    file_ = open("images/cr_logo.png", "rb")
    contents = file_.read()
    cr_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    
    header_style = """
        <style>            
        [class*="navbar-header"] {
            height: 200px;
            font-family: 'Anuphan', sans-serif;
            color: #FF884B;
            
        }
        .navbar-brand {
            margin-left: 27%;
            margin-bottom: 10px;
        }
        .individualbtnposition {
            margin-left: 5%;
        }
        [class*="navbar fixed-top navbar-expand-lg navbar-dark"] {
            box-shadow: 0 1px 10px 0 #FFEBEB;
        }
        """
    st.markdown(f"""
        <div class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #ffffff;">
            <a class="navbar-brand"><br><br><img src="data:image/gif;base64,{logo_url}", width="170"></a>    
            <div class="navbar-header" id="navbarNav">
                <div class="header">
                <br>
                <br>
                <br>
                    <img src="data:image/gif;base64,{name_url}", width="600">
                </div>
            </div>
            <div class="individualbtnposition"><img src="data:image/gif;base64,{kmutt_url}", width="100"><img src="data:image/gif;base64,{cr_url}", width="200"></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(header_style, unsafe_allow_html=True)