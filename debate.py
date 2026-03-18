from autogen_agentchat.base import TaskResult
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from pyexpat.errors import messages
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.ollama import OllamaChatCompletionClient
async def teamconfig(topic):
    load_dotenv()
    #model = OllamaChatCompletionClient(model="llama3",
       #                                host="http://localhost:11434")#(

    model=OpenAIChatCompletionClient(
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.1-8b-instant",
        api_key=os.environ["GROQ_API_KEY"],
        model_info={
           "vision": False,
           "function_calling": True,
           "json_output": True,
           "family": "unknown", }
    )


    host = AssistantAgent(name='Host',
                          model_client=model,
                          system_message="You are anYou are unbiased speaker  and mediator of the debate,  You will look which argument is in favour of Indian interest and you will announce the round number at beginning of the round ,you will listen to arguments made by Narendra and Rahul about the "f"topic{topic} and decide the winner after  that say TERMINATE")
    Supporter = AssistantAgent(
        name="Narendra",
        system_message=(
            'You are Narendra, a supporter agent in debate for the 'f'topic{topic}. You will debate Rahul, who is Your Opposition Agent.'),
        model_client=model)

    Opposition = AssistantAgent(
        name="Rahul",
        system_message=(
            'You are Rahul, a Opposition agent in the debate 'f' topic {topic}. You will be debating against Narendra,The supporter agent.'),
        model_client=model,
    )

    team = RoundRobinGroupChat(
        participants=[host, Supporter, Opposition],
        max_turns=8,
        termination_condition=TextMentionTermination(text="TERMINATE"),
    )
    return team


async def debate(team):



    #res=await team.run(task="Start the debate!")
    async  for message in team.run_stream(task="Start the debate!"):
        print("-"*20)
        if isinstance(message, TaskResult):
            message=f'Stopping reason:{message.stop_reason}'
            yield message
        else:
            message=f'Message:{message.source}:{message.content}'
            yield message



    #res=await model.create(messages=[UserMessage(content='Hi! How are you' ,source='user')])
    #for message in res.messages:
     #   print("-"*20)
      #  print(f'{message.source}: {message.content}')

async def main():
    topic = "Should India buy Russian Oil"
    team=await teamconfig(topic)
    async for message in debate(team):
        print("_"*20)
        print(message)




if __name__ == '__main__':
    topic = "Should India buy Russian Oil"
    asyncio.run(main())

