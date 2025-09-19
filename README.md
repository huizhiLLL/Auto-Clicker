# Auto Clicker Tool

A simple auto clicker tool that simulates mouse clicks and supports customizable click intervals.

## Features

- Supports left, right, and middle mouse button clicks
- Customizable click interval (in seconds)
- Hotkey control (start/stop, pause/resume)
- Graphical user interface

## Installation

Install required Python libraries:

```
pip install -r requirements.txt
```

## Usage

Run the GUI version:

```
python gui_auto_clicker.py
```

In the GUI, you can:
- Set click interval via input field
- Select click button type from dropdown
- Control auto click with buttons or hotkeys
- View real-time status

### GUI Controls

- **Interval Settings**: Enter the time interval between clicks in seconds
- **Button Settings**: Choose which mouse button or key to simulate
- **Control Buttons**: Start, pause, and stop the auto click functionality
- **Hotkeys**: 
  - `F6`: Start/Stop auto click
  - `F8`: Pause/Resume auto click
  - `F9`: Stop auto click
  - `Esc`: Exit program

## Notes

- The click position will be where your mouse cursor is located when starting
- Use with caution to avoid unintended operations
- Administrator privileges may be required on some systems