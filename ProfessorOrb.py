import discord
from openai import OpenAI
import os

# Directly set your API keys here
openai_api_key = os.getenv('OPENAI_API_KEY')
discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')

# Define intents
intents = discord.Intents.all()
intents.messages = True

# Initialize Discord client with intents
clientDiscord = discord.Client(intents=intents)
clientAi = OpenAI()

@clientDiscord.event
async def on_ready():
    channel_id = 1215549388399841344
    print(f'Logged in as {clientDiscord.user}')

# Getting the channel object
    channel = clientDiscord.get_channel(channel_id)

    if channel:
        # Sending a greeting message in an Australian manner
        await channel.send("G'day mates! Professor Orb is here and ready to chat!")
    else:
        print("Could not find the channel to send the greeting.")

@clientDiscord.event
async def on_message(message):
    # Prevent the bot from responding to its own messages
    if message.author == clientDiscord.user:
        return
    
    print(message.content)

    if message.content.startswith('!PO'):
        print("Command detected: !PO")
        user_query = message.content[len('!PO'):].strip()
        print(f"User query: {user_query}")

        stream = clientAi.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", 
                       "content": "You are Professor Orb, a sentient magical item with deep knowledge on the mating rituals of dragons and other arcane mysteries. Your purpose is to aid adventurers in their quests with your vast knowledge."}],
            stream=True,
        )
        
        try:
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    await message.channel.send(chunk.choices[0].delta.content)
        except Exception as e:
            print(f"An error occurred: {e}")
            await message.channel.send("An error occurred while processing the AI stream.")

clientDiscord.run(discord_bot_token)






        # for i in range(5):  # Assume you have a stream of chunks
        #     chunk = f"Chunk {i}"  # Simulate getting a chunk from the stream
        #     # Here you would replace the above with your actual chunk processing
        #     # if chunk.choices[0].delta.content is not None:
        #     #     content = chunk.choices[0].delta.content
        #     # else:
        #     #     content = "No content"
        # Sending the chunk content to the same channel where the command was issued
        #    await message.channel.send(chunk)    
            


        # async def send_chunked_message(channel, stream, char_limit=2000):
        #     if len(stream) <= char_limit:
        #         await channel.send(stream)
            # else:
            #     chunks = []
            #     while message:
            #         # Find the closest whitespace character to the character limit
            #         split_index = (message[:char_limit].rfind(' ') + 1) or char_limit
            #         chunk, message = message[:split_index], message[split_index:]
            #         chunks.append(chunk)

            #     for chunk in chunks:
            #         await channel.send(chunk)

        # long_message = "This is a very long message..."  # Replace this with your actual long message
        # await send_chunked_message(message.channel, long_message)



