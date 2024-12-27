import streamlit as st
import pandas as pd
import plotly.express as px
import Elements as el
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Dashboard",    
    page_icon="⚽", 
    layout="wide",
    )

st.markdown(el.tabStyling(), unsafe_allow_html=True)

data = pd.read_csv("data_cleaned.csv")
messi_data = data[data['Player'] == 'LIONEL MESSI']
ronaldo_data = data[data['Player'] == 'CRISTIANO RONALDO']

stats = pd.read_excel("stat.xlsx", sheet_name="Factors Stat")
awards = pd.read_excel("stat.xlsx", sheet_name="Awards")

games_stats = pd.read_excel("stat.xlsx", sheet_name="All Compitition Exclude Country")
games_stats['Year'] = games_stats['Year'].astype(str)
games_stats = games_stats.sort_values(by='Year', ascending=True)

st.title("The Goat: Messi vs Ronaldo")

with st.container():
    st.write("Who is the real GOAT? The competition between Lionel Messi and Cristiano Ronaldo for the title of The Greatest Player of All Time.")
    
col1, col2 = st.columns(2)
with st.container():
    with col1:
        col1_1, col1_2, col1_3= st.columns([1.5, 1, 2])
        with col1_1:
            st.image("./assets/images/messi.png", use_container_width=True)
            
        with col1_2:
            messi_games = games_stats["Messi Games"].sum()
            messi_goals = games_stats["Messi Goals"].sum()
            messi_assists = games_stats["Messi Assists"].sum()
            messi_awards = awards["Messi"].sum()
            st.markdown(
                el.statBox(messi_games, messi_goals, messi_assists, messi_awards), unsafe_allow_html=True
            )
         
        with col1_3:
            st.plotly_chart(el.donutRatingChart(stats, "LIONEL MESSI"), use_container_width=True)
            
    with col2:
        col2_1, col2_2, col2_3 = st.columns([2, 1, 1.5])
        
        with col2_1:
            st.plotly_chart(el.donutRatingChart(stats, "CRISTIANO RONALDO"), use_container_width=True)
            
        with col2_2:
            ronaldo_games = games_stats["Ronaldo Games"].sum()
            ronaldo_goals = games_stats["Ronaldo Goals"].sum()
            ronaldo_assists = games_stats["Ronaldo Assists"].sum()
            ronaldo_awards = awards["Ronaldo"].sum()
            st.markdown(
                el.statBox(ronaldo_games, ronaldo_goals, ronaldo_assists, ronaldo_awards), unsafe_allow_html=True
            )
      
        with col2_3:
            st.image("./assets/images/ronaldo.png", use_container_width=True)

st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
            
with st.container():    
    st.write("Lionel Messi and Cristiano Ronaldo have consistently delivered excellent performances, showing goal scoring ability and playmaking skills")       
    
    tab1, tab2, tab3 = st.tabs(["Goals Over Time", "Goals", "Assists"]) 
    with tab1:
        df = pd.DataFrame(games_stats)
        df_long = pd.melt(df, id_vars=["Year"], value_vars=["Messi Goals", "Ronaldo Goals"])
        df_wide = df_long.pivot(index="Year", columns="variable", values="value")
        df = df_wide.copy()
        df.reset_index(inplace=True)
        
        df['Messi All Goals'] = df['Messi Goals'].cumsum()
        df['Ronaldo All Goals'] = df['Ronaldo Goals'].cumsum()

        timeval = 'Year'
        name1 = 'Messi All Goals'  
        name2 = 'Ronaldo All Goals'  
        
        group1 = df[name1].tolist()
        group2 = df[name2].tolist()

        fig = go.Figure()
        trace1 = go.Scatter(
            x=df[timeval],
            y=group1,
            mode='lines',
            line=dict(width=3, color='#2E5077'),
            name=name1
        )

        trace2 = go.Scatter(
            x=df[timeval],
            y=group2,
            mode='lines',
            line=dict(width=3, color='#4DA1A9'),
            name=name2
        )

        len_frames = len(group1)
        frames = [dict(
            data=[
                dict(type='scatter', x=df[timeval][:k+1], y=group1[:k+1]),
                dict(type='scatter', x=df[timeval][:k+1], y=group2[:k+1])
            ],
            traces=[0, 1]
        ) for k in range(1, len_frames)]

        layout = go.Layout(
            height=500,
            showlegend=True,
            hovermode='closest',
            updatemenus=[dict(
                type='buttons',
                showactive=False,
                y=-0.05,
                x=1.15,
                xanchor='left',
                yanchor='top',
                pad=dict(t=0, r=10),
                buttons=[dict(
                    label='Play Animation',
                    method='animate',
                    args=[None,
                        dict(frame=dict(duration=200, redraw=True), transition=dict(duration=0), mode='immediate')]
                )]
            ),],
            xaxis=dict(
                title="Year", 
                type='category',  
                tickvals=df[timeval],  
                ticktext=df[timeval].apply(lambda x: str(x)),
                tickangle=45,
                autorange=True  
            ),
            yaxis=dict(
                title="Games Played", 
                zeroline=False
            ),
            title="Goals Over Time",
            margin=dict(l=0, r=0, t=50, b=0)
        )

        fig = go.Figure(data=[trace1, trace2], frames=frames, layout=layout)    
        st.plotly_chart(fig, use_container_width=True)
            
    with tab2:
        df = pd.DataFrame(games_stats)
        df_long = pd.melt(df, id_vars=["Year"], value_vars=["Messi Goals", "Ronaldo Goals", "Messi Games", "Ronaldo Games"])
        df_wide = df_long.pivot(index="Year", columns="variable", values="value")
        df = df_wide.copy()
        df.reset_index(inplace=True)

        timeval = 'Year'
        name1_goals = 'Messi Goals'  
        name2_goals = 'Ronaldo Goals'
        name1_games = 'Messi Games'
        name2_games = 'Ronaldo Games'

        group1_goals = df[name1_goals].tolist()
        group2_goals = df[name2_goals].tolist()
        group1_games = df[name1_games].tolist()
        group2_games = df[name2_games].tolist()
        

        fig = go.Figure()
        trace1_goals = go.Scatter(
            x=df[timeval],
            y=group1_goals,
            mode='lines',
            line=dict(width=4, color='#2E5077', dash='solid'),
            name=name1_goals,
            hovertemplate='%{y} goals in %{x} season<br><extra></extra>',
        )
        

        trace2_goals = go.Scatter(
            x=df[timeval],
            y=group2_goals,
            mode='lines',
            line=dict(width=4, color='#73c9d1', dash='solid'),
            name=name2_goals,
            hovertemplate='%{y} goals in %{x} season<br><extra></extra>',
        )

        trace1_games = go.Bar(
            x=df[timeval],
            y=group1_games,
            name=name1_games,
            marker=dict(color='#78a0cf'),  
            hovertemplate='%{y} games in %{x} season<br><extra></extra>',
        )

        trace2_games = go.Bar(
            x=df[timeval],
            y=group2_games,
            name=name2_games,
            marker=dict(color='#74c7cf'),  
            hovertemplate='%{y} games in %{x} season<br><extra></extra>',
        )

        fig.add_trace(trace1_goals)
        fig.add_trace(trace2_goals)
        fig.add_trace(trace1_games)
        fig.add_trace(trace2_games)

        layout = go.Layout(
            height=500,
            width=800,
            barmode='group',  
            showlegend=True,
            hovermode='closest',
            margin=dict(l=0, r=0, t=0, b=0),
            autosize=True,
            
        )
        st.write("**Goals and Games**")
        st.plotly_chart(fig, use_container_width=True)
            
    with tab3:
        fig = px.bar(
        games_stats, 
            x='Year', 
            y=['Messi Assists', 'Ronaldo Assists'],  
            title="Messi and Ronaldo Season Assists", 
            text_auto='.2s', 
            color_discrete_map={
                "Messi Assists": "#2E5077",  
                "Ronaldo Assists": "#4DA1A9" 
            }
            )
        fig.update_layout(
            showlegend=True,
            margin=dict(t=50, b=0, l=0, r=0),)
        st.plotly_chart(fig)
        
    st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)


