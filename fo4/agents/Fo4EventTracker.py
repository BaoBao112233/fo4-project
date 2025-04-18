# Fo4 Event Tracker Agent

import os
import time
import schedule
from datetime import datetime
from langchain.agents import AgentType, initialize_agent
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from fo4.tools.Fo4EventScraper import Fo4EventScraperTool
# Load environment variables
load_dotenv()


class Fo4EventTrackerAgent:
    """Agent that tracks FIFA Online 4 events and provides summaries."""
    
    def __init__(self):
        # Initialize OpenAI API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
            
        # Initialize LLM
        self.llm = ChatOpenAI(
            temperature=0.2,
            model="gpt-4-mini",
            openai_api_key=self.api_key
        )
        
        # Initialize tools
        self.tools = [Fo4EventScraperTool()]
        
        # Initialize agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )
        
        # Initialize event summarization chain
        self.summarize_prompt = PromptTemplate(
            input_variables=["events"],
            template="""
            You are an expert on FIFA Online 4 (Fo4). Below are the latest events scraped from the official website:
            
            {events}
            
            Please provide a concise summary of these events, highlighting the most important ones.
            Focus on new game features, special promotions, and tournaments.
            Also mention if there are any limited-time events that players should be aware of.
            """
        )
        
        self.summarize_chain = LLMChain(
            llm=self.llm,
            prompt=self.summarize_prompt
        )
        
        # Initialize storage
        self.latest_events = None
        self.last_update_time = None
        
    def update_events(self):
        """Update the latest events from FIFA Online 4 website."""
        try:
            # Get the events
            events_data = self.tools[0]._run()
            self.latest_events = events_data
            self.last_update_time = datetime.now()
            
            # Log the update
            print(f"Updated events at {self.last_update_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 50)
            print(events_data)
            print("-" * 50)
            
            # You can implement additional logic here, such as:
            # - Sending notifications
            # - Storing events in a database
            # - Comparing with previous events to detect changes
            
            return True
        except Exception as e:
            print(f"Error updating events: {str(e)}")
            return False
    
    def get_events_summary(self):
        """Get a summary of the latest events."""
        if not self.latest_events:
            return "No events have been fetched yet. Please update events first."
            
        try:
            summary = self.summarize_chain.run(events=self.latest_events)
            return summary
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def run_scheduled_updates(self):
        """Run scheduled updates at 7:00 AM every day."""
        # Schedule the update_events function to run daily at 7:00 AM
        schedule.every().day.at("07:00").do(self.update_events)
        
        print("Starting scheduled updates. Press Ctrl+C to exit.")
        
        # Run immediately once
        self.update_events()
        
        # Run the scheduler in a loop
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


