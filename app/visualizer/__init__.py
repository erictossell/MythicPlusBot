from datetime import datetime

import os

from matplotlib import colors
from adjustText import adjust_text
import pandas as pd

import app.db as db
import app.raiderIO as raiderIO
from discord import File
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



async def weekly_guild_runs_scatter_plot(discord_guild_id: int):
    guild_runs = await db.get_all_weekly_guild_runs(discord_guild_id)
    
    df = pd.DataFrame(guild_runs)
    
    df['completed_at'] = pd.to_datetime(df['completed_at'])
    
    plt.plot(x=df['completed_at'],y= df['score'])
    
    plt.show()
    
    
async def daily_guild_runs_plot(df: pd.DataFrame, discord_guild_id: int):
    plt.close('all')
    plt.ioff()
    plt.figure()
    with plt.rc_context({'axes.facecolor': 'black', 'axes.edgecolor': 'white', 
                     'axes.labelcolor': 'white', 'xtick.color': 'white', 
                     'ytick.color': 'white', 'text.color': 'white', 
                     'lines.color': 'white'}):
        score_colors = raiderIO.get_score_colors()
        colors_list = []
        for color in reversed(score_colors):
            color_value = color.color
            colors_list.append(color_value)
        
        cmap = colors.LinearSegmentedColormap.from_list('mycmap', colors_list)
        
        df['completed_at'] = pd.to_datetime(df['completed_at'])
                

        # Get the time of day of the run completion
        df['time_of_day'] = df['completed_at'].dt.hour
        
        # Calculate the time difference in hours and add 3 hours to account for the time difference between the server and the API
        df['completed_at'] = df['completed_at'] + pd.Timedelta(hours=-3)
        now = datetime.now()
        df['hours_passed'] = (now - df['completed_at']).dt.total_seconds() / 3600
         

        # Plot the data with color based on 'score'
        plt.scatter(x=df['hours_passed'], y=df['mythic_level'], c=df['score'], cmap=cmap)
        
        annotations = []
        for i, txt in enumerate(df['short_name']):
            
            annotation = plt.annotate(txt, (df['hours_passed'].iat[i], df['mythic_level'].iat[i]), fontsize=8, color='white')
            
            annotations.append(annotation)

        adjust_text(annotations, expand_points=(1.2, 1.2), expand_text=(1.2, 1.2), force_text=0.5)
           

        # Label axes
        plt.xlabel('Hours Since Completion')
        plt.ylabel('Mythic Level')
        plt.title('Daily Guild Runs')
        plt.style.use('dark_background')      

        plt.colorbar(label='Score') 
        
        directory = 'images'
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        date = datetime.now().strftime("%Y-%m-%d")
        
        if os.path.isfile(f'images/{date}_{discord_guild_id}_dgr_plot.png'):
            os.remove(f'images/{date}_{discord_guild_id}_dgr_plot.png')
        
        plt.savefig(f'images/{date}_{discord_guild_id}_dgr_plot.png')
        
        

    return File(f'images/{date}_{discord_guild_id}_dgr_plot.png')
    