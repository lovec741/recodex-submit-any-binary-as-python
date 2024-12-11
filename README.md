# Recodex - Submit Any Binary as Python
# !!! This project is no longer actively maintained. If you want support for more languages with more features then you should look into [rustcodex](https://github.com/rkuklik/rustcodex).

This Python script converts a compiled binary and it's source code into a single Python script for submission to Recodex.

## Disclaimer

This script should only be used if your instructor has explicitly approved submitting your code written in a different programming language. For example, this might be appropriate if the exercise was adapted from another source and the instructor is flexible about the programming language used. Always confirm with your instructor before using this method for submission.

## Usage

This script has the following positional arguments:

* `binary`: Path to the compiled binary to be run
* `src`: Path to the source directory (should only include text files)
* `output`: Path to the output script (default: ./out.py)

Example usage:

> python3 convert_for_recodex.py target/release/example_binary src
