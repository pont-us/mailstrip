#!/usr/bin/env python3

"""Output the important bits of an email message as plain text

Raw email message is read from standard input.
A plain text representation of selected message headers and content
is written to standard output.
If an argument is given, it is interpreted as a directory path, and the
message and its attachments are saved to files in this directory.

By Pontus Lurcock, 2020–2023. Released into the public domain.
"""

import sys
import email
import email.policy
import argparse
import pathlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="write message and attachments to this directory",
    )
    args = parser.parse_args()
    message = email.message_from_file(sys.stdin, policy=email.policy.SMTP)
    if args.output_dir is None:
        write_some_headers_and_body(sys.stdout, message)
    else:
        output_path = pathlib.Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        with open(str(output_path.joinpath("email.txt")), "w") as fh:
            write_some_headers_and_body(fh, message)
        for part in message.walk():
            if part.is_attachment():
                attachment_path = output_path.joinpath(part.get_filename())
                with open(str(attachment_path), "wb") as fh:
                    fh.write(part.get_content())


def write_some_headers_and_body(
    destination, message: email.message.EmailMessage
):
    write_headers(destination, message)
    destination.write("\n")
    body = message.get_body(preferencelist=("plain", "html", "related"))
    destination.write(body.get_content() + "\n")


def write_headers(destination, message):
    for header in "from", "to", "subject", "date":
        if header in message:
            destination.write(
                header.capitalize() + ": " + message[header] + "\n"
            )


if __name__ == "__main__":
    main()
