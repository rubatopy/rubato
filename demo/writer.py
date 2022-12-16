import pyautogui, sys, keyboard, os
"""
This file will write out other python files slowly in order to be screen recorded.
It will then run the file in the command line.

Usage:
    Make a file with the filename and a _ in front of it. (ex: _test.py)
    python .\writer.py .\<filename>
    You must disable all suggestions of vscode in order for this to work. (like notepad)
    Escape will stop the program.
"""

# asynchronously await user input "escape" to stop the program
keyboard.add_hotkey("esc", lambda: os._exit(0))


# Write the file out slowly function
def write_slowly(lines):
    for line in lines:
        line = line.replace("\n", "")
        # scuffed way to get rid of all leading space
        s = line.strip()
        if s == "":
            pyautogui.press("enter")
            continue
        else:
            line = line.split(s[0], 1)
            pyautogui.write(line[0], interval=0)
            pyautogui.typewrite(s[0] + line[1], interval=0.001)
            pyautogui.press("enter")


# Open the file to write to
if __name__ == "__main__":
    # # print screen position to test pyautogui
    # print(pyautogui.position())

    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = f.readlines()

    # move into writing position
    pyautogui.moveTo(x=777, y=270)

    # click mouse button
    pyautogui.click()

    # Write the file out slowly
    write_slowly(lines)

    # Save the file with ctrl + s
    pyautogui.hotkey("ctrl", "s")

    # move cursor to command line
    pyautogui.moveTo(x=955, y=983)

    # click mouse button
    pyautogui.click()

    # Run the file in the command line
    filename = filename.split("\\")
    pyautogui.typewrite(f"python {filename[0]}\\_{filename[1]}", interval=0.01)

    pyautogui.press("enter")
