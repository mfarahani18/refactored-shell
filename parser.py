class Parser:
    def parse(self, text):
        args = []
        word = ""

        in_single_quotes = False
        in_double_quotes = False
        escape_next = False

        for i, char in enumerate(text):
            if escape_next:
                word += char
                escape_next = False
                continue

            if char == "\\":
                if in_single_quotes:
                    word += char
                elif in_double_quotes:
                    if (
                        i + 1 < len(text)
                        and text[i + 1] in ['"', "\\"]
                    ):
                        escape_next = True
                    else:
                        word += char
                else:
                    escape_next = True
                continue

            if char == "'" and not in_double_quotes:
                in_single_quotes = not in_single_quotes
            elif char == '"' and not in_single_quotes:
                in_double_quotes = not in_double_quotes
            elif (
                char.isspace()
                and not in_single_quotes
                and not in_double_quotes
            ):
                if word:
                    args.append(word)
                    word = ""
            else:
                word += char

        if word:
            args.append(word)

        return args
