---
comments: true
---

How to write your own plugins
=============================
Thread-Everything is a highly extensible project that allows you to define your own plugins in the `modules` directory. We have implemented some plugins, they lie in:

```
.
├── common.py
├── detect_others.py
├── gesture.py
├── gpio_controller.py
├── __init__.py
├── meditation_assistant.py
├── music_player.py
└── utils.py
```
To integrate your own function, you should:
1. Implement all your features in a Python module.
2. Encaplulate all your functions to a single function.
3. Create a new thread instance in `detective.runner.runner_engine, together with your arguments.

Here is a step-by-step demontration:

## Create a new Python module
In this example, we implement a music player feature in `music_player.py` which lies in `detective/runner`, and the class is defined as:
```python
class MusicPlayer:
    def __init__(
        self, music_dir, volume_step=5, volume_update_interval=0.5
    ):
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
```
## Create the function
Then create a single function:
```python
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
```
You may need to import external packages.

## Create a thread instance
In `detective/runner/runner_engine`, create a `music_thread` instance.
```python
music_thread = threading.Thread(
        target=music_play,
        args=(
            music_player,
            resent_gesture_queue,
        ),
    )
```
You also need to assign a name so that the config parser can load the plugin.
```python
def name2thread(name):
            return {
                "information_server": server_thread,
                "working_detect": working_detect_thread,
                "music_server": music_thread, # this is the new plugin
                "gpio_controller": gpio_controller_thread,
                "gesture_detection": gesture_detection_thread,
                "meditation_helper": meditation_helper_thread,
            }[name]
```
## Load your plugin in the `config.json` file
Finally, configure your plugin in the `config.json`, 
```json
{
    // ...
    "plugin_list": [
        // other plugins
        "music_server"
    ]
    // ...
}
```
and then you can launch your plugin!

