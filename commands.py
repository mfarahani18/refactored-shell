import os
import sys
class BaseCommand:
    """Base class for every built-in command."""

    name = ""

    def __init__(self, shell):
        self.shell = shell

    def execute(self, *args):
        raise NotImplementedError


class EchoCommand(BaseCommand):
    name = "echo"

    def execute(self, *args):
        return " ".join(args) + "\n"


class ExitCommand(BaseCommand):
    name = "exit"

    def execute(self, *args):
        if self.shell.histfile:
            self.shell._write_history_file(
                self.shell.histfile,
                self.shell.history_data,
            )
        sys.exit()


class PwdCommand(BaseCommand):
    name = "pwd"

    def execute(self):
        return os.getcwd() + "\n"


class CdCommand(BaseCommand):
    name = "cd"

    def execute(self, *args):
        if args[0] == "~":
            home = os.environ["HOME"]
            os.chdir(home)
        elif os.path.isdir(args[0]):
            os.chdir(args[0])
        else:
            print(
                f"cd: {args[0]}: "
                f"No such file or directory"
            )


class TypeCommand(BaseCommand):
    name = "type"

    def execute(self, *args):
        if args[0] in self.shell.builtin_commands:
            return f"{args[0]} is a shell builtin\n"

        full_path = self.shell.find_executable(args[0])

        if full_path:
            return f"{args[0]} is {full_path}\n"

        return f"{args[0]}: not found\n"


class CompleteCommand(BaseCommand):
    name = "complete"

    def execute(self, *args):
        return self.shell.completion_manager.complete(*args)


class JobsCommand(BaseCommand):
    name = "jobs"

    def execute(self, *args):
        return self.shell.job_manager.jobs()


class HistoryCommand(BaseCommand):
    name = "history"

    def execute(self, *args):
        return self.shell.history_manager.history(*args)


class DeclareCommand(BaseCommand):
    name = "declare"

    def execute(self, *args):
        return self.shell.variables_manager.declare(*args)
