
# Examples

## Solving a CTF channel
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


## TAMUCTF challenge
The provided challenge string is:
```text
dah-dah-dah-dah-dah dah-di-di-dah di-di-di-di-dit dah-dah-di-di-dit dah-dah-di-di-dit dah-dah-dah-dah-dah di-di-dah-dah-dah di-dah dah-di-di-di-dit dah-di-dah-dit di-di-di-di-dit dah-dah-dah-di-dit dah-dah-di-di-dit di-di-di-di-dah di-di-di-di-dah dah-dah-di-di-dit di-di-di-di-dit di-dah-dah-dah-dah di-di-di-dah-dah dah-dah-dah-di-dit dah-di-di-di-dit di-di-di-di-dit di-di-di-dah-dah dah-dah-dah-di-dit dah-dah-di-di-dit di-dah-dah-dah-dah dah-di-di-di-dit dit dah-di-di-di-dit dah-di-dit di-di-di-di-dah dah-di-dit di-di-di-di-dit dah-dah-dah-dah-dit di-di-di-di-dit di-di-di-di-dit di-di-dah-dah-dah di-dah dah-dah-di-di-dit di-di-di-dah-dah dah-dah-di-di-dit dah-di-di-di-dit di-di-di-di-dah dah-di-di-di-dit di-di-di-di-dah dah-dah-dah-di-dit dah-di-di-di-dit dah-di-di-dit dah-di-di-di-dit di-dah di-di-di-di-dah dah-dah-dah-dah-dit dah-dah-di-di-dit di-di-di-di-dah di-di-dah-dah-dah di-dah di-di-di-di-dit di-di-dah-dah-dah di-di-di-di-dit di-dah-dah-dah-dah di-di-dah-dah-dah dah-di-di-di-dit di-di-di-di-dah di-dah dah-dah-di-di-dit dah-dah-dah-dah-dah di-di-di-di-dit di-dah dah-dah-di-di-dit dah-di-di-di-dit dah-di-di-di-dit di-dah dah-di-di-di-dit dah-di-dit di-di-dah-dah-dah di-dah-dah-dah-dah di-di-dah-dah-dah di-di-di-di-dit di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-dit di-di-di-di-dah di-di-di-di-dah dah-di-di-di-dit dah-di-di-dit dah-di-di-di-dit dah-di-di-di-dit dah-dah-di-di-dit dah-dah-dah-dah-dah di-di-dah-dah-dah di-di-di-dah-dah di-di-di-di-dit dit di-di-di-di-dah dit di-di-di-dah-dah dah-dah-dah-dah-dit dah-di-di-di-dit dah-di-di-di-dit dah-di-di-di-dit dah-di-di-dit di-di-di-dah-dah di-di-di-di-dah dah-di-di-di-dit di-di-di-di-dah di-di-di-di-dit di-di-di-di-dit di-di-di-dah-dah di-di-di-di-dah dah-di-di-di-dit dah-di-dah-dit di-di-di-di-dah di-di-dah-dah-dah di-di-di-dah-dah di-di-di-dah-dah dah-dah-di-di-dit di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-di-dit di-di-dah-dit di-di-di-di-dit di-di-di-di-dah di-di-di-dah-dah dah-dah-dah-dah-dah di-di-di-di-dit dah-dah-dah-dah-dah di-di-di-di-dit di-dah di-di-di-di-dit di-dah-dah-dah-dah dah-di-di-di-dit dah-di-dit di-di-di-di-dah di-di-di-dah-dah di-di-di-di-dit di-dah-dah-dah-dah di-di-di-di-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-dit di-di-di-di-dit dah-dah-dah-dah-dit di-di-di-di-dah di-di-dah-dah-dah di-di-di-dah-dah di-di-di-di-dah di-di-di-di-dit di-dah di-di-di-di-dah dah-di-dit dah-dah-di-di-dit dah-di-di-di-dit di-di-dah-dah-dah di-dah di-di-dah-dah-dah di-dah-dah-dah-dah di-di-di-di-dah dah-di-di-di-dit dah-di-di-di-dit dah-di-di-dit di-di-di-dah-dah dah-dah-dah-di-dit dah-di-di-di-dit dah-di-dah-dit di-di-dah-dah-dah di-di-di-di-dit dah-di-di-di-dit di-di-dah-dah-dah dah-di-di-di-dit di-dah dah-dah-di-di-dit di-dah-dah-dah-dah dah-di-di-di-dit dah-di-dah-dit di-di-di-di-dit dah-dah-dah-dah-dah di-di-di-di-dah dah-di-dit dah-di-di-di-dit dah-di-di-di-dit di-di-di-di-dah dah-dah-dah-dah-dit di-di-di-di-dah dah-dah-di-di-dit dah-di-di-di-dit dah-di-dit dah-di-di-di-dit di-dah-dah-dah-dah di-di-dah-dah-dah di-di-di-di-dit di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-di-dit dah-dah-di-di-dit di-dah di-di-di-di-dah dah-dah-di-di-dit di-di-dah-dah-dah dah-dah-dah-dah-dah dah-di-di-di-dit dah-dah-di-di-dit dah-di-di-di-dit dah-dah-dah-dah-dit dah-di-di-di-dit dah-dah-di-di-dit dah-di-di-di-dit di-di-di-di-dit dah-di-di-di-dit dah-di-dit dah-dah-di-di-dit dah-di-di-dit di-di-di-di-dah di-di-di-dah-dah di-di-di-dah-dah di-dah-dah-dah-dah dah-di-di-di-dit dah-dah-dah-dah-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-di-dah dah-di-di-dit di-di-di-di-dit di-di-dah-dit dah-di-di-di-dit di-di-di-dah-dah dah-di-di-di-dit dah-di-dah-dit di-di-di-dah-dah di-dah-dah-dah-dah di-di-di-di-dah di-di-di-dah-dah di-di-di-di-dah dah-di-di-dit di-di-dah-dah-dah dah-di-dit dah-dah-di-di-dit dah-dah-dah-dah-dit di-di-di-dah-dah dah-dah-dah-dah-dah dah-dah-di-di-dit di-di-di-di-dit di-di-di-di-dit di-di-dah-dit dah-di-di-di-dit dah-dah-dah-di-dit di-di-di-dah-dah di-di-di-di-dah dah-dah-di-di-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-dah-dah di-di-di-di-dit di-di-dah-dit dah-di-di-di-dit dah-di-dit di-di-di-dah-dah di-di-di-di-dah di-di-di-di-dah dah-dah-dah-dah-dit di-di-di-dah-dah di-dah-dah-dah-dah dah-dah-di-di-dit dah-di-dit di-di-dah-dah-dah dah-dah-dah-dah-dah dah-dah-di-di-dit di-di-di-di-dit dah-dah-di-di-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-di-dah dah-dah-di-di-dit dah-di-di-di-dit dah-dah-di-di-dit di-dah di-di-di-di-dah dah-di-di-dit di-di-di-di-dit di-dah dah-dah-di-di-dit di-di-di-di-dah di-di-di-dah-dah di-di-di-di-dah dah-dah-di-di-dit dah-dah-dah-dah-dit dah-di-di-di-dit di-di-dah-dit dah-di-di-di-dit dah-di-dit dah-di-di-di-dit dah-dah-dah-dah-dit di-di-di-di-dah di-di-di-di-dah di-di-di-di-dit di-di-di-dah-dah dah-di-di-di-dit dah-dah-dah-di-dit di-di-di-di-dah dah-di-dah-dit dah-di-di-di-dit dah-di-dit di-di-di-dah-dah dah-dah-dah-di-dit di-di-di-di-dit di-dah-dah-dah-dah di-di-di-di-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-di-dit dah-di-di-di-dit dit di-di-di-di-dit di-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dah dah-dah-di-di-dit dah-dah-di-di-dit di-di-di-di-dah di-dah di-di-di-di-dah dah-dah-dah-dah-dah di-di-di-di-dah dit dah-dah-di-di-dit di-di-di-di-dit di-di-di-di-dah di-di-dah-dit di-di-di-di-dit dah-dah-dah-dah-dit dah-di-di-di-dit dah-di-di-di-dit di-di-di-di-dit dah-dah-dah-di-dit di-di-dah-dah-dah dah-di-di-di-dit di-di-di-dah-dah dah-dah-dah-di-dit dah-dah-di-di-dit di-di-di-di-dit di-di-di-di-dah dah-dah-dah-dah-dah di-di-di-di-dah dah-dah-di-di-dit dah-di-di-di-dit dit di-di-dah-dah-dah di-dah-dah-dah-dah di-di-di-dah-dah di-dah-dah-dah-dah di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dit di-di-di-di-dah dah-dah-di-di-dit di-dah-dah-dah-dah dah-dah-di-di-dit dah-di-di-di-dit di-di-di-dah-dah dah-dah-dah-dah-dah di-di-di-di-dit dah-di-di-di-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-di-dit di-di-dah-dah-dah dah-dah-di-di-dit di-dah di-di-di-di-dit dah-di-di-di-dit di-di-dah-dah-dah di-dah-dah-dah-dah dah-di-di-di-dit di-dah di-di-dah-dah-dah di-dah-dah-dah-dah dah-dah-di-di-dit dah-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dit dah-dah-di-di-dit dah-dah-dah-dah-dah di-di-di-dah-dah dah-dah-dah-di-dit di-di-di-di-dah di-di-dah-dah-dah dah-di-di-di-dit di-dah dah-di-di-di-dit di-di-di-di-dah di-di-di-di-dah dit di-di-di-di-dah dah-dah-dah-dah-dit dah-dah-di-di-dit di-dah-dah-dah-dah di-di-di-di-dah di-di-di-di-dit di-di-di-dah-dah di-di-di-di-dit dah-dah-di-di-dit dah-dah-di-di-dit di-di-dah-dah-dah di-di-di-dah-dah di-di-dah-dah-dah di-di-di-di-dah di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-di-dah di-di-di-di-dit di-di-di-di-dit di-di-di-di-dit di-dah di-di-di-di-dah di-di-dah-dit di-di-di-di-dit dah-dah-dah-dah-dit di-di-di-di-dit di-dah di-di-di-dah-dah di-di-dah-dah-dah dah-dah-di-di-dit di-dah di-di-di-dah-dah dah-dah-di-di-dit di-di-di-di-dit di-di-di-di-dah di-di-di-dah-dah di-di-dah-dah-dah di-di-di-dah-dah di-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dah di-di-di-dah-dah dah-dah-di-di-dit di-di-dah-dah-dah dah-di-di-di-dit dah-dah-di-di-dit dah-dah-dah-di-dit di-di-di-di-dah dah-di-dah-dit di-di-di-di-dah dah-dah-dah-dah-dah di-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dah di-di-dah-dit di-di-di-dah-dah dah-dah-di-di-dit di-di-di-dah-dah di-di-di-di-dah di-di-di-dah-dah di-dah-dah-dah-dah di-di-di-dah-dah dah-dah-dah-dah-dah di-di-di-di-dit di-dah-dah-dah-dah di-di-di-di-dah dah-dah-dah-dah-dit
```

