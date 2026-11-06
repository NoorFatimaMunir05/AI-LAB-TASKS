class ClassroomAgent:
    def __init__(self):
        self.previous = None

    def target(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"

    def act(self, temp, occupied):
        before = self.previous
        mode = self.target(temp, occupied)
        send = mode != before
        if send:
            self.previous = mode
        return before, mode, "COMMAND" if send else "NO COMMAND"

agent = ClassroomAgent()
percepts = [(29, True), (29, True), (20, True), (26, True), (19, True), (29, False), (26.1, True), (25.9, True), (26.1, True)]
print("STEP | PERCEPT | REFLEX | PREVIOUS | TARGET | ACTION")
for i, percept in enumerate(percepts, 1):
    previous, target, action = agent.act(*percept)
    print(i, percept, agent.target(*percept), previous, target, action, sep=" | ")
