import sys
import click
import os
from dotenv import load_dotenv
import openai

from langchain.agents import initialize_agent, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory, ConversationEntityMemory, CombinedMemory
from langchain.agents.loading import AGENT_TO_CLASS


from .memx_monitoring_agent.base import MemxMonitoringAgent
# from .memx_monitoring_agent.tools import MemxMonitoringAgentTools
from .memx_programming_agent.base import MemxProgrammingAgent
# from .memx_programming_agent.tools import MemxProgrammingAgentTools
from .memx_discord_agent.base import DiscordAgent
from .memx_discord_agent.tools import DiscordAgentTools

AGENT_TO_CLASS["monitoring-agent"] = MemxMonitoringAgent
AGENT_TO_CLASS["programming-agent"] = MemxProgrammingAgent
AGENT_TO_CLASS["discord-agent"] = DiscordAgent

AGENT_TO_TOOLS = {}
# AGENT_TO_TOOLS["monitoring-agent"] = MemxMonitoringAgentTools
# AGENT_TO_TOOLS["programming-agent"] = MemxProgrammingAgentTools
AGENT_TO_TOOLS["discord-agent"] = DiscordAgentTools

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

class MemxAgent:

    def __init__(self, agent_type, temperature=0, model="gpt-3.5-turbo", basic_tools=None, extra_tools=None):
        self.llm = ChatOpenAI(temperature=temperature, model=model)
        convMemory = ConversationSummaryBufferMemory(llm=self.llm, memory_key="chat_history", max_token_limit=3500, return_messages=True)
        # entityMemory = ConversationEntityMemory(llm=self.llm, return_messages=True)
        self.memory = convMemory #CombinedMemory(memories=[entityMemory, convMemory])
        
        tool_class = AGENT_TO_TOOLS[agent_type]()
        if basic_tools == None:
            basic_tools = tool_class.default_tools
        if extra_tools == None:
            extra_tools = tool_class.extra_tools

        self.tools = self.set_up_tools(basic_tools, extra_tools)
        self.agent = self.set_up_agent(agent_type)

    def set_up_tools(self, tools, extra_tools):

        loaded_tools = load_tools(tools,
                                  llm=self.llm)

        if extra_tools is not None:
            loaded_tools += extra_tools

        return loaded_tools

    def set_up_agent(self, agent_type):
        agent = initialize_agent(self.tools,
                                 self.llm,
                                 agent=agent_type,
                                 verbose=True,
                                 memory=self.memory)

        return agent

    def get_response(self, message):
        return self.agent.run(input=message)


def print_available_agents():
    print("Available agents:")
    for agent_name in AGENT_TO_CLASS.keys():
        print(f"- {agent_name}")

@click.group()
def cli():
    pass

@cli.command()
def list_agents():
    print_available_agents()

@cli.command()
@click.option('--agent-type', default='discord-agent', help='The type of agent to use')
def run_agent(agent_type):
    agent = MemxAgent(agent_type=agent_type)
        
    while True:
        try:
            # Read a line of input from stdin
            input_text = input("> ")
            
            # If the input is empty, continue to the next iteration of the loop
            if not input_text:
                continue
            
            # Send the input to the ChatBot and print the response
            response = agent.get_response(input_text)
            print(response)
            
        except (KeyboardInterrupt, EOFError):
            # Exit the loop if the user presses Ctrl+C or sends an EOF signal
            print("\nGoodbye!")
            sys.exit()

if __name__ == '__main__':
    cli()