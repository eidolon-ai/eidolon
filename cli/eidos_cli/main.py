from eidos_cli.terminal import SubcommandsExample


def main():
    import sys

    app = SubcommandsExample()
    sys.exit(app.cmdloop())


if __name__ == "__main__":
    main()
