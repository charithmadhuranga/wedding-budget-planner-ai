import os
from dotenv import load_dotenv
from graph import app
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Check for Google API Key
if not os.getenv("GOOGLE_API_KEY"):
    print("GOOGLE_API_KEY not found. Please set it in the .env file.")
    exit()

def run_wedding_planner():
    print("Welcome to the Wedding Planner AI!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Invoke the graph with the user's input
        # The 'input' key maps to the 'input' placeholder in the prompt
        # The 'messages' key is for the chat history, initialized with the human message
        for s in app.stream(
            {"messages": [HumanMessage(content=user_input)]},
            {"recursion_limit": 50} # Adjust recursion limit if needed for complex conversations
        ):
            if "__end__" not in s:
                print(s)
            else:
                final_state = s["__end__"]
                # Assuming the last message in the final state is the agent's response
                if final_state and final_state["messages"]:
                    last_message = final_state["messages"][-1]
                    if hasattr(last_message, 'content'):
                        print(f"Agent: {last_message.content}")
                    elif isinstance(last_message, str): # Direct tool output
                        print(f"Agent: {last_message}")
                    else:
                        print(f"Agent: I processed your request.")
                else:
                    print("Agent: I'm not sure how to respond.")


if __name__ == "__main__":
    run_wedding_planner()
