from typing import List, Tuple

DEFAULT_VFS_NAME = "test_vfs"
MAX_CD_ARGUMENTS = 1
COMMAND_INDEX = 0
ARGS_START_INDEX = 1


class CommandResult:
    def __init__(
        self,
        output: str = "",
        error: str = "",
        should_exit: bool = False
    ) -> None:
        self.output = output
        self.error = error
        self.should_exit = should_exit


class ShellEmulator:
    def __init__(self, vfs_name: str = DEFAULT_VFS_NAME) -> None:
        self.vfs_name = vfs_name

    def parse_input(self, raw_input: str) -> Tuple[str, List[str]]:
        tokens = raw_input.strip().split()
        if not tokens:
            return "", []
        command = tokens[COMMAND_INDEX]
        args = tokens[ARGS_START_INDEX:]
        return command, args

    def handle_ls(self, args: List[str]) -> CommandResult:
        joined_args = " ".join(args)
        message = f"ls: команда вызвана, аргументы: [{joined_args}]"
        return CommandResult(output=message)

    def handle_cd(self, args: List[str]) -> CommandResult:
        if len(args) > MAX_CD_ARGUMENTS:
            return CommandResult(
                error="cd: слишком много аргументов (ожидается не более 1)"
            )
        target = args[0] if args else "~"
        message = f"cd: переход в '{target}' (заглушка)"
        return CommandResult(output=message)

    def handle_exit(self, args: List[str]) -> CommandResult:
        if args:
            return CommandResult(
                error="exit: команда не принимает аргументов"
            )
        return CommandResult(
            output="Выход из эмулятора...",
            should_exit=True
        )

    def execute(self, raw_input: str) -> CommandResult:
        command, args = self.parse_input(raw_input)
        if not command:
            return CommandResult()

        if command == "ls":
            return self.handle_ls(args)
        if command == "cd":
            return self.handle_cd(args)
        if command == "exit":
            return self.handle_exit(args)

        return CommandResult(
            error=f"эмулятор: команда не найдена: {command}"
        )