#### Script
```python
from chepy import Chepy

data = "dah-dah-dah-dah-dah dah-di-di-dah di-di-di-di-dit dah-dah-di-di-dit dah-dah-di-di-dit dah-dah-dah-dah-dah di-di-dah-dah-dah di-dah dah-di-di-di-dit dah-di-dah-dit di-di-di-di-dit dah-dah-dah-di-dit dah-dah-di-di-dit di-di-di-di-dah di-di-di-di-dah dah-dah-di-di-dit di-di-di-di-dit di-dah-dah-dah-dah di-di-di-dah-dah dah-dah-dah-di-dit dah-di-di-di-dit di-di-di-di-dit di-di-di-dah-dah dah-dah-dah-di-dit dah-dah-di-di-dit di-dah-dah-dah-dah dah-di-di-di-dit dit dah-di-di-di-dit dah-di-dit di-di-di-di-dah dah-di-dit di-di-di-di-dit dah-dah-dah-dah-dit di-di-di-di-dit di-di-di-di-dit di-di-dah-dah-dah di-dah dah-dah-di-di-dit di-di-di-dah-dah dah-dah-di-di-dit dah-di-di-di-dit di-di-di-di-dah dah-di-di-di-dit di-di-di-di-dah dah-dah-dah-di-dit dah-di-di-di-dit dah-di-di-dit dah-di-di-di-dit di-dah di-di-di-di-dah dah-dah-dah-dah-dit dah-dah-di-di-dit di-di-di-di-dah di-di-dah-dah-dah di-dah di-di-di-di-dit di-di-dah-dah-dah di-di-di-di-dit di-dah-dah-dah-dah di-di-dah-dah-dah dah-di-di-di-dit di-di-di-di-dah di-dah dah-dah-di-di-dit dah-dah-dah-dah-dah di-di-di-di-dit di-dah dah-dah-di-di-dit dah-di-di-di-dit dah-di-di-di-dit di-dah dah-di-di-di-dit dah-di-dit di-di-dah-dah-dah di-dah-dah-dah-dah di-di-dah-dah-dah di-di-di-di-dit di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-dit di-di-di-di-dah di-di-di-di-dah dah-di-di-di-dit dah-di-di-dit dah-di-di-di-dit dah-di-di-di-dit dah-dah-di-di-dit dah-dah-dah-dah-dah di-di-dah-dah-dah di-di-di-dah-dah di-di-di-di-dit dit di-di-di-di-dah dit di-di-di-dah-dah dah-dah-dah-dah-dit dah-di-di-di-dit dah-di-di-di-dit dah-di-di-di-dit dah-di-di-dit di-di-di-dah-dah di-di-di-di-dah dah-di-di-di-dit di-di-di-di-dah di-di-di-di-dit di-di-di-di-dit di-di-di-dah-dah di-di-di-di-dah dah-di-di-di-dit dah-di-dah-dit di-di-di-di-dah di-di-dah-dah-dah di-di-di-dah-dah di-di-di-dah-dah dah-dah-di-di-dit di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-di-dit di-di-dah-dit di-di-di-di-dit di-di-di-di-dah di-di-di-dah-dah dah-dah-dah-dah-dah di-di-di-di-dit dah-dah-dah-dah-dah di-di-di-di-dit di-dah di-di-di-di-dit di-dah-dah-dah-dah dah-di-di-di-dit dah-di-dit di-di-di-di-dah di-di-di-dah-dah di-di-di-di-dit di-dah-dah-dah-dah di-di-di-di-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-dit di-di-di-di-dit dah-dah-dah-dah-dit di-di-di-di-dah di-di-dah-dah-dah di-di-di-dah-dah di-di-di-di-dah di-di-di-di-dit di-dah di-di-di-di-dah dah-di-dit dah-dah-di-di-dit dah-di-di-di-dit di-di-dah-dah-dah di-dah di-di-dah-dah-dah di-dah-dah-dah-dah di-di-di-di-dah dah-di-di-di-dit dah-di-di-di-dit dah-di-di-dit di-di-di-dah-dah dah-dah-dah-di-dit dah-di-di-di-dit dah-di-dah-dit di-di-dah-dah-dah di-di-di-di-dit dah-di-di-di-dit di-di-dah-dah-dah dah-di-di-di-dit di-dah dah-dah-di-di-dit di-dah-dah-dah-dah dah-di-di-di-dit dah-di-dah-dit di-di-di-di-dit dah-dah-dah-dah-dah di-di-di-di-dah dah-di-dit dah-di-di-di-dit dah-di-di-di-dit di-di-di-di-dah dah-dah-dah-dah-dit di-di-di-di-dah dah-dah-di-di-dit dah-di-di-di-dit dah-di-dit dah-di-di-di-dit di-dah-dah-dah-dah di-di-dah-dah-dah di-di-di-di-dit di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-di-dit dah-dah-di-di-dit di-dah di-di-di-di-dah dah-dah-di-di-dit di-di-dah-dah-dah dah-dah-dah-dah-dah dah-di-di-di-dit dah-dah-di-di-dit dah-di-di-di-dit dah-dah-dah-dah-dit dah-di-di-di-dit dah-dah-di-di-dit dah-di-di-di-dit di-di-di-di-dit dah-di-di-di-dit dah-di-dit dah-dah-di-di-dit dah-di-di-dit di-di-di-di-dah di-di-di-dah-dah di-di-di-dah-dah di-dah-dah-dah-dah dah-di-di-di-dit dah-dah-dah-dah-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-di-dah dah-di-di-dit di-di-di-di-dit di-di-dah-dit dah-di-di-di-dit di-di-di-dah-dah dah-di-di-di-dit dah-di-dah-dit di-di-di-dah-dah di-dah-dah-dah-dah di-di-di-di-dah di-di-di-dah-dah di-di-di-di-dah dah-di-di-dit di-di-dah-dah-dah dah-di-dit dah-dah-di-di-dit dah-dah-dah-dah-dit di-di-di-dah-dah dah-dah-dah-dah-dah dah-dah-di-di-dit di-di-di-di-dit di-di-di-di-dit di-di-dah-dit dah-di-di-di-dit dah-dah-dah-di-dit di-di-di-dah-dah di-di-di-di-dah dah-dah-di-di-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-dah-dah di-di-di-di-dit di-di-dah-dit dah-di-di-di-dit dah-di-dit di-di-di-dah-dah di-di-di-di-dah di-di-di-di-dah dah-dah-dah-dah-dit di-di-di-dah-dah di-dah-dah-dah-dah dah-dah-di-di-dit dah-di-dit di-di-dah-dah-dah dah-dah-dah-dah-dah dah-dah-di-di-dit di-di-di-di-dit dah-dah-di-di-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-di-dah dah-dah-di-di-dit dah-di-di-di-dit dah-dah-di-di-dit di-dah di-di-di-di-dah dah-di-di-dit di-di-di-di-dit di-dah dah-dah-di-di-dit di-di-di-di-dah di-di-di-dah-dah di-di-di-di-dah dah-dah-di-di-dit dah-dah-dah-dah-dit dah-di-di-di-dit di-di-dah-dit dah-di-di-di-dit dah-di-dit dah-di-di-di-dit dah-dah-dah-dah-dit di-di-di-di-dah di-di-di-di-dah di-di-di-di-dit di-di-di-dah-dah dah-di-di-di-dit dah-dah-dah-di-dit di-di-di-di-dah dah-di-dah-dit dah-di-di-di-dit dah-di-dit di-di-di-dah-dah dah-dah-dah-di-dit di-di-di-di-dit di-dah-dah-dah-dah di-di-di-di-dah di-di-di-di-dit di-di-di-di-dah dah-di-di-di-dit dah-di-di-di-dit dit di-di-di-di-dit di-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dah dah-dah-di-di-dit dah-dah-di-di-dit di-di-di-di-dah di-dah di-di-di-di-dah dah-dah-dah-dah-dah di-di-di-di-dah dit dah-dah-di-di-dit di-di-di-di-dit di-di-di-di-dah di-di-dah-dit di-di-di-di-dit dah-dah-dah-dah-dit dah-di-di-di-dit dah-di-di-di-dit di-di-di-di-dit dah-dah-dah-di-dit di-di-dah-dah-dah dah-di-di-di-dit di-di-di-dah-dah dah-dah-dah-di-dit dah-dah-di-di-dit di-di-di-di-dit di-di-di-di-dah dah-dah-dah-dah-dah di-di-di-di-dah dah-dah-di-di-dit dah-di-di-di-dit dit di-di-dah-dah-dah di-dah-dah-dah-dah di-di-di-dah-dah di-dah-dah-dah-dah di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dit di-di-di-di-dah dah-dah-di-di-dit di-dah-dah-dah-dah dah-dah-di-di-dit dah-di-di-di-dit di-di-di-dah-dah dah-dah-dah-dah-dah di-di-di-di-dit dah-di-di-di-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-di-dit di-di-dah-dah-dah dah-dah-di-di-dit di-dah di-di-di-di-dit dah-di-di-di-dit di-di-dah-dah-dah di-dah-dah-dah-dah dah-di-di-di-dit di-dah di-di-dah-dah-dah di-dah-dah-dah-dah dah-dah-di-di-dit dah-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dit dah-dah-di-di-dit dah-dah-dah-dah-dah di-di-di-dah-dah dah-dah-dah-di-dit di-di-di-di-dah di-di-dah-dah-dah dah-di-di-di-dit di-dah dah-di-di-di-dit di-di-di-di-dah di-di-di-di-dah dit di-di-di-di-dah dah-dah-dah-dah-dit dah-dah-di-di-dit di-dah-dah-dah-dah di-di-di-di-dah di-di-di-di-dit di-di-di-dah-dah di-di-di-di-dit dah-dah-di-di-dit dah-dah-di-di-dit di-di-dah-dah-dah di-di-di-dah-dah di-di-dah-dah-dah di-di-di-di-dah di-di-dah-dah-dah di-di-di-di-dit di-di-di-di-dit dah-di-di-di-dit di-di-di-dah-dah di-di-di-di-dah di-di-di-di-dit di-di-di-di-dit di-di-di-di-dit di-dah di-di-di-di-dah di-di-dah-dit di-di-di-di-dit dah-dah-dah-dah-dit di-di-di-di-dit di-dah di-di-di-dah-dah di-di-dah-dah-dah dah-dah-di-di-dit di-dah di-di-di-dah-dah dah-dah-di-di-dit di-di-di-di-dit di-di-di-di-dah di-di-di-dah-dah di-di-dah-dah-dah di-di-di-dah-dah di-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dah di-di-di-dah-dah dah-dah-di-di-dit di-di-dah-dah-dah dah-di-di-di-dit dah-dah-di-di-dit dah-dah-dah-di-dit di-di-di-di-dah dah-di-dah-dit di-di-di-di-dah dah-dah-dah-dah-dah di-di-di-di-dit dah-dah-di-di-dit di-di-di-di-dah di-di-dah-dit di-di-di-dah-dah dah-dah-di-di-dit di-di-di-dah-dah di-di-di-di-dah di-di-di-dah-dah di-dah-dah-dah-dah di-di-di-dah-dah dah-dah-dah-dah-dah di-di-di-di-dit di-dah-dah-dah-dah di-di-di-di-dah dah-dah-dah-dah-dit"

c = (
    Chepy(data)
    .find_replace("\-", "")
    .find_replace("(dit?)", ".")
    .find_replace("dah", "-")
    .from_morse_code()
    .slice(2)
    .hex_to_str()
    .regex_search("gigem.+}")
)

print(c.o)
>>> ['gigem{C1icK_cl1CK-y0u_h4v3_m4I1}']
```

