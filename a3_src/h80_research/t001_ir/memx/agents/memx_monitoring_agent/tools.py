# def monitoring_tool(input):
#     return "MONITORING_ALARM_AKNOWLEDGED"

# extra_tools = [
#     Tool(
#         name="MEMX_RAISE_MONITORING_ALARM",
#         func=monitoring_tool,
#         description="A function to raise a monitoring alarm when you have a positive detection. Use it when you need to raise a MONITORING_ALARM. Input should be the part of the message you think violates your monitoring rule."
#     ),
#     Tool(
#         name="MEMX_LISTDIR",
#         func=os.listdir,
#         description="List the files in a directory. Input should be a directory path."
#     ),
#     Tool(
#         name="MEMX_TERMINAL",
#         func=lambda x: os.system(x),
#         description="Execute a command in the terminal. Input should be a terminal command. This tool can be used for a variety of tasks, such as running a Python script, installing packages with pip, or navigating the file system."
#     ),
#     # Tool(
#     #     name="MEMX_OPENAI_COMPLETION",
#     #     func=completion,
#     #     description="Generates a text completion from OpenAI's GPT-3 language model. Input should be a prompt."
#     # ),
#     # Tool(
#     #     name="MEMX_GITHUB_SEARCH",
#     #     func=github_search,
#     #     description="Searches GitHub for repositories related to a given topic. Input should be a search query."
#     # )
#     # Tool(
#     #     name="MEMX_INTERNET_SEARCH_ENGINE",
#     #     func=searx_search.run,
#     #     description="A meta search engine. Useful for when you need to answer questions about current events. Input should be a search query."
#     # )

# ]
