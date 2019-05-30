# tandbergProxy
Scripts to repurpose cisco tandberg equipment as generic RTSP camera streams

## Dependancies
1. Uses PJSIP / SIPSimple for initiating the stream


## Workflow
1. Initiate SIP session
2. Get tandberg capabilities (m= line in SIP/SDP session).
3. Pipe stream info into FFMPEG and serve over HTTP for external use-case
