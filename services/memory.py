class UserMemory:
    def __init__(self):
        self.history = {}
        self.last_response = {}

    def add(self, user_id, query, answer):
        self.history.setdefault(user_id, []).append(f"Q: {query}\nA: {answer}")
        self.history[user_id] = self.history[user_id][-3:]
        self.last_response[user_id] = answer

    def get_history(self, user_id):
        return "\n".join(self.history.get(user_id, []))

    def get_last_response(self, user_id):
        return self.last_response.get(user_id)