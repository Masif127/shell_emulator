import tkinter as tk
from tkinter import scrolledtext
from src.emulator import DEFAULT_VFS_NAME, ShellEmulator

WINDOW_WIDTH = 760
WINDOW_HEIGHT = 480
FONT_FAMILY = "Monospace"
FONT_SIZE = 11
EXIT_DELAY_MS = 300


class EmulatorGUI:
    def __init__(
        self,
        root: tk.Tk,
        vfs_name: str = DEFAULT_VFS_NAME
    ) -> None:
        self.root = root
        self.emulator = ShellEmulator(vfs_name=vfs_name)
        self.root.title(
            f"VFS: {self.emulator.vfs_name} - Shell Emulator"
        )
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg="#1e1e1e")

        self.history_area = self._create_history_area()
        self.input_entry = self._create_input_panel()
        self._print_welcome_message()

    def _create_history_area(self) -> scrolledtext.ScrolledText:
        history = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            bg="#121212",
            fg="#e0e0e0",
            insertbackground="#ffffff",
            font=(FONT_FAMILY, FONT_SIZE),
            state=tk.DISABLED
        )
        history.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        history.tag_config("prompt", foreground="#00e676")
        history.tag_config("output", foreground="#e0e0e0")
        history.tag_config("error", foreground="#ff5252")
        return history

    def _create_input_panel(self) -> tk.Entry:
        panel = tk.Frame(self.root, bg="#1e1e1e")
        panel.pack(fill=tk.X, padx=8, pady=(0, 8))

        prompt_lbl = tk.Label(
            panel,
            text=f"{self.emulator.vfs_name}$ ",
            bg="#1e1e1e",
            fg="#00e676",
            font=(FONT_FAMILY, FONT_SIZE, "bold")
        )
        prompt_lbl.pack(side=tk.LEFT)

        entry = tk.Entry(
            panel,
            bg="#2a2a2a",
            fg="#ffffff",
            insertbackground="#ffffff",
            font=(FONT_FAMILY, FONT_SIZE),
            relief=tk.FLAT
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 8))
        entry.bind("<Return>", lambda event: self.process_command())
        entry.focus_set()

        submit_btn = tk.Button(
            panel,
            text="Выполнить",
            bg="#37474f",
            fg="#ffffff",
            activebackground="#455a64",
            activeforeground="#ffffff",
            font=(FONT_FAMILY, FONT_SIZE),
            command=self.process_command
        )
        submit_btn.pack(side=tk.RIGHT)
        return entry

    def _append_text(self, text: str, tag: str = "output") -> None:
        self.history_area.config(state=tk.NORMAL)
        self.history_area.insert(tk.END, text + "\n", tag)
        self.history_area.see(tk.END)
        self.history_area.config(state=tk.DISABLED)

    def _print_welcome_message(self) -> None:
        self._append_text(
            f"Эмулятор оболочки ОС. "
            f"Загружена VFS: {self.emulator.vfs_name}",
            "prompt"
        )
        self._append_text(
            "Доступные команды: ls, cd, exit.",
            "output"
        )

    def process_command(self) -> None:
        command_line = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        if not command_line.strip():
            return

        prompt_prefix = f"{self.emulator.vfs_name}$ {command_line}"
        self._append_text(prompt_prefix, "prompt")

        result = self.emulator.execute(command_line)
        if result.output:
            self._append_text(result.output, "output")
        if result.error:
            self._append_text(f"Ошибка: {result.error}", "error")

        if result.should_exit:
            self.root.after(EXIT_DELAY_MS, self.root.destroy)


def main() -> None:
    root = tk.Tk()
    _ = EmulatorGUI(root=root)
    root.mainloop()


if __name__ == "__main__":
    main()