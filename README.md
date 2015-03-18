# dsl-ac68_stats
Python script to collect DSL stats from the Asus DSL-AC68U

./dsl-ac68_stats.py --help
```
usage: dsl-ac68_stats.py [-h] [-t] [-m] [-d] [-u] [-p]

optional arguments:
  -h, --help        show this help message and exit
  -t , --target     Hostname or IP (DEFAULT: router.asus.com)
  -m , --mode       http | https (DEFAULT: http)
  -d , --display    cli | cacti (DEFAULT: cli)
  -u , --username   login username (DEFAULT: admin)
  -p , --password   login password (DEFAULT: admin)

dsl-ac68_stats.py
    Author      : rob0r - github.com/rob0r
    Description : collect DSL stats from the Asus DSL-AC68U
    Version     : 2015031801
```

# example
```
[root@dsl-ac68_stats]# ./dsl-ac68_stats.py -m https -t 192.168.1.254:8443
rate down:           12787 kbps
rate up:             1023 kbps
max rate down:       16624 kbps
max rate up:         1119 kbps
snr down:            11.3 dB
snr up:              9.0 dB
attenuation down:    35.3 dB
attenuation up:      21.3 dB
power down:          19.0 dbm
power up:            9.3 dbm
CRC errors down:     4820
CRC errors up:       i826

[root@dsl-ac68_stats]# ./dsl-ac68_stats.py -m https -t 192.168.1.254:8443 -d cacti
rate_down:12787 rate_up:1023 max_rate_down:16624 max_rate_up:1115 snr_down:11.3 snir_up:8.9 attenuation_down:35.3 attenuation_up:21.3 power_down:19.0 power_up:9.3 crc_error_down:4822 crc_error_up:827
```
