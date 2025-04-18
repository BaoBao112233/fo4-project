from fo4.agents.Fo4EventTracker import Fo4EventTrackerAgent

def main():
    """Main function to run the agent."""
    try:
        agent = Fo4EventTrackerAgent()
        agent.run_scheduled_updates()
    except KeyboardInterrupt:
        print("\nExiting the application...")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()