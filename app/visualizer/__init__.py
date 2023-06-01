import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import app.db as db



async def weekly_guild_runs_scatter_plot(discord_guild_id: int):
    guild_runs = await db.get_all_weekly_guild_runs(discord_guild_id)
    
    df = pd.DataFrame(guild_runs)
    
    df['completed_at'] = pd.to_datetime(df['completed_at'])
    
    df.plot.scatter(x='completed_at', y='score', title='Weekly Guild Runs')
    
    plt.show()