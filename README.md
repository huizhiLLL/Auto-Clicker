# Auto Clicker Tool

A simple auto clicker tool that simulates mouse clicks and supports customizable click intervals.

## Features

- Supports left, right, and middle mouse button clicks
- Customizable click interval (in seconds)
- Hotkey control (start/stop, pause/resume)
- Command-line interface
- Graphical user interface

## Installation

Install required Python libraries:

```
pip install -r requirements.txt
```

## Usage

### Command-line Version

Run the tool:

```
python auto_clicker.py
```

Hotkeys:
- `F6`: Start/Stop auto click
- `F8`: Pause/Resume auto click
- `F9`: Stop auto click
- `Esc`: Exit program

Menu options:
1. Change click interval
2. Change click button (left/right/middle/space)
3. Exit program

### GUI Version

Run the GUI version:

```
python gui_auto_clicker.py
```

In the GUI, you can:
- Set click interval via input field
- Select click button type from dropdown
- Control auto click with buttons or hotkeys
- View real-time status

## Notes

- The click position will be where your mouse cursor is located when starting
- Use with caution to avoid unintended operations
- Administrator privileges may be required on some systems