with st.container():
    goal_counts = data.groupby(['Player', 'Type']).size().reset_index(name='Goal_Count')
    top_5_messi = goal_counts[goal_counts['Player'] == 'LIONEL MESSI'].nlargest(5, 'Goal_Count')
    top_5_ronaldo = goal_counts[goal_counts['Player'] == 'CRISTIANO RONALDO'].nlargest(5, 'Goal_Count')

    st.title("Top 5 Goals of Messi and Ronaldo by Category")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=top_5_messi['Goal_Count'],
        x=top_5_messi['Type'],
        mode='markers+lines',
        marker=dict(color='#2E5077', size=10),
        line=dict(width=2, color='#2E5077'),
        name='Messi',
        hovertemplate="Goals: %{y}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        y=top_5_ronaldo['Goal_Count'],
        x=top_5_ronaldo['Type'],
        mode='markers+lines',
        marker=dict(color='#4DA1A9', size=10),
        line=dict(width=2, color='#4DA1A9'),
        name='Ronaldo',
        hovertemplate="Goals: %{y}<extra></extra>"
    ))

    fig.update_layout(
        xaxis_title="Goal Count",
        yaxis_title="Shot Type",
        template="plotly_white",
        showlegend=True,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=False)
    )

    st.plotly_chart(fig)
    
with st.container():
    competitions = [
        "UEFA SUPER CUP", "UEFA CHAMPIONS LEAGUE", "SUPERCOPA", 
        "LALIGA", "FIFA CLUB WORLD CUP", "COPA DEL REY"
    ]

    df_messi_filtered = messi_data[messi_data['Competition'].isin(competitions)]
    df_ronaldo_filtered = ronaldo_data[ronaldo_data['Competition'].isin(competitions)]

    messi_goals_per_competition = df_messi_filtered.groupby('Competition').size().reset_index(name='Messi_Goals')
    ronaldo_goals_per_competition = df_ronaldo_filtered.groupby('Competition').size().reset_index(name='Ronaldo_Goals')

    final_stats = pd.merge(messi_goals_per_competition, ronaldo_goals_per_competition, on='Competition', how='outer').fillna(0)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=final_stats['Competition'],
        x=final_stats['Messi_Goals'],
        name='Messi Goals',
        orientation='h',
        marker=dict(color='#2E5077'),
        hovertemplate="Messi Goals: %{x}<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        y=final_stats['Competition'],
        x=-final_stats['Ronaldo_Goals'],
        name='Ronaldo Goals',
        orientation='h',
        marker=dict(color='#4DA1A9'),
        hovertemplate="Messi Goals: %{x}<extra></extra>"
    ))

    fig.update_layout(
        xaxis=dict(
            tickvals=[-500, -400, -300, -200, -100, 0, 100, 200, 300, 400, 500],
            ticktext=["500", "400", "300", "200", "100", "0", "100", "200", "300", "400", "500"],
        ),
        yaxis=dict(title="Competition"),
        barmode="overlay",
        template="plotly_white",
        legend=dict(title="Legend"),
    )

    st.title("Messi vs Ronaldo - Goals in Competitions")
    st.plotly_chart(fig, use_container_width=True)


    

