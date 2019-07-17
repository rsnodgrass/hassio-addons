# Xantech Multi-Zone Audio Amplifiers and Controllers

Support for Xantech multi-zone matrix audio amplifiers and controllers.

# Examples

You can easily test this from the command line:

```
curl http://localhost:5000/api/xantech/zones/1
```

```json
{"zone": "1"}
```

Mute zone 4 of the amplifier:

```
curl -X POST http://localhost:5000/api/xantech/zones/1/mute/on
```

# Supported Hardware

The following 8-zone matrix audio amplifiers/controllers are supported:

- MRAUDIO8X8 / MRAUDIO8X8m
- MRC88 / MRC88m
- MX88 / MX88a / MX88ai / MX88vi
- Monoprice MPR-SG6Z (possibly)

### Unsupported

The following do not seem to support the Xantech multi-zone matrix audio RS232 protocol:

- MRAUDIO4X4
- MRC44 / MRC44CTL

# See Also

* [Home Assistant integration](https://github.com/rsnodgrass/hass-integrations/tree/master/custom_components/xantech_mza)