from datetime import datetime

class LazyTimedCache(object):
    def __init__(self, worker, ttl):
        self.worker = worker
        self.ttl = ttl
        self.value = None
        self.timestamp = None
    
    def eager(self):
        self.value = self.worker()
        self.timestamp = datetime.now()
        return self.value
    
    def get(self):
        if self.value is None:
            return self.eager()
        else:
            delta = datetime.now() - self.timestamp
            if delta >= ttl:
                return self.eager()
            return self.value
