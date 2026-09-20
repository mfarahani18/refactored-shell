import os
import subprocess
import sys


class PipelineManager:
    def __init__(self, shell):
        self.shell = shell

    def run(self, parts):
        commands = self.split(parts)

        processes = []
        previous_pipe = None

        for i, command_parts in enumerate(commands):
            command = command_parts[0]
            args = command_parts[1:]

            if i == 0:
                previous_pipe = self.run_first(
                    command, args, processes
                )
            elif i == len(commands) - 1:
                self.run_last(
                    command,
                    args,
                    previous_pipe,
                    processes,
                )

                if previous_pipe is not None:
                    os.close(previous_pipe)
            else:
                previous_pipe = self.run_middle(
                    command,
                    args,
                    previous_pipe,
                    processes,
                )

        for process in processes:
            process.wait()

    def split(self, parts):
        commands = []
        current = []

        for part in parts:
            if part == "|":
                commands.append(current)
                current = []
            else:
                current.append(part)

        commands.append(current)
        return commands

    def run_first(self, command, args, processes):
        read_pipe, write_pipe = os.pipe()

        if command in self.shell.commands:
            result = self.shell.commands[command].execute(*args)

            if result is not None:
                os.write(write_pipe, result.encode())
        else:
            full_path = self.shell.find_executable(command)

            process = subprocess.Popen(
                [command, *args],
                executable=full_path,
                stdout=write_pipe,
            )
            processes.append(process)

        os.close(write_pipe)
        return read_pipe

    def run_middle(
        self,
        command,
        args,
        previous_pipe,
        processes,
    ):
        read_pipe, write_pipe = os.pipe()

        if command in self.shell.commands:
            result = self.shell.commands[command].execute(*args)

            if result is not None:
                os.write(write_pipe, result.encode())
        else:
            full_path = self.shell.find_executable(command)

            process = subprocess.Popen(
                [command, *args],
                executable=full_path,
                stdin=previous_pipe,
                stdout=write_pipe,
            )
            processes.append(process)

        os.close(previous_pipe)
        os.close(write_pipe)
        return read_pipe

    def run_last(
        self,
        command,
        args,
        previous_pipe,
        processes,
    ):
        if command in self.shell.commands:
            result = self.shell.commands[command].execute(*args)

            if result is not None:
                sys.stdout.write(result)
                sys.stdout.flush()
            return

        full_path = self.shell.find_executable(command)

        process = subprocess.Popen(
            [command, *args],
            executable=full_path,
            stdin=previous_pipe,
            text=True,
        )
        processes.append(process)
