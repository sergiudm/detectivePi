""" 
This module plays music from a directory with different modes and volume control
using Pygame. It also decodes gestures to control the music playback.

gesture_decode(gesture):
    
    returns:
    ch_mode, volume_up, volume_down, pause, resume, play_next


    if gesture == "OK":
        ch_mode = True
    elif gesture == "Like":
        play_next = True
    elif gesture == "Return":
        resume = True
    elif gesture == "Pause":
        pause = True
    elif gesture == "Right":
        volume_down = True
    elif gesture == "Left":
        volume_up = True
    else:
        ch_mode = False
        volume_up = False
        volume_down = False
"""

import os
import random
import time
import pygame


class MusicPlayer:
    def __init__(self):
        self.previous_gesture = "None"  # Keep track of the previous gesture
        self.mode = "normal"  # "normal" or "change_mode"
        self.volume_debounce_time = (
            0.3  # Seconds to ignore volume gestures after a change
        )
        self.last_volume_change_time = 0
        self.paused = False
        self.volume = 0.5  # initial volume

    def gesture_decode(self, gesture):
        current_time = time.time()

        # Change mode
        if gesture == "OK" and self.previous_gesture != "OK":
            self.mode = "change_mode" if self.mode == "normal" else "normal"

        # Play Next
        elif gesture == "Like" and self.previous_gesture != "Like":
            if self.mode == "change_mode":
                # play next song
                print("Playing next song")
                pass

        # Pause/Resume
        elif gesture == "Return" and self.previous_gesture != "Return":
            if self.mode == "normal":
                if self.paused:
                    print("Resuming")
                    self.paused = False
                else:
                    print("Pausing")
                    self.paused = True

        # Volume Down
        elif gesture == "Right" and self.previous_gesture != "Right":
            if (
                self.mode == "normal"
                and current_time - self.last_volume_change_time
                > self.volume_debounce_time
            ):
                self.volume = max(self.volume - 0.1, 0.0)
                print(f"Volume: {self.volume:.1f}")
                self.last_volume_change_time = current_time

        # Volume Up
        elif gesture == "Left" and self.previous_gesture != "Left":
            if (
                self.mode == "normal"
                and current_time - self.last_volume_change_time
                > self.volume_debounce_time
            ):
                self.volume = min(self.volume + 0.1, 1.0)
                print(f"Volume: {self.volume:.1f}")
                self.last_volume_change_time = current_time

        self.previous_gesture = gesture  # Update previous gesture


def play_music(music_dir, resent_gesture_queue, mode="sequence", initial_volume=0.5):
    """
    Plays music from a directory with different modes and volume control.

    Args:
        music_dir: The directory containing the music files.
        mode: The playback mode ('shuffle', 'sequence', or 'repeat').
        initial_volume: The initial volume (0.0 to 1.0).
    """

    try:
        # Initialize Pygame
        pygame.init()

        # Initialize Pygame mixer
        pygame.mixer.init()

        player = MusicPlayer()

        # Set initial volume
        pygame.mixer.music.set_volume(initial_volume)

        # Get a list of music files
        music_files = [
            f for f in os.listdir(music_dir) if f.endswith((".mp3", ".wav", ".ogg"))
        ]

        if not music_files:
            print("No music files found in the directory.")
            return

        if mode == "shuffle":
            random.shuffle(music_files)
        elif mode == "repeat":
            pass  # Repeat mode will be handled within the main loop
        elif mode != "sequence":
            print("Invalid mode. Defaulting to 'sequence'.")

        # Main playback loop
        track_num = 0
        while True:
            # Repeat the sequence from the beginning
            if track_num >= len(music_files):
                track_num = 0

            current_track = os.path.join(music_dir, music_files[track_num])
            print(f"Now playing: {music_files[track_num]} (Mode: {mode})")

            try:
                pygame.mixer.music.load(current_track)
                pygame.mixer.music.play()

                # Inner loop for handling events while music is playing
                while pygame.mixer.music.get_busy():
                    # Check for gesture
                    if not resent_gesture_queue.empty():
                        gesture = resent_gesture_queue.get()
                        print(f"Received gesture: {gesture}")
                        player.gesture_decode(gesture)

                    if player.paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                    pygame.mixer.music.set_volume(player.volume)

                    if gesture == "Like" and player.mode == "change_mode":
                        pygame.mixer.music.stop()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.mixer.music.stop()
                            pygame.mixer.quit()
                            return

                    time.sleep(0.1)  # Check for events less frequently

            except pygame.error as e:
                print(f"Error playing {music_files[track_num]}: {e}")

            track_num += 1

            if mode == "sequence" and track_num >= len(music_files):
                break  # Exit after playing all tracks in sequence mode

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.mixer.quit()
        pygame.quit()


if __name__ == "__main__":
    from queue import Queue

    music_directory = "assets/music"
    playback_mode = "sequence"
    initial_volume = 0.7  # Set initial volume (0.0 - 1.0)
    gesture_queue = Queue(maxsize=1)
    gesture_queue.put("OK")  # Simulate gesture input

    play_music(music_directory, gesture_queue, playback_mode, initial_volume)
