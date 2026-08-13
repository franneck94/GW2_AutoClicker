import argparse
import threading
import sys
import time
from pathlib import Path

import pyautogui
import pygame
from pynput import keyboard


def get_cursor_position() -> tuple[int, int]:
    return pyautogui.position()


def send_left_click() -> None:
    pyautogui.click()
    print(f"Sent left click. Current cursor position: {get_cursor_position()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Auto clicker with configurable delays."
    )
    parser.add_argument(
        "click_count",
        type=int,
        help="Number of left clicks to send",
        default=0,
    )
    parser.add_argument(
        "--wait-before-first",
        type=float,
        default=3.0,
        help="Seconds to wait before the first click (default: 3)",
    )
    parser.add_argument(
        "--wait-between-clicks",
        type=float,
        default=0.400,
        help="Seconds to wait between clicks (default: 0.25)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output",
    )
    return parser.parse_args()


def _create_stop_listener(stop_event: threading.Event) -> keyboard.Listener:
    ctrl_pressed = False
    c_pressed = False

    def on_press(key: keyboard.Key | keyboard.KeyCode | None) -> bool:
        nonlocal ctrl_pressed
        nonlocal c_pressed

        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            ctrl_pressed = True
            print("Ctrl key pressed.")
        if key == keyboard.KeyCode.from_char("c"):
            c_pressed = True
            print("C key pressed.")

        if ctrl_pressed and c_pressed:
            stop_event.set()
            print("Stop requested by user (Ctrl+C).")
            return False
        return True

    def on_release(key: keyboard.Key | keyboard.KeyCode | None) -> bool:
        nonlocal ctrl_pressed
        nonlocal c_pressed

        if key in (keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            ctrl_pressed = False
        if key == keyboard.KeyCode.from_char("c"):
            c_pressed = False

        return True

    return keyboard.Listener(on_press=on_press, on_release=on_release)


def main() -> int:
    args = parse_args()

    if args.click_count < 0:
        print("Error: click_count must be 0 or greater.")
        return 1

    if args.wait_before_first < 0:
        print("Error: --wait-before-first must be 0 or greater.")
        return 1

    if args.wait_between_clicks < 0:
        print("Error: --wait-between-clicks must be 0 or greater.")
        return 1

    debug_mode = args.debug

    print(
        f"Waiting for {args.wait_before_first} seconds before the first click..."
    )
    print(
        f"Will send {args.click_count} left clicks with {args.wait_between_clicks} seconds between each click."
    )
    print("Press Ctrl+C to stop early.")

    stop_event = threading.Event()
    listener = _create_stop_listener(stop_event)
    listener.start()

    time.sleep(args.wait_before_first)

    x, y = get_cursor_position()
    print(f"Clicking at current cursor position: ({x}, {y})")

    for i in range(args.click_count):
        if stop_event.is_set():
            print("Stopping before sending the next click.")
            break

        print(f"Click number {i + 1} / {args.click_count}")
        if not debug_mode:
            pyautogui.doubleClick()

        if stop_event.wait(timeout=args.wait_between_clicks):
            print("Stopping during wait interval.")
            break

    listener.stop()
    listener.join()

    if stop_event.is_set():
        print("Stopped by user.")
    else:
        print(f"Done. Sent {i + 1} double clicks.")

    pygame.mixer.init()
    if getattr(sys, "frozen", False):
        print("frozen dir")
        mp3_path = Path(sys._MEIPASS) / "media" / "stop.mp3"  # type: ignore
    else:
        mp3_path = Path(__file__).parent.parent / "media" / "stop.mp3"

    if mp3_path.exists():
        print("playing sound")
        pygame.mixer.music.load(str(mp3_path))
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(1.0)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
