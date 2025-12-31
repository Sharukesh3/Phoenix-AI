import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from src.manager.workflow_graph import WorkflowGraph

def main():
    print("Initializing Agentic Career Guide System...")
    try:
        workflow = WorkflowGraph()
    except Exception as e:
        print(f"Error initializing workflow: {e}")
        return

    print("System Ready! Enter details below.")
    print("Type 'exit' to quit.")
    
    while True:
        print("\n--- New Session ---")
        resume_path = input("Resume Path (optional): ").strip()
        if resume_path.lower() == 'exit': break
        
        github_user = input("GitHub Username (optional): ").strip()
        
        rejection_context = input("Did you face a rejection? describe it (optional): ").strip()
        
        user_input = {
            'resume_path': resume_path if resume_path else None,
            'github_username': github_user if github_user else None,
            'rejection_scenario': bool(rejection_context),
            'rejection_context': rejection_context
        }
        
        print("\nRunning workflow...")
        try:
            result = workflow.run(user_input)
            print("\n--- Final Output ---")
            print(result.get('final_output'))
            print("\nMessages:")
            for msg in result.get('messages', []):
                print(f"- {msg}")
        except Exception as e:
            print(f"Error executing workflow: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
