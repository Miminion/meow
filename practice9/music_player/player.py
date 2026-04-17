import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.playlist = []     
        self.current_index = 0  
        self.is_playing = False

    def load_music_folder(self, folder):
      
        for f in sorted(os.listdir(folder)):
            if f.endswith(('.wav', '.mp3')):
                self.playlist.append(os.path.join(folder, f))

    def get_track_name(self):
        if not self.playlist:
            return "No tracks loaded"
        return os.path.basename(self.playlist[self.current_index])

    def play(self):
        if not self.playlist:
            return
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev_track(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_position(self):
      
        if self.is_playing:
            return pygame.mixer.music.get_pos() // 1000  
        return 0