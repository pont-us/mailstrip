#!/usr/bin/python

'Print the important bits of an email message'

import email, sys

message = email.message_from_file(sys.stdin)
for header in 'from to subject date'.split(' '):
    if header in message:
        print header.capitalize()+': '+message[header]

payload = message
while (type(payload) != str):
    payload = payload.get_payload(decode = not payload.is_multipart())
    if (type(payload) == list): payload = payload[0]

print
css = []
cs = message.get_content_charset()
if (cs==None):
    # the filter removes the 'None' elements (since None is false)
    css = filter(None, message.get_charsets())
    if len(css)>0: cs = css[0]
    else: cs = 'ascii' # fallback
payload_u = unicode(payload, cs)
print payload_u.encode('utf-8')
