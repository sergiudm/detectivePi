import os
import pytest
import pygame
from queue import Queue
from detective.modules.music_player import MusicPlayer, play_music

# Define a test directory with some sample music files
TEST_MUSIC_DIR = os.path.join(os.path.dirname(__file__), "test_music")

# Create the directory and sample files if they don't exist
if not os.path.exists(TEST_MUSIC_DIR):
    os.makedirs(TEST_MUSIC_DIR)
    # Create dummy .mp3 files for testing (you can replace these with actual short mp3 files if needed)
    for i in range(3):
        with open(os.path.join(TEST_MUSIC_DIR, f"test_song{i + 1}.mp3"), "wb") as f:
            f.write(b"")  # Write some dummy data


@pytest.fixture
def music_player():
    """
    Fixture to create a MusicPlayer instance for each test.
    """
    pygame.init()
    pygame.mixer.init()
    player = MusicPlayer()
    yield player  # This allows cleanup after the test
    pygame.mixer.quit()
    pygame.quit()


def test_gesture_decode_change_mode(music_player):
    """
    Test that the 'OK' gesture toggles the mode.
    """
    music_player.gesture_decode("OK")
    assert music_player.mode == "change_mode"
    music_player.gesture_decode("OK")
    assert music_player.mode == "normal"


def test_gesture_decode_play_next(music_player):
    """
    Test that the 'Like' gesture in change_mode triggers playing the next song.
    (We're just checking for the print statement in this example.
     Ideally, you would mock or modify play_music to verify the behavior more thoroughly.)
    """
    music_player.mode = "change_mode"
    with pytest.raises(Exception) as e:
        music_player.gesture_decode("Like")
    assert str(e.value) == ""


def test_gesture_decode_pause_resume(music_player):
    """
    Test that the 'Return' gesture toggles pause/resume in normal mode.
    """
    music_player.gesture_decode("Return")
    assert music_player.paused is True
    music_player.gesture_decode("Return")
    assert music_player.paused is False


def test_gesture_decode_volume_down(music_player):
    """
    Test that the 'Right' gesture decreases volume with debouncing.
    """
    music_player.gesture_decode("Right")
    assert music_player.volume == 0.4
    music_player.gesture_decode("Right")  # Should be ignored due to debouncing
    assert music_player.volume == 0.4


def test_gesture_decode_volume_up(music_player):
    """
    Test that the 'Left' gesture increases volume with debouncing.
    """
    music_player.gesture_decode("Left")
    assert music_player.volume == 0.6
    music_player.gesture_decode("Left")  # Should be ignored due to debouncing
    assert music_player.volume == 0.6


def test_play_music_sequence_mode(music_player):
    """
    Test the play_music function in sequence mode.
    (This is a basic test. You might want to add more comprehensive tests
    to check for things like correct track order, handling of errors, etc.)
    """
    gesture_queue = Queue()
    play_music(TEST_MUSIC_DIR, gesture_queue, mode="sequence", initial_volume=0.5)
