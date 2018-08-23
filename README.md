# A soundboard for RaspberryPi
Built for, but not limited to RaspberryPi (will run on most Unix based systems)

## Credits
This was originally forked from **Dude036** (https://github.com/Dude036/soundboard) and edited/improved. So credits to Dude036!

## Installation
Follow this tutorial: https://www.instructables.com/id/Raspberry-Pi-Soundboard/

...or:
Run `sudo apt-get install python3 python3-pip vlc libvlc-dev`


## Usage
Run `python3 main.py`

## Keycodes on the numpad:
`/`, `*`,<br>
`7`, `8`, `9`,<br>
`4`, `5`, `6`,<br>
`1`, `2`, `3`,<br>
`0`, `.`<br>
Sound 1-13
<br>

`+`<br>
Next page
<br>

`-`<br>
Previous page
<br>

`Backspace`<br>
Go to page 1
<br>

`Return` / `Enter`<br>
Stop playback of current sound
<br>

`Del` / `Delete`<br>
Plays all paths/URL's inside the `url.txt` file
`<br>

<br>

`Home`<br>
Reboot device (runs `sudo reboot`)
<br>

`End`<br>
Exits the program
<br>

`PageUp`<br>
Reconnect wifi (runs `sudo ifup wlan0`)
<br>

`PageDown`<br>
Disconnect wifi (runs `sudo ifdown wlan0`)
