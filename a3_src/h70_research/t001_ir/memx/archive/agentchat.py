
import openai
import os


api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key

class Agent:
    def __init__(self, name, api_key):
        """
        Initializes the Agent instance with a given name and OpenAI API key.
        """
        self.name = name
        self.chatroom = None

    def get_response(self, message):
        """
        Sends a message to the OpenAI API and returns the AI-generated response.
        """
        response = openai.Completion.create(
            engine="davinci",
            prompt=message,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

    def join_chatroom(self, chatroom):
        """
        Joins a chatroom by adding the agent instance to the chatroom's agents list and setting the chatroom property.
        """
        self.chatroom = chatroom
        chatroom.join(self)

    def send_message(self, message):
        """
        Sends a message to the chatroom.
        """
        self.chatroom.broadcast(message, sender=self)

    def receive_message(self, message):
        """
        Receives a message from the chatroom and generates a response using the OpenAI API.
        """
        response = self.get_response(message)
        self.send_message(response)

    def add_message(self, message):
        """
        Adds a message to the agent's message history.
        """
        self.chatroom.add_message(f"{self.name}: {message}")


class Chatroom:
    def __init__(self, name):
        """
        Initializes the Chatroom instance with a given name and empty agents list and message history.
        """
        self.name = name
        self.agents = []
        self.messages = []

    def join(self, agent):
        """
        Adds an agent to the chatroom's agents list.
        """
        self.agents.append(agent)

    def broadcast(self, message, sender=None):
        """
        Sends a message to all agents in the chatroom except for the sender (if specified).
        """
        for agent in self.agents:
            if agent != sender:
                agent.receive_message(message)

    def add_message(self, message):
        """
        Adds a message to the chatroom's message history.
        """
        self.messages.append(message)

    def start_chat(self):
        """
        Starts a chat session in the chatroom by sending an initial message to all agents and waiting for their responses.
        """
        initial_message = f"Welcome to the {self.name} chatroom! Please introduce yourselves."
        self.broadcast(initial_message)

        while True:
            message = input(">> ")
            if message == "/exit":
                break
            self.add_message(f"User: {message}")
            self.broadcast(message)

# Create the chatroom and agents
chatroom = Chatroom("Test Chatroom")
agent1 = Agent("Agent 1", os.environ["OPENAI_API_KEY"])
agent2 = Agent("Agent 2", os.environ["OPENAI_API_KEY"])

# Join the agents to the chatroom
agent1.join_chatroom(chatroom)
agent2.join_chatroom(chatroom)
chatroom.start_chat()