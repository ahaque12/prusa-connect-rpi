# prusa-connect-rpi
Connect Raspberry Pi camera to Prusa Connect

I had an old Octopi setup that I wanted to repurpose to work with my Prusa MK4. This repo allows you to reuse the raspberry pi camera you have setup.

# Setup

## Environment variables
Update all environment variables in `config.env`. You will need `FINGERPRINT` and `TOKEN` from Prusa Connect. You can get the fingerprint by adding a new camera and looking at the request headers using Chrome Developer Tools (or similar). 

## Running
```bash
poetry install
nohup poetry run picam.py &
```

## Run as a service (linux)
Edit file
```bash
$ sudo vim /etc/systemd/system/prusa_picam.service
```
and include
```
[Unit]
Description=Prusa PiCam service
After=multi-user.target
[Service]
Type=simple
Restart=always
EnvironmentFile=/home/<username>/<path>/prusa-connect-rpi/config.env
ExecStart=/usr/bin/python3 /home/<username>/<path>/prusa-connect-rpi/picam.py
[Install]
WantedBy=multi-user.target
```
Note the python directory and path to file should be adjusted as needed. Environment file `config.env` should be edited to remove "export " prefix on each line.
Reload the daemon and start the service
```bash
$ sudo systemctl daemon-reload
$ sudo systemctl enable prusa_picam.service
$ sudo systemctl start prusa_picam.service
```

You can look at the logs for the service with
```bash
$ journalctl -u prusa_picam.service -f -n 100
```
# FAQ
**I already have octopi running and don't want to shut down the service, can I reuse the web stream?**

Yes, you can set the `STREAM_URL` in `config.env` to the stream. In my case it is `http://octopi.local/webcam/?action=stream`
