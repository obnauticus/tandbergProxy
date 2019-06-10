import transport
import uuid

def response_sdp(params):
    
    text = '''v=0
o=qumu 166 2 IN IP4 {local_ip}
s=-
c=IN IP4 {local_ip}
t=0 0
m=audio 65066 RTP/AVP 0 101
a=rtpmap:0 PCMU/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-15
m=video 53146 RTP/AVP 126
a=label:11
a=rtpmap:126 H264/90000
a=fmtp:126 profile-level-id=42E014;packetization-mode=1;max-mbps=108000;max-fs=3600;max-cpb=100;max-dpb=5400;max-br=2500;max-rcmd-nalu-size=196608;max-fps=6000
a=content:main
m=video 0 RTP/AVP 31 34 96 97
a=rtpmap:97 H264/90000
a=content:slides
a=inactive
m=application 0 UDP/BFCP *
c=IN IP4 0.0.0.0
'''.format(local_ip=params['lh'])
    return text.replace('\n', '\r\n')


def response_sdp2(params):
    
    text = '''v=0
o=qumu 166 2 IN IP4 {local_ip}
s=-
c=IN IP4 {local_ip}
t=0 0
m=audio 65066 RTP/AVP 0 101
a=rtpmap:0 PCMU/8000
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-15
m=video 53146 RTP/AVP 126
a=label:11
a=rtpmap:126 H264/90000
a=fmtp:126 profile-level-id=42E014;packetization-mode=1;max-mbps=108000;max-fs=3600;max-cpb=100;max-dpb=5400;max-br=2500;max-rcmd-nalu-size=196608;max-fps=6000
a=content:main
m=video 0 RTP/AVP 31 34 96 97
a=rtpmap:97 H264/90000
a=content:slides
a=inactive
m=application 0 UDP/BFCP *
c=IN IP4 0.0.0.0
m=application 55522 RTP/AVP 100
a=rtpmap:100 H224/4800
'''.format(local_ip=params['lh'])
    return text.replace('\n', '\r\n')

def sdp(params):
    sdp_text = '''v=0
o=qumu 166 2 IN IP4 {local_ip}
s=-
c=IN IP4 {local_ip}
b=AS:512
t=0 0
m=audio {audio_port} RTP/AVP 9
a=rtpmap:9 G722/8000
m=video {video_port} RTP/AVP 126 97
a=rtpmap:126 H264/90000
a=fmtp:126 profile-level-id=42e014;max-mbps=47700;max-fs=1590;max-dpb=2385;max-fps=6000;packetization-mode=1;max-rcmd-nalu-size=196608
a=rtpmap:97 H264/90000
a=fmtp:97 profile-level-id=42e014;max-mbps=47700;max-fs=1590;max-dpb=2385;max-fps=6000;max-rcmd-nalu-size=196608
'''.format(local_ip=params['lh'], 
           audio_port=10000, 
           video_port=10002) 
    
    return sdp_text.replace('\n', '\r\n')

def sdp2(params):
    sdp_text = '''v=0
o=qumu 166 2 IN IP4 {local_ip}
s=-
c=IN IP4 {local_ip}
b=AS:512
t=0 0
m=audio {audio_port} RTP/AVP 9
a=rtpmap:9 G722/8000
m=video {video_port} RTP/AVP 126 97
a=rtpmap:126 H264/90000
a=fmtp:126 profile-level-id=42e014;max-mbps=47700;max-fs=1590;max-dpb=2385;max-fps=6000;packetization-mode=1;max-rcmd-nalu-size=196608
a=rtpmap:97 H264/90000
a=fmtp:97 profile-level-id=42e014;max-mbps=47700;max-fs=1590;max-dpb=2385;max-fps=6000;max-rcmd-nalu-size=196608
m=application 55522 RTP/AVP 100
a=rtpmap:100 H224/4800
'''.format(local_ip=params['lh'], 
           audio_port=10000, 
           video_port=10002) 
    
    return sdp_text.replace('\n', '\r\n')

def increment_seq(params):
    if not 'seq' in params:
        params['seq']=0
    params['seq']=params['seq']+1
    return params['seq']
    
