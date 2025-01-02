import tkinter as tk
from tkinter.scrolledtext import ScrolledText


class TextBox(ScrolledText):
    def __init__(self, *args, **kwargs) -> None:
        ScrolledText.__init__(self, *args, **kwargs)

        # The next two lines are needed for the two callbacks.
        self._execution_id = ""  # this one is needed for the first callback
        self.edit_modified(False)  # and this one is need for the second callback

        self.bind("<Key>", self.on_key)  # Binding to <KeyPress> may work too.

    # First callback:
    def on_key(self, event: tk.Event) -> None:
        # Firstly, we start by cancelling any scheduled executions of the second
        # callback that have not yet been executed.
        if self._execution_id:
            self.after_cancel(self._execution_id)
        # Secondly, we schedule an execution of the second callback using the
        # `after_idle` command. (see https://tcl.tk/man/tcl8.5/TclCmd/after.htm#M9)
        self._execution_id = self.after_idle(self.on_modified, event)

    # Second callback:
    def on_modified(self, event: tk.Event) -> None:
        # Firstly, we use the built-in `edit_modified` method to check if the
        # content of the text widget has changed. (see https://tcl.tk/man/tcl8.5/TkCmd/text.htm#M93)
        # Otherwise, we abort the second callback. This is necessary to filter out
        # key presses that do not change the contents of the Text widget, such as
        # pressing arrow keys, Ctrl, Alt, etc.
        if not self.edit_modified():
            return
        # Secondly, we do whatever we want with the content of the Text widget.
        content = self.get("1.0", "end")
        print("! on_modified:", repr(content))
        # Thirdly, we set the built-in modified flag of the Text widget to False.
        self.edit_modified(False)


if __name__ == "__main__":
    root = tk.Tk()
    text = TextBox(root, height=10, width=50)
    text.pack(fill="both", expand=True, padx=10, pady=10)
    text.focus_set()
    root.mainloop()