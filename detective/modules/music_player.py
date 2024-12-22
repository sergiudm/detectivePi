import pygame
import time


def music_play(music_player, resent_gesture_queue, initial_volume=50):
    try:
        music_player.volume = initial_volume
        pygame.mixer.music.set_volume(music_player.volume / 100.0)
        music_player.play_music()

        while True:
            if not resent_gesture_queue.empty():
                gesture = resent_gesture_queue.get()
                music_player.gesture_decode(gesture)
            time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()
