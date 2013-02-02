def lookup_lm_hash(hash):
    pass


def lookup_nt_hash(hash):
    pass


def convert_lm_to_ntlm(lm_plain, nt):
    pass


def crack_passwords(request):
    for p in request['passwords']:
        lm_plain = lookup_lm_hash(p['lm'])
        nt_plain = lookup_nt_hash(p['nt'])

        if nt_plain is not None:
            p['plain'] = nt_plain
        else:
            if lm_plain is not None:
                p['plain'] = convert_lm_to_ntlm(lm_plain, p['nt'])
            else:
                p['plain'] = None

    return request

def update_crack_count(ck):
    pass