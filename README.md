# MemeQuant
A system of agent framework for researching, launching and trading memecoins on Pump.fun

This project uses IBM Watsonx.ai studio and CrewAI to design a system of agents. I used Llama 3.3 70B Instruct for four agents: 

Agent 1: Web Scraper

This agent scrapes the web and Twitter for news keywords that could be useful for meme coin titles.

Agent 2: Meme Coin Creator

This agent picks the top 3 keywords and creates one meme coin for each keyword with a unique name, image, and brief memo. The intention is to post these on pump.fun, so the output should be optimized to get maximum engagement.

Agent 3: Outbound Marketer

This agent distributes the new meme coin by generating messages for relevant Telegram groups and Reddit memecoinsubreddits, as well as generating comments on the pump.fun post to get people to pump the coin and boost visibility.

Agent 4: Trader

This agent issues recommendations to buy or sell the meme coin based on current market conditions (from pump.fun's market data API) and the news sentiment. The agent should provide immediate text updates to recommend buying or selling, and the reasoning behind the recommendation.

Libraries/services used in this project include Watsonx.ai, LangChain, CrewAI, Serper (for webscraping) and the Pump.fun data and transaction APIs.
