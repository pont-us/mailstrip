#!/usr/bin/env python3

"""Print the important bits of an email message"""

import email
import sys


def main():
    message = email.message_from_file(sys.stdin)
    for header in "from", "to", "subject", "date":
        if header in message:
            print header.capitalize() + ": " + message[header]

    payload = message
    while type(payload) != str:
        payload = payload.get_payload(decode=not payload.is_multipart())
        if type(payload) == list:
            payload = payload[0]

    print

    charset = message.get_content_charset()
    if charset is None:
        # the filter removes the "None" elements (since None is false)
        charsets = filter(None, message.get_charsets())
        if len(charsets) > 0:
            charset = charsets[0]
        else:
            charset = "ascii"  # fallback
    payload_u = unicode(payload, charset)
    print payload_u.encode("utf-8")


if __name__ == "__main__":
    main()
