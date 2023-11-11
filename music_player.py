class Music_player():
    def __init__(self):
        self.queue = []
        self.loop = False
        self.previous_song = [None, None]

    def add_song(self, song):
        self.queue.append(song)
    
    def add_as_next_song(self, song):
        self.queue.insert(0, song)

    def has_next(self):
        return True if len(self.queue) > 0 else False

    def get_next_song(self):
        next_song = self.queue[0]
        self.queue = self.queue[1:]
        # Store previous song
        self.previous_song[0] = self.previous_song[1]
        self.previous_song[1] = next_song
        return next_song
    
    def get_previous_song(self):
        return self.previous_song[1]

    def clear_queue(self):
        self.queue = []

    def toggle_loop(self):
        self.loop = not self.loop
    
    def is_current_and_previous_same(self):
        return self.previous_song[0] == self.previous_song[1] != None
    
    def set_prev_songs(self):
        if self.previous_song == [None, None]:
            self.previous_song = [self.queue[0], self.queue[0]]