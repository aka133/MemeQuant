from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain_ibm import WatsonxLLM
import asyncio
from market_datamanager import PumpMarketManager, MarketAwareAgent, MarketAwareTask
from pydantic import SecretStr

import os
os.environ["WATSON_APIKEY"] = "INSERT API KEY HERE"
os.environ["SERPER_API_KEY"] = "INSERT SERPER API KEY HERE"
os.environ["WATSONX_USERNAME"] = "INSERT USERNAME HERE"
os.environ["WATSONX_PASSWORD"] = "INSERT PASSWORD HERE"
os.environ["WATSONX_INSTANCE_ID"] = "INSERT INSTANCE ID HERE"

# Parameters for the model
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 500
}

#Create the first LLM
llm = WatsonxLLM(model_id="meta-llama/llama-3-3-70b-instruct", 
                 url=SecretStr("https://workbench-api.res.ibm.com"), 
                 params=parameters, 
                 project_id="INSERT PROJECT ID HERE",
                 version=SecretStr("5.1"),
                 )

llm_2 = WatsonxLLM(model_id="meta-llama/llama-3-3-70b-instruct", 
                 url=SecretStr("https://workbench-api.res.ibm.com"), 
                 params=parameters, 
                 project_id="INSERT PROJECT ID HERE",
                 version=SecretStr("5.1")
                 )

search = SerperDevTool()

def run_creation_phase():
    #Create the first agent
    researcher = Agent(
        llm=llm,
        function_calling_llm=llm_2,
        role="Researcher",
        goal="Find news keywords that could be useful for meme coin titles",
        backstory="You are a researcher who is tasked with finding news keywords that could be useful for meme coin titles.",
        allow_delegation=True,
        tools=[search],
        verbose=True,
    )

    creator = Agent(llm=llm, 
                function_calling_llm=llm_2,
                role="Meme Coin Creator",
                goal="Create 3 meme coin postings on pump.fun in line with current hype cycles and likely to profit 10x within 48 hours",
                backstory="You are a meme coin creator who is tasked with creating 3 meme coins on pump.fun with each having a unique name, image, and brief memo.",
                allow_delegation=True,
                verbose=True,
                )

    task1 = Task(
        description="Find news keywords that could be useful for meme coin titles",
        expected_output="A list of news keywords that could be useful for meme coin titles",
        output_file="news_keywords.txt",
        agent=researcher,
    )

    task2 = Task(
        description="Pick the top 3 keywords and create one meme coin for each keyword with a unique name, image, and brief memo",
        expected_output="A rich text file with the meme coin information and images",
        output_file="meme_coin_link.rtf",
        agent=creator,
    )

    creation_crew = Crew(agents=[researcher, creator], tasks=[task1, task2])

    print(creation_crew.kickoff())

async def run_trading_phase(token_addresses: list):
    # Initialize market manager with multiple tokens
    market_manager = PumpMarketManager()
    
    # Subscribe to multiple tokens
    for address in token_addresses:
        await market_manager.subscribe_token(address)
    
    # Marketing & Trading Agents
    marketer = MarketAwareAgent(
        market_manager=market_manager,
        llm=llm,
        function_calling_llm=llm_2,
        role="Marketing Strategist",
        goal="Maximize visibility and volume for monitored tokens",
        backstory="""You are a viral marketing expert who knows how to create FOMO and
                  drive engagement in crypto communities. You can manage multiple campaigns
                  simultaneously.""",
        allow_delegation=True,
        verbose=1,
    )

    trader = MarketAwareAgent(
        market_manager=market_manager,
        llm=llm,
        function_calling_llm=llm_2,
        role="Trading Strategist",
        goal="Generate profitable trading signals based on market activity",
        backstory="""You are an experienced meme coin trader who can analyze market sentiment,
                  volume patterns, and price action to identify profitable entry and exit points
                  across multiple tokens.""",
        allow_delegation=True,
        verbose=1,
    )

    # Trading & Marketing Tasks
    marketing_task = Task(
        description="""Generate engagement-optimized messages for:
                   - Telegram crypto groups
                   - Reddit meme coin communities
                   - pump.fun comment section
                   Track engagement metrics and adjust strategy accordingly.
                   Coordinate messaging across multiple tokens to maximize impact.""",
        expected_output="Marketing campaign with platform-specific messages for each token",
        output_file="marketing_campaign.txt",
        agent=marketer,
    )

    trading_task = MarketAwareTask(
        market_manager=market_manager,
        description="""Monitor market conditions and provide:
                   - Entry/exit signals for each token
                   - Position size recommendations
                   - Risk management guidelines
                   - Portfolio allocation suggestions
                   Update recommendations based on market response.""",
        expected_output="Real-time trading signals with reasoning for all monitored tokens",
        output_file="trading_signals.txt",
        agent=trader,
    )

    trading_crew = Crew(
        agents=[marketer, trader],
        tasks=[marketing_task, trading_task],
    )

    return trading_crew.kickoff()

# Main execution
if __name__ == "__main__":
    # Phase 1: Create meme coins
    creation_results = run_creation_phase()
    print("Creation Phase Complete:", creation_results)
    
    # Get multiple token addresses
    token_addresses = []
    while True:
        address = input("Enter token address (or 'done' to finish): ")
        if address.lower() == 'done':
            break
        token_addresses.append(address)
    
    # Phase 2: Trading and marketing
    trading_results = run_trading_phase(token_addresses)
    print("Trading Phase Active:", trading_results)