import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from src.agent.core import CareerAgent

# Load .env file
load_dotenv()

def main():
    print("Initializing Career Agent...")
    try:
        agent = CareerAgent()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return

    print("Agent Ready! Type 'exit' to quit.")
    
    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        chat_history.append(HumanMessage(content=user_input))
        
        inputs = {"messages": chat_history}
        
        try:
            result = agent.run(inputs)
            response = result["messages"][-1]
            print(f"Agent: {response.content}")
            chat_history.append(response)
        except Exception as e:
            print(f"Error executing agent: {e}")

if __name__ == "__main__":
    main()
