# Wedding Planner AI

This project is a command-line chatbot that acts as a simple AI wedding planner. It's designed to help you keep track of your wedding budget by allowing you to add expenses, view your current budget, and see your total spending.

## How it Works

The Wedding Planner AI is built with Python using the `langchain` and `langgraph` libraries to create a conversational AI agent. The agent is powered by Google's Gemini model and can understand and respond to your requests in a natural way.

The agent has access to a set of tools that allow it to:

*   **Add expenses:** You can tell the agent to add a new expense to your budget, specifying the item and the cost.
*   **View budget:** The agent can show you a list of all the expenses you've added to your budget.
*   **Get total spending:** The agent can calculate and tell you the total amount of money you've spent so far.

All of your budget data is stored in a simple CSV file called `wedding_budget.csv`.

## Getting Started

To get started with the Wedding Planner AI, you'll need to have Python 3 installed on your computer. Then, follow these steps:

1.  **Clone the repository:**
    ```
    git clone https://github.com/your-username/wedding-planner-ai.git
    ```
2.  **Install the dependencies:**
    ```
    pip install -r requirements.txt
    ```
3.  **Set up your environment variables:**

    Create a file called `.env` in the root directory of the project and add your Google API key to it:
    ```
    GOOGLE_API_KEY="your-api-key"
    ```
4.  **Run the application:**
    ```
    python main.py
    ```

Once the application is running, you can start chatting with the Wedding Planner AI. For example, you can try saying:

*   "Hi there! Can you help me with my wedding budget?"
*   "Add a new expense: Wedding dress, $2000"
*   "What's my total spending so far?"
*   "Show me my budget"

## Project Structure

The project is organized into the following files and directories:

*   `main.py`: The main entry point for the application.
*   `graph.py`: Defines the AI agent and its conversational flow.
*   `tools/budget_tracker.py`: Implements the tools for managing the wedding budget.
*   `wedding_budget.csv`: Stores the wedding budget data.
*   `requirements.txt`: Lists the Python dependencies for the project.
*   `.env`: Stores your Google API key.
