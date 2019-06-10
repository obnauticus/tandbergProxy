import sip
import transport
import time
import media


def handle(params, message):
   
    print(message.replace('\r\n', '\n'))
    res = sip.parse_message(message)
    headers = res[0]
    header = headers[0]
    print("incoming <====== {}".format(header))
    
    if 'INVITE' in header:
        #sdp = res[2]
        #p = media.gst(media.parse_sdp(sdp))
    
        ir =  sip.create_invite_response(params, headers)
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        print(ir.replace('\r\n', '\n'))
        return ir
    elif 'ACK' in header:
        time.sleep(1)
        ir = sip.create_re_invite(params, sip.response_sdp2(params))
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        print(ir.replace('\r\n', '\n'))
        return ir
    elif 'Trying' in header:
        return ''
    elif '200 OK' in header:
        ir = sip.create_ack(params)
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        print(ir.replace('\r\n', '\n'))
        return ir
    
    elif 'BYE' in header:
        ir =  sip.create_bye_response(params, headers)
        #print("respond ======> {}".format(sip.parse_message(ir)[0]))
        print(ir.replace('\r\n', '\n'))
        return ir
    else:
        raise RuntimeError("{}  ...not implemented yet.".format(header))

def run(params):
    
    transport.server(params, handle)
    
    
    