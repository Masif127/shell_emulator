import unittest
from src.emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):
    def setUp(self) -> None:
        self.emulator = ShellEmulator(vfs_name="test_vfs")

    def test_parse_input_simple(self) -> None:
        cmd, args = self.emulator.parse_input("ls -la")
        self.assertEqual(cmd, "ls")
        self.assertEqual(args, ["-la"])

    def test_parse_input_multiple_arguments(self) -> None:
        cmd, args = self.emulator.parse_input(
            "cd path/to/dir extra_arg"
        )
        self.assertEqual(cmd, "cd")
        self.assertEqual(args, ["path/to/dir", "extra_arg"])

    def test_parse_input_empty(self) -> None:
        cmd, args = self.emulator.parse_input("   ")
        self.assertEqual(cmd, "")
        self.assertEqual(args, [])

    def test_ls_stub(self) -> None:
        result = self.emulator.execute("ls -l /home")
        self.assertIn("ls: команда вызвана", result.output)
        self.assertIn("-l /home", result.output)
        self.assertEqual(result.error, "")

    def test_cd_stub_valid(self) -> None:
        result = self.emulator.execute("cd /usr/bin")
        self.assertIn("cd: переход в '/usr/bin'", result.output)
        self.assertEqual(result.error, "")

    def test_cd_stub_too_many_arguments(self) -> None:
        result = self.emulator.execute("cd dir1 dir2")
        self.assertIn("слишком много аргументов", result.error)
        self.assertEqual(result.output, "")

    def test_exit_command(self) -> None:
        result = self.emulator.execute("exit")
        self.assertTrue(result.should_exit)
        self.assertEqual(result.error, "")

    def test_exit_command_with_args(self) -> None:
        result = self.emulator.execute("exit now")
        self.assertFalse(result.should_exit)
        self.assertIn("не принимает аргументов", result.error)

    def test_unknown_command(self) -> None:
        result = self.emulator.execute("mkdir test")
        self.assertIn("команда не найдена: mkdir", result.error)
        self.assertEqual(result.output, "")


if __name__ == "__main__":
    unittest.main()