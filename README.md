# prusa-connect-rpi
Connect Raspberry Pi camera to Prusa Connect

I had an old octopi setup that I wanted to repurpose to work with my Prusa MK4. This allows you to reuse your rpi camera you have setup.

# Running
```bash
poetry install
nohup poetry run picam.py &
```

# Setup as a service (linux)
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
ExecStart=/usr/bin/python3 /home/<username>/<path>/prusa-connect-rpi/picam.py
[Install]
WantedBy=multi-user.target
```
Note the python directory and path to file should be adjusted as needed. Reload the daemon and start the service
```bash
$ sudo systemctl daemon-reload
$ sudo systemctl enable prusa_picam.service
$ sudo systemctl start prusa_picam.service
```
