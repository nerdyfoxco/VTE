import sys

# Proof: AI Cannot Ask More Than Budget
# Enforces "Question Budget" to prevent cost runaways.

class BudgetController:
    def __init__(self, limit=5):
        self.limit = limit
        self.usage = 0
        
    def ask_question(self, question):
        if self.usage >= self.limit:
             raise RuntimeError("Question Budget Exceeded. Halting Workflow.")
        self.usage += 1
        return "Answer"

def prove_budget_cap():
    print("Testing Question Budget Enforcement...")
    controller = BudgetController(limit=3)
    
    # 1. Consume Budget
    for i in range(3):
        controller.ask_question(f"Q{i}")
    print("  Consumed 3/3 questions.")
        
    # 2. Exceed Budget
    try:
        controller.ask_question("One more?")
        print("  [FAIL] Controller allowed exceeding budget!")
        return False
    except RuntimeError as e:
        print(f"  [PASS] Controller blocked excess question: {e}")
        return True

if __name__ == "__main__":
    if prove_budget_cap():
        sys.exit(0)
    else:
        sys.exit(1)
