from shell import Shell
import readline


def main():
    shell = Shell()

    readline.set_completer(shell.autocomplete)
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(" \t\n")
    readline.set_completion_display_matches_hook(shell.display_matches)

    shell.run()


if __name__ == "__main__":
    main()
