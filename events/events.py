#@tasks.loop(minutes=1)
#async def create_events():
    #now = datetime.utcnow()
    #if now.weekday() in event_days and now.hour == event_time.hour and now.minute == event_time.minute:
        #channel = bot.get_channel(raid_lobby_id)
        #event = await channel.create_event(name="Raid Night", start=event_time + timedelta(hours=1),end=event +timedelta(hours=2),description="Raid Night! 7:30pm EST")
        #bot_bunker = bot.get_channel(bot_bunker_id)
        #await bot_bunker.send(event_message)

async def event_exists(name):
    channel = bot.get_channel(bot_bunker_id)
    async for message in channel.history():
        if message.author == bot.user and message.content ==name:
            return True
    return False

async def create_event(name, start, end, description):   
    raid_channel = bot.get_channel(raid_lobby_id)
    event = await raid_channel.create_event(name=name, start=start, end=end, description=description)
    return event

async def check_and_create_events():
    for name in event_name:
        if not await event_exists(name):
            time = f'{event_days} {event_start}'
            await create_event(name, time)