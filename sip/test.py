import sip
import media
import time
import sys
import server


def test_server():
    params={'alias':'test',
            'rh':'10.0.4.234',
            'rp':5060,
            'lh':'10.0.4.43',
            'lp':5060,
            'transport':'tcp',
            }
    server.run(params)
    
def test_re_invite():
    params={'alias':'test',
            'rh':'10.0.4.234',
            'rp':5060,
            'lh':'10.0.4.43',
            'lp':5060,
            'transport':'tcp',
            }
     
    sip.send_invite(params)
    res = sip.get_invite_response(params)
    if (res[0] > 299):
        sys.exit(1)
    sip.send_ack(params)
    print('in call...')
    time.sleep(1)
    sip.send_re_invite(params, sip.sdp2(params))
    res = sip.get_invite_response(params)
    sip.send_ack(params)
    if (res[0] == 200):
        sdp = res[2]
        p = media.gst(media.parse_sdp(sdp))
        time.sleep(30)
    p.kill()
    sip.send_bye(params)
    time.sleep(1)

def test_call_media():
    params={'alias':'test',
            'rh':'10.0.4.234',
            'rp':5060,
            'lh':'10.0.4.43',
            'lp':5060,
            'transport':'tcp',
            }
    sip.send_invite(params)
    res = sip.get_invite_response(params)
    if (res[0] > 299):
        sys.exit(1)
    sip.send_ack(params)
    print('in call...')
    sdp = res[2]
    p = media.gst(media.parse_sdp(sdp))
    time.sleep(30)
    p.kill()
    sip.send_bye(params)
    time.sleep(1)
    
def test_call2():
    params={'alias':'test',
            'rh':'10.0.4.234',
            'rp':5060,
            'lh':'10.0.4.43',
            'lp':5060,
            'transport':'tcp',
            }
    sip.send_invite(params)
    res = sip.get_invite_response(params)
    if (res[0] > 299):
        sys.exit(1)
    time.sleep(1)
    sip.send_ack(params)
    print('in call...')
    time.sleep(10)
    sip.send_bye(params)
    time.sleep(1)
    
    
    
#test_server()
test_call_media()
#test_call2()
