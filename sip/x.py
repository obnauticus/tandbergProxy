import sip
import media

def test_parse():
    params={'alias':'broadcast1',
               'rh':'10.1.195.217',
               'rp':5060,
               'lh':'10.1.195.200',
               'lp':5060,
               'transport':'tcp',
               'branch':'z9hG4bKwxCUIdAXzfF9ByGk3mNljD68S4TsHJRW',
               'local_tag':'amrT5tq0Wekwn1iE',
               'call_id':'78b776d5-ec0a-4c25-b8a5-3a65f62d5acf'
               }
    
    i = sip.create_invite(params, sip.sdp(params))
    
    
    print(i)
    
    print("========sdp=======")
    print(sip.parse_message((i)[1]))
    
    print('media is {}'.format(media.parse_sdp(sip.parse_message(i)[1])))
    
    headers = sip.parse_message(i)[0]
    print("========headers=======")
    for header in headers:
        print(header)
        if 'To:' in header:
            to = header
    
    print("========tag=======")
    print(sip.get_tag(headers, "From:"))
    
    params['peer_tag'] = sip.get_tag(headers, "From:")
    a = sip.create_ack(params)
    
    print("========ack=======")
    print(a)