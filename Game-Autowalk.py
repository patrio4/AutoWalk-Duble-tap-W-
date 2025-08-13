import keyboard
import time
import os
import sys
from threading import Lock

# Script states
double_tap_hold = False
last_w_release = 0
lock = Lock()

def handle_w_release(e):
    global last_w_release, double_tap_hold
    
    if e.name != 'w':
        return
        
    with lock:
        current_time = time.time()
        if current_time - last_w_release < 0.4:
            keyboard.press('w')
            double_tap_hold = True
            print("\n[AutoWalk] Movement active (Double tap W to stop)")
        last_w_release = current_time

def handle_s_press(e):
    global double_tap_hold
    
    if not double_tap_hold:
        return
        
    with lock:
        keyboard.release('w')
        if keyboard.is_pressed('s'):
            keyboard.release('s')
        double_tap_hold = False
        print("\n[AutoWalk] Movement stopped (Double tap W to move)")

def handle_w_press(e):
    global double_tap_hold
    
    if not double_tap_hold:
        return
        
    with lock:
        keyboard.release('w')
        double_tap_hold = False
        print("\n[AutoWalk] Movement stopped (Double tap W to move)")

def exit_script():
    with lock:
        if double_tap_hold:
            keyboard.release('w')
        keyboard.unhook_all()
        os._exit(0)

def main():
    # Clear console
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("AutoWalk - Simplified Version")
    print("============================")
    print("Controls:")
    print("- Double tap W to start auto-walking")
    print("- Press S or W again to stop")
    print("- Close window to exit")
    print("\n[Ready] Double tap W to start")
    
    # Set up keyboard events
    keyboard.on_release_key('w', handle_w_release)
    keyboard.on_press_key('s', handle_s_press)
    keyboard.on_press_key('w', handle_w_press)
    
    # For clean exit when window is closed
    if os.name == 'nt':
        import win32api
        win32api.SetConsoleCtrlHandler(lambda _: exit_script(), True)
    
    # Main loop
    try:
        keyboard.wait()
    except (KeyboardInterrupt, SystemExit):
        exit_script()

if __name__ == "__main__":
    main()