#### Cli
[![asciicast](https://asciinema.org/a/hvdE6i8X4gxkw4UeZ1AoOysZF.svg)](https://asciinema.org/a/hvdE6i8X4gxkw4UeZ1AoOysZF)

#### CyberChef solution
[CyberChef](https://gchq.github.io/CyberChef/#recipe=Find_/_Replace(%7B'option':'Regex','string':'-'%7D,'',true,false,true,false)Find_/_Replace(%7B'option':'Regex','string':'(dit?)'%7D,'.',true,false,true,false)Find_/_Replace(%7B'option':'Regex','string':'dah'%7D,'-',true,false,true,false)From_Morse_Code('Space','Line%20feed')Drop_bytes(0,2,false)From_Hex('Auto')&input=ZGFoLWRhaC1kYWgtZGFoLWRhaCBkYWgtZGktZGktZGFoIGRpLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGFoLWRhaC1kYWgtZGFoIGRpLWRpLWRhaC1kYWgtZGFoIGRpLWRhaCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kYWgtZGl0IGRpLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRhaC1kaS1kaXQgZGFoLWRhaC1kaS1kaS1kaXQgZGktZGktZGktZGktZGFoIGRpLWRpLWRpLWRpLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kaXQgZGktZGFoLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRhaC1kYWggZGFoLWRhaC1kYWgtZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGktZGktZGktZGktZGl0IGRpLWRpLWRpLWRhaC1kYWggZGFoLWRhaC1kYWgtZGktZGl0IGRhaC1kYWgtZGktZGktZGl0IGRpLWRhaC1kYWgtZGFoLWRhaCBkYWgtZGktZGktZGktZGl0IGRpdCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kaXQgZGktZGktZGktZGktZGFoIGRhaC1kaS1kaXQgZGktZGktZGktZGktZGl0IGRhaC1kYWgtZGFoLWRhaC1kaXQgZGktZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kYWgtZGFoLWRhaCBkaS1kYWggZGFoLWRhaC1kaS1kaS1kaXQgZGktZGktZGktZGFoLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkYWgtZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkYWgtZGFoLWRhaC1kaS1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGktZGFoIGRpLWRpLWRpLWRpLWRhaCBkYWgtZGFoLWRhaC1kYWgtZGl0IGRhaC1kYWgtZGktZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkaS1kaS1kYWgtZGFoLWRhaCBkaS1kYWggZGktZGktZGktZGktZGl0IGRpLWRpLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kYWgtZGFoLWRhaC1kYWggZGktZGktZGFoLWRhaC1kYWggZGFoLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGktZGFoIGRhaC1kYWgtZGktZGktZGl0IGRhaC1kYWgtZGFoLWRhaC1kYWggZGktZGktZGktZGktZGl0IGRpLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGktZGFoIGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRpLWRpdCBkaS1kaS1kYWgtZGFoLWRhaCBkaS1kYWgtZGFoLWRhaC1kYWggZGktZGktZGFoLWRhaC1kYWggZGktZGktZGktZGktZGl0IGRpLWRpLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGktZGktZGFoIGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRhaC1kaS1kaS1kaXQgZGFoLWRhaC1kYWgtZGFoLWRhaCBkaS1kaS1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRpLWRpLWRpdCBkaXQgZGktZGktZGktZGktZGFoIGRpdCBkaS1kaS1kaS1kYWgtZGFoIGRhaC1kYWgtZGFoLWRhaC1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRpLWRpLWRhaCBkYWgtZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkaS1kaS1kaS1kaS1kaXQgZGktZGktZGktZGktZGl0IGRpLWRpLWRpLWRhaC1kYWggZGktZGktZGktZGktZGFoIGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRpLWRhaC1kaXQgZGktZGktZGktZGktZGFoIGRpLWRpLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRhaC1kYWggZGktZGktZGktZGFoLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kaS1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kaS1kaXQgZGktZGktZGktZGktZGFoIGRhaC1kaS1kaS1kaS1kaXQgZGktZGktZGFoLWRpdCBkaS1kaS1kaS1kaS1kaXQgZGktZGktZGktZGktZGFoIGRpLWRpLWRpLWRhaC1kYWggZGFoLWRhaC1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kaS1kaXQgZGFoLWRhaC1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kaS1kaXQgZGktZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kYWgtZGFoLWRhaC1kYWggZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kYWgtZGFoLWRhaC1kYWggZGktZGktZGktZGktZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kaXQgZGFoLWRhaC1kYWgtZGFoLWRpdCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGFoLWRhaC1kYWggZGktZGktZGktZGFoLWRhaCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGktZGktZGl0IGRpLWRhaCBkaS1kaS1kaS1kaS1kYWggZGFoLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRpLWRpLWRhaC1kYWgtZGFoIGRpLWRhaCBkaS1kaS1kYWgtZGFoLWRhaCBkaS1kYWgtZGFoLWRhaC1kYWggZGktZGktZGktZGktZGFoIGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGktZGktZGl0IGRpLWRpLWRpLWRhaC1kYWggZGFoLWRhaC1kYWgtZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRpLWRhaC1kaXQgZGktZGktZGFoLWRhaC1kYWggZGktZGktZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGktZGktZGFoLWRhaC1kYWggZGFoLWRpLWRpLWRpLWRpdCBkaS1kYWggZGFoLWRhaC1kaS1kaS1kaXQgZGktZGFoLWRhaC1kYWgtZGFoIGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRpLWRhaC1kaXQgZGktZGktZGktZGktZGl0IGRhaC1kYWgtZGFoLWRhaC1kYWggZGktZGktZGktZGktZGFoIGRhaC1kaS1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkYWgtZGFoLWRhaC1kYWgtZGl0IGRpLWRpLWRpLWRpLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkaS1kYWgtZGFoLWRhaC1kYWggZGktZGktZGFoLWRhaC1kYWggZGktZGktZGktZGktZGl0IGRpLWRpLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kYWggZGktZGktZGktZGktZGFoIGRhaC1kYWgtZGktZGktZGl0IGRpLWRpLWRhaC1kYWgtZGFoIGRhaC1kYWgtZGFoLWRhaC1kYWggZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRhaC1kYWgtZGFoLWRhaC1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kaXQgZGFoLWRhaC1kaS1kaS1kaXQgZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGktZGFoLWRhaCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRhaC1kYWgtZGFoLWRhaCBkYWgtZGktZGktZGktZGl0IGRhaC1kYWgtZGFoLWRhaC1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRpLWRpLWRhaCBkYWgtZGktZGktZGl0IGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kYWgtZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGktZGktZGktZGFoLWRhaCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kYWgtZGl0IGRpLWRpLWRpLWRhaC1kYWggZGktZGFoLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRpLWRhaCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRpLWRpLWRhaCBkYWgtZGktZGktZGl0IGRpLWRpLWRhaC1kYWgtZGFoIGRhaC1kaS1kaXQgZGFoLWRhaC1kaS1kaS1kaXQgZGFoLWRhaC1kYWgtZGFoLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRhaC1kYWgtZGFoLWRhaC1kYWggZGFoLWRhaC1kaS1kaS1kaXQgZGktZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kYWgtZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRhaC1kYWgtZGktZGl0IGRpLWRpLWRpLWRhaC1kYWggZGktZGktZGktZGktZGFoIGRhaC1kYWgtZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGktZGktZGktZGFoLWRhaCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kYWgtZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRpLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRpLWRpLWRhaCBkaS1kaS1kaS1kaS1kYWggZGFoLWRhaC1kYWgtZGFoLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRhaC1kYWgtZGFoLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGktZGl0IGRpLWRpLWRhaC1kYWgtZGFoIGRhaC1kYWgtZGFoLWRhaC1kYWggZGFoLWRhaC1kaS1kaS1kaXQgZGktZGktZGktZGktZGl0IGRhaC1kYWgtZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGktZGktZGktZGFoLWRhaCBkaS1kaS1kaS1kaS1kYWggZGFoLWRhaC1kaS1kaS1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kYWggZGktZGktZGktZGktZGFoIGRhaC1kaS1kaS1kaXQgZGktZGktZGktZGktZGl0IGRpLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGktZGFoLWRhaCBkaS1kaS1kaS1kaS1kYWggZGFoLWRhaC1kaS1kaS1kaXQgZGFoLWRhaC1kYWgtZGFoLWRpdCBkYWgtZGktZGktZGktZGl0IGRpLWRpLWRhaC1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRhaC1kYWgtZGFoLWRpdCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGktZGktZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRhaC1kYWgtZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkYWgtZGktZGFoLWRpdCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kaXQgZGktZGktZGktZGFoLWRhaCBkYWgtZGFoLWRhaC1kaS1kaXQgZGktZGktZGktZGktZGl0IGRpLWRhaC1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkYWgtZGktZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGl0IGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kaXQgZGFoLWRhaC1kaS1kaS1kaXQgZGktZGktZGktZGktZGFoIGRhaC1kYWgtZGktZGktZGl0IGRhaC1kYWgtZGktZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkaS1kYWggZGktZGktZGktZGktZGFoIGRhaC1kYWgtZGFoLWRhaC1kYWggZGktZGktZGktZGktZGFoIGRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kaXQgZGktZGktZGktZGktZGFoIGRpLWRpLWRhaC1kaXQgZGktZGktZGktZGktZGl0IGRhaC1kYWgtZGFoLWRhaC1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRhaC1kaS1kaXQgZGktZGktZGFoLWRhaC1kYWggZGFoLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRhaC1kYWgtZGFoLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kaXQgZGktZGktZGktZGktZGFoIGRhaC1kYWgtZGFoLWRhaC1kYWggZGktZGktZGktZGktZGFoIGRhaC1kYWgtZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGl0IGRpLWRpLWRhaC1kYWgtZGFoIGRpLWRhaC1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRhaC1kYWgtZGFoLWRhaCBkaS1kaS1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kaS1kaXQgZGktZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kYWgtZGFoLWRhaC1kYWggZGFoLWRhaC1kaS1kaS1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRhaC1kYWgtZGFoLWRhaC1kYWggZGktZGktZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGFoLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kYWgtZGFoLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kYWggZGktZGktZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGktZGktZGFoLWRhaC1kYWggZGktZGFoLWRhaC1kYWgtZGFoIGRhaC1kaS1kaS1kaS1kaXQgZGktZGFoIGRpLWRpLWRhaC1kYWgtZGFoIGRpLWRhaC1kYWgtZGFoLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGktZGktZGktZGl0IGRhaC1kYWgtZGktZGktZGl0IGRpLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kaXQgZGFoLWRhaC1kaS1kaS1kaXQgZGFoLWRhaC1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kYWgtZGFoIGRhaC1kYWgtZGFoLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGFoLWRhaC1kYWggZGFoLWRpLWRpLWRpLWRpdCBkaS1kYWggZGFoLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGktZGktZGFoIGRpdCBkaS1kaS1kaS1kaS1kYWggZGFoLWRhaC1kYWgtZGFoLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kYWgtZGFoLWRhaC1kYWggZGktZGktZGktZGktZGFoIGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kaS1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kYWgtZGFoIGRpLWRpLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRpLWRhaCBkaS1kaS1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kaS1kaXQgZGktZGktZGktZGktZGl0IGRhaC1kaS1kaS1kaS1kaXQgZGktZGktZGktZGFoLWRhaCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGktZGktZGl0IGRpLWRpLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kaXQgZGktZGFoIGRpLWRpLWRpLWRpLWRhaCBkaS1kaS1kYWgtZGl0IGRpLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRhaC1kYWgtZGl0IGRpLWRpLWRpLWRpLWRpdCBkaS1kYWggZGktZGktZGktZGFoLWRhaCBkaS1kaS1kYWgtZGFoLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kYWggZGktZGktZGktZGFoLWRhaCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kaXQgZGktZGktZGktZGktZGFoIGRpLWRpLWRpLWRhaC1kYWggZGktZGktZGFoLWRhaC1kYWggZGktZGktZGktZGFoLWRhaCBkaS1kaS1kaS1kaS1kaXQgZGFoLWRhaC1kaS1kaS1kaXQgZGktZGktZGktZGktZGFoIGRpLWRpLWRpLWRhaC1kYWggZGFoLWRhaC1kaS1kaS1kaXQgZGktZGktZGFoLWRhaC1kYWggZGFoLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkYWgtZGFoLWRhaC1kaS1kaXQgZGktZGktZGktZGktZGFoIGRhaC1kaS1kYWgtZGl0IGRpLWRpLWRpLWRpLWRhaCBkYWgtZGFoLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRpLWRpdCBkYWgtZGFoLWRpLWRpLWRpdCBkaS1kaS1kaS1kaS1kYWggZGktZGktZGFoLWRpdCBkaS1kaS1kaS1kYWgtZGFoIGRhaC1kYWgtZGktZGktZGl0IGRpLWRpLWRpLWRhaC1kYWggZGktZGktZGktZGktZGFoIGRpLWRpLWRpLWRhaC1kYWggZGktZGFoLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRhaC1kYWggZGFoLWRhaC1kYWgtZGFoLWRhaCBkaS1kaS1kaS1kaS1kaXQgZGktZGFoLWRhaC1kYWgtZGFoIGRpLWRpLWRpLWRpLWRhaCBkYWgtZGFoLWRhaC1kYWgtZGl0)


## TAMUCTF xor bruteforce
In this example, we will combine the `Chepy` class, with a function from chepy extras called `xor_bruteforce_multi`. The main Chepy class can do single byte xor, but this function can bruteforce any length key.

#### Script
```python
from chepy import Chepy
from chepy.extras.crypto_extras import xor_bruteforce_multi
import re

chall = "XUBdTFdScw5XCVRGTglJXEpMSFpOQE5AVVxJBRpLT10aYBpIVwlbCVZATl1WTBpaTkBOQFVcSQdH"
c = Chepy(chall).base64_decode()
for match in xor_bruteforce_multi(c.o, min=2, max=2):
    if re.search('gigem', match['out'], re.I):
        print(match)
```
The `xor_bruteforce_multi` is not available in the cli.

## Convert a png to asciiart

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

## Bruteforce xor
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

## m1con mobile CTF - Chepy fork
This example shows how to use the `fork` method in Chepy. The `fork` method allows one to call the same methods on all the states that are available. This avoids duplication. The `fork` method argument structure can be quite complex. Essentially, it is an array of tuples. Each tuple must have the name of the method to call at index 0, followed by a dict of all the arguments that method may require. We then stack these tuples in the order we want them to run. 

Steps to take are:
- Load all 4 base64 encoded strings into chepy
- base64 decode them
- decrypt AES

The challenge gives 4 base64 encoded strings, which must be decrypted using AES. 

#### Script
```python
from chepy import Chepy
from pprint import pprint

challs = [
    "VgF6Ndz6kbPdTodjKtleWQ==",
    "/gFXZh1UIMgjwgRt3jxIPb94pIKDmcbiW8AghzmWcFA=",
    "Qqb1yxdZYPpO7IkgcwgY8Viv4lmNw/MQlb128tpcC1n+05vNWKRZrypzDWE3rtuG",
    "5CJD6tajuiEnHEHhlSKBZDxlQ0DEGhbZeLC7hpyzaVo=",
]

c = Chepy(*challs).fork(
    [
        ("base64_decode",),
        (
            "aes_decrypt",
            {"key": "kiwi037900000000", "iv": "itsasecret000000", "hex_iv": False},
        ),
    ]
)
pprint(c.states)
{0: b'handsomerob3709',
 1: b'DI{k3y_t0_ev3ryth!ng}',
 2: b'Congratulations on finishing the challenge! :)',
 3: b'DI{Th15_u53r_15_l0gg3d_1n}'}
```

#### Cli

```eval_rst
.. important::
    It is important to remember that the array of tuples being passed to the fork method in the cli does not contain any spaces. This is because of BASH will interpret it. Not tested in Windows. 
```

[![asciicast](https://asciinema.org/a/dXFIwHUuNLTPb7z0CTzHiTrBV.svg)](https://asciinema.org/a/dXFIwHUuNLTPb7z0CTzHiTrBV)