import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
team_analytics_01 = st.beta_container()
team_analytics_02 = st.beta_container()
team_analytics_03 = st.beta_container()


@st.cache
def load_data(file_name01):
    dframe = pd.read_csv(
        file_name01,
        na_values=['NA', 'Missing', None],
        error_bad_lines=False, sep='\t',
        lineterminator='\n',
        dtype=str,
    )
    dframe.columns = dframe.columns.str.replace(" ", "", regex=True)
    dframe['Date/TimeGrabbed'] = pd.to_datetime(dframe['Date/TimeGrabbed'], errors='coerce')
    dframe['Date/TimeClosed'] = pd.to_datetime(dframe['Date/TimeClosed'], errors='coerce')
    dframe['year_month'] = dframe['Date/TimeGrabbed'].dt.strftime('%Y-%m')
    dframe['diffTime'] = (dframe['Date/TimeClosed'] - dframe['Date/TimeGrabbed']).dt.days
    dframe['DateGrabbed'] = dframe['Date/TimeGrabbed'].dt.strftime('%Y-%m-%d')
    dframe['DateClosed'] = dframe['Date/TimeGrabbed'].dt.strftime('%Y-%m-%d')
    dframe = dframe.rename(columns={'SIS(StudentInformationSystem)': 'SIS'})
    dframe['CaseOwner'] = dframe['CaseOwner'].replace(
        {'Alejandro Hassan': 'Ale', 'Alexander Rodriguez': 'Alex', 'Douglas Carmona': 'Doug',
         'Fabricio Chungo': 'Fabri', 'Federico Bufanio': 'Fede', 'Fernando Diaz Coetzee': 'Fer',
         'Fernando Zavatto': 'Steven', 'Martin Belzunce': 'Tincho',
         'Matias Zulberti': 'Mati', 'Nicolas Pantazis': 'Nico', 'Raul Sosa': 'Rulo', 'Sergio Leyes': 'Sergio'},
        regex=True)
    owners = dframe['CaseOwner'].drop_duplicates()
    year_month = dframe['year_month'].drop_duplicates()
    return dframe, owners, year_month


uploaded_file = st.sidebar.file_uploader(
    label="Uploade CSV file to use as Dataframe",
    type=['csv']
    )
print(uploaded_file)
if uploaded_file is not None and "bb_team" in uploaded_file.name:
    print(uploaded_file)
    print("Ready to start..!")
    try:

        df, owners, year_month = load_data(uploaded_file)
    except Exception as e:
        print(e)



try:
    with team_analytics_01:
        st.title('Team Cases Analytics')
        st.header('Dataframe')
        try:
            table = go.Table(df)
            table.update_layout()
            st.write(table)
        except Exception as e:
            st.write(df)

        st.header('Total Cases/Month')
        cases_month = df['year_month'].value_counts()
        st.bar_chart(cases_month)

        st.header('Total Cases/Owner')
        cant_cases = df['CaseOwner'].value_counts()
        # st.write(cant_cases)
        st.bar_chart(cant_cases)

        left_col, right_col = st.beta_columns(2)

        cases_pivot1 = df.pivot_table(index='CaseOwner', columns='year_month', values='Status', aggfunc='count')
        cases_pivot2 = df.pivot_table(index='year_month', columns='CaseOwner', values='Status', aggfunc='count')
        cases_month_owner = df.groupby(['year_month', 'CaseOwner'])['CaseNumber']. \
            count().to_frame('count').reset_index().set_index(['year_month'])
        cases_owner_month = df.groupby(['CaseOwner', 'year_month'])['CaseNumber']. \
            count().to_frame('count').reset_index().set_index('CaseOwner')

        left_col.header('Cases/Owner/Month')
        left_col.write(cases_pivot1)
        right_col.header('Cases/Month/Owner')
        right_col.write(cases_pivot2)

        left_col.header('Avg Cases/Month/Owner')
        avg_cases1 = cases_pivot1.reset_index().mean().round(0).to_frame('avg')
        left_col.bar_chart(avg_cases1)
        avg_cases1 = avg_cases1.reset_index()
        plot1 = px.pie(avg_cases1, values='avg', names='year_month')
        left_col.plotly_chart(plot1)

        right_col.header('Avg Cases/Owner/Month')
        avg_cases2 = cases_pivot2.reset_index().mean().round(0).to_frame('avg')
        right_col.bar_chart(avg_cases2)
        avg_cases2 = avg_cases2.reset_index()
        plot2 = px.pie(avg_cases2, values='avg', names='CaseOwner')
        right_col.plotly_chart(plot2)

        # table = go.Figure(data=cases_pivot1)
        # table.update_layout(width=900, height=300)
        # table.show()
        # st.write(table)

        plot1 = px.bar(data_frame=cases_pivot1)
        plot2 = px.bar(data_frame=cases_pivot2)
        left_col.plotly_chart(plot1)
        right_col.plotly_chart(plot2)

        selectbox01 = st.sidebar.selectbox("Select Search Field: ", options=['CaseNumber', 'CaseOwner', 'SIS', 'AccountName'])

        options = df[selectbox01].drop_duplicates().tolist()
        selectbox02 = st.sidebar.selectbox("Select an Option: ", options=options)
        df_owner = df[df[selectbox01] == selectbox02]
        df_owner2 = df_owner.loc[:, ['DateGrabbed', 'DateClosed', 'CaseOwner', 'CaseNumber', 'AccountName',
                                     'SIS', 'Subject']].drop(selectbox01, axis='columns')
        st.write(df_owner2)

        # st.header('Select a Case Owner')
        # selectbox01 = st.sidebar.selectbox("Select CaseOwner: ", options=owners.tolist())
        # df_owner = df[df['CaseOwner'] == selectbox01]
        # df_owner2 = df_owner.loc[:,['DateGrabbed', 'DateClosed', 'CaseNumber', 'AccountName',
        #                               'SIS', 'Subject']]
        # st.write(df_owner2)
        #
        # st.header('Select a SIS')
        # sis = df['SIS'].drop_duplicates().tolist()
        # selectbox01 = st.sidebar.selectbox("Select SIS: ", options=sis)
        # df_owner = df[df['SIS'] == selectbox01]
        # df_owner2 = df_owner.loc[:, ['DateGrabbed', 'DateClosed', 'CaseNumber', 'AccountName',
        #                              'CaseOwner', 'Subject']]
        # st.write(df_owner2)
        #
        # st.header('Select Account Name:')
        # account = df['AccountName'].drop_duplicates().tolist()
        # selectbox01 = st.sidebar.selectbox("Select Account Name: ", options=account)
        # df_owner = df[df['AccountName'] == selectbox01]
        # df_owner2 = df_owner.loc[:, ['DateGrabbed', 'DateClosed', 'CaseNumber', 'SIS',
        #                              'CaseOwner', 'Subject']]
        # st.write(df_owner2)

except Exception as e:
    print("Error de la aplicacion: ", e)