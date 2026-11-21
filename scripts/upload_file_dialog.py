import sys
import time
import os
import ctypes

user32 = ctypes.windll.user32

WM_SETTEXT = 0x000C
WM_COMMAND = 0x0111

def handle_open_dialog(filepath, timeout=20):
    print(f"Waiting for Open dialog (timeout {timeout}s)...")
    start = time.time()
    while time.time() - start < timeout:
        hwnd = user32.FindWindowW("#32770", None)
        if hwnd:
            # Look for ComboBoxEx32 -> ComboBox -> Edit
            cb_ex = user32.FindWindowExW(hwnd, 0, "ComboBoxEx32", None)
            edit = 0
            if cb_ex:
                cb = user32.FindWindowExW(cb_ex, 0, "ComboBox", None)
                if cb:
                    edit = user32.FindWindowExW(cb, 0, "Edit", None)
            if not edit:
                edit = user32.FindWindowExW(hwnd, 0, "Edit", None)

            if edit:
                print(f"Found dialog hwnd: {hwnd}, edit control: {edit}")
                user32.SendMessageW(edit, WM_SETTEXT, 0, str(filepath))
                time.sleep(0.3)
                user32.PostMessageW(hwnd, WM_COMMAND, 1, 0)
                print("Submitted filepath successfully!")
                return True
        time.sleep(0.3)
    print("Timeout: Open dialog did not appear.")
    return False

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else ""
    handle_open_dialog(path)
