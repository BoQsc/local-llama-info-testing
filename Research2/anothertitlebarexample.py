import tkinter, win32api #win32api is used for getting the mouse position

windowPos = [0, 0] #This is used so we can change the window pos
window = tkinter.Tk()
window.geometry("600x600+0+0") #the "+0+0" are the y and x positions
window.overrideredirect(True)

windowMoving = False
mousePos = win32api.GetCursorPos()

def titleBarPressed(event):
    global windowMoving, mousePos
    mousePos = win32api.GetCursorPos()
    windowMoving = True
    
def titleBarReleased(event):
    global windowMoving
    windowMoving = False
    
titleBar = tkinter.Label(window, text = "Title Bar", bg = "#000000", fg = "#FFFFFF")
titleBar.place(x = 0, y = 0, width = 600, height = 30)
titleBar.bind("<Button-1>", titleBarPressed)
titleBar.bind("<ButtonRelease-1>", titleBarReleased)

while True:
    if windowMoving == True:
        windowPos[0] = windowPos[0] - (mousePos[0] - win32api.GetCursorPos()[0])
        windowPos[1] = windowPos[1] - (mousePos[1] - win32api.GetCursorPos()[1])
        
        mousePos = win32api.GetCursorPos()

    window.geometry(f"600x600+{windowPos[0]}+{windowPos[1]}")
    
    window.update()