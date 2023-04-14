from dotenv import load_dotenv

from langchain.agents import Tool
from langchain.utilities import SearxSearchWrapper
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper

from utils.imagegenerator import generate_image_tool
from utils.summariser.youtube_summariser import summarize_video_transcript, query_youtube_video
from utils.summariser.website_summariser import summarize_website, query_website

load_dotenv()

searx_search = SearxSearchWrapper(searx_host="http://localhost:8080")

class DiscordAgentTools:
    def __init__(self):
        self.zapier = ZapierNLAWrapper()
        self.toolkit = ZapierToolkit.from_zapier_nla_wrapper(self.zapier)

        self.default_tools = [
            "wolfram-alpha",
            "wikipedia",
            "llm-math",
            # "python_repl"
        ]

        self.extra_tools = [
            Tool(
                name="INTERNET_SEARCH_ENGINE",
                func=searx_search.run,
                description="A meta search engine. Useful for when you need to answer questions about things you don't know. Input should be a search query."
            ),
            Tool(
                name="IMAGE_GENERATOR",
                func=generate_image_tool,
                description="A tool to generate images with. Input should be description of what you wish to create."
            ),
            Tool(
                name="YOUTUBE_VIDEO_SUMMARY",
                func=summarize_video_transcript,
                description="A tool to get a summary of a youtube video. Input should be the Video ID after the ?= inside the URL of the video link and NOTHING ELSE."
            ),
            Tool(
                name="YOUTUBE_VIDEO_QUERY",
                func=query_youtube_video,
                description="A tool answer a specific question details about a youtube video. Input should be: [\"natural language query/question\", \"video_id\"]."
            ),
            # Tool(
            #     name="RECOMMENDER",
            #     func=recommender,
            #     description="A tool that returns a list of related topic recommendations based on a message. Input should be natural language"
            # ),
            # Tool(
            #     name="WEBSITE_SUMMARY",
            #     func=summarize_website,
            #     description="A tool to get a summary of an online article. Input should be the website URL and NOTHING ELSE."
            # ),
            # Tool(
            #     name="WEBSITE_QUERY",
            #     func=query_website,
            #     description="A tool answer a specific question details about an online article. Input should be [\"natural language query/question\", \"website_url\"]."
            # ),
            # Tool(
            #     name="LONG_TERM_CHAT_MEMORY",
            #     func=summarize_website,
            #     description="A tool that tells you if you have encountered a question before, and what was the answer you gave."
            # ),
            # Tool(
            #     name="LONG_TERM_MEMORY",
            #     func=summarize_website,
            #     description="A tool that tells you if you have encountered a question before, and what was the answer you gave."
            # ),
        ] + self.toolkit.get_tools()