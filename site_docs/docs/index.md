Thread-Everything：An easy-to-use interface to run threads from different machines
==================================================
[![site deployment](https://github.com/sergiudm/detectivePi/actions/workflows/mkdocs.yml/badge.svg)](https://github.com/sergiudm/detectivePi/actions/workflows/mkdocs.yml)
[![CI Tests](https://github.com/sergiudm/detectivePi/actions/workflows/test.yml/badge.svg)](https://github.com/sergiudm/detectivePi/actions/workflowstest.yml)
[![PyPI version](https://badge.fury.io/py/detective-pi.svg)](https://pypi.org/project/Thread-Everything/)
![GitHub license](https://img.shields.io/github/license/sergiudm/detectivePi)
## Introduction

[Thread-Everything](https://github.com/sergiudm/Thread-Everything) is a powerful and user-friendly Python framework that simplifies multi-threaded communication and control across different devices. It supports Windows and Linux, works seamlessly on x86 and ARM architectures, and enables you to effortlessly deploy and coordinate tasks across multiple machines.

Thread-Everything empowers you to:

- Easily distribute your functionalities to separate devices for enhanced performance and flexibility.

- Effortlessly orchestrate multi-device communication using a unified API.

- Develop custom applications via an intuitive plugin system, tailoring Thread-Everything to your specific needs.

Imagine these possibilities:

- Controlling a remote robot army with a single Windows client.

- Creating immersive online action games based on real-time gesture recognition.

- Building a smart KTV system with gesture-controlled song selection and dynamic lighting.

- Developing a universal GPIO scheduler for simplified hardware control - perfect for streamlining university lab assignments.

## Architecture

```mermaid
graph TD
    subgraph "Resource Manager"
        C[config.json]
        C-->P[Assets Loader]
    end

    subgraph "Core Components"
        B(Plugin Manager) -- loads--> C
        B --> D[Runner Engine]
        D --> E[State Machine]
        D --> N[Vision Engine]
        D --> F[Music Engine]
    end

    subgraph "Plugins (modules)"
        F --> G[Music Player]
        D --> J[Other User Defined Plugins] 
        N --> H[Body Feature Extractor]
        N --> O[Gesture detector]
        E --> I[GPIO Controller]
    end
    
    subgraph "Communication Module"
      D --> K[Socket Module]
      D --> L[Mailbot]
      K <--> M[Other Machines]
    end

   

    style B fill:#336,stroke:#ccc,stroke-width:2px
    style D fill:#363,stroke:#ccc,stroke-width:2px
    style G fill:#663,stroke:#ccc,stroke-width:2px
    style H fill:#663,stroke:#ccc,stroke-width:2px
    style I fill:#663,stroke:#ccc,stroke-width:2px
    style J fill:#663,stroke:#ccc,stroke-width:2px
    style O fill:#663,stroke:#ccc,stroke-width:2px
    style K fill:#336,stroke:#ccc,stroke-width:2px
    style L fill:#336,stroke:#ccc,stroke-width:2px
```
Thread-Everything's core is a robust plugin scheduler that loads and manages the execution of individual plugins. Each plugin is a self-contained Python module designed for a specific task, such as:

- GPIO control

- Facial recognition

- Music playback

...and much more!

The plugin scheduler is highly configurable through a unified config.json file. To streamline plugin development, we've provided powerful core components, including:

- Vision Engine: Simplifies computer vision tasks.

- Music Engine: Facilitates audio management and playback.

- State Machine: Enables complex state-based logic.

Built upon this framework are several pre-built plugins like:

- Gesture Detection:

  - Uses your computer's camera to detect hand gestures (e.g., "OK," "Thumbs Up").

  - Sends recognized gestures to other devices via the communication module.

- Posture Detection:

    - Analyzes your posture using the camera and provides feedback on whether you're sitting upright or slouching.

- Music Control:

  - Controls music playback on your device (play/pause, volume, etc.).

  - Can be controlled via command line input or integrated with other plugins like gesture detection.

  - Simply place music files in the designated directory for automatic playback.

- Universal GPIO Controller (Raspberry Pi Only):

  - Provides control over GPIO pins on a Raspberry Pi.

  - Can be integrated with other plugins for advanced automation.

- Personalized Mailbot:

  - Sends customized emails based on events triggered by other plugins.

  - Can include images captured by the camera or other relevant data.

Furthermore, the communication module enables seamless peer-to-peer (P2P) communication between devices.

## Contribution
This project is open to contributions. You can contribute in the following ways:

- Add more plugins
- Improve the existing code

## Future Work


- Enhanced Vision Engine:

  - Move beyond the current reliance on MediaPipe to create a more generic vision processing module.

  - Support for different vision libraries and custom algorithms.

- Integrated Voice Processing Module:

  - Add basic voice processing capabilities for remote calling, voice input, and other plugin enhancements.

- Improved GPIO Controller:

  - Expand the GPIO controller to support advanced features like PWM and I2C.

## Acknowledgement
- [mediapipe](https://github.com/google-ai-edge/mediapipe)

- [cv2](https://docs.opencv.org/4.x/index.html)

- [pygame](https://www.pygame.org/docs/)