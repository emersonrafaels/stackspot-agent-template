from pathlib import Path

from stackspot import StackspotAi
from stackspot.stackspot_auth import StackspotAuth


def create_stackspot_agent():
    """
    Creates and configures a StackSpot AI agent
    """
    # Get the current workspace directory as root using pathlib
    root_dir = Path(__file__).parent.parent.resolve()

    # Configure authentication with the root directory
    auth = StackspotAuth(root=str(root_dir))

    # Create the AI agent instance
    agent = StackspotAi(auth)

    return agent


def run_agent_task():
    """
    Example of running a task with the StackSpot AI agent
    """
    # Create the agent
    agent = create_stackspot_agent()

    # Define the task or prompt for the agent
    task = "Create a simple Python FastAPI application"

    try:
        # Use the quick command feature to execute the task
        quick_command = agent.quick_command(task)

        # Execute the command and get the response
        response = quick_command.execute()

        # Process the agent's response
        print("Agent Response:", response)

    except Exception as e:
        print(f"Error executing agent task: {str(e)}")


if __name__ == "__main__":
    run_agent_task()
