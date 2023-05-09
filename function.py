from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

import pandas as pd
import streamlit as st

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
                st.write(str(user_cat_input))
                df = df[df[column].astype(str).str.contains(user_cat_input, regex=True)]
                # df = df[df[column].isin(user_cat_input)]


            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df