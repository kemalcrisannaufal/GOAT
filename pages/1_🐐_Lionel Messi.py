import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import Elements as el

st.set_page_config(
    page_title="Lionel Messi",    
    page_icon="🐐", 
    layout="wide",
)

st.markdown(el.tabStyling(), unsafe_allow_html=True)

data = pd.read_csv("data_cleaned.csv")
messi_data = data[data['Player'].str.contains('Messi', case=False, na=False)]

st.title("Lionel Messi")

col1, col2, col3 = st.columns([1, 2, 2])

with st.container():
    with col1:
        st.image("./assets/images/messi.png", width=200)
    with col2:
        st.write("")  
        st.write("")
        st.write("") 
        st.write("""
                **Full Name:** Lionel Andrés Messi  
                **Born:** June 24, 1987  
                **Current Club:** Inter Miami CF  
                **National Team:** Argentina**
                """
        )
    with col3:
        position_count = messi_data['Playing_Position'].value_counts().reset_index()
        fig = px.treemap(   
            position_count,
            path=["Playing_Position"],  
            color="Playing_Position",
            values="count",
            color_discrete_map={                
                "RW": "#2E5077",
                "LW": "#edebeb",
                "CF": "#4DA1A9",
                "SS": "#79D7BE",
                "AM": "#F6F4F0",
            }  
        )
        
        fig.update_traces(
            hovertemplate="Goal by Position: %{value}<extra></extra>",   
        )
        
        fig.update_layout(
            margin=dict(t=0, l=0, r=0, b=0),
            height=300,
        )

        st.plotly_chart(fig, use_container_width=True)

st.markdown("""
            <div style="text-align: justify;">
            Lionel Messi is one of the greatest football players of all time. He has won eight Ballon d'Or awards and six European Golden Shoes. Messi has also earned two Copa America titles and one FIFA World Cup with Argentina, adding to his reputation as one of the most decorated players in the history of football.<br><br>

            **Club Career:**
            Messi spent the majority of his career at Barcelona, where he won 34 trophies, including ten La Liga titles and four UEFA Champions League trophies. He is the all-time top scorer for Barcelona and La Liga, with 474 goals in Spain’s top division. In 2021, Messi move to Paris Saint-Germain (PSG) before later joining Inter Miami CF.  

            **Achievements:**
            - Eight Ballon d'Or awards  
            - Six European Golden Shoes  
            - 2022 FIFA World Cup Champion  
            - Most goals (474), hatricks (36) and assists (192) in La Liga
            - Most goals ever by a player for a single club  
            </div>
            """, unsafe_allow_html=True)

with st.container():
        messi_data['Minute'] = messi_data['Minute'].str.extract(r'(\d+)').astype(float)
        messi_minute_counts = messi_data['Minute'].value_counts().sort_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=messi_minute_counts.index,
            y=[1] * len(messi_minute_counts),  
            mode='markers',
            name='Messi',
            marker=dict(
                size=messi_minute_counts.values * 4, 
                color='#2E5077',
                sizemode='area'
            ),
            customdata=messi_minute_counts.values,
            hovertemplate="Minute: %{x}<br>Goals: %{customdata}<extra></extra>",
        ))
        
        fig.update_layout(
            title="Goal by Minute",
            xaxis=dict(title="Match Minute", range=[0, 92]),
            yaxis=dict(
                range=[-0.5, 1.5],
                tickmode='array',
                tickvals=[1],
                ticktext=['Goals']
            ),
            showlegend=False,
            height=250,
        )

        st.plotly_chart(fig, use_container_width=True)           

