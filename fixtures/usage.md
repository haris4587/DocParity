# Greeting CLI

Run from the repository root with Python 3.11 or later. No packages are needed.

The --name parameter selects the person to greet.

    python fixtures/cli.py --name Ada

Expected exit code: 0
Expected output: Hello, Ada!

## Obsolete example

The --uppercase parameter prints the greeting in uppercase.

    python fixtures/cli.py --uppercase

Expected exit code: 0
Expected output: HELLO, DEVELOPER!

## Unsupported guarantee

The greeting command encrypts the output before printing it.

    python fixtures/cli.py --name Ada

Expected exit code: 0
Expected output: Hello, Ada!