def create_invite(params, sdp):
    params['branch']='z9hG4bK{}'.format(uuid.uuid4())
    params['local_tag']=uuid.uuid4()
    params['call_id']=uuid.uuid4()
    tag = ''
    seq = increment_seq(params)
    if 'peer_tag' in params:
        tag = ';tag={}'.format(params['peer_tag'])
    text = '''INVITE sip:{alias}@{rh}:{rp} SIP/2.0
Via: SIP/2.0/{transport} {lh}:{lp};branch={branch}
From: test <sip:test@{lh}:{lp}>;tag={local_tag}
To: sut <sip:{alias}@{rh}:{rp}>{tag_param}
Call-ID: {call_id}
CSeq: {seq} INVITE
Contact: sip:test@{lh}:{lp}
Max-Forwards: 70
Subject: Performance Test
Content-Type: application/sdp
Content-Length: {content_length}

{sdp_text}'''.replace('\n', '\r\n').format(alias=params['alias'],
                                           rh=params['rh'],
                                           rp=params['rp'],
                                           transport=params['transport'],
                                           branch=params['branch'],
                                           local_tag=params['local_tag'],
                                           tag_param=tag,
                                           call_id=params['call_id'],
                                           seq=params['seq'],
                                           lh=params['lh'],
                                           lp=params['lp'],
                                           content_length=len(sdp),
                                           sdp_text=sdp)

    return text

def create_ack(params):
    params['branch']='z9hG4bK{}'.format(uuid.uuid4())
    ack = '''ACK sip:{rh}:{rp} SIP/2.0
Via: SIP/2.0/{transport} {lh}:{lp};branch={branch}
From: test <sip:test@{lh}:{lp}>;tag={local_tag}
To: sut <sip:{alias}@{rh}:{rp}>;tag={peer_tag}
{call_id_header}
CSeq: {seq} ACK
Contact: sip:test@{lh}:{lp}
Max-Forwards: 70
Content-Length: 0

'''.format(alias=params['alias'],
           rh=params['rh'],
           rp=params['rp'],
           transport=params['transport'],
           branch=params['branch'],
           local_tag=params['local_tag'],
           peer_tag=params['peer_tag'],
           call_id_header=params["Call-ID"],
           seq=params['seq'],
           lh=params['lh'],
           lp=params['lp'])
    return ack.replace('\n', '\r\n')

def create_bye(params):
    params['branch']='z9hG4bK{}'.format(uuid.uuid4())
    increment_seq(params)
    bye = '''BYE sip:{rh}:{rp} SIP/2.0 
Via: SIP/2.0/{transport} {lh}:{lp};branch={branch}  
From: test <sip:test@{lh}:{lp}>;tag={local_tag}
To: sut <sip:{alias}@{rh}:{rp}>;tag={peer_tag}
Call-ID: {call_id}
CSeq: {seq} BYE 
Contact: sip:test@{lh}:{lp} 
Max-Forwards: 70
Content-Length: 0

'''.format(alias=params['alias'],
           rh=params['rh'],
           rp=params['rp'],
           transport=params['transport'],
           branch=params['branch'],
           local_tag=params['local_tag'],
           peer_tag=params['peer_tag'],
           call_id=params['call_id'],
           seq=params['seq'],
           lh=params['lh'],
           lp=params['lp'])
           
    return bye.replace('\n', '\r\n')

def parse_message(message):
    parts = message.split('\r\n\r\n')
    headers = parts[0].split('\r\n')
    sdp = None
    if len(parts) > 1:
        sdp = parts[1]
    return (headers, sdp)

def parse_response(message):
    return parse_message(message)

def get_status(headers):
    return int(headers[0].split()[1])
    
def get_tag(headers, header):   
    for h in headers:
        if header in h:
            parameters = h.split(';')
            for p in parameters:
                if 'tag=' in p:
                    return p[4:].rstrip()
    return None

def get_parameter(header, name):
    parameters = header.split(';')
    name = '{}='.format(name)
    for p in parameters:
        if name in p:
            return p[len(name):].rstrip()
    return None
    
def get_header(headers, name):
    for h in headers:
        if name in h:
            return h
    return None

def send_invite(params):
   
    i = create_invite(params, sdp(params))
    print("sent=============>")
    print(i.replace('\r\n', '\n'))
    transport.open_socket(params)
    transport.send_tcp(params, i)
    
def send_re_invite(params, sdp):
    
    i = create_re_invite(params, sdp)
    print("sent=============>")
    print(i.replace('\r\n', '\n'))
    transport.send_tcp(params, i)
    
def get_invite_response(params):
    r = transport.recv_tcp(params)
    print("<=============recv")
    print(r.replace('\r\n', '\n'))
    res= parse_response(r)
    headers = res[0]
    status = get_status(headers)
    params['Call-ID'] = get_header(headers, 'Call-ID')
    if (status == 200):
        params['peer_tag'] = get_tag(headers, 'To:')
    while (status < 200):
        r = transport.recv_tcp(params)
        print("<=============recv")
        print(r.replace('\r\n', '\n'))
        res= parse_response(r)
        headers = res[0]
        status = get_status(headers)
        print (status)
        if (status == 200):
            params['peer_tag'] = get_tag(headers, 'To:')
    return (status, headers, res[1])

