#!/usr/bin/env python3

"""Output the important bits of an email message as plain text

Raw email message is read from standard input.
A plain text representation of selected message headers and content
is written to standard output.

By Pontus Lurcock, 2020–2023. Released into the public domain.
"""

import sys
import email
import email.policy


def main():
    message = email.message_from_file(sys.stdin, policy=email.policy.SMTP)
    write_some_headers_and_body(sys.stdout, message)


def write_some_headers_and_body(
        destination,
        message: email.message.EmailMessage
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
