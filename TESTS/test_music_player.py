import pytest
import pygame
import os
import time
from unittest.mock import patch
import random


class MusicPlayer:
    def __init__(self, music_dir, volume_step=5, volume_update_interval=0.5):
        pygame.init()
        pygame.mixer.init()

        self.music_dir = music_dir
        self.playlist = self.load_playlist()
        self.current_track_index = 0
        self.ch_mode = "sequence"  # "sequence", "shuffle", "single"
        self.volume = 50  # Initial volume
        pygame.mixer.music.set_volume(self.volume / 100.0)
        self.is_playing = False
        self.last_gesture = None
        self.volume_timer = 0
        self.volume_step = volume_step
        self.volume_update_interval = volume_update_interval
        self.load_current_track()

    def load_playlist(self):
        """Loads all .mp3 and .wav files from the music directory into a playlist."""
        playlist = []
        for filename in os.listdir(self.music_dir):
            if filename.endswith((".mp3", ".wav")):  # Add other audio formats if needed
                playlist.append(os.path.join(self.music_dir, filename))
        if not playlist:
            print(
                "Warning: no music file detected, please check ./assets/music directory"
            )
        return playlist

    def load_current_track(self):
        """Loads the current track from the playlist."""
        if 0 <= self.current_track_index < len(self.playlist):
            try:
                pygame.mixer.music.load(self.playlist[self.current_track_index])
                print(f"Loaded track: {self.playlist[self.current_track_index]}")
            except pygame.error as e:
                print(f"Error loading track: {self.playlist[self.current_track_index]}")
                print(e)
                # Handle the error (e.g., remove the track from the playlist, skip to the next)
                self.playlist.pop(self.current_track_index)
                self.current_track_index = max(
                    0, self.current_track_index - 1
                )  # prevent index out of range
                self.load_current_track()  # recursively load next track

    def play_music(self):
        """Plays the current track."""
        if self.playlist:
            pygame.mixer.music.play()
            self.is_playing = True

    def gesture_decode(self, gesture):
        current_time = time.time()

        # Edge detection for ch_mode, play_next, pause, resume
        if gesture != self.last_gesture:
            if gesture == "OK":
                self.toggle_ch_mode()
                print(f"Change mode toggled to: {self.ch_mode}")
            elif gesture == "Like":
                self.play_next()
                print("Play next")
            elif gesture == "Return":
                if not self.is_playing:
                    self.resume()
                    print("Resume")
            elif gesture == "Pause":
                if self.is_playing:
                    self.pause()
                    print("Pause")

        # Volume control with timer
        if gesture == "Right":
            if current_time - self.volume_timer > self.volume_update_interval:
                self.volume_down()
                self.volume_timer = current_time
        elif gesture == "Left":
            if current_time - self.volume_timer > self.volume_update_interval:
                self.volume_up()
                self.volume_timer = current_time

        self.last_gesture = gesture

        # Check if the current song has ended
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.handle_song_end()

    def toggle_ch_mode(self):
        if self.ch_mode == "sequence":
            self.ch_mode = "shuffle"
        elif self.ch_mode == "shuffle":
            self.ch_mode = "single"
        else:
            self.ch_mode = "sequence"

    def volume_up(self):
        self.volume = min(100, self.volume + self.volume_step)
        pygame.mixer.music.set_volume(self.volume / 100.0)
        print(f"Volume up: {self.volume}")

    def volume_down(self):
        self.volume = max(0, self.volume - self.volume_step)
        pygame.mixer.music.set_volume(self.volume / 100.0)
        print(f"Volume down: {self.volume}")

    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False

    def resume(self):
        pygame.mixer.music.unpause()
        self.is_playing = True

    def play_next(self):
        if self.ch_mode == "sequence":
            self.current_track_index = (self.current_track_index + 1) % len(
                self.playlist
            )
        elif self.ch_mode == "shuffle":
            self.current_track_index = random.randint(0, len(self.playlist) - 1)
        # "single" mode doesn't change the track
        self.load_current_track()
        self.play_music()

    def handle_song_end(self):
        if self.ch_mode == "sequence":
            self.current_track_index = (self.current_track_index + 1) % len(
                self.playlist
            )
        elif self.ch_mode == "shuffle":
            self.current_track_index = random.randint(0, len(self.playlist) - 1)
        # In "single" mode, we just stop
        if self.ch_mode != "single":
            self.load_current_track()
            self.play_music()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False


