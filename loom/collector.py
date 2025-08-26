from .tracer import Tracer

class Collector:
    def __init__(self, tracer: Tracer):
        self.tracer = tracer

    def snapshot(self):
        return {
            'timestamp': __import__('time').time(),
            'tasks': self.tracer.snapshot()
        }
