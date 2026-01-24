import json

class BacklogController:
    def __init__(self):
        self.state = "RUNNING"
        
    def evaluate(self, metrics):
        if metrics["backlog_size"] > 1000:
            return {"action": "SCALE_UP", "reason": "BACKLOG_HIGH"}
        return {"action": "NO_OP", "reason": "STABLE"}
