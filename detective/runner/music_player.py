import os
import random
import time
import pygame


def play_music(music_dir, mode="sequence"):
    """
    Plays music from a directory with different modes.

    Args:
        music_dir: The directory containing the music files.
        mode: The playback mode ('shuffle', 'sequence', or 'repeat').
    """

    try:
        # Initialize Pygame mixer
        pygame.mixer.init()

        # Get a list of music files
        music_files = [
            f for f in os.listdir(music_dir) if f.endswith((".mp3", ".wav", ".ogg"))
        ]  # Add or remove file extensions as needed

        if not music_files:
            print("No music files found in the directory.")
            return

        if mode == "shuffle":
            random.shuffle(music_files)
        elif mode == "repeat":
            # Repeat mode will be handled within the main loop
            pass
        elif mode != "sequence":
            print("Invalid mode. Defaulting to 'sequence'.")

        # Main playback loop
        track_num = 0
        while True:
            if mode == "repeat" and track_num >= len(music_files):
                track_num = 0

            current_track = os.path.join(music_dir, music_files[track_num])
            print(f"Now playing: {music_files[track_num]} (Mode: {mode})")

            try:
                pygame.mixer.music.load(current_track)
                pygame.mixer.music.play()

                # Keep the script alive while the music plays
                while pygame.mixer.music.get_busy():
                    time.sleep(1)

            except pygame.error as e:
                print(f"Error playing {music_files[track_num]}: {e}")

            track_num += 1

            if mode == "sequence" and track_num >= len(music_files):
                break  # Exit after playing all tracks in sequence mode

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.mixer.quit()


if __name__ == "__main__":
    music_directory = "/path/to/your/music/directory"  # Replace with the actual path
    playback_mode = "shuffle"  # Change to 'sequence' or 'repeat' as needed

    play_music(music_directory, playback_mode)
