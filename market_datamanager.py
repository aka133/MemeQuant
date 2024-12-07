import asyncio
from crewai import Agent, Task
import websockets
import json
from typing import Dict, List

class PumpMarketManager:
    def __init__(self):
        self.uri = "wss://pumpportal.fun/api/data"
        self.websocket = None
        self.market_data = {
            "new_tokens": [],
            "token_trades": {},
            "market_summary": ""
        }
        
    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        
    async def subscribe_all(self):
        # Subscribe to new token creation events
        await self.websocket.send(json.dumps({
            "method": "subscribeNewToken"
        }))
        
        # Can add more subscriptions as needed
        
    async def subscribe_token(self, token_addresses):
        if not self.websocket:
            await self.connect()
        await self.websocket.send(json.dumps({
            "method": "subscribeTokenTrade",
            "keys": token_addresses
        }))
        
    async def process_messages(self):
        try:
            if not self.websocket:
                await self.connect()
            if self.websocket:  # Verify connection succeeded
                async for message in self.websocket:
                    data = json.loads(message)
                    self.update_market_summary(data)
            else:
                print("Failed to establish WebSocket connection")
        except Exception as e:
            print(f"WebSocket error: {e}")
        
    def update_market_summary(self, data):
        # Format data into natural language for LLM
        summary = f"""
        Latest Market Update:
        New Token: {data.get('token_name', 'N/A')}
        Price: {data.get('price', 'N/A')}
        Volume: {data.get('volume', 'N/A')}
        Recent Trades: {data.get('recent_trades', [])}
        """
        self.market_summary = summary

class MarketAwareAgent(Agent):
    def __init__(self, market_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.market_manager = market_manager
        
    def get_market_context(self):
        return self.market_manager.market_summary

class MarketAwareTask(Task):
    def __init__(self, market_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.market_manager = market_manager
        
    def get_context(self):
        market_data = self.market_manager.market_summary
        return f"""
        Current Market Context:
        {market_data}
        
        Based on this data and your analysis, {self.description}
        """