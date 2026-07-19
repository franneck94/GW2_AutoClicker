import sys
import time
import ctypes

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


def send_left_click() -> None:
    ctypes.windll.user32.mouse_event(
        MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP,
        0,
        0,
        0,
        0,
    )


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python auto_clicker.py <click_count>")
        print("Example: python auto_clicker.py 100")
        return 1

    try:
        click_count = int(sys.argv[1])
    except ValueError:
        print("Error: click_count must be an integer.")
        return 1

    if click_count < 0:
        print("Error: click_count must be 0 or greater.")
        return 1

    for _ in range(click_count):
        send_left_click()
        time.sleep(0.2)

    print(f"Done. Sent {click_count} left clicks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