# Fixture for creating a MusicPlayer instance with a temporary directory.
@pytest.fixture
def player():
    # Initialize the MusicPlayer with the temporary directory
    pygame.init()
    with patch("pygame.mixer.init") as mock_mixer_init:  # Mock mixer.init
        yield MusicPlayer("assets/music")

    pygame.quit()


@patch("pygame.mixer.music.play")
def test_play_music(mock_play, player):
    # Test that music starts playing
    player.play_music()
    mock_play.assert_called_once()
    assert player.is_playing


def test_gesture_decode_volume_right(player):
    # Test for volume down
    initial_volume = player.volume
    player.gesture_decode("Right")
    assert player.volume == initial_volume - player.volume_step
    time.sleep(player.volume_update_interval + 0.1)  # Wait for the timer to reset
    player.gesture_decode("Right")
    assert player.volume == initial_volume - 2 * player.volume_step


def test_gesture_decode_volume_left(player):
    # Test for volume up
    initial_volume = player.volume
    player.gesture_decode("Left")
    assert player.volume == initial_volume + player.volume_step
    time.sleep(player.volume_update_interval + 0.1)
    player.gesture_decode("Left")
    assert player.volume == initial_volume + 2 * player.volume_step


def test_toggle_ch_mode(player):
    # More tests for mode toggling
    assert player.ch_mode == "sequence"
    player.toggle_ch_mode()
    assert player.ch_mode == "shuffle"
    player.toggle_ch_mode()
    assert player.ch_mode == "single"
    player.toggle_ch_mode()
    assert player.ch_mode == "sequence"


def test_volume_up(player):
    # Test for volume up limits
    initial_volume = player.volume
    player.volume_up()
    assert player.volume == initial_volume + player.volume_step
    player.volume = 100
    player.volume_up()
    assert player.volume == 100  # Should not exceed 100


def test_volume_down(player):
    # Test for volume down limits
    initial_volume = player.volume
    player.volume_down()
    assert player.volume == initial_volume - player.volume_step
    player.volume = 0
    player.volume_down()
    assert player.volume == 0  # Should not go below 0


def test_pause(player):
    # Test for pause functionality
    player.is_playing = True
    player.pause()
    assert not player.is_playing


def test_resume(player):
    # Test for resume functionality
    player.is_playing = False
    player.resume()
    assert player.is_playing


@patch("pygame.mixer.music.play")
def test_play_next_sequence(mock_play, player):
    # Test for playing next in sequence mode
    player.ch_mode = "sequence"
    initial_index = player.current_track_index
    player.play_next()
    assert player.current_track_index == (initial_index + 1) % len(player.playlist)
    mock_play.assert_called_once()


@patch("pygame.mixer.music.play")
def test_play_next_shuffle(mock_play, player):
    # Test for playing next in shuffle mode
    player.ch_mode = "shuffle"
    with patch("random.randint", return_value=2):
        player.play_next()
        assert player.current_track_index == 2
    mock_play.assert_called_once()


@patch("pygame.mixer.music.play")
def test_play_next_single(mock_play, player):
    # Test for playing next in single mode
    player.ch_mode = "single"
    initial_index = player.current_track_index
    player.play_next()
    assert player.current_track_index == initial_index  # Index should not change
    mock_play.assert_called_once()


@patch("pygame.mixer.music.get_busy", return_value=False)
def test_handle_song_end_single(mock_get_busy, player):
    # Test for handling song end in single mode
    player.ch_mode = "single"
    player.is_playing = True
    player.handle_song_end()
    assert player.is_playing  # Should still be playing (or paused)


def test_stop(player):
    # Test for stop functionality
    player.is_playing = True
    player.stop()
    assert not player.is_playing
