import time

class TimedArray:
    def __init__(self, lifetime):
        self.array = []
        self.lifetime = lifetime
        self.timestamps = []

    def append(self, element):
        self.array.append(element)
        self.timestamps.append(time.time())

    def __getitem__(self, index):
        self.cleanup()
        return self.array[index]

    def __len__(self):
        self.cleanup()
        return len(self.array)

    def contains(self, element):
        self.cleanup()
        return element in self.array

    def cleanup(self):
        current_time = time.time()
        i = 0
        while i < len(self.timestamps):
            if current_time - self.timestamps[i] > self.lifetime:
                del self.array[i]
                del self.timestamps[i]
            else:
                i += 1
