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
    payload = extract_payload(message)
    print(payload)


def print_headers(message):
    for header in "from", "to", "subject", "date":
        if header in message:
            print(header.capitalize() + ": " + message[header])


def extract_payload(message):
    payload = message
    while type(payload) in (email.message.Message, email.message.EmailMessage):
        payload = payload.get_payload()
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
