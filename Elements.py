import streamlit as st
import plotly.graph_objects as go

def tabStyling():
    return """
        <style>
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
            }

            .stTabs [data-baseweb="tab"] {
                height: 30px;
                width: 100%;
                white-space: pre-wrap;
                background-color: #F0F2F6;
                border-radius: 4px 4px 0px 0px;
                gap: 1px;
                padding-top: 10px;
                padding-bottom: 10px;
            }

            .stTabs [aria-selected="true"] {
                background-color: #FFFFFF;
            }
        </style> """
            


def statBox(games, goals, assists, awards):
    return f"""
                <div style="width: 130px; height: 72px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding-top: 20px; padding-bottom: 20px; color: #404040;">
                    <p style="font-size: 18px; margin: 0; padding: 0; font-weight: semibold;">Games</p>
                    <p style="font-size: 20px; margin: 0; padding: 0; font-weight: bold;">{games}</p>
                </div>
                <div style="width: 130px; height: 72px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding-top: 20px; padding-bottom: 20px; color: #404040;">
                    <p style="font-size: 18px; margin: 0; padding: 0; font-weight: 600;">Goals</p>
                    <p style="font-size: 20px; margin: 0; padding: 0; font-weight: 700;">{goals}</p>
                </div>
                <div style="width: 130px; height: 72px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding-top: 20px; padding-bottom: 20px; color: #404040;">
                    <p style="font-size: 18px; margin: 0; padding: 0; font-weight: semibold;">Assists</p>
                    <p style="font-size: 20px; margin: 0; padding: 0; font-weight: bold;">{assists}</p>
                </div>

                <div style="width: 130px; height: 72px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding-top: 20px; padding-bottom: 20px; color: #404040;">
                    <p style="font-size: 18px; margin: 0; padding: 0; font-weight: semibold;">Awards</p>
                    <p style="font-size: 20px; margin: 0; padding: 0; font-weight: bold;">{awards}</p>
                </div>
            """

def donutRatingChart(stats, player):
    if player == "LIONEL MESSI":
        idx_player = 1
    else:
        idx_player = 2
    max_rating = 10
    player_ratings = stats[stats["Factors"] == "Average match Rating"].values[0][idx_player]
    percentage_player_ratings = (player_ratings / max_rating) * 100
    player_values = [percentage_player_ratings / 10, (100 - percentage_player_ratings) / 10]
    colors = ['#2E5077', '#4DA1A9']
            
    fig = go.Figure(data=[go.Pie(labels=["Rating", "Rating to 10"], 
                                         values=player_values, 
                                         hole=.6, 
                                         textinfo='none', 
                                         hoverinfo='label+value')])
    
    fig.update_traces(marker=dict(colors=colors))
    fig.update_layout(
                title_text="Average Match Ratings",
                title_x=0.1,
                showlegend=False,
                margin=dict(t=50, b=0, l=0, r=0),
                height=270,
                annotations=[dict(text=f"{player_ratings}", font_size=30, showarrow=False, xanchor="center")],     
            ),
    return fig
