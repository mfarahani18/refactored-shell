import os


class HistoryManager:
    def __init__(self):
        self.history_data = []
        self.last_append_index = 0
        self.histfile = os.environ.get("HISTFILE")
        self.load()

    def load(self):
        if not self.histfile:
            return

        with open(self.histfile) as file:
            for line in file:
                line = line.rstrip("\n")
                if line:
                    self.history_data.append(line)

        self.last_append_index = len(self.history_data)

    def history(self, *args):
        if not args:
            self.print_full()
        elif args[0] == "-r":
            self.read_file(args[1])
        elif args[0] == "-w":
            self.write_file(args[1], self.history_data)
        elif args[0] == "-a":
            self.append_file(args[1])
        else:
            self.print_recent(int(args[0]))

    def print_full(self):
        for number, command in enumerate(
            self.history_data, start=1
        ):
            print(f"{number} {command}")

    def read_file(self, path):
        with open(path) as file:
            for line in file:
                line = line.rstrip("\n")
                if line:
                    self.history_data.append(line)

    def write_file(self, path, history):
        with open(path, "w") as file:
            for command in history:
                file.write(command + "\n")

    def append_file(self, path):
        with open(path, "a") as file:
            for command in self.history_data[
                self.last_append_index:
            ]:
                file.write(command + "\n")

        self.last_append_index = len(self.history_data)

    def print_recent(self, number):
        recent_history = self.history_data[-number:]
        start = len(self.history_data) - number + 1

        for index, command in enumerate(
            recent_history,
            start=start,
        ):
            print(f"{index} {command}")
