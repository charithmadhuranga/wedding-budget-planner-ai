import pandas as pd
from langchain.tools import tool
import os

BUDGET_FILE = "wedding_budget.csv"

def get_budget_df():
    if os.path.exists(BUDGET_FILE):
        return pd.read_csv(BUDGET_FILE)
    else:
        df = pd.DataFrame(columns=["Category", "Item", "Cost"])
        df.to_csv(BUDGET_FILE, index=False)
        return df

@tool
def add_expense(category: str, item: str, cost: float):
    """
    Adds a new expense to the wedding budget.

    Args:
        category (str): The category of the expense (e.g., "Venue", "Catering").
        item (str): The specific item for the expense (e.g., "Reception Hall", "Dinner").
        cost (float): The cost of the item.
    """
    df = get_budget_df()
    new_expense = pd.DataFrame([{"Category": category, "Item": item, "Cost": cost}])
    df = pd.concat([df, new_expense], ignore_index=True)
    df.to_csv(BUDGET_FILE, index=False)
    return f"Added expense: {item} ({category}) - ${cost:.2f}"

@tool
def view_budget():
    """
    Views the current state of the wedding budget.
    """
    df = get_budget_df()
    if df.empty:
        return "The budget is currently empty."
    else:
        return df.to_string()

@tool
def get_total_spending():
    """
    Calculates the total spending so far.
    """
    df = get_budget_df()
    total_cost = df["Cost"].sum()
    return f"Total spending: ${total_cost:.2f}"
