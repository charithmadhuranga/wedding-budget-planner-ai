from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from tools.budget_tracker import add_expense, view_budget, get_total_spending

# 1. Define Agent State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]


# 2. Define Tools
tools = [add_expense, view_budget, get_total_spending]

# 3. Define the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash") # Using gemini-pro, can be changed based on needs

# 4. Create the Tool-Calling Agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a wedding planner AI. You help plan weddings, manage budgets, and suggest ideas. "
               "You have access to tools to manage the wedding budget."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent_runnable = create_agent(llm, tools, system_prompt="You are a wedding planner AI. You help plan weddings, manage budgets, and suggest ideas. You have access to tools to manage the wedding budget.")

# 5. Define Nodes
def run_agent(state: AgentState):
    """
    Executes the agent's runnable.
    """
    agent_outcome = agent_runnable.invoke(state)
    return {"messages": agent_outcome["messages"]}

def execute_tools(state: AgentState):
    """
    Executes tools based on the agent's decisions.
    """
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        # Assuming direct execution for now, in a real scenario you might
        # map tool_name to actual tool functions
        if tool_name == "add_expense":
            result = add_expense.invoke(tool_args)
        elif tool_name == "view_budget":
            result = view_budget.invoke(tool_args)
        elif tool_name == "get_total_spending":
            result = get_total_spending.invoke(tool_args)
        else:
            result = f"Unknown tool: {tool_name}"
        results.append(result)
    
    return {"messages": results}

# 6. Define the Graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", run_agent)
workflow.add_node("tools", execute_tools)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    # Decide which path to take after the agent runs
    lambda state: "tools" if state["messages"][-1].tool_calls else END,
    {"tools": "tools", END: END}
)
workflow.add_edge("tools", "agent")

app = workflow.compile()
