import os
import readline
import subprocess
import sys


class CompletionManager:
    def __init__(self, external_runner):
        self.completions = {}
        self.external_runner = external_runner

    def find_matches(self, text, args):
        if args:
            return self.find_argument_matches(args[-1])

        return self.find_command_matches(text)

    def find_argument_matches(self, text):
        if "/" in text:
            return self.find_file_by_path(text)

        return self.find_entry_by_prefix(text)

    def find_command_matches(self, text):
        matches = []

        if text == "":
            return self.find_entry_by_prefix("")

        # Built-in names are supplied by the caller through the registry
        # in autocomplete(), so completion remains centralized here.
        for command in self.builtin_commands:
            if command.startswith(text):
                matches.append(command)

        external_commands = (
            self.external_runner.find_executable_by_prefix(text)
        )

        for command in external_commands:
            if command not in matches:
                matches.append(command)

        return matches

    def autocomplete(self, text, state):
        line = readline.get_line_buffer()
        command, *args = line.split()

        comp_line = line
        comp_point = str(len(comp_line))

        if command in self.completions:
            matches = self.run_custom_completion(
                command,
                args,
                text,
                comp_line,
                comp_point,
            )
        else:
            self.builtin_commands = self._get_builtin_commands()
            matches = self.find_matches(text, args)

        if state < len(matches):
            match = matches[state]

            if match.endswith("/"):
                return match

            if len(matches) == 1:
                return match + " "

            return match

        return None

    def _get_builtin_commands(self):
        # Set by Shell after construction; fallback keeps the manager usable.
        return getattr(self, "_shell_builtin_commands", [])

    def bind_builtin_commands(self, commands):
        self._shell_builtin_commands = commands
        self.builtin_commands = commands

    def run_custom_completion(
        self,
        command,
        args,
        text,
        comp_line,
        comp_point,
    ):
        full_path = self.completions[command]

        if len(args) < 2:
            previous = command
        else:
            previous = args[-2]

        result = subprocess.run(
            [
                full_path,
                command,
                text,
                previous,
            ],
            capture_output=True,
            text=True,
            env={
                "COMP_LINE": comp_line,
                "COMP_POINT": comp_point,
            },
        )

        return result.stdout.split()

    def display_matches(
        self, user_input, matches, longest_match_length
    ):
        sys.stdout.write("\r\n")
        sys.stdout.write(" ".join(sorted(matches)))
        sys.stdout.write(
            "\r\n$ " + readline.get_line_buffer()
        )
        sys.stdout.flush()

    def find_entry_by_prefix(self, prefix):
        matches = []
        path = os.getcwd()

        for entry in os.listdir(path):
            if not entry.startswith(prefix):
                continue

            full_path = os.path.join(path, entry)

            if os.path.isdir(full_path):
                entry = entry + "/"

            if entry not in matches:
                matches.append(entry)

        return matches

    def find_file_by_path(self, text):
        import os

        matches = []

        idx = text.rfind("/")
        directory = text[:idx]
        file_name = text[idx + 1:]
        prefix = text[:idx + 1]

        for entry in os.listdir(directory):
            if not entry.startswith(file_name):
                continue

            full_path = os.path.join(directory, entry)

            if os.path.isdir(full_path):
                entry_name = prefix + entry + "/"
            else:
                entry_name = prefix + entry

            if entry_name not in matches:
                matches.append(entry_name)

        return matches

    def complete(self, *args):
        if args[0] == "-C":
            value = args[1]
            key = args[2]
            self.completions[key] = value

        elif args[0] == "-p":
            if args[1] in self.completions:
                return (
                    f"complete -C "
                    f"'{self.completions[args[1]]}' "
                    f"{args[1]}\n"
                )

            return (
                f"complete: {args[1]}: "
                f"no completion specification\n"
            )

        elif args[0] == "-r":
            self.completions.pop(args[1], None)
