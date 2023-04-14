import time
import queue
import threading

import requests

class RateLimitedAPI():
    def __init__(self):
        self.q = queue.Queue()
        self.max_calls = 299
        self.period = 60 # seconds
        self.lock = threading.Lock()
        self.last_reset_time = time.monotonic()
        
    def _reset(self):
        self.q = queue.Queue()
        self.last_reset_time = time.monotonic()
        
    def _process_queue(self):
        
        while True:
            try:
                item = self.q.get(block=False)
            except queue.Empty:
                break
            
            #call the API
            url = item
            response = self._make_api_call(url)
            
            
            with self.lock:
                if self.q.empty():
                    elapsed_time = time.monotonic() - self.last_reset_time
                    if elapsed_time < self.period:
                        time.sleep(self.period - elapsed_time)
                    self._reset()
            return response
    
    def _make_api_call(self, url):
        response = requests.get(url, timeout=1)
        return response
    
    def call_api(self, url):
        with self.lock:
            if self.q.qsize() == self.max_calls:
                elapsed_time = time.monotonic() - self.last_reset_time
                if elapsed_time < self.interval:
                    time.sleep(self.interval - elapsed_time)
                self._reset()

            self.q.put(url)

        self._process_queue()