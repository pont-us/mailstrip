#!/usr/bin/env python3

"""Print the important bits of an email message.

Raw email message is read from standard input.
A plain text representation of selected message headers and content
is written to standard output.

By Pontus Lurcock, 2020. Released into the public domain.
"""

import email
import sys


def main():
    message = email.message_from_file(sys.stdin)
    print_headers(message)
    print()
    payload = extract_payload(message)
    charset = get_charset(message)
    print(str(payload, encoding=charset))


def print_headers(message):
    for header in "from", "to", "subject", "date":
        if header in message:
            print(header.capitalize() + ": " + message[header])


def extract_payload(message):
    payload = message
    while type(payload) == email.message.Message:
        payload = payload.get_payload(decode=not payload.is_multipart())
        if type(payload) == list:
            payload = payload[0]
    return payload


def get_charset(message):
    charset = message.get_content_charset()
    if charset is None:
        # the filter removes the "None" elements (since None is false)
        charsets = list(filter(None, message.get_charsets()))
        if len(charsets) > 0:
            charset = charsets[0]
        else:
            charset = "ascii"  # fallback
    return charset


if __name__ == "__main__":
    main()
