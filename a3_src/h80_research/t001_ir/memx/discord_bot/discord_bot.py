import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv
import tempfile
from gtts import gTTS
import whisper

from utils.utils import extract_file_path
from agents.agent import MemxAgent

load_dotenv()
discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')

model = whisper.load_model("small")
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
agent = MemxAgent("discord-agent")


def tts_play(ctx, arg):
    # Generate the audio file from the text
    tts = gTTS(text=arg, lang='en', slow=False)
    tts.save("tts_audio.mp3")

    # Open the audio file and write its contents to a temporary file
    with open("tts_audio.mp3", "rb") as f:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as audio:
            audio.write(f.read())
            audio.flush()
            audio.seek(0)

            # Play the audio in the voice channel
            prepared_audio = discord.FFmpegOpusAudio(
                audio.name, executable="ffmpeg")
            ctx.guild.voice_client.play(prepared_audio, after=None)

    # Remove the temporary audio file
    os.remove("tts_audio.mp3")


async def reply_to_user(ctx, reply):
    path_type, file_path = extract_file_path(reply)

    if path_type is None:
        await ctx.send(reply)
    elif path_type == "url":
        await ctx.send(reply)
    elif path_type == "file":
        await ctx.send(file=discord.File("./"+file_path))
    elif ctx.author.voice:
        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()
        tts_play(ctx, reply)
    else:
        await ctx.send(reply)


async def callback(sink: discord.sinks, ctx):
    for user_id, audio in sink.audio_data.items():
        if user_id == ctx.author.id:
            audio: discord.sinks.core.AudioData = audio
            print(user_id)
            filename = "audio.wav"
            with open(filename, "wb") as f:
                f.write(audio.file.getvalue())
            text = model.transcribe(filename)["text"]
            os.remove(filename)
            print(f"Received from {ctx.author.name}: {text}")
            reply = agent.get_response(text)
            print(f"Reply: {reply}")
            await reply_to_user(ctx, reply)


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))

@client.event
async def on_reaction_add(reaction, user):
    print(reaction.emoji)
    if reaction.emoji != "🔍":
        return
    message = reaction.message
    await message.reply("Generating related topics to think about. Please wait...")
    prompt = f"The following is an output from an advanced conversation recomendation algorithm. \n \
    The algorithm always returns related, interesting, unique conversation topic ideas, based on some input message from a user. \n \n \
    User message: \"I'm studying psychology and I'm interested in learning more about cognitive development\" \n \
    Algorithm Final Answer: \"['Jean Piaget's theory of cognitive development', 'Lev Vygotsky's sociocultural theory', 'The role of genetics and environment in cognitive development', 'Cognitive development in infants and children', 'Cognitive development in adulthood']\" \n \
    User message: \"I'm curious about the meaning of life\" \n \
    Algorithm Final Answer: \"['Existentialism and the meaning of life', 'Eastern philosophy and the meaning of life', 'The relationship between happiness and the meaning of life', 'The role of spirituality in finding meaning', 'The search for purpose and fulfillment']\"\\n \
    User message: \"I'm bored and looking for something fun to do\"\n \
    Algorithm Final Answer: \"['Board game night with friends', 'Trying a new restaurant or cuisine', 'Outdoor activities like hiking or kayaking', 'Visiting a local museum or art exhibit', 'Attending a live music or comedy show']\"\n \
    User message: \"I'm interested in improving my leadership skills\"\n \
    Algorithm Final Answer: \"['Leadership development programs and courses', 'Books and articles on effective leadership', 'Mentorship and coaching opportunities', 'The importance of emotional intelligence in leadership', 'Leading through change and uncertainty']\"\n \
    User message: \"I want to learn more about environmental policy\"\n \
    Algorithm Final Answer: \"['Environmental regulations and laws', 'International climate agreements and policies', 'The role of government in environmental protection', 'The impact of climate change on communities and ecosystems', 'Sustainable development and renewable energy solutions']\"\n \n \
        your output should look like: \n \
            \"action\": \"Final Answer\", \
            \"action_input\":  \"['Example related topic 0', 'Example related topic 1', 'Example related topic 21', 'Example related topic 3'...]\" \n \n \
    Only return up to 10 related topics. \n \
    User message: \"{message.content}\" \n \
    Please provide the algorithm output encased in a string. \
    "
    # 
    # Return the recommendations as a list with emoji indices \n \":zero:\" \n \":one:\" \n \":two:\" \n etc.
    response = agent.get_response(prompt)

    lst_str = response[1:-1].split(',')
    lst = [s.strip()[1:-1] for s in lst_str][:10]
    
    tags = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    lst = [f"{tags[i]} {s}" for i, s in enumerate(lst)]
    lst = '\n'.join(lst)
    print(lst)
    reply = await message.reply('\n' + lst)
    for i in range(len(lst)):
        await reply.add_reaction(tags[i])


@client.command(name="join", category="Voice")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("not in a voice channel!")
join.help = "Connects the bot to the voice channel you are currently in."


@client.command(name="leave", category="Voice")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("not in a voice channel!")
leave.help = "Disconnects the bot from the voice channel it is currently in."


@client.command(name="shut_up", category="Voice")
async def shut_up(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Playback stopped.")
    else:
        await ctx.send("I am not currently playing any audio.")
shut_up.help = "Stops the bot from speaking in the voice channel."


@client.command(name="listen", category="Voice")
async def listen(ctx):
    if ctx.voice_client:
        ctx.voice_client.start_recording(
            discord.sinks.WaveSink(), callback, ctx)
        await ctx.send("listening...")
    else:
        await ctx.send("not in a voice channel!")
listen.help = "Starts recording audio from the voice channel the bot is currently in."


@client.command(name="stop", category="Voice")
async def stop(ctx):
    ctx.voice_client.stop_recording()
stop.help = "Stops the recording of audio from the voice channel the bot is currently in."


@client.command(name="summarize", category="General")
async def summarize(ctx):
    await reply_to_user(ctx, "I am summarizing the conversation in this channel. This may take some time, please be patient.")
    n = int(ctx.message.content.replace('!summarize', '').strip())
    messages = []
    async for msg in ctx.channel.history(limit=n):
        messages.append(msg)
    messages_text = '\n'.join([msg.content for msg in messages].reverse())
    print(messages_text)
    prompt = f"Summarize the following messages. Provide a summary of each participant's views separately, and highlight any key points of agreement or disagreement. Messages: {messages_text}"
    response = agent.get_response(prompt)
    await reply_to_user(ctx, response)
summarize.help = "Summarizes the given text into a shorter, more concise version."


@client.command(name="related", category="General")
async def related(ctx):
    await reply_to_user(ctx, "Generating related topics to think about. Please wait...")
    n = int(ctx.message.content.replace('!related', '').strip())
    messages = []
    async for msg in ctx.channel.history(limit=n):
        messages.append(msg.content)
    message_str = '\n'.join(messages.reverse())
    prompt = f"Provide related topics to think about based on the following messages: {message_str}"
    response = agent.get_response(prompt)
    await reply_to_user(ctx, response)
related.help = "Searches the web for related topics based on the given query."


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        await client.process_commands(message)
    elif client.user.mentioned_in(message):
        ctx = await client.get_context(message)
        await reply_to_user(ctx, "Got it! Let me process your message...")
        prompt = f'{message.content}'.format(message.content)
        response = agent.get_response(prompt)
        await reply_to_user(ctx, response)


client.run(discord_bot_token)
