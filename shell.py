import sys

from commands import (
    BaseCommand,
    CdCommand,
    CompleteCommand,
    DeclareCommand,
    EchoCommand,
    ExitCommand,
    HistoryCommand,
    JobsCommand,
    PwdCommand,
    TypeCommand,
)
from completion import CompletionManager
from external import ExternalCommandRunner
from history import HistoryManager
from jobs import JobManager
from parser import Parser
from pipeline import PipelineManager
from redirection import RedirectionManager
from variables import VariableManager


class Shell:
    redirect_symbols = [">", "1>", "2>", ">>", "1>>", "2>>"]

    def __init__(self):
        self.parser = Parser()
        self.variables_manager = VariableManager()
        self.history_manager = HistoryManager()
        self.job_manager = JobManager()
        self.external_runner = ExternalCommandRunner()
        self.completion_manager = CompletionManager(self.external_runner)
        self.redirection_manager = RedirectionManager(self)
        self.pipeline_manager = PipelineManager(self)

        self.commands = self._build_commands()
        self.completion_manager.bind_builtin_commands(self.builtin_commands)

    def _build_commands(self):
        commands = [
            ExitCommand(self),
            EchoCommand(self),
            PwdCommand(self),
            CdCommand(self),
            TypeCommand(self),
            CompleteCommand(self),
            JobsCommand(self),
            HistoryCommand(self),
            DeclareCommand(self),
        ]
        return {command.name: command for command in commands}

    @property
    def builtin_commands(self):
        return list(self.commands.keys())

    # Compatibility/state properties: the state now lives in managers.
    @property
    def completions(self):
        return self.completion_manager.completions

    @property
    def jobs_data(self):
        return self.job_manager.jobs_data

    @property
    def history_data(self):
        return self.history_manager.history_data

    @property
    def last_append_index(self):
        return self.history_manager.last_append_index

    @property
    def variables(self):
        return self.variables_manager.variables

    @property
    def histfile(self):
        return self.history_manager.histfile

    def run(self):
        while True:
            self.reap_jobs()

            try:
                user_input = input("$ ")
            except EOFError:
                break

            if not user_input.strip():
                continue

            self.history_data.append(user_input)
            self.execute_line(user_input)

    def execute_line(self, user_input):
        parts = self.parse_input(user_input)

        if not parts:
            return

        parts = self.expand_variables(parts)

        if "|" in parts:
            self.run_pipeline(parts)
            return

        command = parts[0]
        args = parts[1:]

        if args and args[-1] == "&":
            print(self.run_background(command, args, user_input))
            return

        if self._handle_redirection(command, args):
            return

        self._execute_command(command, args)

    def _execute_command(self, command, args):
        if command in self.commands:
            result = self.commands[command].execute(*args)
            if result is not None:
                sys.stdout.write(result)
        else:
            self.run_not_found(command, *args)

    # Facades keep the old Shell API while delegating responsibility.
    def parse_input(self, text):
        return self.parser.parse(text)

    def expand_variables(self, parts):
        return self.variables_manager.expand(parts)

    def declare(self, *args):
        return self.variables_manager.declare(*args)

    def find_executable(self, command):
        return self.external_runner.find_executable(command)

    def find_executable_by_prefix(self, prefix):
        return self.external_runner.find_executable_by_prefix(prefix)

    def run_not_found(self, command, *args, capture=False):
        return self.external_runner.run(command, *args, capture=capture)

    def autocomplete(self, text, state):
        return self.completion_manager.autocomplete(text, state)

    def display_matches(self, user_input, matches, longest_match_length):
        return self.completion_manager.display_matches(
            user_input, matches, longest_match_length
        )

    def complete(self, *args):
        return self.completion_manager.complete(*args)

    def _handle_redirection(self, command, args):
        return self.redirection_manager.handle(command, args)

    def redirect(self, command, real_args, file_name, symbol):
        return self.redirection_manager.redirect(
            command, real_args, file_name, symbol
        )

    def _run_for_redirection(self, command, args):
        return self.redirection_manager.run_for_redirection(command, args)

    def _redirect_stdout(self, file_name, output, append):
        return self.redirection_manager.redirect_stdout(
            file_name, output, append
        )

    def _redirect_stderr(self, file_name, error, append):
        return self.redirection_manager.redirect_stderr(
            file_name, error, append
        )

    def history(self, *args):
        return self.history_manager.history(*args)

    def _load_history(self):
        return self.history_manager.load()

    def _print_full_history(self):
        return self.history_manager.print_full()

    def _read_history_file(self, path):
        return self.history_manager.read_file(path)

    def _write_history_file(self, path, history):
        return self.history_manager.write_file(path, history)

    def _append_history_file(self, path):
        return self.history_manager.append_file(path)

    def _print_recent_history(self, number):
        return self.history_manager.print_recent(number)

    def run_background(self, command, args, original_command):
        return self.job_manager.run_background(
            command, args, original_command
        )

    def reap_jobs(self):
        return self.job_manager.reap_jobs()

    def jobs(self):
        return self.job_manager.jobs()

    def _job_marker(self, job_number, job_numbers):
        return self.job_manager.job_marker(job_number, job_numbers)

    def _print_running_job(self, job_number, data, job_numbers):
        return self.job_manager.print_running_job(
            job_number, data, job_numbers
        )

    def print_done_job(self, job_number, data, job_numbers):
        return self.job_manager.print_done_job(
            job_number, data, job_numbers
        )

    def run_pipeline(self, parts):
        return self.pipeline_manager.run(parts)

    def _split_pipeline(self, parts):
        return self.pipeline_manager.split(parts)

    def _run_first_pipeline_command(self, command, args, processes):
        return self.pipeline_manager.run_first(
            command, args, processes
        )

    def _run_middle_pipeline_command(
        self, command, args, previous_pipe, processes
    ):
        return self.pipeline_manager.run_middle(
            command, args, previous_pipe, processes
        )

    def _run_last_pipeline_command(
        self, command, args, previous_pipe, processes
    ):
        return self.pipeline_manager.run_last(
            command, args, previous_pipe, processes
        )
