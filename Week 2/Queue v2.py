# from collections import deque

# class ClimateQueue:
#     def __init__(self):
#         self.events = deque()

#     def add_challenge(self, event_name):
#         self.events.append(event_name)              # enqueue: joins the back of the line
#         pushAction(f"Climate event queued: {event_name}")
#         updateClimateQueue(list(self.events))

#     def process_hazard(self):
#         if self.is_empty():
#             showMessage("No hazards waiting in the queue.")
#             return None
#         event = self.events.popleft()                # dequeue: FIFO, oldest leaves first
#         pushAction(f"Resolved hazard: {event}")
#         showMessage(f"{event} swept through the farm!")
#         updateClimateQueue(list(self.events))
#         return event

#     def is_empty(self):
#         return len(self.events) == 0


# q = ClimateQueue()
# q.add_challenge("Storm")
# q.add_challenge("Floods")
# q.add_challenge("Drought")

# q.process_hazard()   # resolves "Storm" first — it was queued first

# print("Climate Queue was ready!")