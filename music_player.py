class Music_player():
    def __init__(self):
        self.queue = []
        self.loop = False
        self.current_song = None

    def add_song(self, song):
        self.queue.append(song)
    
    def add_as_next_song(self, song):
        self.queue.insert(0, song)

    def has_next(self):
        return True if len(self.queue) > 0 else False

    def get_next_song(self):
        next_song = self.queue[0]
        self.queue = self.queue[1:]
        # dont Store previous song
        self.current_song = next_song
        return next_song
    
    def get_current_song(self):
        return self.current_song

    def clear_queue(self):
        self.queue = []

    def toggle_loop(self):
        self.loop = not self.loop