col1, col2 = st.columns(2)
with col1:
    messi = messi_data.copy()
    messi['Type'] = messi['Type'].apply(lambda x:'PENALTY' if x == 'PENALTY' else 'NO PENALTY')
    messi = messi.groupby(['Competition', 'Type']).size().reset_index(name='Goals')
    competition = ["UEFA CHAMPIONS LEAGUE", "LALIGA", "COPA DEL REY", 'LIGUE 1']
    colors = ["#ffffff", "#4DA1A9", "#2E5077", "#79D7BE", "#89A8B2"]
    labels = [
        "Total Goals", 
        "UEFA CHAMPIONS LEAGUE", 
        "LALIGA", 
        "COPA DEL REY", 
        "LIGUE 1", 
        "PENALTY", 
        "NO PENALTY", 
        "PENALTY ", 
        "NO PENALTY ", 
        "PENALTY  ", 
        "NO PENALTY  ", 
        "PENALTY   ", 
        "NO PENALTY   "
    ]

    parents = ["", "Total Goals", "Total Goals", "Total Goals", "Total Goals", "UEFA CHAMPIONS LEAGUE", "UEFA CHAMPIONS LEAGUE", "LALIGA", "LALIGA", "COPA DEL REY", "COPA DEL REY", "LIGUE 1", "LIGUE 1"]
    total_goals = 0
    values = [total_goals]
    
    for el in competition:
        goals = messi.loc[messi['Competition'] == el, 'Goals'].values.sum()
        values.append(goals)
        total_goals += goals

    values[0] = total_goals
    type = ["PENALTY", "NO PENALTY"]    
    for c in competition:
        for t in type: 
            values.append(messi.loc[(messi['Competition'] == c) & (messi['Type'] == t), 'Goals'].sum())
    

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total", 
        marker=dict(colors=colors)
    ))
    
    fig.update_traces(
        hovertemplate="Goals: %{value}<extra></extra>",
    )

    fig.update_layout(
        margin=dict(t=40, l=0, r=0, b=0),
        height=350
    )
    st.write("**Goals Messi in Top 4 Competitions**")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    messi_data = messi_data.dropna(subset=['Minute'])
    bins = [0, 15, 30, 45, 60, 75, 91]
    labels = ['1-15', '16-30', '31-45', '46-60', '61-75', '76-90']
    
    colors = ["#2E5077" for _ in range(len(labels))]
    messi_data['Minute_Range'] = pd.cut(messi_data['Minute'], bins=bins, labels=labels, right=False)
    minute_distribution = messi_data.groupby('Minute_Range').size().reset_index(name='Goals')

    st.write("**Messi Goals Timing Distribution**")
    fig = px.bar(   
        minute_distribution,
        x='Minute_Range',
        y='Goals',
        labels={'Minute_Range': 'Minute Range', 'Goals': 'Number of Goals'},
        hover_data=['Goals'],
        text='Goals',
        color='Minute_Range',
        color_discrete_map=dict(zip(labels, colors)),
    )

    fig.update_layout(
        xaxis_title="Minute Range",
        yaxis_title="Number of Goals",
        title_x=1.0,
        title_font=dict(size=20),
        margin=dict(t=20, b=0, l=0, r=0),
        height=350
    )

    st.plotly_chart(fig)

st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
with st.container():
    tab1, tab2 = st.tabs(["Type of Goals", "Goals by Competition"])
    
    with tab1:
        goal_counts = messi_data.groupby(['Type']).size().reset_index(name='Goals')
        goal_counts.sort_values(by='Goals', ascending=False, inplace=True)
        fig = go.Figure(go.Scatter(
            x=goal_counts['Type'],
            y=goal_counts['Goals'],
            line=dict(width=2, color='#2E5077'),
            marker=dict(color='#2E5077', size=10),
        ))
        
        fig.update_layout(
            title="Messi Shot Type",
            xaxis_title="Shot Type",
            yaxis_title="Number of Goals",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            margin=dict(t=30, l=0, b=0, r=0)
        )
        
        st.plotly_chart(fig)
    with tab2:
        competition_data = messi_data.groupby(['Competition']).size().reset_index(name='Goals')
        competition_data.sort_values(by='Goals', ascending=False, inplace=True)
    
        colors = ["#2E5077" for _ in range(len(competition_data["Competition"]))]
        fig = px.bar(
            competition_data, 
            x=competition_data["Competition"],
            y=competition_data["Goals"],
            color="Competition",
            color_discrete_map=dict(zip(competition_data["Competition"], colors)),
        )
        
        fig.update_layout(
            title="Goals by Competition",
            showlegend=False
        )
        
        st.plotly_chart(fig)
    