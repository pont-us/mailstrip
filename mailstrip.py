#!/usr/bin/env python3

"""Output the important bits of an email message as plain text

Raw email message is read from standard input.
A plain text representation of selected message headers and content
is written to standard output.

By Pontus Lurcock, 2020–2022. Released into the public domain.
"""

import sys
import email
import email.policy


def main():
    message = email.message_from_file(sys.stdin, policy=email.policy.SMTP)
    print_headers(message)
    print()
    body = message.get_body(preferencelist=("plain", "html", "related"))
    print(body.get_content())


def print_headers(message):
    for header in "from", "to", "subject", "date":
        if header in message:
            print(header.capitalize() + ": " + message[header])


if __name__ == "__main__":
    main()
