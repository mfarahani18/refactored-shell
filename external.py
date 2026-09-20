import os
import subprocess


class ExternalCommandRunner:
    def find_executable(self, command):
        path = os.environ.get("PATH", "")
        paths = path.split(os.pathsep)

        for directory in paths:
            full_path = os.path.join(directory, command)

            if (
                os.path.isfile(full_path)
                and os.access(full_path, os.X_OK)
            ):
                return full_path

            for ext in [".exe", ".cmd", ".bat"]:
                candidate = full_path + ext

                if os.path.isfile(candidate):
                    return candidate

        return None

    def find_executable_by_prefix(self, prefix):
        matches = []
        path = os.environ.get("PATH", "")
        paths = path.split(os.pathsep)

        for path in paths:
            if not os.path.isdir(path):
                continue

            for file_name in os.listdir(path):
                if not file_name.startswith(prefix):
                    continue

                full_path = os.path.join(path, file_name)

                if (
                    os.path.isfile(full_path)
                    and os.access(full_path, os.X_OK)
                    and file_name not in matches
                ):
                    matches.append(file_name)

        return matches

    def run(self, command, *args, capture=False):
        full_path = self.find_executable(command)

        if full_path:
            if capture:
                result = subprocess.run(
                    [command, *args],
                    executable=full_path,
                    capture_output=True,
                    text=True,
                )
                return result.stdout, result.stderr

            subprocess.run(
                [command, *args],
                executable=full_path,
            )
            return None

        if capture:
            return "", f"{command}: command not found\n"

        print(f"{command}: command not found")
        return ""
