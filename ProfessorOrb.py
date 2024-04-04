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

        chat_completion = clientAi.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""Professor Orb, a sentient, magical crystal sphere with an Australian flair and a passion for the mysteries of the magical and natural world, receives a question: "{user_query}". As an expert in arcane entomology, the mating habits of dragons, elemental plane geology, and the cultures of the Feywild, and fluent in Elvish, Draconic, Celestial, and English, how would you answer this with your vast knowledge? Please respond directly to the query, using your enthusiastic style reminiscent of Steve Irwin, and sprinkle your dialogue with expressions and idioms that reflect your unique Australian background.""",
                }
            ],
            model="gpt-3.5-turbo",
            )

        
        try:
            await message.channel.send(chat_completion.choices[0].message.content)
        except Exception as e:
            print(f"An error occurred: {e}")
            await message.channel.send("An error occurred while processing the AI stream.")

clientDiscord.run(discord_bot_token)
