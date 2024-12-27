import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go
import Elements as el

st.set_page_config(
    page_title="Cristiano Ronaldo",    
    page_icon="👑", 
    layout="wide",
)

st.markdown(el.tabStyling(), unsafe_allow_html=True)

data = pd.read_csv("data_cleaned.csv")
ronaldo_data = data[data['Player'] == "CRISTIANO RONALDO"]

st.title("Cristiano Ronaldo")

col1, col2, col3 = st.columns([1, 2, 2])

with st.container():
    with col1:
        st.image("./assets/images/ronaldo.png", use_container_width=True)
    with col2:
        st.write("")  
        st.write("")
        st.write("") 
        st.write("""
                **Full Name:** Cristiano Ronaldo dos Santos Aveiro
                **Born:** February 5, 1985   
                **Current Club:** Al-Nassr FC  
                **National Team:** Portugal
                """
        )
    with col3:
        position_count = ronaldo_data['Playing_Position'].value_counts()
        position_count_df = position_count.reset_index()
        position_count_df.columns = ['Position', 'Count']
        fig = px.treemap(
            position_count_df,
            path=["Position"],  
            color="Position",
            values="Count",
            color_discrete_map={
                "LW": "#2E5077",
                "CF": "#4DA1A9",
                "RW": "#79D7BE",
                "OTHER": "#F6F4F0",
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
            Cristiano Ronaldo is one of the greatest football players of all time. He has won five Ballon d'Or awards and four European Golden Shoes. Ronaldo has won 35 major trophies in his career, including seven league titles, five UEFA Champions League titles, one UEFA European Championship, and one UEFA Nations League title. He holds multiple records, including the most goals (140) and assists (42) in the UEFA Champions League, the most goals in the UEFA European Championship (14), and the most international goals by a male player (123). He is also one of the few players to have made over 1,100 career appearances, scoring over 891 official goals for both club and country.
            <br><br>

            **Club Career:**
            Ronaldo began his senior club career at Sporting CP before moving to Manchester United in 2003. He won several titles at Manchester United, including the Premier League, Champions League, and FIFA Club World Cup. In 2009, he transferred to Real Madrid for a then-world record €94 million, where he became the club's all-time top scorer and won numerous trophies, including four Champions League titles. After his time at Real Madrid, Ronaldo moved to Juventus in 2018, where he won two Serie A titles. He returned to Manchester United in 2021 before joining Al-Nassr FC.
            <br><br>

            **Achievements:**
            - Five Ballon d'Or awards
            - Four European Golden Shoes
            - Five UEFA Champions League Titles
            - Most appearances (183), goals (140) and assists (42) in the Champions League
            - First footballer in history to earn $1 billion in career earnings
            </div>
            """, unsafe_allow_html=True)

with st.container():
        ronaldo_data['Minute'] = ronaldo_data['Minute'].str.extract(r'(\d+)').astype(float)
        ronaldo_minute_counts = ronaldo_data['Minute'].value_counts().sort_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ronaldo_minute_counts.index,
            y=[1] * len(ronaldo_minute_counts),  
            mode='markers',
            name='ronaldo',
            marker=dict(
                size=ronaldo_minute_counts.values * 4, 
                color='#2E5077',
                sizemode='area'
            ),
            customdata=ronaldo_minute_counts.values,
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
    ronaldo = ronaldo_data.copy()
    ronaldo['Type'] = ronaldo['Type'].apply(lambda x:'PENALTY' if x == 'PENALTY' else 'NO PENALTY')
    ronaldo = ronaldo.groupby(['Competition', 'Type']).size().reset_index(name='Goals')
    competition = ["UEFA CHAMPIONS LEAGUE", "LALIGA", "PREMIER LEAGUE", 'SERIE A']
    colors = ["#ffffff", "#4DA1A9", "#2E5077", "#79D7BE", "#89A8B2"]
    labels = [
        "Total Goals", 
        "UEFA CHAMPIONS LEAGUE", 
        "LALIGA", 
        "PREMIER LEAGUE", 
        "SERIE A", 
        "PENALTY", 
        "NO PENALTY", 
        "PENALTY ", 
        "NO PENALTY ", 
        "PENALTY  ", 
        "NO PENALTY  ", 
        "PENALTY   ", 
        "NO PENALTY   "
    ]

    parents = ["", "Total Goals", "Total Goals", "Total Goals", "Total Goals", "UEFA CHAMPIONS LEAGUE", "UEFA CHAMPIONS LEAGUE", "LALIGA", "LALIGA", "PREMIER LEAGUE", "PREMIER LEAGUE", "SERIE A", "SERIE A"]
    total_goals = 0
    values = [total_goals]
    
    for el in competition:
        goals = ronaldo.loc[ronaldo['Competition'] == el, 'Goals'].values.sum()
        values.append(goals)
        total_goals += goals

    values[0] = total_goals
    type = ["PENALTY", "NO PENALTY"]    
    for c in competition:
        for t in type: 
            values.append(ronaldo.loc[(ronaldo['Competition'] == c) & (ronaldo['Type'] == t), 'Goals'].sum())
    

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
    st.write("**Goals ronaldo in Top 4 Competitions**")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    ronaldo_data = ronaldo_data.dropna(subset=['Minute'])
    bins = [0, 15, 30, 45, 60, 75, 91]
    labels = ['1-15', '16-30', '31-45', '46-60', '61-75', '76-90']
    
    colors = ["#2E5077" for _ in range(len(labels))]
    ronaldo_data['Minute_Range'] = pd.cut(ronaldo_data['Minute'], bins=bins, labels=labels, right=False)
    minute_distribution = ronaldo_data.groupby('Minute_Range').size().reset_index(name='Goals')

    st.write("**ronaldo Goals Timing Distribution**")
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
        goal_counts = ronaldo_data.groupby(['Type']).size().reset_index(name='Goals')
        goal_counts.sort_values(by='Goals', ascending=False, inplace=True)
        fig = go.Figure(go.Scatter(
            x=goal_counts['Type'],
            y=goal_counts['Goals'],
            line=dict(width=2, color='#2E5077'),
            marker=dict(color='#2E5077', size=10),
        ))
        
        fig.update_layout(
            title="Ronaldo Shot Type",
            xaxis_title="Shot Type",
            yaxis_title="Number of Goals",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            margin=dict(t=30, l=0, b=0, r=0)
        )
        
        st.plotly_chart(fig)
    with tab2:
        competition_data = ronaldo_data.groupby(['Competition']).size().reset_index(name='Goals')
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
    