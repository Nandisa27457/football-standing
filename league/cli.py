"""Command-line interface for the league standings app."""

import argparse
import sys
from typing import TextIO

from league.formatter import format_table
from league.parser import ParseError, parse_matches
from league.standings import calculate_standings


def _read_lines(input_file: str | None) -> tuple[TextIO, bool]:
    if input_file is None:
        return sys.stdin, False
    return open(input_file, encoding="utf-8"), True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?")
    parser.add_argument("-o", dest="output_file", metavar="OUTPUT_FILE")
    args = parser.parse_args(argv)

    input_stream: TextIO | None = None
    close_input = False
    output_stream: TextIO | None = None
    close_output = False
    try:
        input_stream, close_input = _read_lines(args.input_file)
        if args.output_file is None:
            output_stream = sys.stdout
        else:
            output_stream = open(args.output_file, "w", encoding="utf-8", newline="")
            close_output = True

        matches = parse_matches(input_stream)
        standings = calculate_standings(matches)
        output_stream.write(format_table(standings))
        return 0
    except ParseError as error:
        print(error, file=sys.stderr)
        return 1
    except OSError as error:
        filename = getattr(error, "filename", None)
        if filename:
            message = f"Cannot read or write file '{filename}': {error.strerror or error}"
        else:
            message = f"Cannot read or write file: {error}"
        print(message, file=sys.stderr)
        return 2
    finally:
        if close_input and input_stream is not None:
            input_stream.close()
        if close_output and output_stream is not None:
            output_stream.close()


if __name__ == "__main__":
    raise SystemExit(main())
