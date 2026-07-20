import argparse
import time

import pyautogui


def get_cursor_position() -> tuple[int, int]:
    return pyautogui.position()


def send_left_click() -> None:
    pyautogui.click()
    print(f"Sent left click. Current cursor position: {get_cursor_position()}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto clicker with configurable delays.")
    parser.add_argument("click_count", type=int, help="Number of left clicks to send")
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
    return parser.parse_args()


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

    print(f"Waiting for {args.wait_before_first} seconds before the first click...")
    print(f"Will send {args.click_count} left clicks with {args.wait_between_clicks} seconds between each click.")

    time.sleep(args.wait_before_first)

    x, y = get_cursor_position()
    print(f"Clicking at current cursor position: ({x}, {y})")

    for _ in range(args.click_count):
        pyautogui.doubleClick()
        time.sleep(args.wait_between_clicks)

    print(f"Done. Sent {args.click_count} double clicks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
