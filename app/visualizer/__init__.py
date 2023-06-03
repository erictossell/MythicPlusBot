import asyncio
import datetime
import os
import ssl
import httpx

from matplotlib import colors
from adjustText import adjust_text
from matplotlib import dates
from matplotlib.dates import DateFormatter
import pandas as pd


import app.raiderIO as raiderIO
from discord import File
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



    
    
async def daily_guild_runs_plot(runs: list, discord_guild_id: int):
    
    all_runs_dict = [{'completed_at': run.completed_at, 'score': run.score, 'mythic_level': run.mythic_level, 'short_name': run.short_name} for run in runs]
    df = pd.DataFrame(all_runs_dict)
    plt.close('all')
    plt.ioff()
    plt.figure()
    with plt.rc_context({'axes.facecolor': 'black', 'axes.edgecolor': 'white', 
                     'axes.labelcolor': 'white', 'xtick.color': 'white', 
                     'ytick.color': 'white', 'text.color': 'white', 
                     'lines.color': 'white'}):
        score_colors = None
        retries = 3
        while retries > 0:
            try:
                score_colors = raiderIO.get_score_colors()
                break
            except (httpx.ReadTimeout, ssl.SSLWantReadError):
                await asyncio.sleep(2 ** (3 - retries))
                retries -= 1
                
        colors_list = []
        for color in reversed(score_colors):
            color_value = color.color
            colors_list.append(color_value)
        
        cmap = colors.LinearSegmentedColormap.from_list('mycmap', colors_list)
        
        df['completed_at'] = pd.to_datetime(df['completed_at'])
                

        # Get the time of day of the run completion
        df['time_of_day'] = df['completed_at'].dt.hour
        
        # Calculate the time difference in hours and add 3 hours to account for the time difference between the server and the API
        
        now = datetime.datetime.now()
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
            
        
        
        if os.path.isfile(f'images/{discord_guild_id}_dgr_plot.png'):
            os.remove(f'images/{discord_guild_id}_dgr_plot.png')
        
        plt.savefig(f'images/{discord_guild_id}_dgr_plot.png')
        
        

    return File(f'images/{discord_guild_id}_dgr_plot.png')

async def weekly_guild_runs_plot(runs: list, guild_runs: list, discord_guild_id: int):
    try:
        all_runs_dict = [{'completed_at': run.completed_at, 'score': run.score, 'mythic_level': run.mythic_level, 'short_name': run.short_name} for run in runs]
        df = pd.DataFrame(all_runs_dict)
        
        # Convert the guild_runs list into a DataFrame
        guild_runs_df = pd.DataFrame([{'completed_at': run[0].completed_at} for run in guild_runs])

        # Now use the DataFrame in the isin() function
        df['is_guild_run'] = df['completed_at'].isin(guild_runs_df['completed_at'])

        plt.close('all')
        plt.ioff()
        plt.figure()

        with plt.rc_context({'axes.facecolor': 'black', 'axes.edgecolor': 'white', 
                            'axes.labelcolor': 'white', 'xtick.color': 'white', 
                            'ytick.color': 'white', 'text.color': 'white', 
                            'lines.color': 'white'}):
            
            score_colors = None
            retries = 3
            while retries > 0:
                try:
                    score_colors = raiderIO.get_score_colors()
                    break
                except (httpx.ReadTimeout, ssl.SSLWantReadError):
                    await asyncio.sleep(2 ** (3 - retries))
                    retries -= 1
                    
            colors_list = []
            for color in reversed(score_colors):
                color_value = color.color
                colors_list.append(color_value)
                
            cmap = colors.LinearSegmentedColormap.from_list('mycmap', colors_list)
            
            df['completed_at'] = pd.to_datetime(df['completed_at'])
            df.sort_values('completed_at', inplace=True)
            
            # Get the day of week of the run completion
            df['day_of_week'] = df['completed_at'].dt.day_name()
            
            # Plot the data with color based on 'score'
            plt.scatter(x=df['completed_at'], y=df['mythic_level'], c=df['score'], cmap=cmap)
            

            # Set x-tick labels
            ax = plt.gca()
            ax.xaxis.set_major_locator(dates.DayLocator())
            ax.xaxis.set_major_formatter(dates.DateFormatter('%a'))

            # Label axes
            plt.xlabel('Day of the Week')
            plt.ylabel('Mythic Level')
            plt.title('Weekly Guild Runs')
            plt.style.use('dark_background')      

            plt.colorbar(label='Score') 
            
            annotations = []
            for i, txt in enumerate(df['short_name']):
                if df['is_guild_run'].iat[i]:
                    annotation = plt.annotate(txt, (df['completed_at'].iat[i], df['mythic_level'].iat[i]), fontsize=8, color='white')
                    annotations.append(annotation)
            adjust_text(annotations, expand_points=(1.2, 1.2), expand_text=(1.2, 1.2), force_text=0.5)
                        
            directory = 'images'
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            if os.path.isfile(f'images/{discord_guild_id}_wgr_plot.png'):
                os.remove(f'images/{discord_guild_id}_wgr_plot.png')
            
            plt.savefig(f'images/{discord_guild_id}_wgr_plot.png')
                      
        return File(f'images/{discord_guild_id}_wgr_plot.png')
    except Exception as e:
        print(e)
        return None

def rotate_weekdays(current_day):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    while days_of_week[-1] != current_day:
        days_of_week = days_of_week[1:] + days_of_week[:1]
    return days_of_week



    