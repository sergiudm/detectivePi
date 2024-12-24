Getting Started
=================================================

## Environment Requirements       
| Environment | Version                                |
| ----------- | -------------------------------------- |
| OS          | Ubuntu22.04, Raspberry Pi OS, Window11 |
| Python      | >=3.8                                  |

## Installation        
## pip install
```bash
pip install Thread-Everything
```

## Source code installation

```bash
git clone https://github.com/sergiudm/Thread-Everything.git
cd detective
conda create -n detective python=3.10 -y
echo "conda environment created"
conda activate detective
pip install -r requirements.txt
```

## Usage
Before you start, you need to create a `config.json` file in the root directory of the project,
Here is an example(you can find it in the `config_template.json`):

```json
{
    "use_pi": false,
    "plugin_list": [ # Note: plugins related to GPIO need to enable `use_pi`, if you don't use GPIO-related libraries, turn it off
        "information_server",
        "GPIO_controller",
        "music_server",
        "gpio_controller",
    ],
    "default_detect_mode": "others",
    "use_camera": true,
    "use_visualization": false, # if you want to see the detection result, set it to true
    "server_email": "youremail@example.com",
    "server_email_password": "your email password",# Note: if you use QQ email, you need to set an app password
    "target_email": [
        "email1",
        "email2"
    ],
    "smtp_server":"your smtp server",
    "smtp_port": 587,
    "video_path": "assets/videos/sit.mp4", # if you want to use a video file for detection, set it here
    "image_path": "resources", # if you want to use an image file for detection, set it here
    "send_delay": 13, # the interval between sending emails
    "effective_detection_duration": 2,
    "max_num_hands": 2,
    "min_detection_confidence": 0.65,
    "min_tracking_confidence": 0.65,
    "pin_data": {
        "pin_list": [ # if you use GPIO, you need to set the pin list
            17,
            23,
            24,
            25,
            27
        ],
        "pin_map": { # mapping the gesture to the pin
            "Right": [
                17,
                23,
                24
            ],
            "Return": [
                23,
                24
            ],
            "Left": [
                17,
                24
            ],
            "Pause": [],
            "Like": [
                25
            ],
            "OK": [
                27
            ]
        }
    }
}
```
!!! warning
    In the `config.json` file, you need to remove all the comments before running the program.     

### Run the program
Linux:
```bash
sudo chmod +x run.sh
./run.sh
```
Windows:
```bash
./win_run.bat
```