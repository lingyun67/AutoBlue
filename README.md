# AutoBlue

A simple auto-farming script that utilizes third-party libraries for color detection, simulated joystick input, and simulated mouse input.

[简体中文](README.zh-CN.md) | [English](README.md) | [日本語](README.jp.md)

## Getting Started

Download this project to your local machine and navigate to the project folder. Then run the following command:

```
pip install -r requirements.txt
```

This will install the required third-party libraries.

Before using it for the first time, you need to perform local adaptation.

You need to obtain the coordinates of the health bar on your game client. Download the Grab Tool from [https://wwuh.lanzout.com/iAItC115cv2d]. After opening the Grab Tool, target any enemy and position the mouse cursor on the far left of its health bar, leaving a few pixels from the left edge and trying to align the cursor vertically in the center of the health bar. Then press Ctrl+Alt+1, and the Grab Tool will display the coordinates of the selected position.

Repeat the same process to obtain the coordinates of your own health bar, which should be positioned around 80% from the left side of the health bar (not applicable for archers). 

Open the `config.ini` file, which has the following default values:

```ini
[General]
# Color of the current target
target_color = 247, 1, 0
# Color of the health bar background
hp_color = 51, 51, 51
x_original_value = 821
y_original_value = 61
hp_x = 831
hp_y = 1045
# Color tolerance range
color_tolerance = 10
# Combat timeout
timeout = 30
# Offset caused by buffs moving the health bar
target_window_pianyi_original = 7
```

Replace the values `x_original_value` and `y_original_value` with the coordinates you obtained earlier (e.g., 821, 61).

By default, the third skill (3) and the second combat illusion (2) are used as means of life recovery. If you don't want to change the code, please adjust the positions of the skills in your game.

Now you can run the script:

```
py main.py
```

## Script Logic

The workflow is as follows: start -> reset the current perspective -> rotate and search for targets -> lock onto a target -> enter skill loop -> target dies -> search for a new target.

If the color at the coordinates indicated by the `target_color` matches red, it is considered that the current target is locked, and the script enters the combat loop. Otherwise, it enters the search loop.

If the color at the coordinates indicated by the `hp_color` matches the background color of the player's health bar, it forcibly enters the life recovery loop.

To account for the possibility of losing the lock on the target, the script will force a new target search after a specified time.

To account for the possibility of searching in unusual perspectives without finding any enemies, the script will reset the perspective after a specified time.

When the health is low, it automatically enters the life recovery loop (only applicable for archers).

The script uses the `vgamepad` library for simulated joystick input and the `pyautogui` library for mouse wheel input.

As long as the game window is scaled to a 16:9 aspect ratio, it can be placed anywhere on the screen, and the health bar position will be repositioned within 30 seconds.

## Notes

- By default, the script scrolls the mouse wheel downward because Bandai does not allow target switching using a gamepad.
- If a gamepad is already connected, the script will not work because the game only allows control from a single gamepad.

## Custom Settings

To be added.



## Recommended Farming Locations

### Levels 1-5: Anywhere on the first wilderness map
Simply follow the main storyline for a short while, and you'll reach level 5. After that, you can enter Free Exploration.

### Levels 3-14: Entrance of Free Exploration
Invincible spot with no damage taken.
![img](https://raw.githubusercontent.com/lingyun67/AutoBlue/main/img/3-14.png)

### Levels 11-21: Resting Place of Pilgrims
You can stand on a rock here and attack wolves without taking damage. However, Goblin Camp might be more efficient for leveling up.
![img](https://raw.githubusercontent.com/lingyun67/AutoBlue/main/img/11-21.png)

### Levels 14-22: Goblin Camp
There is no safe spot here, but there are many enemies. While it might be annoying to deal with elite mobs, you can focus on leveling up, and once they die, they won't interfere anymore.
![img](https://raw.githubusercontent.com/lingyun67/AutoBlue/main/img/14-22.png)

## Implementation of Complex Functions

Method `get_target_health_bar_coordinates`:

If there is a red pixel at coordinates (821, 61) on the screen in 1080p full-screen mode, the variables `x_original_value` and `y_original_value` represent those coordinates.

When the `get_target_health_bar_coordinates` method is called, it invokes the existing `get_window_coordinates` method, which returns four values: `window_left`, `window_top`, `window_width`, and `window_height`. These values represent the x-coordinate of the window's top-left corner, the y-coordinate of the window's top-left corner, the width of the window, and the height of the window, respectively.

After obtaining these four values, the `get_target_health_bar_coordinates` method divides the window width by the screen width and the window height by the screen height to obtain the scaling factors.

Then, it multiplies the variables `x_original_value` and `y_original_value` by the scaling factors and adds them to the coordinates of the scaled window's top-left corner, thus repositioning the red pixel.

Later, the `get_target_health_bar_coordinates` method is split into the `get_scaling_factors` and `calculate_target_coordinates` methods. The former is used to obtain the scaling factors, while the latter is used to calculate the specific coordinates.

## Changelog

- v0.1 Attempted using AutoHotkey: detected color at specified position (target health bar) and performed auto-attack (auto-click) and mouse wheel scroll to switch targets and attack all nearby enemies.
- v0.2 Switched to Python due to limitations in rotating the perspective. Utilized `vgamepad` library for simulated joystick input and `pyautogui` library for mouse wheel input.
