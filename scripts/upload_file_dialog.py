import sys
import time
import win32gui
import win32con

def handle_open_dialog(filepath, timeout=15):
    print(f"Waiting for Open dialog (timeout {timeout}s)...")
    start = time.time()
    while time.time() - start < timeout:
        # Search for #32770 dialog
        def enum_cb(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                cls = win32gui.GetClassName(hwnd)
                if cls == "#32770" or "Open" in title:
                    results.append((hwnd, title))
            return True

        dialogs = []
        win32gui.EnumWindows(enum_cb, dialogs)
        
        for hwnd, title in dialogs:
            # Look for Edit control
            edit = None
            cb_ex = win32gui.FindWindowEx(hwnd, 0, "ComboBoxEx32", None)
            if cb_ex:
                cb = win32gui.FindWindowEx(cb_ex, 0, "ComboBox", None)
                if cb:
                    edit = win32gui.FindWindowEx(cb, 0, "Edit", None)
            if not edit:
                edit = win32gui.FindWindowEx(hwnd, 0, "Edit", None)

            if edit:
                print(f"Found dialog hwnd: {hwnd} ('{title}'), edit control: {edit}")
                # Set text to filepath
                win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, str(filepath))
                time.sleep(0.3)
                # Press Enter or click Open
                win32gui.PostMessage(hwnd, win32con.WM_COMMAND, 1, 0)
                print("Submitted filepath successfully!")
                return True
        time.sleep(0.5)
    print("Timeout: Open dialog did not appear.")
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = r"E:\work station\gta 6\data\clips\carry_post30m_viral\clip_00995-01018.mp4"
    handle_open_dialog(path)
