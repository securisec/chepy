
# Examples

### Solving a CTF channel
We are given a file called encoding which contains the following string.

```
=0GDAqREMS0EEWHGOEHJWWRAZqGDHAyHDSxDWyHImRHEEcIGOAyZMqHDPyHFScIDUSyDASREMS0EYS0AWEyJMyRARyHDQWGGUSxJAqREEy1EIWHFOAIDXqHHP1HDRyIDUSyHQySFPImEGW0AOAHHWqHIPy0GHcIDSAyJAS0DEEmEGWHGOEHJOqHHP1HIOMwDVIREFySFESHEMcIGOAxZMqHDP5HFRSIDSIyHASREMS0EEWHGOExEEOSJn5HGSMwDSSxJBqREEEmEHWHFAExZOIHDX1HERyIDUSyDASREMyxD0DxJUE0DFOIDPyHFRAGDSEyJAS0DlR1EOWHFYIIJOqHHP1HDRyIDUgHD3ZSEP50E0DHFOASAAqHDF1HFRSIGUEyDWS0DPM0EEWHGOEHJOqHHFAHJLAyDVIyD3R0DEI1EKWHFEEyJOIHIn1HDQSIDVWyDASREMS0EEWHGISxAnyxHP9HJVSIDSqyDBS0HM10EOW0GUEHHOIxIX1HDRyIDUSyDASRETSSHFWyGUIxAPIHDX10ERSIJUEyDWqRElRHEOWIGQEHJOqHHP1HDRyIFPEQGFq0EQWSHOWHFYExZOIRIF5HDQWGHUSxDW1HEMS0EEWHGOEHJOq0FOqGIHcIHCEQEWS0HO50EOcIGUEHHEqRJPyHDGWxDUSyDASREMS0EEW1DMuSJP9RIQqGDQSIJWqyDWSRImRHEHcxGOAHHSuHHP1HDRyIDUSyDAIID24RHUAxIMuHHOI0Dl4HDQAGHUSxDBgREESHEKWHGOEHJOqHHP1HDRMHHDE0FmHRF2VHEOcIGWEHHEy0IPyHEHAGDSSxJASREMS0EEWHGOEHJWWRAmZGFLcxHDSxDW1HEmRHEIcyGOAyJIqHDPyHDRyIDUSyDASREMS0E
```

#### Script
We can script the solution using the following python script:
```python
from chepy import Chepy

c = (
    Chepy("/tmp/demo/encoding")
    .load_file()
    .reverse()
    .rot_13()
    .base64_decode()
    .base32_decode()
    .hexdump_to_str()
)
print(c.o)
StormCTF{Spot3:DcEC6181F48e3B9D3dF77Dd827BF34e0}
```

#### Cli
[![asciicast](https://asciinema.org/a/3yBYcxTVp1ZIF3e81Lp9ZBggu.svg)](https://asciinema.org/a/3yBYcxTVp1ZIF3e81Lp9ZBggu)

### Convert a png to asciiart

#### Script
```python
from chepy import Chepy

c = (
    Chepy("py.png")
    .load_file()
    .image_to_asciiart(art_width=60)
    .write('art.txt')
)
```
```
.::.:..................................................:.::.
.::......................................................::.
:.......................&SSSSSSSSSS!.......................:
...................*SSSSSSSSSSSSSSSSSSSS....................
..................SSSS$@SSSSSSSSSSSSSSSSSS..................
.................:SSS....SSSSSSSSSSSSSSSSSS.................
.................:SSS....SSSSSSSSSSSSSSSSSS.................
.................:SSSSSSSSSSSSSSSSSSSSSSSSS.................
..................SSSSSSSSSSSSSSSSSSSSSSSSS.................
..............................SSSSSSSSSSSSS.*****!..........
........SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.*********.......
......SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.**********......
.....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS.***********.....
.....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS..************....
....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS..************....
....SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS...*************....
....SSSSSSSSSSSSSSSS.....................***************....
....SSSSSSSSSSSSS....***********************************....
....SSSSSSSSSSSS...*************************************....
.....SSSSSSSSSSS..**************************************....
.....SSSSSSSSSSS..*************************************.....
......SSSSSSSSSS..************************************......
.......SSSSSSSSS..**********************************!.......
..........SSSSSS..************..............................
..................*************************.................
..................*************************.................
..................******************...****.................
..................*****************.....***.................
..................******************:.****..................
....................*********************...................
:.......................!***********:......................:
.::......................................................::.
.::.:..................................................:.::.
```

#### Cli
[![asciicast](https://asciinema.org/a/af0ANsUaDbcxjRxrrQk1BxUa9.svg)](https://asciinema.org/a/af0ANsUaDbcxjRxrrQk1BxUa9)

### Bruteforce xor
#### Script

```python
from chepy import Chepy

c = (
    Chepy("322422332435612c243232202624")
    .hex_to_str()
    .xor_bruteforce()
)
print(c.o)

{
    ...
    '3a': bytearray(b'\\x08\\x1e\\x18\\t\\x1e\\x0f[\\x16\\x1e\\x08\\x08\\x1a\\x1c\\x1e'),
    '3b': bytearray(b'\\t\\x1f\\x19\\x08\\x1f\\x0eZ\\x17\\x1f\\t\\t\\x1b\\x1d\\x1f'),
    '3c': bytearray(b'\\x0e\\x18\\x1e\\x0f\\x18\\t]\\x10\\x18\\x0e\\x0e\\x1c\\x1a\\x18'),
    '3d': bytearray(b'\\x0f\\x19\\x1f\\x0e\\x19\\x08\\\\\\x11\\x19\\x0f\\x0f\\x1d\\x1b\\x19'),
    '3e': bytearray(b'\\x0c\\x1a\\x1c\\r\\x1a\\x0b_\\x12\\x1a\\x0c\\x0c\\x1e\\x18\\x1a'),
    '3f': bytearray(b'\\r\\x1b\\x1d\\x0c\\x1b\\n^\\x13\\x1b\\r\\r\\x1f\\x19\\x1b'),
    '40': bytearray(b'rdbsdu!ldrr`fd'),
    '41': bytearray(b'secret message'),
    '42': bytearray(b'pf`qfw#nfppbdf'),
    '43': bytearray(b'qgapgv"ogqqceg'),
    '44': bytearray(b'v`fw`q%h`vvdb`'),
    ...
}
```