import re


class VariableManager:
    def __init__(self):
        self.variables = {}

    def expand(self, parts):
        expanded = []

        for part in parts:
            part = re.sub(
                r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}"
                r"|\$([a-zA-Z_][a-zA-Z0-9_]*)",
                lambda match: self.variables.get(
                    match.group(1) or match.group(2),
                    "",
                ),
                part,
            )

            if part != "":
                expanded.append(part)

        return expanded

    def declare(self, *args):
        if args[0] == "-p":
            if args[1] in self.variables:
                print(
                    f'declare -- {args[1]}='
                    f'"{self.variables[args[1]]}"'
                )
            else:
                print(
                    f"declare: {args[1]}: not found"
                )
            return

        name, value = args[0].split("=")

        if re.match(
            r"^[a-zA-Z_][a-zA-Z0-9_]*$",
            name,
        ):
            self.variables[name] = value
        else:
            print(
                f"declare: `{args[0]}': "
                f"not a valid identifier"
            )
