from eidos_cli.terminal2 import EidolonCLI


def main():
    import sys

    app = EidolonCLI()
    sys.exit(app.main())


if __name__ == "__main__":
    main()