def send_ack(params):
    
    a = create_ack(params)
    print("sent=============>")
    print(a.replace('\r\n', '\n'))
    transport.send_tcp(params, a)
    
def send_bye(params):
    
    b = create_bye(params)
    print("sent======>")
    print(b.replace('\r\n', '\n'))
    transport.send_tcp(params, b)
    r = transport.recv_tcp(params)
    print("<=============recv")
    print(r.replace('\r\n', '\n'))
    transport.close_socket(params)
    
def create_re_invite(params, sdp):
    params['branch']='z9hG4bK{}'.format(uuid.uuid4())
    increment_seq(params)
    from_text = 'From: {}'.format(params['To'][4:])
    to_text = 'To: {}'.format(params['From'][6:])
    params["From"] = from_text
    params["To"] = to_text

    text = '''INVITE sip:{alias}@{rh}:{rp} SIP/2.0
Via: SIP/2.0/{transport} {lh}:{lp};branch={branch}
{from_header}
{to_header}
{call_id_header}
CSeq: {seq} INVITE
Contact: sip:test@{lh}:{lp}
Max-Forwards: 70
Content-Type: application/sdp
Content-Length: {content_length}

{sdp_text}'''.replace('\n', '\r\n').format(alias=params['alias'],
                                           rh=params['rh'],
                                           rp=params['rp'],
                                           transport=params['transport'],
                                           branch=params['branch'],
                                           from_header=params["From"],
                                           to_header=params["To"],
                                           call_id_header=params["Call-ID"],
                                           seq=params['seq'],
                                           lh=params['lh'],
                                           lp=params['lp'],
                                           content_length=len(sdp),
                                           sdp_text=sdp)

    return text


def create_invite_response(params, headers):
    seq = int(get_header(headers, "CSeq").split()[1].strip())
    params['seq'] = seq
    params['branch'] = get_parameter(get_header(headers, "Via"), 'branch')
    params['local_tag'] = uuid.uuid4()
    params['From']=get_header(headers, "From")
    params['peer_tag'] = get_tag(headers, 'From:')
    
    params['Call-ID']=get_header(headers, "Call-ID")
    if not 'local_tag' in params:
        params['local_tag']=uuid.uuid4()
    tag = ';tag={}'.format(params['local_tag'])
    params['To']="{}{}".format(get_header(headers, "To"), tag)
    sdp = response_sdp(params)
    text = '''SIP/2.0 200 OK
Via: SIP/2.0/{transport} {lh}:{lp};branch={branch}
{from_header}
{to_header}
{call_id_header}
{cseq_header}
Contact: sip:test@{lh}:{lp}
Content-Type: application/sdp
Content-Length: {content_length}

{sdp_text}'''.replace('\n', '\r\n').format(transport=params['transport'],
                                           branch=params['branch'],
                                           tag_param=tag,
                                           lh=params['lh'],
                                           lp=params['lp'],
                                           from_header=params["From"],
                                           to_header=params["To"],
                                           call_id_header=params["Call-ID"],
                                           cseq_header=get_header(headers, "CSeq"),
                                           content_length=len(sdp),
                                           sdp_text=sdp)

    return text


def create_bye_response(params, headers):
    seq = int(get_header(headers, "CSeq").split()[1].strip())
    params['seq'] = seq
    params['branch'] = get_parameter(get_header(headers, "Via"), 'branch')
    params['local_tag'] = uuid.uuid4()
    params['From']=get_header(headers, "From")
    params['peer_tag'] = get_tag(headers, 'From:')
    
    params['Call-ID']=get_header(headers, "Call-ID")
    if not 'local_tag' in params:
        params['local_tag']=uuid.uuid4()
    tag = ';tag={}'.format(params['local_tag'])
    params['To']="{}{}".format(get_header(headers, "To"), tag)
    sdp = response_sdp(params)
    text = '''SIP/2.0 200 OK
Via: SIP/2.0/{transport} {lh}:{lp};branch={branch}
{from_header}
{to_header}
{call_id_header}
{cseq_header}
Contact: sip:test@{lh}:{lp}
Content-Length: 0
'''.replace('\n', '\r\n').format(transport=params['transport'],
                                           branch=params['branch'],
                                           tag_param=tag,
                                           lh=params['lh'],
                                           lp=params['lp'],
                                           from_header=params["From"],
                                           to_header=params["To"],
                                           call_id_header=params["Call-ID"],
                                           cseq_header=get_header(headers, "CSeq"),
                                           content_length=len(sdp),
                                           sdp_text=sdp)

    return text

    
