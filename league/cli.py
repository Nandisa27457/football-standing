
import argparse
import sys
from typing import TextIO

from league.formatter import format_table
from league.parser import ParseError, parse_matches
from league.standings import calculate_standings


def _read_lines(input_file: str | None) -> tuple[TextIO, bool]:
    # Read from standard input if no input file was provided.
    if input_file is None:
        return sys.stdin, False

    # Open the specified input file and indicate that it must be closed later.
    return open(input_file, encoding="utf-8"), True


def main(argv: list[str] | None = None) -> int:
    # Create the command-line argument parser.
    parser = argparse.ArgumentParser()

    # Allow the user to provide an optional input file.
    parser.add_argument("input_file", nargs="?")

    # Allow the user to specify an output file using the -o option.
    parser.add_argument("-o", dest="output_file", metavar="OUTPUT_FILE")

    # Read the command-line arguments.
    args = parser.parse_args(argv)

    # Initialise the input and output streams and their close flags.
    input_stream: TextIO | None = None
    close_input = False
    output_stream: TextIO | None = None
    close_output = False

    try:
        # Open the input file or use standard input.
        input_stream, close_input = _read_lines(args.input_file)

        # Write to the terminal if no output file was specified.
        if args.output_file is None:
            output_stream = sys.stdout
        else:
            # Open the output file for writing, using UTF-8 encoding.
            # newline="" lets the CSV writer control line endings.
            output_stream = open(
                args.output_file, "w", encoding="utf-8", newline=""
            )
            close_output = True

        # Parse the input lines into Match objects.
        matches = parse_matches(input_stream)

        # Calculate each team's statistics and sort the standings.
        standings = calculate_standings(matches)

        # Format the standings as CSV and write them to the output stream.
        output_stream.write(format_table(standings))

        # Return 0 to indicate that the program completed successfully.
        return 0

    except ParseError as error:
        # Display invalid input errors on standard error and return exit code 1.
        print(error, file=sys.stderr)
        return 1

    except OSError as error:
        # Handle file-related errors, such as missing files or write failures.
        filename = getattr(error, "filename", None)

        # Include the filename in the message when it is available.
        if filename:
            message = (
                f"Cannot read or write file '{filename}': "
                f"{error.strerror or error}"
            )
        else:
            message = f"Cannot read or write file: {error}"

        # Display the error message and return exit code 2.
        print(message, file=sys.stderr)
        return 2

    finally:
        # Close the input file only if this program opened it.
        # Do not close standard input.
        if close_input and input_stream is not None:
            input_stream.close()

        # Close the output file only if this program opened it.
        # Do not close standard output.
        if close_output and output_stream is not None:
            output_stream.close()


# Run the CLI when this file is executed directly.
if __name__ == "__main__":
    # Exit with the status code returned by main().
    raise SystemExit(main())