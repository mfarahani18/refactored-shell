import os
import sys


class RedirectionManager:
    redirect_symbols = [">", "1>", "2>", ">>", "1>>", "2>>"]

    def __init__(self, shell):
        self.shell = shell

    def handle(self, command, args):
        for symbol in self.redirect_symbols:
            if symbol in args:
                idx = args.index(symbol)
                file_name = args[idx + 1]
                real_args = args[:idx]

                self.redirect(
                    command,
                    real_args,
                    file_name,
                    symbol,
                )
                return True

        return False

    def redirect(
        self, command, real_args, file_name, symbol
    ):
        directory = os.path.dirname(file_name)

        if directory:
            os.makedirs(directory, exist_ok=True)

        output, error = self.run_for_redirection(
            command, real_args
        )

        if symbol in [">", "1>"]:
            self.redirect_stdout(
                file_name, output, append=False
            )
            if error:
                sys.stderr.write(error)

        elif symbol in [">>", "1>>"]:
            self.redirect_stdout(
                file_name, output, append=True
            )
            if error:
                sys.stderr.write(error)

        elif symbol == "2>":
            if output:
                sys.stdout.write(output)

            self.redirect_stderr(
                file_name, error, append=False
            )

        elif symbol == "2>>":
            if output:
                sys.stdout.write(output)

            self.redirect_stderr(
                file_name, error, append=True
            )

    def run_for_redirection(self, command, args):
        if command in self.shell.commands:
            output = self.shell.commands[command].execute(*args)
            return output, ""

        return self.shell.run_not_found(
            command, *args, capture=True
        )

    def redirect_stdout(self, file_name, output, append):
        mode = "a" if append else "w"

        with open(file_name, mode) as file:
            if output:
                file.write(output)

    def redirect_stderr(self, file_name, error, append):
        mode = "a" if append else "w"

        with open(file_name, mode) as file:
            if error:
                file.write(error)
