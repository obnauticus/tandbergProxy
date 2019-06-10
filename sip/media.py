import subprocess, platform, re

def parse_sdp(sdp):
    state = 'start'
    vport = None
    for line in sdp.split('\n'):
        if 'start' in state:
            if 'c=' in line:
                con = line.split()[2]
        
        if 'm=audio' in line:
            state = 'audio'
            aport = line.split()[1]
        if 'm=video' in line and vport == None:
            state = 'video'
            vport = line.split()[1]
        if 'video' in state :
            if 'a=rtpmap' in line and 'H264' in line:
                m = re.match('a=rtpmap:\s*(\d+)', line)
                vptype = m.group(1)
        if 'audio' in state:
            if 'a=rtpmap' in line and 'G722' in line:
                m = re.match('a=rtpmap:\s*(\d+)', line)
                aptype = m.group(1)             
    return (con, aport, aptype, vport, vptype)

def gst(addrs):
    
    host = addrs[0]
    vport= int(addrs[3])
    vptype = addrs[4]
    aport = int(addrs[1])
    aptype = addrs[2]
    cmd = 'C:\\gstreamer\\1.0\\x86_64\\bin\\gst-launch-1.0'
    if 'Linux' in platform.system():
        cmd = 'gst-launch-1.0 '
    args = ''' rtpbin name=rtpbin \
        videotestsrc ! videoconvert ! x264enc ! rtph264pay ! \
         application/x-rtp, media=(string)video, payload=(int){vp}, clock-rate=(int)90000, encoding-name=(string)H264 ! \
         rtpbin.send_rtp_sink_0 \
                  rtpbin.send_rtp_src_0 ! udpsink port={vrtpport} host={host_ip}                            \
                  rtpbin.send_rtcp_src_0 ! udpsink port={vrtcpport} host={host_ip} sync=false async=false    \
                  udpsrc port=5005 ! rtpbin.recv_rtcp_sink_0                           \
        audiotestsrc ! avenc_g722 ! rtpg722pay ! \
        application/x-rtp, media=(string)audio, payload=(int){ap}, clock-rate=(int)8000, encoding-name=(string)G722 ! \
         rtpbin.send_rtp_sink_1                   \
                  rtpbin.send_rtp_src_1 ! udpsink port={artpport}  host={host_ip}                           \
                  rtpbin.send_rtcp_src_1 ! udpsink port={artcpport}  host={host_ip} sync=false async=false    \
                  udpsrc port=5007 ! rtpbin.recv_rtcp_sink_1'''.format(host_ip=host,
                                                                       vp=vptype,
                                                                       vrtpport=vport, 
                                                                       vrtcpport=vport+1,
                                                                       ap=aptype,
                                                                       artpport=aport,
                                                                       artcpport=aport+1)
    
    
    p = subprocess.Popen(cmd + args)
    return p