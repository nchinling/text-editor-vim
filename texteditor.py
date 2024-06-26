import tkinter as tk
from tkinter import filedialog


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Vim++")
        self.textarea = tk.Text(self.root, undo=True, font=("Fixedsys", 16))
        self.textarea.pack(expand=True, fill='both')
        self.textarea.configure(bg="#99dee5")

        # Menubar
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save as", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.textarea.edit_undo)
        edit_menu.add_command(label="Redo", command=self.textarea.edit_redo)
        edit_menu.add_command(label="Yank", command=self.yank)
        edit_menu.add_command(label="Put", command=self.put)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menubar)

        toolbar = tk.Frame(self.root)
        toolbar.pack(side="top", fill="x")

        undo_button = tk.Button(toolbar, text="Undo",
                                command=self.textarea.edit_undo)
        undo_button.pack(side="left", padx=2, pady=2)
        undo_button = tk.Button(toolbar, text="Redo",
                                command=self.textarea.edit_redo)
        undo_button.pack(side="left", padx=2, pady=2)

        # keyboard shortcut
        self.root.bind("<Command-c>", self.yank)
        self.root.bind("<Command-v>", self.put)
        self.root.bind("<Command-z>", self.textarea.edit_undo)
        self.root.bind("<Command-y>", lambda event: self.textarea.edit_redo())

    def new_file(self):
        self.textarea.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.textarea.delete(1.0, tk.END)
                self.textarea.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                                                 ("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.textarea.get(1.0, tk.END)
                file.write(content)

    def yank(self, event=None):
        selected_text = self.textarea.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)

    def put(self, event=None):
        if event:
            return
        clipboard_text = self.root.clipboard_get()
        self.textarea.insert(tk.INSERT, clipboard_text)


def main():
    root = tk.Tk()
    text_editor = TextEditor(root)
    # root.attributes('-fullscreen', True)

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window width and height to 50% of screen dimensions
    width = int(screen_width * 0.8)
    height = int(screen_height * 0.8)
    root.geometry(f"{width}x{height}")
    root.mainloop()


if __name__ == "__main__":
    main()
