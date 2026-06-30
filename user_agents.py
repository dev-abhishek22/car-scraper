"""User-agent collections extracted from useragent_spoofer.py.

The original order and every original string are preserved.
Use UNIQUE_USER_AGENTS for a deduplicated collection.
Select one user agent when creating an HTTP client and keep it
stable for that client session.
"""

from __future__ import annotations

from random import SystemRandom
from typing import Final

LATEST_USER_AGENT: Final[list[str]] = ['Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like '
 'Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
 'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; Nexus S Build/GRJ22) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1; en-us; GT-N7100 Build/JRO03C) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3; en-us; SAMSUNG-SGH-I717 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.113 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.113 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.132 Safari/537.36']

IPAD_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13F69 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13D15 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E238 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13C75 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14C92 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A456 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12B410 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B435 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12A405 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G35 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B329 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G34 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D201 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B554a Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A452 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D167 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13G36',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
 'Version/4.0.4 Mobile/7B367 Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9A405 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A404 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11A465 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A344 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E233 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B93 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 '
 'Mobile/9B176 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A402 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B146 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A404',
 'Mozilla/5.0 (iPad; CPU OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A403 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A372 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C114 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A421 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/63.0.3239.73 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12A365 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B651 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 '
 'Mobile/9B176 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A5376e Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15G77',
 'Mozilla/5.0 (iPad; CPU OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14B72 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B511 Safari/9537.53',
 'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A523 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B150 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10B141 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Mobile/14G60',
 'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B176 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A5355d Safari/8536.25',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'CriOS/35.0.1916.38 Mobile/11D167 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/16.0.124986583 Mobile/13F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
 'Version/4.0.4 Mobile/7B334b Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26(KHTML, like Gecko) Version/6.0 '
 'Mobile/10A5355d Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Mobile/9B206',
 'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A8426 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B329',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/51.0.2704.104 Mobile/13F69 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/19.0.133715217 Mobile/14A456 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B436 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14E277 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 '
 'Mobile/9A334 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E237 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A403 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A406 Safari/8536.25 evaliant',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/47.1.192149458 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B101 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/12.0.68608 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12D508',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F90 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12F69',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/63.0.3239.73 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.4.141508723 Mobile/14C92 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B329 [Pinterest/iOS]',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
 'Mozilla/5.0 (iPad;U;CPU OS 5_1_1 like Mac OS X; zh-cn)AppleWebKit/534.46.0(KHTML, like '
 'Gecko)CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/19.0.133715217 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13B143',
 'Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/41.0.178428663 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B405 Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11A501 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'GSA/42.0.183854831 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/69.0.3497.105 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/54.0.2840.91 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/56.0.2924.79 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.0.41735 Mobile/12B435 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/55.0.2883.79 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/41.0.2272.56 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.3.48993 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14B150 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/55.0.2883.79 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/59.0.3071.102 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/61.0.3163.73 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/12B435 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Mobile/11D257',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/61.0.3163.73 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/40.0.2214.69 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
 'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/70.0.3538.75 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/65.0.3325.152 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/66.0.3359.122 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/47.0.2526.107 Mobile/13C75 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'CriOS/29.0.1547.11 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/20.3.136880903 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/8.0.57838 Mobile/13B5110e Safari/600.1.4 evaliant',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/48.0.2564.104 Mobile/13D15 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/6.0.51363 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12H321',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'GSA/4.1.0.31802 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'FxiOS/10.6b8836 Mobile/15D60 Safari/604.5.6',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8J3 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/66.0.3359.122 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B137 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'GSA/3.2.0.25255 Mobile/11B554a Safari/8536.25',
 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.4.141508723 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/47.0.2526.107 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/15.1.122860578 Mobile/13F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A406 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/20.3.136880903 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/20.3.136880903 Mobile/14A456 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/60.0.3112.89 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13G36 [FBAN/FBIOS;FBDV/iPad2,5;FBMD/iPad;FBSN/iPhone '
 'OS;FBSV/9.3.5;FBSS/1;FBCR/;FBID/tablet;FBLC/es_LA;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/70.0.3538.60 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E234 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/67.0.3396.87 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'FxiOS/10.6b8836 Mobile/15D100 Safari/604.5.6',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/29.0.159059490 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/537.51.3 (KHTML, like Gecko) '
 'Version/8.0 Mobile/11A4132 Safari/9537.145 evaliant',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) '
 'Mobile/14D27',
 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/30.0.1599.114 Safari/537.36 Puffin/5.2.2IT',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/55.0.2883.79 Mobile/14A456 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/45.0.2454.89 Mobile/13A452 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML like Gecko) '
 'Mobile/12A405 Version/7.0 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/41.0.2272.58 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/12B435 Safari/600.1.4',
 'Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9A334 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13D15',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; de-de) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G34 Safari/601.1 evaliant',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F8089 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'GSA/3.2.1.25875 Mobile/12B440 Safari/8536.25',
 'Mozilla/5.0 (iPad; U; CPU OS 5_0_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12H143',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/65.0.3325.152 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_1_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/62.0.3202.70 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/64.0.3282.112 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/14.1.119979954 Mobile/13E238 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/56.0.208290612 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Mobile/14F89',
 'Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/17.1.129017588 Mobile/13G35 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A5341f Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.4.141508723 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/64.0.3282.112 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/9.0.60246 Mobile/13B143 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E230 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/28.0.157793287 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/11.1.66360 Mobile/13C75 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'GSA/4.1.0.31802 Mobile/12B410 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.0.141836113 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/18.1.132077863 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/12B440 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/41.0.178428663 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/53.0.2785.109 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/12A405 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.5.50480 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/13.1.72140 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.1.146053689 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/64.0.3282.112 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12B440',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/23.0.147401934 Mobile/14D27 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/49.0.2623.73 Mobile/13D15 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13E238',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/35.0.167640935 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.1 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B5066f Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/55.0.2883.79 Mobile/14C92 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/62.1.220348572 Mobile/16B92 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D100',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F91 Safari/602.1',
 'Mozilla/5.0 (iPad; U; CPU OS 5_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B176 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.0.141836113 Mobile/14C92 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/51.0.198805899 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/51.0.198805899 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Mobile/9A405',
 'Mozilla/5.0 (iPad; U; CPU OS 5_1_1 like Mac OS X; en-us) AppleWebKit/534.46.0 (KHTML, like '
 'Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'FxiOS/14.0b12646 Mobile/16B92 Safari/605.1.15',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'GSA/41.0.178428663 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'FxiOS/10.4b8288 Mobile/15C153 Safari/604.4.7',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/47.0.2526.107 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/8.0.57838 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B146',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/54.0.2840.91 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/40.1.177082287 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12B466',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/41.0.178428663 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'FxiOS/5.3 Mobile/14B100 Safari/602.2.14',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/16.0.124986583 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/10.0.63022 Mobile/13B143 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10A523',
 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/9.0.60246 Mobile/13A452 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.1.139288856 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'GSA/10.0.63022 Mobile/11A501 Safari/9537.53']

NEXAS5_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like '
 'Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/LMY48B ) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.181 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MRA58N) AppleWebKit/537.36(KHTML, like Gecko) '
 'Chrome/69.0.3464.0 Mobile Safari/537.36 Chrome-Lighthouse',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MRA58N) AppleWebKit/537.36(KHTML, like Gecko) '
 'Chrome/61.0.3116.0 Mobile Safari/537.36 Chrome-Lighthouse',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2490.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like '
 'Gecko) Chrome/38.0.1025.166 Mobile Safari/535.19 Google',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; Nexus 5 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/40.0.2214.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2490.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/BuildID) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.132 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/43.0.2357.93 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/LRX21O) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/39.0.2171.93 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/38.0.2125.114 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/45.0.2454.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 NMWorker/0.1',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/47.0.2526.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/37.0.2062.117 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/_BuildID_) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.137 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.81 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29S) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/47.0.2526.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/43.0.2357.93 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.2272.96 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.85 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/163.0.0.43.91;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.132 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; Nexus 5 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.2272.96 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/34.0.1847.114 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; Nexus 5 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/40.0.2214.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29Q) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/48.0.2564.95 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/48.0.2564.23 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30Y) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/59.0.3071.115 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29Q; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/47.0.2526.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/63.0.0.37.81;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30Y; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/51.0.2704.81 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/88.0.0.22.76;]',
 'Mozilla/5.0 (Linux; Android 4.4.4; en-us; Nexus 5 Build/JOP40D) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/40.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/45.0.2454.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/LPX13D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/KRT16M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/31.0.1650.59 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/33.0.1750.166 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.5647.466 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/49.0.2623.105 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.7658.945 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/109.0.0.15.71;]',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/LRX21O) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/39.0.2171.59 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MRA58N) AppleWebKit/537.36(KHTML, like Gecko) '
 'Chrome/66.0.3359.30 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MRA58N) AppleWebKit/537.36(KHTML, like Gecko) '
 'Chrome/61.0.3116.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/32.0.1700.99 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.181 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/47.0.2526.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/LPX13D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.81 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/47.0.2526.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB31E; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/KRT16M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/53.0.2785.124 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/49.0.2623.105 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like '
 'Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 5 Build/NMF26Q) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.9584.787 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36 OPR/36.2.2254.130496',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/KRT16M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/49.0.2623.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/47.0.2526.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; Nexus 5 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/44.0.2403.90 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/50.0.2661.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.110 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.126 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.81 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/KRT16M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/40.0.2214.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/43.0.2357.121 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.68 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko; '
 'Hound) Chrome/27.0.1453 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Google Nexus 5 - 6.0.0 - API 23 - 1080x1920 Build/MRA58K; wv) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/40.0.0.0 Mobile Safari/537.361427449366820',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.99 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/LPX13D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; Google Nexus 5 - 4.4.2 - API 19 - 1080x1920 Build/KOT49H) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB31E) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/53.0.2785.124 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.140 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/45.0.2454.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.85 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like '
 'Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MRA58N) AppleWebKit/537.36(KHTML, like Gecko) '
 'Chrome/71.0.3559.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/50.0.2110.518 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.8683.267 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36evme-launcher',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/KRT16M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/49.0.2623.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3329.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/LPX13D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/40.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Google Nexus 5 - 5.0.0 - API 21 - 1080x1920 Build/LRX21M) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/LRX21O) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.2272.96 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.75 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/30.0.0.0 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/45.0.2454.78 Mobile Safari/537.36 OPR/32.0.1953.96473',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/44.0.7894.1 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2912.667 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/KRT16M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/45.0.2454.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.5988.878 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.4988.302 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.9339.269 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.9199.672 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/40.0.4835.828 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/40.0.0.0 Mobile Safari/537.361427449401871',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/49.0.1653.727 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.5075.68 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.9313.625 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/45.0.2454.95 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.139 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.113 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/50.0.2661.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3237.7 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2725.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MPA44G) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.81 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.186 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Google Nexus 5 - 5.1.0 - API 22 - 1080x1920 Build/LMY47D) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.154 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2490.42 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-us; Nexus 5 Build/LMY47D) AppleWebKit/537.16 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/537.16',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/43.0.2357.78 Mobile Safari/537.36 OPR/30.0.1856.93524',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like '
 'Gecko; Google Transcoder) Chrome/38.0.1025.166 Mobile Safari/535.19',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30P; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/51.0.2704.81 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.116 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/47.0.2526.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/47.0.2526.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.77 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/40.0.0.0 Mobile Safari/537.36; DailymotionEmbedSDK 1.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30Y) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Nexus 5 Build/MMB29S) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.9 NTENTBrowser/4.0.0.20 (Handy-UK) Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Nexus 5 Build/MMB29S) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.9 NTENTBrowser/4.0.0.28 (Handy-UK) Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; zh-tw; Nexus 5 Build/LMY47D) AppleWebKit/537.16 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/537.16',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36 MainLauncher/2.1.7',
 'Mozilla/5.0 (Linux; Android 8.1.0; Nexus 5 Build/OPM2.171026.006.H1; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB31K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.154 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Nexus 5 Build/MMB29S) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.9 NTENTBrowser/4.1.0.86 (Handy-UK) Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.108 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Google Nexus 5 - 4.4.4 - API 19 - 1080x1920 Build/KTU84P) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/50.0.2661.102 Crosswalk/20.50.533.5 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2490.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29Q) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/49.0.2623.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47O; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30Y) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/32.0.1700.99 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2490.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Google Nexus 5 - 5.0.0 - API 21 - 1080x1920 Build/LRX21M) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Crosswalk/22.52.561.4 Mobile '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2490.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; Nexus 5 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.81 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2490.43 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/50.0.2661.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Nexus 5 Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/45.0.2454.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.81 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/43.0.2357.78 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.2272.74 Mobile Safari/537.36 OPR/28.0.1764.89981',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/59.0.3071.86 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MMB29Q) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/60.0.3112.78 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/71.0.3559.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Nexus 5 Build/MMB29S) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.9 NTENTBrowser/4.1.0.90 (Handy-UK) Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/45.0.2454.95 Mobile Safari/537.36 ACHEETAHI/2100502010',
 'Mozilla/5.0 (Android 6.0.1; Nexus 5 Build/MMB29S) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.9 NTENTBrowser/4.0.0.27 (Handy-UK) Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84Q) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.81 Mobile Safari/537.36 PTST/333',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/LRX21O) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2490.76 Mobile Safari/537.36 PTST/0 PTST/286',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.75 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 BingWeb/5.2.0.20140710',
 'Mozilla/5.0 (Android 6.0.1; Nexus 5 Build/MMB29S) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.9 NTENTBrowser/4.0.0.24 (Handy-UK) Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/45.0.2454 Mobile Safari/537.36)',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.154 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.85 Mobile Safari/537.36',
 'Dalvik/2.1.0 (Linux; U; Android 5.0.1; Nexus 5 Build/LRX22C)',
 'Mozilla/5.0 (Linux; Android 4.4.3; Nexus 5 Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/35.0.1916.138 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like '
 'Gecko; Google Wireless Transcoder) Chrome/38.0.1025.166 Mobile Safari/535.19',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/45.0.2454.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 ACHEETAHI/2100050038',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.167 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.70 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 ACHEETAHI/2100050090',
 'Mozilla/5.0 (Linux; Android 7.0; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36 MainLauncher/2.2.15',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48I; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/44.0.2403.117 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48I) AppleWebKit/537.36 (KHTML, like Gecko; '
 'Hound) Chrome/41.0.2272.118 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/M4B30Z; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 NAVER(inapp; search; 510; 7.6.2)',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.162 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/KRT16M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/30.0.1599.105 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/48.0.2564.95 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB31E) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.84 Safari/537.36 Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 '
 'Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile '
 'Safari/535.19',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MOB30Z) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.97 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; Nexus 5 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Nexus 5 Build/M4B30X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; Nexus 5 Build/KTU84M) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/9.8.0.435 U3/0.8.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Android 6.0.1; Nexus 5 Build/MMB29S) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.9 NTENTBrowser/4.1.0.88 (Handy-SG) Mobile Safari/537.36']

UC_BROWSER_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; HUAWEI MT7-TL00 Build/HuaweiMT7-TL00) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.3.8.909 '
 'Mobile Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux i686; en-US) U2/1.0.0 UCBrowser/9.3.1.344',
 'UCWEB/2.0 (Java; U; MIDP-2.0; Nokia203/20.37) U2/1.0.0 UCBrowser/8.7.0.218 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; id; SM-G900 Build/KOT49H) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-G920F Build/LMY47X) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.10.0.796 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; Micromax A102 Build/MicromaxA102) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.1.0.882 U3/0.8.0 Mobile '
 'Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.1; en-US; AN10BG2DT Build/GINGERBREAD) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.0.1.512 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; XT1022 Build/KXC21.5-40) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.7.0.636 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 5.0.1; en-US; GT-I9505 Build/LRX22C) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.9.8.770 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 5.0.1; en-US; Lenovo TAB 2 A10-70L Build/LRX21M) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.2.960 U3/0.8.0 Mobile '
 'Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; Smartfren Andromax NC36B1G Build/KVT49L) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.1.5.890 U3/0.8.0 Mobile '
 'Safari/534.30',
 'Mozilla/5.0 (Linux; Android 4.4.2; Infinix X509 Build/KOT49H) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36 Mobile UCBrowser/3.4.3.532',
 'Mozilla/5.0 (Linux; U; Android 7.0; es-LA; Moto C Build/NRD90M.068) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.5.1146 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.3; zh-CN; SCH-N719 Build/JSS15J) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 UCBrowser/9.9.5.489 U3/0.8.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 8.0.0; en-US; ONEPLUS A3003 Build/OPR6.170623.013) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.0.0.1088 '
 'Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-US; GT-N7000 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.2.8.945 U3/0.8.0 Mobile Safari/534.30',
 'UCWEB/2.0 (Symbian; U; S60 V5; en-US; Nokia5233) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Nokia302/5.0 (14.78) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Windows; U; Windows NT '
 '6.0; en-US; Desktop) AppleWebKit/534.13 (KHTML, like Gecko) UCBrowser/9.4.1.377',
 'UCWEB/2.0 (Symbian; U; S60 V3; id; NokiaE63) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; EVA-AL10 Build/HUAWEIEVA-AL10) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.2.1.888 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 nokiac1-01/UC '
 'Browser7.8.0.95/70/351 UNTRUSTED/1.0',
 'Mozilla/5.0 (iPad; U; CPU OS 5_1 like Mac OS X) AppleWebKit/531.21.10 (KHTML, like Gecko) '
 'Version/4.0.4 Mobile/7B367 Safari/531.21.10 UCBrowser/3.4.3.532',
 'NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-in; '
 'nokiac1-01) UCBrowser8.4.0.159/70/352/UCWEB Mobile',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; Micromax A102 Build/MicromaxA102) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.0.8.855 U3/0.8.0 Mobile '
 'Safari/534.30',
 'UCWEB/8.8 (iPhone; CPU OS_6; en-US)AppleWebKit/534.1 U3/3.0.0 Mobile',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X; en-US) AppleWebKit/537.51.2 (KHTML, like '
 'Gecko) Mobile/11D201 UCBrowser/4.2.1.541 Mobile',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; itel it1407 Build/KOT49H) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.10.5.809 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Windows NT 6.2; ARM; Trident/7.0; Touch; rv:11.0; WPDesktop) like Gecko '
 'UCBrowser/4.2.1.541',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 4 Build/MMB29M) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.0; en-us; Lenovo K50a40 Build/LRX21M) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-US; GT-I8160 Build/GINGERBREAD) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.1.0.527 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 4 Build/MMB29M) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'UCWEB/2.0 (MIDP-2.0; U; Adr 4.0.4; en-US; ZTE_U795) U2/1.0.0 UCBrowser/10.7.6.805 U2/1.0.0 '
 'Mobile',
 'UCWEB/2.0(Java; U; MIDP-2.0; fr-fr; nokia5530c-2) U2/1.0.0 UCBrowser/8.7.0.218 U2/1.0.0 Mobile '
 'UNTRUSTED/1.0 3gpp-gba',
 'Nokia302/5.0 (14.78) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; '
 'fr-FR; Nokia302) U2/1.0.0 UCBrowser/9.4.1.377 U2/1.0.0 Mobile UNTRUSTED/1.0',
 'NokiaC3-00/5.0 (08.63) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; '
 'fr-FR; NokiaC3-00) U2/1.0.0 UCBrowser/9.3.0.326 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; Micromax A102 Build/MicromaxA102) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile '
 'Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J500F Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.5.1121 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'UCWEB/2.0 (Symbian; U; S60 V5; en-US; Nokia5235) U2/1.0.0 UCBrowser/9.1.0.319 U2/1.0.0 Mobile',
 'UCWEB/2.0(Symbian; U; S60 V5; en-US; Nokia5233) U2/1.0.0 UCBrowser/8.8.1.252 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; PRA-LX1 Build/HUAWEIPRA-LX1) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36 UCBrowser/11.4.1.1138 (UCMini) '
 'Mobile',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; Tizen Phone with ACL Build/KTU84Q) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.2.960 U3/0.8.0 Mobile '
 'Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-US; samsungs7562) AppleWebKit/533.1 (KHTML, like Gecko) '
 'Version/4.0 UCBrowser/4.2.1.541 U3/0.8.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 4A Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; Lenovo A2020a40 Build/LMY47V) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.8.0.718 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 7.0; es-LA; SM-G570M Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.5.1146 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J210F Build/MMB29Q) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.0.0.1088 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; GT-I8190 Build/JZO54K) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/9.8.0.435 U3/0.8.0 Mobile Safari/533.1',
 'NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 nokiac1-01/UC '
 'Browser7.7.1.88/69/444 UNTRUSTED/1.0',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; es-LA; SM-J700M Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.5.1146 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.2.5.1102 Mobile Safari/537.36',
 'UCWEB/2.0 (MIDP-2.0; U; Adr 4.4.2; en-US; Micromax_A310) U2/1.0.0 UCBrowser/10.7.9.856 U2/1.0.0 '
 'Mobile',
 'UCWEB/2.0 (MIDP-2.0; U; Adr 5.1.1; en-US; LG-H634) U2/1.0.0 UCBrowser/10.7.9.856 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 3 Build/MMB29M) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; Desktop) AppleWebKit/534.13 (KHTML, like Gecko) '
 'UCBrowser/9.2.0.336',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 4 Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'UCWEB/2.0 (iPad; U; CPU OS 7_1 like Mac OS X; en; iPad3,6) U2/1.0.0 UCBrowser/9.3.1.344',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; es-LA; ASUS_X00BD Build/LMY47V) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.2.5.1102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-J701F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi 4 Build/N2G47H) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.5.1121 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; SM-J110G Build/KTU84P) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.2.8.945 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; Micromax A102 Build/MicromaxA102) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.1.5.890 U3/0.8.0 Mobile '
 'Safari/534.30',
 'NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 OPENWAVE/UC '
 'Browser7.8.0.95/70/351 UNTRUSTED/1.0',
 'Nokia5320di/UCWEB8.0.3.99/28/999',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G615F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 4X Build/MMB29M) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.10.8.820 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; Desktop) AppleWebKit/534.13 (KHTML, like Gecko) '
 'UCBrowser/9.5.0.449 UNTRUSTED/1.0',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; ASUS_Z010D Build/MMB29P) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; HTC 919d Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.9.10.788 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; EVA-AL10 Build/HUAWEIEVA-AL10) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.2.5.884 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J210F Build/MMB29Q) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'UCWEB/2.0 (Java; U; MIDP-2.0; en-US; SpreadTrum6530) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 '
 'Mobile UNTRUSTED/1.0',
 'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us ; LS670 Build/GRI40) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1/UCBrowser/8.6.1.262/145/355',
 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; vivo 1724 Build/OPM1.171019.011) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.5.1146 Mobile Safari/537.36',
 'NokiaX2-02/2.0 (11.79) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/4.0 (compatible; MSIE '
 '8.0; Windows NT 6.1; Trident/4.0; SLCC2;.NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR '
 '3.0.30729; Media Center PC 6.0; InfoPath.2) UCBrowser8.4.0.159/70/352',
 'NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/4.0 (compatible; MSIE '
 '8.0; Windows NT 6.1; Trident/4.0; SLCC2;.NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR '
 '3.0.30729; Media Center PC 6.0; InfoPath.2)/UC Browser7.9.0.102/70/352',
 'UCWEB/2.0 (Windows; U; wds 10.0; en-US; Microsoft; RM-1099_1014) U2/1.0.0 UCBrowser/4.2.1.541 '
 'U2/1.0.0 Mobile',
 'UCWEB/2.0 (Symbian; U; S60 V3; en-US; NokiaE71) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; Lenovo A6020a40 Build/LMY47V) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.5.2.582 U3/0.8.0 Mobile Safari/534.30',
 'UCWEB/2.0 (Symbian; U; S60 V3; en-US; NOKIAE5-00) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 5.0; en-US; Micromax Q355 Build/LRX21M) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.8.0.718 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi Note 5 Build/N2G47H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0; en-US; Lenovo A7020a48 Build/MRA58K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.8.0.718 U3/0.8.0 Mobile Safari/534.30',
 'Nokia311/5.0 (07.36) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; '
 'en-US; Nokia311) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile UNTRUSTED/1.0',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; vivo Y21L Build/LMY47V) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.10.5.809 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-US; MI MAX 2 Build/NMF26F) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36',
 'UCWEB/2.0 (Symbian; U; S60 V3; en-US; NokiaE63) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Nokia302/5.0 (14.78) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Windows; U; Windows NT '
 '6.0; en-US; Desktop) AppleWebKit/534.13 (KHTML, like Gecko) UCBrowser/9.5.0.449',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; HTC Desire 728 dual sim Build/LMY47D) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.0.950 U3/0.8.0 Mobile '
 'Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 4 Build/MMB29M) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-J701F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 4A Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; '
 'IEMobile/11.0; Microsoft; Lumia 535 Dual SIM) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 '
 '(KHTML, like Gecko) Mobile Safari/537 UCBrowser/4.2.1.541 Mobile',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J111F Build/LMY47V) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.0.2; en-US; XT1032 Build/LXB22.46-28.1) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.2.0.535 U3/0.8.0 Mobile Safari/534.30',
 'UCWEB/2.0 (Linux; U; Opera Mini/7.1.32052/30.3697; en-US; E15i) U2/1.0.0 UCBrowser/10.1.2.571 '
 'Mobile',
 'UCWEB/2.0 (Symbian; U; S60 V3; en-US; NokiaC5-00.2) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'UCWEB/2.0 (Java; U; MIDP-2.0; en-US; sunmicrosystems_wtk) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 '
 'Mobile',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'UCWEB/2.0 (MIDP-2.0; U; Adr 2.1-update1; en-US; E15i) U2/1.0.0 UCBrowser/10.1.2.571 U2/1.0.0 '
 'Mobile',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'UCWEB/2.0 (Symbian; U; S60 V3; id; NokiaN73) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.31 (KHTML, like Gecko) '
 'Chrome/17.0.558.0 Safari/534.31 UCBrowser/3.4.3.532',
 'Mozilla/5.0 (Linux; U; Android 6.0; en-US; Lenovo A7020a48 Build/MRA58K) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.0.0.1088 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'LG/GT505/v10a Browser/Teleca-Q7.1 MMS/LG-MMS-V1.0/1.2 MediaPlayer/LGPlayer/1.0 Java/ASVM/1.1 '
 'Profile/MIDP-2.1 Configuration/CLDC-1.1 UNTRUSTED/1.0 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; lg) '
 'U2/1.0.0 UCBrowser/8.9.0.251 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 4 Build/MMB29M) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36',
 'Nokia311/5.0 (07.36) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; '
 'en-US; Nokia311) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile Safari/534.30',
 'UCWEB/2.0 (Windows; U; wds 8.10; en-IN; Microsoft; RM-1090_1001) U2/1.0.0 UCBrowser/4.2.1.541 '
 'U2/1.0.0 Mobile',
 'Nokia114/2.0 (03.33) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; '
 'en-US; nokia114) U2/1.0.0 UCBrowser/9.2.0.311 U2/1.0.0 Mobile',
 'UCWEB/2.0 (Windows; U; wds 10.0; en-IN; Microsoft; RM-1067_1005) U2/1.0.0 UCBrowser/4.2.1.541 '
 'U2/1.0.0 Mobile',
 'Nokia206/2.0 (04.52) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; '
 'en-US; Nokia206) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile UNTRUSTED/1.0',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'J2ME/UCWEB7.2.2.54/139/351',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 4 Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-us; Lenovo A2010-a Build/LMY47D) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like '
 'Gecko) Mobile/12B466 UCBrowser/10.7.11.672 Mobile',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-us; Lenovo A6000 Build/KTU84P) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/9.7.5.418 U3/0.8.0 Mobile Safari/533.1',
 'UCWEB/2.0 (Linux; U; Adr 2.3.6; en-AE; HUAWEI_Y210-0200) U2/1.0.0 UCBrowser/8.6.0.276 U2/1.0.0 '
 'Mobile',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; TECNO M5 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30',
 'NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; '
 'nokiac1-01) UCBrowser8.4.0.159/69/352/UCWEB Mobile UNTRUSTED/1.0',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 8.0.0; en-US; Lenovo K8 Note Build/OMB27.43-62) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.8.1140 '
 'Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.5.1121 Mobile Safari/537.36',
 'UCWEB/2.0 (Symbian; U; S60 V3; en-US; NOKIA6120c) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; XT1663 Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.2.0.1089 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J500F Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.0; en-US; Lenovo A1000 Build/S100) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.1.0.527 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.2.1143 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.0.0.1088 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.5.1146 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.1.1; en-US; Moto E (4) Plus Build/NMA26.42-113) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 '
 'Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; GN3001 Build/LMY47I) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.7.0) '
 'WindVane/8.0.0 720X1280 GCanvas/1.4.2.21',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; CPH1701 Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Icon Build/MMB29M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; Lenovo A2010-a Build/LMY47D) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.7.5.658 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Redmi Note 5 Pro Build/OPM1.171019.011) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.7.1153 '
 'Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-J701F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; XT1562 Build/MPD24.107-70-1) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/11.1.5.890 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; Desktop) AppleWebKit/534.13 (KHTML, like Gecko) '
 'UCBrowser/9.4.1.377 UNTRUSTED/1.0',
 'UCWEB/2.0 (Symbian; U; S60 V3; id; NOKIA6120c) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi 5A Build/N2G47H) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; CPH1701 Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 3S Build/MMB29M) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.3.5.972 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi 5A Build/N2G47H) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.1; zh-CN; MC002 Build/Retail_WGMC002) AppleWebKit/534.31 '
 '(KHTML, like Gecko) UCBrowser/9.2.4.329 U3/0.8.0 Mobile Safari/534.31',
 'Mozilla/5.0 (Linux; U; Android 6.0; en-US; vivo 1601 Build/MRA58K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'UCWEB/2.0 (Java; U; MIDP-2.0; en-US; generic) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G615F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'UCWEB/2.0 (Symbian; U; S60 V3; id; NokiaE71) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Redmi Note 5 Pro Build/OPM1.171019.011) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.5.1146 '
 'Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 8.1.0; en-US; Redmi Note 5 pro Build/OPM1.171019.011) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.0.1141 '
 'Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-G920F Build/MMB29K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.9.0.731 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Infinix HOT 4 Build/NRD90M) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'UCWEB/2.0 (MIDP-2.0; U; Adr 5.0; en-US; Micromax_A107) U2/1.0.0 UCBrowser/10.7.5.785 U2/1.0.0 '
 'Mobile',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-J710F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-US; ME302C Build/JSS15Q) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 UCBrowser/10.9.0.731 U3/0.8.0 Mobile Safari/534.30',
 'NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 Mozilla/5.0 (Java; U; en-us; '
 'nokiac1-01) AppleWebKit/530.13 (KHTML, like Gecko) UCBrowser/8.5.0.185/83/352/UCWEB Mobile '
 'UNTRUSTED/1.0',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.2.5.1102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 8.0.0; en-US; TA-1032 Build/O00623) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.5.1121 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; E2303 Build/26.3.A.1.33) AppleWebKit/528.5+ (KHTML, '
 'like Gecko) Version/3.1.2 Mobile Safari/525.20.1 UCBrowser/10.7.9.856 Mobile',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; vivo Y21L Build/LMY47V) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; Aqua Craze Build/LMY47D) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.10.8.820 U3/0.8.0 Mobile Safari/534.30',
 'UCWEB/2.0 (Java; U; MIDP-2.0; en-US; SpreadTrum6530) U2/1.0.0 UCBrowser/9.4.1.377 U2/1.0.0 '
 'Mobile UNTRUSTED/1.0',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; TECNO WX3P Build/NRD90M) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.2.8.945 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A33f Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'UCWEB/2.0 (Symbian; U; S60 V5; id; Nokia5233) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-US; GT-I8262 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.2.0.535 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; Desktop) AppleWebKit/534.13 (KHTML, like Gecko) '
 'UCBrowser/9.5.0.449',
 'Mozilla/5.0 (Linux; U; Android 6.0; en-US; Lenovo A7020a48 Build/MRA58K) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.2.5.1102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J210F Build/MMB29Q) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.6.1017 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; TECNO M5 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; AL-6 Build/GRJ90) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 UCBrowser/9.9.0.459 U3/0.8.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-G610F Build/MMB29K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.2.0.915 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-US; SM-G800F Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.7.5.658 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; vivo 1610 Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; P5W Build/LMY47I) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 UCBrowser/10.4.1.565 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; HUAWEI LUA-L01 Build/HUAWEILUA-L01) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.0.950 U3/0.8.0 Mobile '
 'Safari/534.30',
 'Mozilla/5.0 (Windows NT 6.2; ARM; Trident/7.0; Touch; rv:11.0; WPDesktop) like Gecko '
 'UCBrowser/4.0.0.498',
 'Nokia5130c-2/2.0 (07.97) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; '
 'en-US; Nokia5130c-2) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile UNTRUSTED/1.0',
 'Mozilla/5.0 (Windows NT 6.2; ARM; Trident/7.0; Touch; rv:11.0; WPDesktop) like Gecko '
 'UCBrowser/4.2.0.524',
 'NokiaX2-02/2.0 (11.79) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; '
 'en-US; NokiaX2-02) U2/1.0.0 UCBrowser/9.4.1.377 U2/1.0.0 Mobile',
 'NokiaX2-02/2.0 (11.84) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; '
 'en-US; NokiaX2-02) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; vivo 1714 Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Coolpad 3600I Build/MMB29M) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.10.5.809 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; ASUS_Z010D Build/MMB29P) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0; en-US; CPH1609 Build/MRA58K) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 4 Build/MMB29M) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/11.3.8.976 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; Lenovo P1ma40 Build/LMY47D) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/11.0.5.850 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi 4A Build/MMB29M) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.4.5.1005 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; A33f Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.0.1109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; Moto G (4) Build/NPJS25.93-14-10) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 4 Build/MMB29M) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.0.0.1088 Mobile Safari/537.36',
 'Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; '
 'IEMobile/11.0; Microsoft; Lumia 430 Dual SIM) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 '
 '(KHTML, like Gecko) Mobile Safari/537 UCBrowser/4.2.1.541 Mobile',
 'Mozilla/5.0 (Linux; U; Android 6.0; en-US; V504730 Build/MRA58K) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 UCBrowser/11.3.5.972 U3/0.8.0 Mobile Safari/534.30',
 'UCWEB/2.0 (MIDP-2.0; U; Adr 2.3.5; en-US; AL-6) U2/1.0.0 UCBrowser/9.7.0.520 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; A65A Build/A65A) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 UCBrowser/11.0.0.828 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 6.0; en-US; vivo 1601 Build/MRA58K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/11.4.2.995 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us ; Lenovo A690 Build/GRK39F) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1/UCBrowser/8.4.1.204/145/33482',
 'UCWEB/2.0 (Windows; U; wds 8.0; en-IN; NOKIA; RM-914_im_india_269) U2/1.0.0 UCBrowser/4.2.1.541 '
 'U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 6.0; en-US; XT1706 Build/MRA58K) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-US; Lenovo A7010a48 Build/LMY47D) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/10.5.2.582 U3/0.8.0 Mobile Safari/534.30',
 'NokiaC1-01/2.0 (04.40) Profile/MIDP-2.1 Configuration/CLDC-1.1 UCWEB/2.0(Java; U; MIDP-2.0; '
 'en-US; nokiac1-01) U2/1.0.0 UCBrowser/8.8.1.252 U2/1.0.0 Mobile',
 'UCWEB/2.0 (Java; U; MIDP-2.0; en-US; opera) U2/1.0.0 UCBrowser/8.9.0.251 U2/1.0.0 Mobile '
 'UNTRUSTED/1.0',
 'Mozilla/5.0 (Linux; U; Android 5.1.1; en-US; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.0.0.1088 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.5.1111 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/40.0.2214.89 Safari/537.36 UCBrowser/11.4.8.1012',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; OPPO R9sk Build/MMB29M) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/1.0.0.100 U3/0.8.0 Mobile Safari/534.30 AliApp(TB/6.7.0) '
 'WindVane/8.0.0 1080X1920 GCanvas/1.4.2.21',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0; en-US; Lenovo A7020a48 Build/MRA58K) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.1015 Mobile Safari/537.36',
 'UCWEB/2.0 (Symbian; U; S60 V3; en-US; NokiaE72-1) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'UCWEB/2.0 (MIDP-2.0; U; Adr 2.3.6; en-US; LG-L38C) U2/1.0.0 UCBrowser/10.7.5.785 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G570F Build/NRD90M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.9.2.1143 Mobile Safari/537.36',
 'UCWEB/2.0 (Symbian; U; S60 V5; en-US; Nokia5230) U2/1.0.0 UCBrowser/9.2.0.336 U2/1.0.0 Mobile',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-US; GT-I8262 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 UCBrowser/10.6.5.623 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 7.1.2; en-US; Redmi Note 5 Build/N2G47H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.8.0.1120 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-US; 2014818 Build/KTU84P) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; en-us; Lenovo P1ma40 Build/LMY47D) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 UCBrowser/9.9.2.467 U3/0.8.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-US; M2 Build/JDQ39) AppleWebKit/534.31 (KHTML, like '
 'Gecko) UCBrowser/9.1.0.297 U3/0.8.0 Mobile Safari/534.31']

SAFARI_BROWSER_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0.1 Safari/605.1.15',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) '
 'Version/9.1.2 Safari/601.7.7',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13F69 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1.2 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.1.2 Safari/603.3.8',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1 Safari/605.1.15',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.1.2 Safari/603.3.8',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0.3 Safari/604.5.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) '
 'Version/5.1.9 Safari/534.59.10',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A372 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) '
 'Version/9.0.3 Safari/601.4.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.1.1 Safari/603.2.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) '
 'Version/10.0.3 Safari/602.4.8',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14C92 Safari/602.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.8 (KHTML, like Gecko) '
 'Version/9.1.3 Safari/537.86.7',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13D15 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13F69 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.1 Safari/603.1.30',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) '
 'Version/9.1.1 Safari/601.6.17',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0.2 Safari/604.4.7',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) '
 'Version/9.1 Safari/601.5.17',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1.1 Safari/605.1.15',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14A456 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12F70 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Safari/604.1.38',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E238 Safari/601.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Safari/605.1.15',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13D15 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E188a Safari/601.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.78.2 (KHTML, like Gecko) '
 'Version/6.1.6 Safari/537.78.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0.1 Safari/602.2.14',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.8 (KHTML, like Gecko) Safari/312.6',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.9 (KHTML, like Gecko) '
 'Version/4.0.3 Safari/531.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0.1 Safari/604.3.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/412.7 (KHTML, like Gecko) Safari/412.5',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.1 (KHTML, like Gecko) Safari/312',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) '
 'Version/8.0.8 Safari/600.8.9',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/419.3 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) '
 'Version/9.0.1 Safari/601.2.7',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13C75 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like '
 'Gecko) Version/3.2.1 Safari/525.27.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Version/11.0 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0.1 Safari/605.1.15',
 'Mozilla/5.0 AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0.2 Safari/602.3.12',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Safari/602.1.50',
 'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B410 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1.2 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.9 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) '
 'Version/5.0.6 Safari/533.22.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.18.1 (KHTML, like '
 'Gecko) Version/5.0.2 Safari/533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E238 Safari/601.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.21.8 (KHTML, like '
 'Gecko) Version/4.0.4 Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13C75 Safari/601.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/416.11 (KHTML, like Gecko) '
 'Safari/416.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.2.5 (KHTML, like Gecko) '
 'Version/10.1.1 Safari/603.2.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1 (compatible; AdsBot-Google-Mobile; '
 '+http://www.google.com/mobile/adsbot.html)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) '
 'Version/7.0.3 Safari/7046A194A',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.8.9 (KHTML, like Gecko) '
 'Version/6.2.8 Safari/537.85.17',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14C92 Safari/602.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0.2 Safari/602.3.12',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.9.1 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.4.4 (KHTML, like Gecko) '
 'Version/9.0.3 Safari/601.4.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) '
 'Version/9.1.3 Safari/601.7.8',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/412.6 (KHTML, like Gecko) Safari/412.2',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; en-us) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.2 Safari/525.20.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.5.1 (KHTML, like Gecko) '
 'Safari/312.3.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418 (KHTML, like Gecko) Safari/417.9.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0.1 Safari/604.3.5',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.5.17 (KHTML, like Gecko) '
 'Version/9.1 Safari/601.5.17',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/412 (KHTML, like Gecko) Safari/412',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A456 Safari/602.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Safari/602.1.50',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-us) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.2 Safari/525.20.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.5.6 (KHTML, like Gecko) '
 'Safari/125.12',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.9 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) '
 'Version/9.0 Safari/601.1.56',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G34 Safari/601.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.9.1 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.2.7 (KHTML, like Gecko) '
 'Version/9.0.1 Safari/601.2.7',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) '
 'Version/8.0.7 Safari/600.7.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0.3 Safari/604.5.6',
 'Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.7.7 (KHTML, like Gecko) '
 'Version/9.1.2 Safari/601.7.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) '
 'Version/8.0.4 Safari/600.4.10',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) '
 'Version/8.0.2 Safari/600.2.5 (Applebot/0.1; +http://www.apple.com/go/applebot)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0.1 Safari/602.2.14',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.2 Safari/525.22',
 'MobileSafari/602.1 CFNetwork/811.5.4 Darwin/16.7.0',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/416.12 (KHTML, like Gecko) '
 'Safari/416.13',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) '
 'Version/8.0.3 Safari/600.3.18',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.5.5 (KHTML, like Gecko) '
 'Safari/125.12',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.4.8 (KHTML, like Gecko) '
 'Version/10.0.3 Safari/602.4.8',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0.2 Safari/604.4.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.2.5 (KHTML, like Gecko) '
 'Version/10.1.1 Safari/603.2.5',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like '
 'Gecko) Version/5.0.3 Safari/533.19.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G35 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12B410 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419.3 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.18.1 (KHTML, like '
 'Gecko) Version/5.0.2 Safari/533.18.5',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0.1 Safari/602.2.14',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.3.9 (KHTML, like Gecko) '
 'Version/9.0.2 Safari/601.3.9',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 (KHTML, like '
 'Gecko) Version/4.0.4 Safari/531.21.10',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.6.17 (KHTML, like Gecko) '
 'Version/9.1.1 Safari/601.6.17',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/85.8.5 (KHTML, like Gecko) '
 'Safari/85.8.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B435 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/523.12 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.12',
 'Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12A405 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1.2 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.4 (KHTML, like Gecko) Safari/125.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) '
 'Version/8.0.6 Safari/600.6.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/523.12.2 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.12.2',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G35 Safari/601.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/525.27.1 (KHTML, like Gecko) '
 'Version/3.2.1 Safari/525.27.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.22.7 (KHTML, like '
 'Gecko) Version/4.0.5 Safari/531.22.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) '
 'Version/8.0.5 Safari/600.5.17',
 'Mozilla/5.0 (iPad; CPU OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B329 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G34 Safari/601.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.8 (KHTML, like Gecko) Safari/312.5',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.17.8 (KHTML, like '
 'Gecko) Version/5.0.1 Safari/533.17.8',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-us) AppleWebKit/523.15.1 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.15',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) '
 'Version/8.0 Safari/600.1.25',
 'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D201 Safari/9537.53',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.5.17 (KHTML, like Gecko) '
 'Version/9.1 Safari/537.86.5',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Safari/602.1.50',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.1.2 Safari/603.3.8',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.5 (KHTML, like Gecko) Safari/125.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Safari/604.1.38',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) '
 'Version/10.0.3 Safari/602.4.8',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-us) AppleWebKit/533.19.4 (KHTML, like '
 'Gecko) Version/5.0.3 Safari/533.19.4',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418 (KHTML, like Gecko) Safari/417.9.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.19.4 (KHTML, like '
 'Gecko) Version/5.0.3 Safari/533.19.4',
 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B554a Safari/9537.53',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.8.1 (KHTML, like Gecko) '
 'Safari/312.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.1 Safari/603.1.30',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418 (KHTML, like Gecko) '
 'Safari/417.9.2',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0.2 Safari/602.3.12',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0.3 Safari/604.5.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) '
 'Version/8.0.2 Safari/600.2.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Version/11.0 Mobile/15A402 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.22.7 (KHTML, like '
 'Gecko) Version/4.0.5 Safari/531.22.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.1 Safari/603.1.30',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.5.2 (KHTML, like Gecko) '
 'Safari/312.3.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) '
 'Version/9.0 Safari/601.1.56',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Version/11.0 Mobile/15A421 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A452 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B411 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/525.28.3 (KHTML, like '
 'Gecko) Version/3.2.3 Safari/525.28.3',
 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A452 Safari/601.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1; en-us) AppleWebKit/531.9 (KHTML, like Gecko) '
 'Version/4.0.3 Safari/531.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) '
 'Version/7.1 Safari/537.85.10',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.1 (KHTML, like Gecko) Safari/312',
 'Mozilla/5.0 (iPad; CPU OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) '
 'Version/9.0.2 Safari/601.3.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.2.5 (KHTML, like Gecko) '
 'Version/7.1.2 Safari/537.85.11',
 'Mozilla/5.0 (iPad; CPU OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.5 (KHTML, like Gecko) Safari/312.3',
 'Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.21.11 (KHTML, like '
 'Gecko) Version/4.0.4 Safari/531.21.10',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B150 Safari/604.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.5.5 (KHTML, like Gecko) '
 'Safari/125.11',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.16 (KHTML, like Gecko) '
 'Version/5.0 Safari/533.16',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/417.9 (KHTML, like Gecko) '
 'Safari/417.9.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.3.18 (KHTML, like Gecko) '
 'Version/7.1.3 Safari/537.85.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) '
 'Version/7.0.6 Safari/537.78.2',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/419.2.1 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C114 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D167 Safari/9537.53',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/85.8.2 (KHTML, like Gecko) '
 'Safari/85.8',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D201 Safari/9537.53',
 'Mozilla/5.0 (en-us) AppleWebKit/525.13 (KHTML, like Gecko; Google Wireless Transcoder) '
 'Version/3.1 Safari/525.13',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/530.19.2 (KHTML, like '
 'Gecko) Version/4.0.2 Safari/530.19',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-us) AppleWebKit/523.10.3 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.10',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; en) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.2 Safari/525.22',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) '
 'Version/7.0.6 Safari/537.78.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) '
 'Version/7.1.8 Safari/537.85.17',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.18.1 (KHTML, like '
 'Gecko) Version/3.1.2 Safari/525.20.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Safari/604.1.38',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0.1 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.9 (KHTML, like Gecko) Safari/312.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/534.57.7 (KHTML, like Gecko) '
 'Version/5.1.7 Safari/534.57.7',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.1 Safari/525.18',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.4.4 (KHTML, like Gecko) '
 'Version/9.0.3 Safari/537.86.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0.2 Safari/604.4.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1.1 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1.1 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.8 (KHTML, like Gecko) '
 'Safari/312.6',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B554a Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12A405 Safari/600.1.4',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.17.8 (KHTML, like '
 'Gecko) Version/5.0.1 Safari/533.17.8',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.16 (KHTML, like Gecko) '
 'Version/5.0 Safari/533.16',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B93 Safari/604.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/523.12 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.12']

INTERNET_EXPLORER_USER_AGENTS: Final[list[str]] = ['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC '
 '5.0; .NET CLR 3.0.04506)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1)',
 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705)',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.0.3705)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.1)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 'InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; '
 'Media Center PC 4.0)',
 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; Win 9x 4.90)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR '
 '2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98; DigExt)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts)',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts)',
 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR '
 '3.0.04506.648; .NET CLR 3.5.21022)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC '
 '6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR '
 '3.0.04506)',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
 'Mozilla/4.0 (compatible; MSIE 5.23; Mac_PowerPC)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC '
 '5.0; .NET CLR 3.0.04506; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media '
 'Center PC 4.0)',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; Trident/5.0)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)',
 'Mozilla/4.0 (compatible ; MSIE 6.0; Windows NT 5.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; '
 'Media Center PC 3.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 5.01; Windows 98)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 'InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; '
 'Media Center PC 4.0; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media '
 'Center PC 4.0; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 1.0.3705)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 '.NET CLR 3.0.04506.30)',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts; SV1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC '
 '5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR '
 '3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; (R1 1.5))',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 4.0)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR '
 '3.0.04506; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.1; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.1; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; FunWebProducts)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; (R1 1.5); .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts; SV1; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR '
 '2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 'InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.1; .NET CLR 1.1.4322; .NET CLR '
 '2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; FunWebProducts)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; FunWebProducts; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; Win 9x 4.90; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR '
 '2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; YPC 3.2.0; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; DigExt)',
 'Mozilla/4.0 (compatible; MSIE 5.22; Mac_PowerPC)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; '
 '.NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Q312461; SV1)',
 'Mozilla/4.0 (compatible; MSIE 5.0; Mac_PowerPC)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 1.0.3705)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Q312461)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC '
 '5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;1813)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; T312461)',
 'Mozilla/5.0 (Windows NT 6.2; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center '
 'PC 5.0; .NET CLR 3.0.04506)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 'InfoPath.1; .NET CLR 3.0.04506.30)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; FunWebProducts; SLCC1; .NET CLR 2.0.50727; '
 'Media Center PC 5.0; .NET CLR 3.0.04506)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
 '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC '
 '5.0; .NET CLR 3.0.04506; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET '
 'CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 5.17; Mac_PowerPC)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Media Center PC 3.0; .NET CLR 1.0.3705; '
 '.NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
 '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Q312461; SV1; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; Q312461)',
 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; (R1 1.5))',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; .NET CLR '
 '3.0.04506; Media Center PC 5.0)',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Media Center PC 3.0; .NET CLR 1.0.3705)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; FunWebProducts)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30; .NET CLR 3.0.04506.648; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 4.0)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET '
 'CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; MSIECrawler)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR '
 '2.0.50727; .NET CLR 3.0.04506.30)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; WOW64; Trident/5.0)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.1; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; GTB6; SLCC1; .NET CLR 2.0.50727; Media Center '
 'PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; '
 '.NET CLR 3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 'InfoPath.1; .NET CLR 3.0.04506.30)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; YPC 3.2.0)',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows 95)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR '
 '3.0.04506; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR '
 '2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705)',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; '
 'Media Center PC 2.8)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 'InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0))',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.4506.2152; .NET CLR 3.5.30729; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR '
 '2.0.50727; .NET CLR 3.0.04506.30)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET CLR '
 '3.0.04506.30)',
 'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98; DigExt; FunWebProducts)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 '.NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
 'Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET '
 'CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 '.NET CLR 3.0.04506.30; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR '
 '3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C; .NET4.0E)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1;)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322; .NET '
 'CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; (R1 1.3); .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; (R1 1.3))',
 'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; SV1; .NET CLR '
 '1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
 '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR '
 '2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR '
 '3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.2; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FDM)',
 'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET '
 'CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR '
 '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; '
 'InfoPath.3)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; T312461; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 4.01; Windows NT)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET CLR 2.0.50727; '
 '.NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
 '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts; .NET CLR 1.0.3705)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media '
 'Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; MathPlayer 2.0; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR '
 '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; )',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; FunWebProducts; .NET CLR 1.1.4322; .NET CLR '
 '2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30; InfoPath.2; .NET CLR 3.0.04506.648)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; GTB6; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 '.NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/5.0 (Windows NT 5.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR '
 '3.5.30729; .NET CLR 3.0.30618)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Tablet PC 1.7; .NET CLR 1.0.3705; .NET '
 'CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; MSN 9.0;MSN 9.1; '
 'MSNbVZ02; MSNmen-us; MSNcOTH; MPLUS)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media '
 'Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.1; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1),gzip(gfe) (via translate.google.com)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; (R1 1.3))',
 'Mozilla/5.0 (Windows NT 6.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; FunWebProducts; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.2; .NET CLR '
 '2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.2; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; DigExt; SV1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Q312461; SV1; .NET CLR 1.0.3705; .NET CLR '
 '1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; '
 'InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; iebar)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.1; .NET CLR 1.1.4322; .NET CLR '
 '2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; .NET CLR 1.1.4322; .NET '
 'CLR 2.0.50727; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR '
 '3.5.30729)',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; LCJB; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; GTB6; SLCC1; .NET CLR 2.0.50727; Media Center '
 'PC 5.0; .NET CLR 3.0.04506)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET '
 'CLR 3.5.30729; .NET CLR 3.0.30729)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; Win 9x 4.90; FunWebProducts)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 '.NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 'InfoPath.2; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDSJS; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
 '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; Q312461)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
 '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; '
 'InfoPath.2)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0)',
 'Mozilla/4.0 (compatible; MSIE 5.14; Mac_PowerPC)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; wbx '
 '1.0.0)',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; T312461)',
 'Mozilla/4.0 (compatible; MSIE 5.00; Windows 98)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MASBJS; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; MSIECrawler)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR '
 '3.0.04506; InfoPath.1)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.0.3705; .NET '
 'CLR 1.1.4322; Media Center PC 4.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.1; .NET CLR 2.0.50727; .NET CLR '
 '1.1.4322)',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; Xbox)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30; InfoPath.1; .NET CLR 3.0.04506.648)',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR '
 '3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center '
 'PC 5.0; .NET CLR 3.0.04506; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR '
 '2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MDDC)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media '
 'Center PC 3.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; MSN 9.0;MSN 9.1; MSNbVZ02; MSNmen-us; '
 'MSNcOTH; MPLUS)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts; SV1; .NET CLR 1.0.3705)']

ANDRIOD_BROWSER_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile '
 'Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; GT-I9300 Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I8190 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; ME371MG Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.2.1; en-us; Nexus One Build/FRG83) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; WT19M-FI Build/KTU84Q)',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I9100 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; GT-P5210 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; pt-br; MZ608 Build/7.7.1-141-7-FLEM-UMTS-LA) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; SM-T110 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-P5110 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Dalvik/1.6.0 (Linux; U; Android 4.0.4; opensign_x86 Build/IMM76L)',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-I8200N Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.1; en-us; MID Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; GT-P5200 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; LG-L38C Build/GRK39F) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1 MMS/LG-Android-MMS-V1.0/1.2',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-P5100 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; SM-T217S Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-N8010 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; GT-P5210 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-P5113 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; SAMSUNG GT-I8190/I8190XXANR6 Build/JZO54K) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-gb; GT-P5110 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-P5210 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SCH-I915 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; WT22M-FI Build/KTU84Q)',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SGH-T599N Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; SAMSUNG GT-I9300/I9300XXUGNA5 Build/JSS15J) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.3; de-de; HTC_One Build/KTU84L) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; de-de; GT-S5830i Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'FBAndroidSDK.3.21.0',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; SCH-S738C Build/IMM76D) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; LGMS500 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-in; Micromax A87 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SAMSUNG-SGH-I467 Build/JZO54K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; ME302C Build/JSS15Q) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-I9105P Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; ZTE V768 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-P5210 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; GT-N7100 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; LGMS769 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SPH-L710 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-US; B1-710 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.1 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; C5170 Build/IML77) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SAMSUNG-SGH-I747 Build/KOT49H) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; GT-N8000 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; GT-N8013 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-P3110 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-P3113 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-M830 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I8190N Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SM-T210R Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; SCH-I800 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; SAMSUNG GT-I9100/I9100XWMS2 Build/JZO54K) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SAMSUNG-SGH-I497 Build/JZO54K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-gb; GT-S5830i Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-de; MD_LIFETAB_P9516 Build/IML74K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; es-mx; Azumi A50c Build/JDQ39) AppleWebKit/534.30 '
 '(KHTML,like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-M840 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SM-T310 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; SM-T210 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; LGL35G/V100) AppleWebKit/533.1 (KHTML, like Gecko) '
 'Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; 0PCV1 Build/KOT49H) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; Huawei Y301A1 Build/HuaweiY301A1) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SM-T217S Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SGH-T999L Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-gb; GT-I9300 Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I605 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-P5200 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; LG-E610 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-gb; GT-P3110 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; EVO Build/JRO03C) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-L300 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; de-de; HTC_One_S Build/JRO03C) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; de-de; GT-I9001 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; Sprint APA9292KT Build/GRJ90) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; SAMSUNG GT-I9300/I9300XXUGNH4 Build/JSS15J) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; de-de; GT-I8160 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.3; he-il; GT-I9300 Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; DROID RAZR Build/9.8.2O-72_VZW-16) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-DE; HUAWEI Y530-U00 Build/HuaweiY530-U00) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-gb; SM-T210 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-gb; GT-S5360 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; SM-T110 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SPH-L900 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2;de-de; Lenovo B8000-F/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.2.2 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-gb; GT-P5210 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; SGH-T679 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; de-de; HUAWEI Y300-0100 Build/HuaweiY300-0100) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-N8000 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'DDG-Android-3.0.14',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; SPH-M820-BST Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; SAMSUNG GT-I9100/I9100XWLSD Build/JZO54K) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; HTC_One_mini Build/KOT49H) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; Android; Windows NT 6.1; en-us) '
 'AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Android; iPhone; Trident/4.0; SLCC1; .NET CLR '
 '2.0.50727; .NET CLR 1.1.4322; InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; MS-RTC LM 8; '
 'OfficeLiveConnector.1.4; OfficeLivePatch.1.3; .NET CLR 3.0.30729)',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-S7710 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; SM-T310 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2; en-us; Windows NT 6.3; Nexus 10 Build/JVP15I; iPhone) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; FP1 Build/JDQ39) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; ZTE N9120 Build/IMM76I) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; pl-pl; GT-I9300 Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; Next8P12 Build/IMM76I) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; LG-LG730 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; he-il; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; EP772 Build/JDQ39) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; LG-E440 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; ZTE_N9511 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-us; SM-S820L Build/KTU84P) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; HTC_One_mini_2 Build/KOT49H) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; SAMSUNG-SM-T217A Build/JDQ39) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; HTC-A9192/1.0 Build/GRI40) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; mk808 Build/JDQ39) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; Z730 Build/JLS36C) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-P3100 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; Lenovo S6000L-F Build/JDQ39) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; SAMSUNG GT-P5100/P5100XXDMJ2 Build/JDQ39) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; SGH-S959G Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; Galaxy Nexus Build/JWR66Y) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; LG-VM696 Build/ZV5.GWK74) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.3.4; de-de; GT-I9100 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SCH-i705 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4; en-us; Nexus 4 Build/JOP24G) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-gb; SM-T310 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; de-de; MID7065 Build/ICS.MID7065.20121212) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-ca; SGH-I747M Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux;u;Android 2.3.7;zh-cn;) AppleWebKit/533.1 (KHTML,like Gecko) Version/4.0 '
 'Mobile Safari/533.1 (compatible; +http://www.baidu.com/search/spi_der.html)',
 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Sprint APA9292KT Build/FRF91) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; H866C Build/HuaweiH866C) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; SCH-R820 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; SAMSUNG GT-I9305/I9305XXUEMKC Build/JSS15J) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; de-de; LIFETAB_S9714 Build/JRO03R) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-L900 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; Z796C Build/JZO54K) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I9300 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; HP 7 Build/JZO54K) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; LG-VS410PP Build/GRK39F) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; SGH-T989 Build/IMM76D) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; en-us; SM-G360P Build/KTU84P) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SGH-T889 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; de-de; SAMSUNG GT-S5839i/S5839iBOMD1 Build/GINGERBREAD) '
 'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-gb; GT-I8190N Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; GT-P7510 Build/IMM76D) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; SCH-S720C Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SGH-T999 Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; pcdadr6350 Build/GRJ22) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SCH-R530U Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30 USCC-R530U',
 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Droid Build/FRG22D) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.0.1; en-us; Droid Build/ESD56) AppleWebKit/530.17 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/530.17',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; X501_USA_Cricket Build/GRK39F) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; HUAWEI Y360-U03 Build/HUAWEIY360-U03) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30;',
 'Tablet-PC-4.1-Mozilla/5.0 (Linux; U; Android 4.1.1; de-de; ADM8000KP_A Build/JRO03H) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; SCH-I500 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; HUAWEI Y625-U51 Build/HUAWEIY625-U51) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; LG-P710 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; DROID X2 Build/4.5.1A-DTN-200-18) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; LG-MS695 Build/GRK39F) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; SM-T311 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; C5155 Build/IML77) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; LGL45C Build/GRJ22) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; LG-LS720 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SGH-T999L Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-ca; SGH-I747M Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.2; de-de; GT-I9000 Build/FROYO) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; N860 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; SM-G350 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; HUAWEI Y360-U61 Build/HUAWEIY360-U61) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30;',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SM-T210R Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; HTC6435LVW 4G Build/KOT49H) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; GT-N5110 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-gb; GT-I8160 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; AT100 Build/IMM76D) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-de; GT-P5110 Build/IML74K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; he-us; GT-I9060 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Dolphin http client/11.3.4(405) (Android)',
 'Mozilla/5.0 (Linux; U; Android 4.4.4; de-de; SAMSUNG GT-I9305/I9305XXUFNL1 Build/KTU84P) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.1; en-us; sdk Build/ERD79) AppleWebKit/530.17 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/530.17',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; GT-N5110 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; de-de; SonyEricssonLT18i Build/4.1.B.0.587) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-gb; SM-T210 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; MID713 Build/MID713) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; FP1U Build/JDQ39) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; RCT6378W2 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; HTC_Desire_500/1.34.161.1 Build/JZO54K) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Fire OS/5.2.6.2 stagefright/1.2 (Linux;Android 5.1.1)',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; A200 Build/IML74K) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-au; GT-P5110 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; SAMSUNG GT-I9305/I9305XXUENH1 Build/JSS15J) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; LG-MS770 Build/IMM76I) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; de-de; HTC_Desire_X Build/JRO03C) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; Nexus S Build/GRJ22) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; Build/JRO03C) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.2.1; en-us; SAMSUNG-SGH-I997 Build/FROYO) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-ca; GT-P5113 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-gb; GT-N8010 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; es-us; GT-S5830M Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; de-de; SAMSUNG GT-I9300/I9300BUALF1 Build/IMM76D) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; HTC-A9192/1.0 Build/GRJ90) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; de-de; GT-S5360 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SAMSUNG-SGH-I547 Build/JZO54K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-N7000 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; ADR8995 4G Build/GRI40) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; HTC_Desire_500 Build/JZO54K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; SAMSUNG-SGH-I727 Build/GINGERBREAD) '
 'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; de-de; SAMSUNG GT-S7500/S7500BUMB1 Build/GINGERBREAD) '
 'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-de; A500 Build/IML74K) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.1-update1; en-us; SGH-T959 Build/ECLAIR) AppleWebKit/530.17 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/530.17',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; de-de; GT-P7501 Build/IMM76D) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Lenovo-A390t_TD/S100 Release/11.2012 Mozilla/5.0 (Linux; U; Android 4.0.3) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; HUAWEI Y330-U01 Build/HuaweiY330-U01) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; pt-br; GT-S6102B Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SGH-T989 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; de-de; SAMSUNG GT-S7500/S7500BULK1 Build/GINGERBREAD) '
 'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; de-de; Cynus T2 Build/IMM76D) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; LGMS659 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SCH-I200 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; HTC_Desire_626G_dual_sim Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; LS670 Build/GRI40) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; HTC_One_mini_2/2.19.111.3 Build/KOT49H) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Dalvik/2.1.0 (Linux; U; Android 7.1.1; E5823 Build/32.4.A.1.54)',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; Transformer TF101 Build/IML74K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; VS840 4G Build/IMM76D) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SCH-R760X Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2; en-us; sdk Build/MR1) AppleWebKit/535.19 (KHTML, like Gecko) '
 'Version/4.2 Safari/535.19',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; HTC_0PCV220/1.11.506.8 Build/KOT49H) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFOT Build/IML74K) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; tolino tab 7 Build/JDQ39) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; BNTV600 Build/IMM76L) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Kodi/17.6 (Linux; Android 7.1.2; AFTN Build/NS6212) Android/7.1.2 Sys_CPU/armv8l App_Bitness/32 '
 'Version/17.6-Git:20171114-a9a7a20',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; IdeaTabA1000L-F Build/JZO54K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'FBAndroidSDK.3.19.0',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; CONNECT Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; SAMSUNG-SGH-I717 Build/IMM76D) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; tolino tab 8.9 Build/JDQ39) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Huawei-U8665 Build/HuaweiU8665B037) '
 'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; PC36100 Build/GRJ90) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; fr-fr; GT-P5110 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; fr-fr; GT-P5210 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30']

FIREFOX_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
 'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; '
 'http://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.10) Gecko/20050716 Firefox/1.0.6',
 'Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7',
 'Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; '
 'https://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:29.0) Gecko/20100101 Firefox/29.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/20.6.14',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8) Gecko/20051111 Firefox/1.5',
 'Mozilla/5.0 (Windows NT 5.1; rv:32.0) Gecko/20100101 Firefox/32.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.7) Gecko/20070914 Firefox/2.0.0.7',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4',
 'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.8) Gecko/20061025 Firefox/1.5.0.8',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.7) Gecko/20050414 Firefox/1.0.3',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4',
 'Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20041001 Firefox/0.10.1',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.9) Gecko/20061206 Firefox/1.5.0.9',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6',
 'Mozilla/5.0 (Windows NT 5.1; rv:42.0) Gecko/20100101 Firefox/42.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:43.0) Gecko/20100101 Firefox/43.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1) Gecko/20061010 Firefox/2.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.9) Gecko/20071025 Firefox/2.0.0.9',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6) Gecko/20050225 Firefox/1.0.1',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 5.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.6) Gecko/20050317 Firefox/1.0.2',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.2) Gecko/20060308 Firefox/1.5.0.2',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows NT 5.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.11) Gecko/20070312 Firefox/1.5.0.11',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
 'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; Jobboerse.com; '
 'http://www.xn--jobbrse-d1a.com) Gecko/20100401 Firefox/24.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.16) Gecko/20080702 Firefox/2.0.0.16',
 'Mozilla/5.0 (X11; U; Linux i586; de; rv:5.0) Gecko/20100101 Firefox/5.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.12) Gecko/20070508 Firefox/1.5.0.12',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080311 Firefox/2.0.0.13',
 'Mozilla/5.0 (Windows NT 5.1; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.2) Gecko/2008091620 Firefox/3.0.2',
 'Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.4) Gecko/20100614 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.4',
 'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.7.12) Gecko/20050919 Firefox/1.0.7',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7 (ax)',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2) Gecko/20070219 Firefox/2.0.0.2',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.5) Gecko/2008120121 '
 'Firefox/3.0.5',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.17',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.4) Gecko/20100625 Gentoo Firefox/3.6.4',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0',
 'Mozilla/5.0 (X11; U; Linux i686; pt-BR; rv:1.9.0.15) Gecko/2009102815 Ubuntu/9.04 (jaunty) '
 'Firefox/3.0.15',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.8) Gecko/20071008 Firefox/2.0.0.8',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.11) Gecko/2009060215 Firefox/3.0.11',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7) Gecko/20040803 Firefox/0.9.3',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7',
 'Mozilla/5.0 (Windows NT 6.1; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)',
 'Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.20) Gecko/20081217 Firefox/2.0.0.20',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; '
 'https://www.jobboerse.com/bot.htm) Gecko/20100401 Firefox/24.0',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.13',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET '
 'CLR 3.5.30729)',
 'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.10) Gecko/20070216 Firefox/1.5.0.10',
 'Mozilla/5.0 (Windows NT 5.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9) Gecko/2008052906 Firefox/3.0',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.16) Gecko/20110323 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.16',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
 'Mozilla/5.0 (Windows NT 6.1; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.17) Gecko/20080829 Firefox/2.0.0.17',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20040913 Firefox/0.10',
 'Mozilla/5.0 (Windows NT 5.1; rv:26.0) Gecko/20100101 Firefox/26.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20040913 Firefox/0.10.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.10) Gecko/20050716 Firefox/1.0.6',
 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Mozilla/5.0 (Windows NT 6.0; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET '
 'CLR 3.5.30729)',
 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (Windows NT 5.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:43.0) Gecko/20100101 Firefox/43.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0',
 'Mozilla/5.0 (Windows NT 5.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
 'Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.6) Gecko/20100625 Firefox/3.6.6',
 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0']

CHROME_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.113 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.113 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.132 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.133 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.77 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.99 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.77 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.102 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 '
 'Safari/537.31',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.87 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.133 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.186 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/59.0.3071.115 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.106 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.87 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.67 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.181 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.181 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.99 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532G Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.102 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.139 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.117 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.67 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; vivo 1713 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/53.0.2785.124 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.89 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.106 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.67 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.94 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.110 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.99 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.110 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.133 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.181 Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.4 (KHTML, like Gecko) '
 'Chrome/5.0.375.99 Safari/533.4',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.89 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.117 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 '
 'Safari/537.36 MVisionPlayer/1.0.0.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/43.0.2357.93 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.132 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.133 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.113 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.133 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.133 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.110 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.77 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; CPH1607 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.99 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
 'Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.100 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; vivo 1603 Build/MMB29M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.186 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.110 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4A Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/60.0.3112.116 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.104 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/59.0.3071.115 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; vivo 1606 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/53.0.2785.124 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.87 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1; vivo 1716 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L22 Build/HUAWEIMYA-L22) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX2 Build/HUAWEITRT-LX2; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.87 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.87 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.87 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.102 Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.17 (KHTML, like Gecko) '
 'Chrome/10.0.649.0 Safari/534.17',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L21 Build/HUAWEICAM-L21; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.94 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 '
 'Safari/534.24',
 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.181 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G7102 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L22 Build/HUAWEICUN-L22; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J730GM Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.77 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 '
 'Safari/537.36',
 'Mozilla/5.0 (Unknown; Linux) AppleWebKit/538.1 (KHTML, like Gecko) Chrome/v1.0.0 Safari/538.1',
 'Mozilla/5.0 (Linux; Android 7.0; BLL-L22 Build/HUAWEIBLL-L22) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J710F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1723 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.79 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.139 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/534.17 (KHTML, like Gecko) '
 'Chrome/10.0.649.0 Safari/534.17',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 '
 'Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.84 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) '
 'Slackware/Chrome/12.0.742.100 Safari/534.30',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.167 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.100 '
 'Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.99 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.101 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.2272.89 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; vivo 1610 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/53.0.2785.124 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG GT-I9195 Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 '
 'Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.1805 '
 'Safari/537.36 MVisionPlayer/1.0.0.0',
 'Mozilla/5.0 (X11; U; Linux i586; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.1 '
 'Safari/533.2',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) '
 'Chrome/7.0.517.44 Safari/534.7',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.162 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.059) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.102 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.94 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J120M Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-14) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.181 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03 Build/HUAWEICAM-L03) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) '
 'Chrome/6.0.472.63 Safari/534.3',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) '
 'Chrome/7.0.517.44 Safari/534.7',
 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.75 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) '
 'Chrome/6.0.472.63 Safari/534.3',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.116 Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) '
 'Chrome/8.0.552.237 Safari/534.10',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.1 '
 'Safari/533.2',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.89 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.81 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.132 Safari/537.36',
 'Mozilla/5.0 (X11; Datanyze; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.181 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J111M Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.117 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 '
 'Safari/537.36']

LINUX_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; '
 'http://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a1) Gecko/20070308 Minefield/3.0a1',
 'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; '
 'https://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0',
 'Apache/2.4.25 (Debian) (internal dummy connection)',
 'Wget/1.12 (linux-gnu)',
 'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; Jobboerse.com; '
 'http://www.xn--jobbrse-d1a.com) Gecko/20100401 Firefox/24.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
 'Mozilla/5.0 (X11; U; Linux i586; de; rv:5.0) Gecko/20100101 Firefox/5.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 '
 'Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30',
 'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.4) Gecko/20100614 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.4',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 '
 'Safari/534.24',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.10 '
 'Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.17) Gecko/20110422 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.17',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.4) Gecko/20100625 Gentoo Firefox/3.6.4',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0',
 'Mozilla/5.0 (X11; U; Linux i686; pt-BR; rv:1.9.0.15) Gecko/2009102815 Ubuntu/9.04 (jaunty) '
 'Firefox/3.0.15',
 'Mozilla/5.0 (Unknown; Linux) AppleWebKit/538.1 (KHTML, like Gecko) Chrome/v1.0.0 Safari/538.1',
 'Mozilla/5.0 (compatible; Linux x86_64; Mail.RU_Bot/2.0; +http://go.mail.ru/help/robots)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.10 '
 'Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30',
 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/47.0 (Chrome)',
 'Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) '
 'Slackware/Chrome/12.0.742.100 Safari/534.30',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.100 '
 'Safari/534.30',
 'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; '
 'https://www.jobboerse.com/bot.htm) Gecko/20100401 Firefox/24.0',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.13',
 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.04 '
 'Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.16) Gecko/20110323 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.16',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko GranParadiso/3.0.11',
 'Mozilla/5.0 (X11; U; Linux i586; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.1 '
 'Safari/533.2',
 'Mozilla/5.0 (SMART-TV; X11; Linux armv7l) AppleWebKit/537.42 (KHTML, like Gecko) '
 'Chromium/25.0.1349.2 Chrome/25.0.1349.2 Safari/537.42',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 '
 'Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30',
 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Exabot-Thumbnails)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML',
 'Mozilla/5.0 (Linux; NetCast; U) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/34.0.1847.137 '
 'Safari/537.31 SmartTV/6.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.2 (KHTML, like Gecko) Chrome/5.0.342.1 '
 'Safari/533.2',
 'Mozilla/5.0 (X11; Datanyze; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.181 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/20.0 (Chrome)',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/10.04 '
 'Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
 'Mozilla/5.0 (Linux; U) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
 'magpie-crawler/1.1 (U; Linux amd64; en-GB; +http://www.brandwatch.net)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.94 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.2',
 'Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0',
 'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.10) Gecko/2009042513 Ubuntu/8.04 (hardy) '
 'Firefox/3.0.10',
 'Mozilla/5.0 (X11; Linux i686; rv:10.0.2) Gecko/20100101 Firefox/10.0.2 DejaClick/2.4.1.6',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.34 '
 'Safari/534.24',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 '
 'Safari/537.36',
 'Mozilla/5.0 (Linux; NetCast; U) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.33 '
 'Safari/537.31 SmartTV/5.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.4) Gecko/20100101 Firefox/4.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) '
 'Chrome/41.0.2272.118 Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
 'Mozilla/5.0 (SMART-TV; Linux; Tizen 2.4.0) AppleWebkit/538.1 (KHTML, like Gecko) '
 'SamsungBrowser/1.1 TV Safari/538.1',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) '
 'Firefox/3.0.3',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.15) Gecko/20110303 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.15',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0',
 'Mozilla/5.0 (SMART-TV; LINUX; Tizen 3.0) AppleWebKit/538.1 (KHTML, like Gecko) Version/3.0 TV '
 'Safari/538.1',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko; Google Web Preview) '
 'Chrome/22.0.1229 Safari/537.4',
 'Mozilla/5.0 (compatible; Konqueror/4.4; Linux) KHTML/4.4.5 (like Gecko) Kubuntu',
 'Wget/1.15 (linux-gnu)',
 'Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.2.1 '
 'Chrome/38.0.2125.122 Safari/537.36 WebAppManager',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0/Nutch-1.12',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0',
 'Mozilla/5.0 (X11; Linux) AppleWebKit/537.21 (KHTML, like Gecko) webbrowser/1.0 Safari/537.21 '
 'Tband',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.5) Gecko/2008121622 Ubuntu/8.10 (intrepid) '
 'Firefox/3.0.5',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Page Speed '
 'Insights) Chrome/41.0.2272.118 Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
 'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
 'Mozilla/5.0 (SMART-TV; Linux; Tizen 2.3) AppleWebkit/538.1 (KHTML, like Gecko) '
 'SamsungBrowser/1.0 TV Safari/538.1',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) '
 'Chrome/27.0.1453 Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.1; compatible; iCjobs Stellenangebote Jobs; '
 'http://www.icjobs.de) Gecko/20100401 iCjobs/3.2.3',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'HeadlessChrome/69.0.3452.0 Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.51 (KHTML, like Gecko; Google Web Preview) '
 'Chrome/12.0.742 Safari/534.51',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:14.0; ips-agent) Gecko/20100101 Firefox/14.0.1',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:20.0) Gecko/20100101 Firefox/20.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
 'Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
 'Mozilla/5.0 (Linux; NetCast; U) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/38.0.2125.122 '
 'Safari/537.31 SmartTV/7.5',
 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.42 (KHTML, like Gecko) Chromium/25.0.1349.2 '
 'Chrome/25.0.1349.2 Safari/537.42',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20150101 Firefox/44.0 (Chrome)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (Unknown; Linux x86_64) AppleWebKit/538.1 (KHTML, like Gecko) PhantomJS/2.1.1 '
 'Safari/538.1',
 'Mozilla/5.0 (Linux x86_64) AppleWebKit/538.19 (KHTML, like Gecko) JavaFX/8.0 Safari/538.19',
 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (Linux; NetCast; U) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/38.0.2125.122 '
 'Safari/537.31 SmartTV/7.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.1.8) Gecko/20100214 Ubuntu/9.10 (karmic) '
 'Firefox/3.5.8',
 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0/Nutch-1.12',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:28.0) Gecko/20100101 Firefox/28.0',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.0.10) Gecko/2009042523 Ubuntu/9.04 (jaunty) '
 'Firefox/3.0.10',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.1.7) Gecko/20100106 Ubuntu/9.10 (karmic) '
 'Firefox/3.5.7',
 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)',
 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Thunderbird/45.3.0',
 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.8.1.4) Gecko/20080721 BonEcho/2.0.0.4',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.44 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.11) Gecko/2009060309 Ubuntu/8.04 (hardy) '
 'Firefox/3.0.11',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.10) Gecko/2009042523 Ubuntu/9.04 (jaunty) '
 'Firefox/3.0.10',
 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0/Nutch-1.9',
 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) Qt/4.7.0 '
 'Safari/533.3',
 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.16 (KHTML, like Gecko) '
 'Chrome/10.0.648.204 Safari/534.16',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 '
 'Safari/537.36',
 'p2/mars-sr0 (Java 1.8.0_121-b13 Oracle Corporation; Linux 3.2.45.6 x86-64; en_US) '
 'org.eclipse.epp.package.jee.product/4.6.1.M20160907-1200 (org.eclipse.ui.ide.workbench)',
 'Mozilla/5.0 (X11; Linux x86_64; rv:29.0) Gecko/20100101 Firefox/29.0 SeaMonkey/2.26',
 'Mozilla/5.0 (Linux; NetCast; U) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 '
 'Safari/537.4 SmartTV/4.6',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US) U2/1.0.0 UCBrowser/9.3.1.344',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Page Speed '
 'Insights) Chrome/27.0.1453 Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:32.0) Gecko/20100101 Firefox/32.0',
 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20061201 Firefox/2.0.0.6 '
 '(Ubuntu-feisty)',
 'Opera/9.80 (X11; Linux zvav; U; en) Presto/2.12.423 Version/12.16',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/69.0.3464.0 '
 'Safari/537.36 Chrome-Lighthouse',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:25.0) Gecko/20100101 Firefox/25.0',
 'KummHttp/1.1 (compatible; KummClient; Linux rulez)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:14.0) Gecko/20100101 Firefox/14.0.1',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008072820 Firefox/3.0.1',
 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.1) Gecko/20060124 Firefox/1.5.0.1',
 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.0.11) Gecko/2009060308 Ubuntu/9.04 (jaunty) '
 'Firefox/3.0.11',
 'Mozilla/5.0 (SMART-TV; X11; Linux i686) AppleWebKit/535.20+ (KHTML, like Gecko) Version/5.0 '
 'Safari/535.20+',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0) Gecko/20100101 Firefox/29.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:34.0) Gecko/20100101 Firefox/34.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:33.0) Gecko/20100101 Firefox/33.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
 'Mozilla/5.0 (X11; Linux i686; rv:5.0) Gecko/20100101 Firefox/5.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
 '5.0 (X11; Linux) AppleWebKit/537.21 (KHTML, like Gecko) Qt/4.8.5 Safari/537.21 Telsey',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 '
 'Safari/537.36 http://notifyninja.com/monitoring',
 'Mozilla/5.0 (X11; U; Linux i686; it; rv:1.9.0.3) Gecko/2008092510 Ubuntu/8.04 (hardy) '
 'Firefox/3.0.3',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:20.0) Gecko/20100101 Firefox/20.0',
 'Mozilla/5.0 (SMART-TV; Linux; Tizen 3.0) AppleWebkit/538.1 (KHTML, like Gecko) '
 'SamsungBrowser/1.1 TV Safari/538.1',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0) Gecko/20100101 Firefox/4.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.0.10) Gecko/2009042523 Ubuntu/8.10 (intrepid) '
 'Firefox/3.0.10',
 'Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0',
 'Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
 'Chromium/31.0.1650.63 Chrome/31.0.1650.63 Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 '
 'Safari/537.36',
 'Mozilla/5.0 (compatible; Konqueror/3.2; Linux) (KHTML, like Gecko)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.7) Gecko/20050414 Firefox/1.0.3',
 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.11) Gecko/20080201 Firefox/2.0.0.11',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) '
 'Firefox/3.6.8',
 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.12) Gecko/20051010 Firefox/1.0.7 (Ubuntu package '
 '1.0.7)',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:13.0) Gecko/20100101 Firefox/13.0.1',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:23.0) Gecko/20100101 Firefox/23.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 '
 'Safari/537.36',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.34 (KHTML, like Gecko) Qt/4.8.1 Safari/534.34',
 'Mozilla/5.0 (X11; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0',
 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Qt/4.7.1 '
 'Safari/533.3',
 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
 'Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (X11; Linux) AppleWebKit/538.15 (KHTML, like Gecko) Chrome/18.0.1025.133 '
 'Safari/538.15 Midori/0.5',
 'Mozilla/5.0 (X11; Linux i686; rv:2.0.1) Gecko/20110430 Firefox/4.0.1 Iceweasel/4.0.1',
 'Mozilla/5.0 (Linux; Ubuntu 14.04) AppleWebKit/537.36 Chromium/35.0.1870.2 Safari/537.36',
 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/4.75 [en] (X11; U; Linux 2.2.16-22 i686)']

WINDOWS_USER_AGENTS: Final[list[str]] = ['Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.113 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 '
 'Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.113 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC '
 '5.0; .NET CLR 3.0.04506)',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1)',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 '
 'Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.0.3705)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.132 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.1)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.133 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.90 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.77 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 'InfoPath.1)',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.10) Gecko/20050716 Firefox/1.0.6',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; '
 'Media Center PC 4.0)',
 'Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.99 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.100 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.77 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; Win 9x 4.90)',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR '
 '2.0.50727)',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7',
 'Mozilla/4.0 (compatible; MSIE 5.0; Windows 98; DigExt)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; FunWebProducts)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.102 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 '
 'Safari/537.31',
 'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.84 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.87 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts)',
 'Mozilla/4.0 (compatible; MSIE 6.0; AOL 9.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0',
 'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1; 125LA; .NET CLR 2.0.50727; .NET CLR '
 '3.0.04506.648; .NET CLR 3.5.21022)',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/57.0.2987.133 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC '
 '6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; .NET4.0C; .NET4.0E)',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.1) Gecko/20060111 Firefox/1.5.0.1',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
 'Yandex/1.01.001 (compatible; Win16; I)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.186 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; .NET CLR '
 '3.0.04506)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/59.0.3071.115 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
 'YaBrowser/17.6.1.749 Yowser/2.5 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.106 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.87 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 98; .NET CLR 1.1.4322)',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727)',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 '
 'Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC '
 '5.0; .NET CLR 3.0.04506; InfoPath.2)',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
 'Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 '
 'YaBrowser/18.3.1.1232 Yowser/2.5 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.2) Gecko/20040804 Netscape/7.2 (ax)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.67 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media '
 'Center PC 4.0)',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.181 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.181 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.99 Safari/537.36',
 'Mozilla/5.0 (Windows NT 5.1; rv:29.0) Gecko/20100101 Firefox/29.0',
 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
 'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; Trident/5.0)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3',
 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; Trident/5.0)',
 'Mozilla/4.0 (compatible ; MSIE 6.0; Windows NT 5.1)',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; '
 'Media Center PC 3.1)',
 'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; InfoPath.2)',
 'Mozilla/4.0 (compatible; MSIE 6.0; AOL 9.0; Windows NT 5.1; SV1)',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.102 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.139 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/20.6.14',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8) Gecko/20051111 Firefox/1.5',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)',
 'Mozilla/5.0 (Windows NT 5.1; rv:32.0) Gecko/20100101 Firefox/32.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.117 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.67 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.7) Gecko/20070914 Firefox/2.0.0.7',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.89 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 '
 'Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
 'Mozilla/4.0 (compatible; MSIE 5.01; Windows 98)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 '
 'Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET '
 'CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.4) Gecko/20060508 Firefox/1.5.0.4',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 'InfoPath.1)',
 'Mozilla/5.0 (Windows NT 5.1; rv:6.0.2) Gecko/20100101 Firefox/6.0.2',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.1)',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
 'Safari/537.36 OPR/43.0.2442.991',
 'Mozilla/4.0 (compatible; MSIE 6.0; AOL 9.0; Windows NT 5.1)',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.106 Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.4) Gecko/2008102920 Firefox/3.0.4',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.8) Gecko/20061025 Firefox/1.5.0.8',
 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.67 Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.94 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.0.3705; .NET CLR 1.1.4322; Media '
 'Center PC 4.0; .NET CLR 2.0.50727)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 1.0.3705)',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
 '.NET CLR 3.0.04506.30)',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
 'Mozilla/4.0 (compatible; MSIE 5.5; Windows 98)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
 'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
 'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.7) Gecko/20050414 Firefox/1.0.3',
 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FunWebProducts; SV1)',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705)',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.110 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC '
 '5.0; .NET CLR 3.0.04506; .NET CLR 1.1.4322)',
 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.99 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.2)',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.110 Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR '
 '3.0.4506.2152; .NET CLR 3.5.30729)',
 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 '
 'Safari/537.36',
 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; (R1 1.5))',
 'Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0',
 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 '
 'Safari/537.36',
 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.5) Gecko/2008120122 Firefox/3.0.5',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3) Gecko/20041001 Firefox/0.10.1',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.9) Gecko/20061206 Firefox/1.5.0.9',
 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 '
 'Safari/537.36']

MAC_OS_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) '
 'Version/9.1.2 Safari/601.7.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.1.2 Safari/603.3.8',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) '
 'Version/5.1.9 Safari/534.59.10',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko) '
 'Version/9.0.3 Safari/601.4.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.8 (KHTML, like Gecko) '
 'Version/9.1.3 Safari/537.86.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) '
 'Version/9.1.1 Safari/601.6.17',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/417.9 (KHTML, like Gecko) Safari/417.8',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko) '
 'Version/9.1 Safari/601.5.17',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.78.2 (KHTML, like Gecko) '
 'Version/6.1.6 Safari/537.78.2',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.8 (KHTML, like Gecko) Safari/312.6',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.9 (KHTML, like Gecko) '
 'Version/4.0.3 Safari/531.9',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/412.7 (KHTML, like Gecko) Safari/412.5',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.1 (KHTML, like Gecko) Safari/312',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) '
 'Version/8.0.8 Safari/600.8.9',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/419.3 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.5) Gecko/2008120121 '
 'Firefox/3.0.5',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) '
 'Version/9.0.1 Safari/601.2.7',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.27.1 (KHTML, like '
 'Gecko) Version/3.2.1 Safari/525.27.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1.2 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.9 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) '
 'Version/5.0.6 Safari/533.22.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.18.1 (KHTML, like '
 'Gecko) Version/5.0.2 Safari/533.18.5',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.21.8 (KHTML, like '
 'Gecko) Version/4.0.4 Safari/531.21.10',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/416.11 (KHTML, like Gecko) '
 'Safari/416.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.2.5 (KHTML, like Gecko) '
 'Version/10.1.1 Safari/603.2.5',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) '
 'Version/7.0.3 Safari/7046A194A',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/600.8.9 (KHTML, like Gecko) '
 'Version/6.2.8 Safari/537.85.17',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0.2 Safari/602.3.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko)',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.9.1 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.4.4 (KHTML, like Gecko) '
 'Version/9.0.3 Safari/601.4.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) '
 'Version/9.1.3 Safari/601.7.8',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/412.6 (KHTML, like Gecko) Safari/412.2',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; en-us) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.2 Safari/525.20.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.5.1 (KHTML, like Gecko) '
 'Safari/312.3.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418 (KHTML, like Gecko) Safari/417.9.2',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.5.17 (KHTML, like Gecko) '
 'Version/9.1 Safari/601.5.17',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/412 (KHTML, like Gecko) Safari/412',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Safari/602.1.50',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.2272.89 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-us) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.2 Safari/525.20.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.5.6 (KHTML, like Gecko) '
 'Safari/125.12',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.9 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/42.0.2311.90 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) '
 'Version/9.0 Safari/601.1.56',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.9.1 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.2.7 (KHTML, like Gecko) '
 'Version/9.0.1 Safari/601.2.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) '
 'Version/8.0.7 Safari/600.7.12',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.5) Gecko/20041107 Firefox/1.0',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.10) Gecko/20050716 Firefox/1.0.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.7.7 (KHTML, like Gecko) '
 'Version/9.1.2 Safari/601.7.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) '
 'Version/8.0.4 Safari/600.4.10',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) '
 'Version/8.0.2 Safari/600.2.5 (Applebot/0.1; +http://www.apple.com/go/applebot)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0.1 Safari/602.2.14',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.2 Safari/525.22',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/416.12 (KHTML, like Gecko) '
 'Safari/416.13',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) '
 'Version/8.0.3 Safari/600.3.18',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.5.5 (KHTML, like Gecko) '
 'Safari/125.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.4.8 (KHTML, like Gecko) '
 'Version/10.0.3 Safari/602.4.8',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.2.5 (KHTML, like Gecko) '
 'Version/10.1.1 Safari/603.2.5',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-us) AppleWebKit/533.19.4 (KHTML, like '
 'Gecko) Version/5.0.3 Safari/533.19.4',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/419.3 (KHTML, like Gecko) Safari/419.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.18.1 (KHTML, like '
 'Gecko) Version/5.0.2 Safari/533.18.5',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0.1 Safari/602.2.14',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.3.9 (KHTML, like Gecko) '
 'Version/9.0.2 Safari/601.3.9',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-us) AppleWebKit/531.21.8 (KHTML, like '
 'Gecko) Version/4.0.4 Safari/531.21.10',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.6.17 (KHTML, like Gecko) '
 'Version/9.1.1 Safari/601.6.17',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/85.8.5 (KHTML, like Gecko) '
 'Safari/85.8.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/523.12 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.12',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 '
 'Firefox/3.0.3',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.4 (KHTML, like Gecko) Safari/125.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.6.3 (KHTML, like Gecko) '
 'Version/8.0.6 Safari/600.6.3',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/523.12.2 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.12.2',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.8) Gecko/20050511 Firefox/1.0.4',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/525.27.1 (KHTML, like Gecko) '
 'Version/3.2.1 Safari/525.27.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.22.7 (KHTML, like '
 'Gecko) Version/4.0.5 Safari/531.22.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) '
 'Version/8.0.5 Safari/600.5.17',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.8 (KHTML, like Gecko) Safari/312.5',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.17.8 (KHTML, like '
 'Gecko) Version/5.0.1 Safari/533.17.8',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-us) AppleWebKit/523.15.1 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.15',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) '
 'Version/8.0 Safari/600.1.25',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.5.17 (KHTML, like Gecko) '
 'Version/9.1 Safari/537.86.5',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Safari/602.1.50',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.1.2 Safari/603.3.8',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.5 (KHTML, like Gecko) Safari/125.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.100 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko) '
 'Version/10.0.3 Safari/602.4.8',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-us) AppleWebKit/533.19.4 (KHTML, like '
 'Gecko) Version/5.0.3 Safari/533.19.4',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418 (KHTML, like Gecko) Safari/417.9.3',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.2) Gecko/20040804 Netscape/7.2',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.19.4 (KHTML, like '
 'Gecko) Version/5.0.3 Safari/533.19.4',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.8.1 (KHTML, like Gecko) '
 'Safari/312.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.1 Safari/603.1.30',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418 (KHTML, like Gecko) '
 'Safari/417.9.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0.2 Safari/602.3.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0.3 Safari/604.5.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) '
 'Version/8.0.2 Safari/600.2.5',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.0.1) Gecko/20060111 '
 'Firefox/1.5.0.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.22.7 (KHTML, like '
 'Gecko) Version/4.0.5 Safari/531.22.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.1 Safari/603.1.30',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.5.2 (KHTML, like Gecko) '
 'Safari/312.3.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.1.56 (KHTML, like Gecko) '
 'Version/9.0 Safari/601.1.56',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.1) Gecko/2008070206 '
 'Firefox/3.0.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/49.0.2623.112 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/525.28.3 (KHTML, like '
 'Gecko) Version/3.2.3 Safari/525.28.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/49.0.2623.112 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.116 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.4) Gecko/2008102920 '
 'Firefox/3.0.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/36.0.1985.125 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1; en-us) AppleWebKit/531.9 (KHTML, like Gecko) '
 'Version/4.0.3 Safari/531.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) '
 'Version/7.1 Safari/537.85.10',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8) Gecko/20051111 Firefox/1.5',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.1 (KHTML, like Gecko) Safari/312',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) '
 'Version/9.0.2 Safari/601.3.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.2.5 (KHTML, like Gecko) '
 'Version/7.1.2 Safari/537.85.11',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.5 (KHTML, like Gecko) Safari/312.3',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.0.7) Gecko/20060909 '
 'Firefox/1.5.0.7',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:36.0) Gecko/20100101 Firefox/36.0',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.21.11 (KHTML, like '
 'Gecko) Version/4.0.4 Safari/531.21.10',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.5.5 (KHTML, like Gecko) '
 'Safari/125.11',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-us) AppleWebKit/533.16 (KHTML, like Gecko) '
 'Version/5.0 Safari/533.16',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/417.9 (KHTML, like Gecko) '
 'Safari/417.9.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.3.18 (KHTML, like Gecko) '
 'Version/7.1.3 Safari/537.85.12',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) '
 'Version/7.0.6 Safari/537.78.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.17 (KHTML, like Gecko) '
 'Chrome/24.0.1312.57 Safari/537.17',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/419.2.1 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.7) Gecko/20070914 Firefox/2.0.0.7',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/85.8.2 (KHTML, like Gecko) '
 'Safari/85.8',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13) Gecko/20101203 '
 'Firefox/3.6.13',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/530.19.2 (KHTML, like '
 'Gecko) Version/4.0.2 Safari/530.19',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-us) AppleWebKit/523.10.3 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.10',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; en) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.2 Safari/525.22',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) '
 'Version/7.0.6 Safari/537.78.2',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.4) Gecko/20030624 Netscape/7.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) '
 'Version/7.1.8 Safari/537.85.17',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.6) Gecko/2009011912 '
 'Firefox/3.0.6',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/525.18.1 (KHTML, like '
 'Gecko) Version/3.1.2 Safari/525.20.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Safari/604.1.38',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.9 (KHTML, like Gecko) Safari/312.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/534.57.7 (KHTML, like Gecko) '
 'Version/5.1.7 Safari/534.57.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.1 Safari/525.18',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.12) Gecko/20080201 Firefox/2.0.0.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.4.4 (KHTML, like Gecko) '
 'Version/9.0.3 Safari/537.86.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0.2 Safari/604.4.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1.1 Safari/605.1.15',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.8 (KHTML, like Gecko) '
 'Safari/312.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.4.4 (KHTML, like Gecko)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.0.5) Gecko/2008120121 '
 'Firefox/3.0.5',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.5.17 (KHTML, like Gecko)',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.17.8 (KHTML, like '
 'Gecko) Version/5.0.1 Safari/533.17.8',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/533.16 (KHTML, like Gecko) '
 'Version/5.0 Safari/533.16',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/523.12 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.12',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) '
 'Version/8.0 Safari/600.1.25',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.57.2 (KHTML, like Gecko) '
 'Version/5.1.7 Safari/534.57.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.2.7 (KHTML, like Gecko)',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.0.6) Gecko/20060728 '
 'Firefox/1.5.0.6',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6; en-us) AppleWebKit/531.9 (KHTML, like Gecko) '
 'Version/4.0.3 Safari/531.9',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/523.12.2 (KHTML, like Gecko) '
 'Version/3.0.4 Safari/523.12.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/49.0.2623.112 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.100 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.7.7 (KHTML, like Gecko) '
 'Version/9.1.2 Safari/537.86.7',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/531.9 (KHTML, like Gecko) '
 'Version/4.0.3 Safari/531.9',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0.1 Safari/604.3.5',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/125.5.5 (KHTML, like Gecko) '
 'Safari/125.12',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.3) Gecko/20070309 '
 'Firefox/2.0.0.3',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3',
 'Ruby, Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/530.19.2 (KHTML, like '
 'Gecko) Version/4.0.2 Safari/530.19',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.7.8 (KHTML, like Gecko) '
 'Version/9.1.3 Safari/601.7.8',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.4.10 (KHTML, like Gecko) '
 'Version/7.1.4 Safari/537.85.13',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.0.4) Gecko/20060508 '
 'Firefox/1.5.0.4',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/419.2 (KHTML, like Gecko) '
 'Safari/419.3',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; en) AppleWebKit/525.27.1 (KHTML, like Gecko) '
 'Version/3.2.1 Safari/525.27.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.3.9 (KHTML, like Gecko) '
 'Version/9.0.2 Safari/537.86.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.103 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.6) Gecko/20070725 '
 'Firefox/2.0.0.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.4.8 (KHTML, like Gecko)',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.17 (KHTML, like Gecko) '
 'Version/6.0.2 Safari/536.26.17',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.10) Gecko/2009042315 '
 'Firefox/3.0.10',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.6.17 (KHTML, like Gecko) '
 'Version/9.1.1 Safari/537.86.6',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:17.0) Gecko/20100101 Firefox/17.0',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:50.0) Gecko/20100101 Firefox/50.0',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US; rv:1.0.2) Gecko/20020924 AOL/7.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:48.0) Gecko/20100101 Firefox/48.0',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/125.5 (KHTML, like Gecko) '
 'Safari/125.9',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.0.1) Gecko/2008070206 '
 'Firefox/3.0.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.1) Gecko/20061204 Firefox/2.0.0.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/125.5.6 (KHTML, like Gecko) '
 'Safari/125.12',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.2.13) Gecko/20101203 '
 'Firefox/3.6.13',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/124 (KHTML, like Gecko) Safari/125.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) '
 'Version/7.1.6 Safari/537.85.15',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.10) Gecko/20100914 '
 'Firefox/3.6.10',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.4) Gecko/20070515 Firefox/2.0.0.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko)',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.1) Gecko/20061204 '
 'Firefox/2.0.0.1',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.95 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/39.0.2171.95 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) '
 'Version/7.0.5 Safari/537.77.4',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/312.5.1 (KHTML, like Gecko) '
 'Safari/312.3.1',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.8 (KHTML, like Gecko) '
 'Version/9.1.2 Safari/601.7.7',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:57.0) Gecko/20100101 Firefox/57.0',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/536.30.1 (KHTML, like Gecko) '
 'Version/6.0.5 Safari/536.30.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_2; en-us) AppleWebKit/525.18 (KHTML, like Gecko) '
 'Version/3.1.1 Safari/525.18',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/531.21.8 (KHTML, like Gecko) '
 'Version/4.0.4 Safari/531.21.10',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.8) Gecko/2009032608 '
 'Firefox/3.0.8',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/45.0.2454.101 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.2272.104 Safari/537.36',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.12) Gecko/20101026 '
 'Firefox/3.6.12',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.1.1 (KHTML, like Gecko) Safari/312',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-us) AppleWebKit/125.5.5 (KHTML, like Gecko) '
 'Safari/125.11',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/41.0.2272.101 Safari/537.36',
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.2.7 (KHTML, like Gecko) '
 'Version/9.0.1 Safari/537.86.2',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/525.13 (KHTML, like Gecko) '
 'Version/3.1 Safari/525.13',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.11) Gecko/20071127 '
 'Firefox/2.0.0.11',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_5; en-us) AppleWebKit/525.27.1 (KHTML, like '
 'Gecko) Version/3.2.1 Safari/525.27.1',
 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.4) Gecko/20070515 '
 'Firefox/2.0.0.4',
 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.0.3) Gecko/20060426 '
 'Firefox/1.5.0.3']

IOS_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13F69 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A372 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14C92 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13D15 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13F69 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14A456 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12F70 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E238 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13D15 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E188a Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13C75 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Version/11.0 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B410 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92',
 'Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E238 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13C75 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1 (compatible; AdsBot-Google-Mobile; '
 '+http://www.google.com/mobile/adsbot.html)',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14C92 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A456 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G34 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G35 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12B410 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B435 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12A405 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G35 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B329 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G34 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D201 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B554a Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Version/11.0 Mobile/15A402 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Version/11.0 Mobile/15A421 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A452 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B411 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A452 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPad; CPU OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B150 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C114 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D167 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D201 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B554a Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12A405 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Mobile/14G60',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B93 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A5376e Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B435 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/69.0.3497.105 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B329 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B411 Safari/600.1.4 (compatible; YandexMobileBot/3.0; '
 '+http://yandex.com/bots)',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13G36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E233 Safari/601.1',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
 'Version/4.0.4 Mobile/7B367 Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9A405 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/68.0.3440.83 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPad; CPU OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A404 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11A465 Safari/9537.53',
 'Outlook-iOS/696.1136898.prod.iphone (2.100.0)',
 'Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A344 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E233 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B93 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 '
 'Mobile/9B176 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A402 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B146 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A404',
 'Mozilla/5.0 (iPad; CPU OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A403 Safari/602.1',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like '
 'Gecko) Version/4.0 Mobile/7A341 Safari/528.16',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D167 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A372 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15C114 Safari/604.1',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
 'Mozilla/5.0 (iPad; CPU OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A421 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A344 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/63.0.3239.73 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13G36',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7',
 'Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 '
 'Mobile/12A365 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14B150 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B651 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12A365 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 '
 'Mobile/9B176 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A5376e Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15G77',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1_2 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, '
 'like Gecko) Version/4.0 Mobile/7D11 Safari/528.16',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/62.1.220348572 Mobile/16B92 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B651 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E234 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14B72 Safari/602.1',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1_3 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, '
 'like Gecko) Version/4.0 Mobile/7E18 Safari/528.16',
 'Mozilla/5.0 (iPad; CPU OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B511 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A404 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14B72 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_3 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11B511 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9A334 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11A465 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B410 Safari/600.1.4 (Applebot/0.1; +http://www.apple.com/go/applebot)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/61.0.217752169 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A523 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B150 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_6 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B500 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/70.0.3538.60 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D100',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/67.0.3396.87 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A405',
 'Outlook-iOS/696.1158777.prod.iphone (2.101.0)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B436 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Mobile/11D257',
 'Mozilla/5.0 (iPad; CPU OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10B141 Safari/8536.25',
 'mozilla/5.0 (iphone; cpu iphone os 7_0_2 like mac os x) applewebkit/537.51.1 (khtml, like gecko) '
 'version/7.0 mobile/11a501 safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Mobile/14G60',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/51.0.2704.104 Mobile/13F69 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B176 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) '
 'Mobile/14D27',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A5355d Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/66.0.3359.122 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12A4345d Safari/600.1.4',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11A4449d Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/64.0.3282.112 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B146 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/41.0.178428663 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/66.0.3359.122 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B350 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'CriOS/35.0.1916.38 Mobile/11D167 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A403 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E216',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/69.0.3497.91 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPod touch; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like '
 'Gecko) Version/9.0 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9A334 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14E277 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A523 Safari/8536.25',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1_3 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like '
 'Gecko) Version/4.0 Mobile/7E18 Safari/528.16',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/51.0.2704.104 Mobile/13F69 Safari/601.1.46 evaliant',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/65.0.3325.152 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/59.0.213668279 Mobile/16A366 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/16.0.124986583 Mobile/13F69 Safari/600.1.4',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/63.0.3239.73 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
 'Version/4.0.4 Mobile/7B334b Safari/531.21.10',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/67.0.3396.87 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12A365',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/69.0.3497.91 Mobile/15E148 Safari/604.1',
 'Outlook-iOS/696.1253802.prod.iphone (2.105.0)',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Version/4.0.5 Mobile/8A306 Safari/6531.22.7',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A5297c Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/11.1.66360 Mobile/13C75 Safari/600.1.4',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1_2 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like '
 'Gecko) Version/4.0 Mobile/7D11 Safari/528.16',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPod; CPU iPhone OS 6_1_6 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B500 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.38 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A300 Safari/602.1',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/60.0.215960477 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/60.0.215960477 Mobile/16A366 Safari/604.1',
 'Outlook-iOS/696.1102041.prod.iphone (2.99.0)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/12.0.68608 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Mobile/14C92',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0_1 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, '
 'like Gecko) Version/4.0 Mobile/7A400 Safari/528.16',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D60',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/58.0.212077146 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/70.0.3538.75 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/56.0.2924.79 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26(KHTML, like Gecko) Version/6.0 '
 'Mobile/10A5355d Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13F69',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) GSA/58.0.212077146 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/62.1.220348572 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/46.0.189829128 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/60.0.3112.89 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/29.0.159059490 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 2_2_1 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, '
 'like Gecko) Version/3.1.1 Mobile/5H11a Safari/525.20',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/55.0.2883.79 Mobile/14C92 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/56.0.208290612 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Mobile/9B206',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/61.0.3163.73 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A8426 Safari/8536.25',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_2_1 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, '
 'like Gecko) Version/3.1.1 Mobile/5H11 Safari/525.20',
 'Mozilla/5.0 (iPod touch; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like '
 'Gecko) Version/7.0 Mobile/11D167 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/27.0.155813979 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/16.0.124986583 Mobile/13F69 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9A405 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.0.141836113 Mobile/14C92 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/49.0.195456936 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B329',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A346 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/45.0.188348008 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/51.0.2704.104 Mobile/13F69 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/23.1.148956103 Mobile/14D27 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/53.1.203016890 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/19.0.133715217 Mobile/14A456 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12B436 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/59.0.3071.102 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14B72c Safari/602.1',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; Android; Windows NT 6.1; en-us) '
 'AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Android; iPhone; Trident/4.0; SLCC1; .NET CLR '
 '2.0.50727; .NET CLR 1.1.4322; InfoPath.2; .NET CLR 3.5.21022; .NET CLR 3.5.30729; MS-RTC LM 8; '
 'OfficeLiveConnector.1.4; OfficeLivePatch.1.3; .NET CLR 3.0.30729)',
 'Mozilla/5.0 (iPad; CPU OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14E277 Safari/602.1',
 'Mozilla/5.0 (Windows NT 5.1; rv:28.0; Android; iPhone) Gecko/20100101 Firefox/28.0',
 'Mozilla/5.0 (Linux; U; Android 4.2; en-us; Windows NT 6.3; Nexus 10 Build/JVP15I; iPhone) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A372 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (Windows NT 6.1; WOW64; Android; iPhone) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/34.0.1847.116 Safari/537.36',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0_2 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Version/4.0.5 Mobile/8A400 Safari/6531.22.7',
 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 '
 'Mobile/9A334 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C153',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like '
 'Gecko) Version/4.0 Mobile/7C144 Safari/528.16',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E237 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/20.3.136880903 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A403 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/44.0.187102957 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/64.0.3282.112 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/47.1.192149458 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/70.0.3538.75 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13D20 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/12B411 Safari/9537.53',
 'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A406 Safari/8536.25 evaliant',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 Instagram 65.0.0.12.86 (iPhone7,2; iOS 12_0; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 125889668)',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/47.1.192149458 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.0.141836113 Mobile/14D27 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Mobile/14F89',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/54.0.2840.91 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/23.0.147401934 Mobile/14D27 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B101 Safari/604.1',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like '
 'Gecko) Mobile/14B100',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C202',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'GSA/4.1.0.31802 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/12.0.68608 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12D508',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/41.0.178428663 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F90 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12F69',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/31.0.161834491 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_5 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8L1 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/65.0.3325.152 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/63.0.3239.73 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.4.141508723 Mobile/14C92 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/27.0.155813979 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B329 [Pinterest/iOS]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14A551 Safari/602.1',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13C75',
 'Mozilla/5.0 (iPad;U;CPU OS 5_1_1 like Mac OS X; zh-cn)AppleWebKit/534.46.0(KHTML, like '
 'Gecko)CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13F69 '
 '[FBAN/FBIOS;FBAV/59.0.0.51.142;FBBV/33266808;FBRV/0;FBDV/iPhone7,1;FBMD/iPhone;FBSN/iPhone '
 'OS;FBSV/9.3.2;FBSS/3;FBCR/Telkomsel;FBID/phone;FBLC/en_US;FBOP/5] evaliant',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13B143',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/19.0.133715217 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13B143',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/48.0.193557427 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/34.1.167176684 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/15.1.122860578 Mobile/13F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/41.0.178428663 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Mobile/15A432',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8C148a Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/47.0.2526.70 Mobile/12B436 Safari/600.1.4 (000410) evaliant',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B405 Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11A501 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'GSA/42.0.183854831 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'FxiOS/12.1b10941 Mobile/15F79 Safari/605.1.15',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/53.0.2785.109 Mobile/14A456 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/67.0.3396.87 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'OPiOS/9.1.0.86723 Mobile/12B440 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/63.0.3239.73 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/69.0.3497.105 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPod; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPod; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B329 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/54.0.2840.91 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.4.141508723 Mobile/14C92 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B329',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/56.0.2924.79 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.0.41735 Mobile/12B435 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/61.0.217752169 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302',
 'Outlook-iOS/696.1188109.prod.iphone (2.102.0)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/57.0.2987.100 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/60.0.215960477 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko)',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/55.0.2883.79 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Mobile/15B202',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X; en-us) AppleWebKit/537.51.1 (KHTML, like '
 'Gecko) Version/7.0 Mobile/11A465 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/41.0.2272.56 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.3.48993 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14B150 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/55.0.2883.79 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/59.0.3071.102 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/61.0.3163.73 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/52.2.201771014 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/12B435 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Mobile/11D257',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/41.0.2272.58 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) Mobile/14A456',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/61.0.3163.73 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'FxiOS/1.4 Mobile/13D15 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/40.0.2214.69 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A405 Safari/601.1',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) '
 'Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/58.0.3029.113 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/70.0.3538.75 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/65.0.3325.152 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/65.0.3325.152 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/12B440 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/66.0.3359.122 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/48.0.193557427 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A5376e Safari/8536.25 (compatible; SMTBot/1.0; '
 '+http://www.similartech.com/smtbot)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/38.0.172903409 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/42.0.2311.47 Mobile/12F70 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_2 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, '
 'like Gecko) Version/3.1.1 Mobile/5G77 Safari/525.20',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/33.0.164895372 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/47.0.2526.107 Mobile/13C75 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 Instagram 65.0.0.12.86 (iPhone9,3; iOS 12_0; es_CO; es-CO; scale=2.00; gamut=wide; '
 '750x1334; 125889668)',
 'Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'CriOS/29.0.1547.11 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/20.3.136880903 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/8.0.57838 Mobile/13B5110e Safari/600.1.4 evaliant',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/48.0.2564.104 Mobile/13D15 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/62.0.3202.70 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/51.0.198805899 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.1.146053689 Mobile/14D27 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/60.2.216743813 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16R381',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/62.0.3202.70 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13D15',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E198 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/11D201 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/8.0.57838 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/6.0.51363 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Mobile/15B202 '
 '[FBAN/FBIOS;FBAV/153.0.0.53.87;FBBV/84268146;FBDV/iPhone9,4;FBMD/iPhone;FBSN/iOS;FBSV/11.1.2;FBSS/3;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12H321',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 Instagram 65.0.0.12.86 (iPhone8,1; iOS 12_0; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 125889668)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12F70 '
 '[FBAN/FBIOS;FBAV/171.0.0.49.95;FBBV/107251038;FBDV/iPhone4,1;FBMD/iPhone;FBSN/iPhone '
 'OS;FBSV/8.3;FBSS/2;FBCR/Sprint;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'GSA/4.1.0.31802 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'FxiOS/10.6b8836 Mobile/15D60 Safari/604.5.6',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_1 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, '
 'like Gecko) Version/3.1.1 Mobile/5F136 Safari/525.20',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/18.1.132077863 Mobile/14A456 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A356 Safari/604.1',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8J3 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/58.0.212077146 Mobile/16A366 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/26.0.154727556 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.40 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A5309d Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/41.0.178428663 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/60.3.217355069 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/66.0.3359.122 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B137 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/69.0.3497.105 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'GSA/3.2.0.25255 Mobile/11B554a Safari/8536.25',
 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.4.141508723 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/47.0.2526.107 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/15.1.122860578 Mobile/13F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 '
 'Mobile/10A406 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/14.1.119979954 Mobile/13E238 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/19.0.133715217 Mobile/14A456 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/20.3.136880903 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/65.0.3325.152 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/63.0.3239.73 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1_1 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like '
 'Gecko) Version/4.0 Mobile/7C145 Safari/528.16',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.4.141508723 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/20.3.136880903 Mobile/14A456 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/60.0.3112.89 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13G36 [FBAN/FBIOS;FBDV/iPad2,5;FBMD/iPad;FBSN/iPhone '
 'OS;FBSV/9.3.5;FBSS/1;FBCR/;FBID/tablet;FBLC/es_LA;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPod; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/44.0.2403.67 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/17.0.128207670 Mobile/13G34 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/60.3.217355069 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'CriOS/70.0.3538.60 Mobile/15E148 Safari/605.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12D508',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B142 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E234 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/67.0.3396.87 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'FxiOS/10.6b8836 Mobile/15D100 Safari/604.5.6',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/10.0.63022 Mobile/13B143 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/31.0.161834491 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/43.0.185608249 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14G5047a Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/29.0.159059490 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/14.0.119004557 Mobile/13E238 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/537.51.3 (KHTML, like Gecko) '
 'Version/8.0 Mobile/11A4132 Safari/9537.145 evaliant',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) '
 'Mobile/14D27',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C114 Instagram 67.0.0.16.99 (iPhone7,2; iOS 11_2; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 127410745)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/35.0.167640935 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/FBIOS;FBAV/189.0.0.44.93;FBBV/124150883;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/TIGO;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/125136024]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/59.0.213668279 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79',
 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 '
 'Mobile/1A543a Safari/419.3',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/55.0.2883.79 Mobile/14A456 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13G34',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/61.0.3163.73 Mobile/15A372 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/45.0.2454.89 Mobile/13A452 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML like Gecko) '
 'Mobile/12A405 Version/7.0 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/41.0.2272.58 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/12B435 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/37.1.171590344 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 Instagram 68.0.0.10.99 (iPhone7,2; iOS 12_0_1; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 128202899)',
 'Outlook-iOS/696.1221480.prod.iphone (2.103.1)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B137 Safari/601.1',
 'Mozilla/5.0 (iPad; U; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9A334 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13D15',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) GSA/61.0.217752169 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B179 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; de-de) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 '
 '[FBAN/FBIOS;FBAV/191.0.0.42.96;FBBV/125515388;FBDV/iPhone10,6;FBMD/iPhone;FBSN/iOS;FBSV/12.0;FBSS/3;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/126680920]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Mobile/15A432 (Ecosia ios@3.0.1.533)',
 'Mozilla/5.0 (iPad; CPU OS 9_3_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13G34 Safari/601.1 evaliant',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/17.1.129017588 Mobile/12A365 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/54.0.204505792 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'FxiOS/7.5b3349 Mobile/14F89 Safari/603.2.4',
 'Gazetapl/3.5.11 EmbeddedBrowser (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 '
 '(KHTML, like Gecko) Mobile/15E302 DeviceUID: 63D6923E-622D-4E0B-B044-4C96641CD7E8',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_6 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'GSA/4.1.0.31802 Mobile/11B651 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/10.0.63022 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F8089 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'GSA/3.2.1.25875 Mobile/12B440 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.3 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14D15 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) Mobile/14E304',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/46.0.189829128 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; U; CPU OS 5_0_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like '
 'Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/61.0.217752169 Mobile/16B92 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C153 '
 '[FBAN/FBIOS;FBAV/157.0.0.42.96;FBBV/90008621;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.2.1;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/69.0.3497.105 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'FxiOS/10.6b8836 Mobile/15D100 Safari/604.5.6',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12H143',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/65.0.3325.152 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A452 Safari/601.1 PTST/402',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B176 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/51.0.198805899 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E5200d Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_1_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/62.0.3202.70 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/64.0.3282.112 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C153 '
 '[FBAN/FBIOS;FBAV/153.0.0.53.87;FBBV/84268146;FBDV/iPhone6,2;FBMD/iPhone;FBSN/iOS;FBSV/11.2.1;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/12B411 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/14.1.119979954 Mobile/13E238 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/56.0.208290612 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Mobile/14F89',
 'Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/17.1.129017588 Mobile/13G35 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11D169 Safari/9537.53',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12H321',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Mobile/15B202 '
 '[FBAN/FBIOS;FBAV/148.0.0.45.64;FBBV/78032376;FBDV/iPhone8,4;FBMD/iPhone;FBSN/iOS;FBSV/11.1.2;FBSS/2;FBCR/Orange;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15A5341f Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/58.0.212077146 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Mobile/15A432 '
 '[FBAN/FBIOS;FBAV/146.0.0.73.91;FBBV/75938921;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.0.3;FBSS/2;FBCR/T-Mobile.pl;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/51.1.199221351 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12H143',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.4.141508723 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/6.0.51363 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/12B435 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/64.0.3282.112 Mobile/15D100 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/17.1.129017588 Mobile/13G35 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/9.0.60246 Mobile/13B143 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/47.0.2526.107 Mobile/13C75 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Version/7.0 Mobile/11A466 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/9.0.60246 Mobile/13B143 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E230 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E230 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/68.0.3440.83 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/28.0.157793287 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/57.0.209471814 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/11.1.66360 Mobile/13C75 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/62.1.220348572 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/41.0.178428663 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'GSA/4.1.0.31802 Mobile/12B410 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.0.141836113 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 Instagram 65.0.0.12.86 (iPhone7,2; iOS 11_4_1; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 125889668)',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/18.1.132077863 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/12B440 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C202 '
 '[FBAN/MessengerForiOS;FBAV/152.0.0.37.98;FBBV/90712625;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.2.2;FBSS/2;FBCR/T-Mobile.pl;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/68.0.3440.83 Mobile/16A404 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A551 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/41.0.178428663 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) Mobile/14A456 '
 '[FBAN/MessengerForiOS;FBAV/139.0.0.66.86;FBBV/75131998;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/10.0.2;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 Instagram 66.0.0.14.101 (iPhone7,2; iOS 11_4_1; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 126719886)',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/53.0.2785.109 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/55.0.206190063 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 8_0_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/4.2.2.38484 Mobile/12A405 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/MessengerForiOS;FBAV/183.0.0.36.93;FBBV/123940704;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPod touch; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like '
 'Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Mobile/15A432 '
 '[FBAN/FBIOS;FBAV/93.0.0.49.65;FBBV/58440824;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.0.3;FBSS/2;FBCR/Orange;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/16A366 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/65.0.3325.152 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12A366 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.5.50480 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 '
 '[FBAN/FBIOS;FBAV/171.0.0.49.95;FBBV/107251038;FBDV/iPhone8,4;FBMD/iPhone;FBSN/iOS;FBSV/11.3.1;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/6.0.51363 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B5084a',
 'Outlook-iOS/696.1086665.prod.iphone (2.98.0)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/53.0.2785.109 Mobile/14A403 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/18.1.132077863 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/60.0.215960477 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/42.0.183854831 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/13.1.72140 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13F69 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10A525 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E237 Safari/601.1',
 'Mozilla/5.0 (iPod touch; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like '
 'Gecko) Version/9.0 Mobile/13E238 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13G35',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13E230',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/17.0.128207670 Mobile/13F69 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'GSA/3.2.1.25875 Mobile/10B329 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Mobile/14C92 '
 '[FBAN/FBIOS;FBAV/75.0.0.48.61;FBBV/45926345;FBRV/0;FBDV/iPad4,2;FBMD/iPad;FBSN/iOS;FBSV/10.2;FBSS/2;FBCR/;FBID/tablet;FBLC/de_DE;FBOP/5]',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Outlook-iOS/696.1045750.prod.iphone (2.96.0)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B145 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.1.146053689 Mobile/14C92 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.1.146053689 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/64.0.3282.112 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Mobile/15B202 Instagram 27.0.0.13.98 (iPhone8,1; iOS 11_1_2; pl_PL; pl-PL; scale=2.00; '
 'gamut=normal; 750x1334)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/38.0.172903409 Mobile/15B93 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13E238',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79 '
 '[FBAN/FBIOS;FBAV/189.0.0.44.93;FBBV/124150883;FBDV/iPad5,4;FBMD/iPad;FBSN/iOS;FBSV/11.4;FBSS/2;FBCR/;FBID/tablet;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12B440',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/15.0.122066290 Mobile/13F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/23.0.147401934 Mobile/14D27 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/55.0.2883.79 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/67.0.3396.59 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 '
 'Mobile/4A102 Safari/419.3',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/49.0.2623.73 Mobile/13D15 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/FBIOS;FBAV/195.0.0.44.99;FBBV/128807583;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/129317357]',
 'Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13E238',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/35.0.167640935 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/67.0.3396.69 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_1 like Mac OS X) AppleWebKit/604.3.1 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B5066f Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/55.0.2883.79 Mobile/14C92 Safari/602.1',
 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 '
 'Mobile/1A543 Safari/419.3',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/62.1.220348572 Mobile/16B92 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D100',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/64.0.3282.112 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F91 Safari/602.1',
 'Mozilla/5.0 (iPad; U; CPU OS 5_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B176 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/10B143 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/63.0.3239.73 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1 like Mac OS X) AppleWebKit/604.3.1 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15B5066f Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/FBIOS;FBAV/196.0.0.52.95;FBBV/129677436;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/en_US;FBOP/5;FBRV/130304466]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 Instagram 67.0.0.16.99 (iPhone7,2; iOS 12_0_1; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 127410745)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/69.0.3497.71 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.0.141836113 Mobile/14C92 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/51.0.198805899 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/51.0.198805899 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D100 '
 '[FBAN/FBIOS;FBAV/167.0.0.50.95;FBBV/102293131;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.2.6;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Mobile/9A405',
 'Mozilla/5.0 (iPod touch; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like '
 'Gecko) Mobile/13G36',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13A452',
 'Mozilla/5.0 (iPad; U; CPU OS 5_1_1 like Mac OS X; en-us) AppleWebKit/534.46.0 (KHTML, like '
 'Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'FxiOS/14.0b12646 Mobile/16B92 Safari/605.1.15',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 Instagram 65.0.0.12.86 (iPhone9,3; iOS 11_4_1; es_PA; es-PA; scale=2.00; '
 'gamut=wide; 750x1334; 125889668)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B141',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 [Pinterest/iOS]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/12F70 Safari/600.1.4',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/63.0.221691834 Mobile/16B92 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 '
 '[FBAN/MessengerForiOS;FBAV/190.1.0.58.95;FBBV/129822925;FBDV/iPhone9,4;FBMD/iPhone;FBSN/iOS;FBSV/12.1;FBSS/3;FBCR/TIGO;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'GSA/41.0.178428663 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'CriOS/47.0.2526.107 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Version/5.1 Mobile/9B208 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B146',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'FxiOS/10.4b8288 Mobile/15C153 Safari/604.4.7',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/47.0.2526.107 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/25.0.152548370 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/48.0.193557427 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/FBIOS;FBAV/194.0.0.38.99;FBBV/127868476;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/2;FBCR/Carrier;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/128660724]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 Instagram 65.0.0.12.86 (iPhone10,4; iOS 12_0; en_CO; en-CO; scale=2.00; '
 'gamut=wide; 750x1334; 125889668)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/13.1.72140 Mobile/13E238 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 '
 '[FBAN/MessengerForiOS;FBAV/183.0.0.36.93;FBBV/123940704;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/12.0;FBSS/2;FBCR/movistar;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 Instagram 67.0.0.16.99 (iPhone8,1; iOS 11_3_1; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 127410745)',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/8.0.57838 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/43.0.185608249 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1_2 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B146',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A342 Safari/601.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/61.0.3163.73 Mobile/15A402 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/6.0.51363 Mobile/12F70 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/54.0.2840.91 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Mercury/8.8.3 Mobile/11B554a Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/28.0.157793287 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/39.0.175034278 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/57.0.2987.137 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/MessengerForiOS;FBAV/189.0.0.41.99;FBBV/128677242;FBDV/iPhone10,2;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/3;FBCR/TIGO;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Mobile/15A421 Instagram 20.0.0.24.81 (iPhone8,1; iOS 11_0_2; pl_PL; pl-PL; scale=2.00; '
 'gamut=normal; 750x1334)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/39.0.175034278 Mobile/15B150 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/40.1.177082287 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12B466',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/49.0.2623.109 Mobile/13E238 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 Instagram 62.1.0.15.94 (iPhone7,2; iOS 11_4_1; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/47.0.2526.70 Mobile/12B436 Safari/600.1.4 (000410)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/63.0.3239.73 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/41.0.178428663 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'FxiOS/5.3 Mobile/14B100 Safari/602.2.14',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/59.0.3071.102 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/MessengerForiOS;FBAV/189.0.0.41.99;FBBV/128677242;FBDV/iPhone8,2;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/3;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/16.0.124986583 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/10.0.63022 Mobile/13B143 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10A523',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/FBIOS;FBAV/195.0.0.44.99;FBBV/128807583;FBDV/iPhone9,4;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/3;FBCR/TIGO;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/129729940]',
 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/9.0.60246 Mobile/13A452 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Version/6.0 Mobile/WK10171 Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.1.139288856 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/58.0.3029.83 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/41.0.178428663 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) FxiOS/13.2b11866 Mobile/15G77 Safari/605.1.15',
 'Mozilla/5.0 (iPad; CPU OS 7_0_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'GSA/10.0.63022 Mobile/11A501 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/48.0.2564.104 Mobile/13D15 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 '
 '[FBAN/MessengerForiOS;FBAV/188.0.0.38.99;FBBV/127861730;FBDV/iPhone10,6;FBMD/iPhone;FBSN/iOS;FBSV/12.0;FBSS/3;FBCR/Avantel;FBID/phone;FBLC/en_US;FBOP/5]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/68.0.3440.83 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/5.2.43972 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) '
 'Mobile/14D27 '
 '[FBAN/FBIOS;FBAV/82.0.0.42.69;FBBV/51077300;FBRV/0;FBDV/iPhone9,4;FBMD/iPhone;FBSN/iOS;FBSV/10.2.1;FBSS/3;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5]',
 'Outlook-iOS/696.1208477.prod.iphone (2.103.0)',
 'Mozilla/5.0 (iPad; CPU OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Mobile/15A402 '
 '[FBAN/FBIOS;FBAV/143.0.0.76.90;FBBV/73343453;FBDV/iPad5,4;FBMD/iPad;FBSN/iOS;FBSV/11.0.1;FBSS/2;FBCR/Carrier;FBID/tablet;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/9.0.60246 Mobile/13A452 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 '
 '[FBAN/FBIOS;FBAV/172.0.0.46.94;FBBV/108425359;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/11.3.1;FBSS/2;FBCR/Play;FBID/phone;FBLC/en_GB;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 2_2_1 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, '
 'like Gecko) Version/3.1.1 Mobile/5H11 Safari/525.20',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/39.0.175034278 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; fr-fr) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'FxiOS/7.5b3349 Mobile/14F89 Safari/603.2.4',
 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Coast/3.21.84640 Mobile/12B411 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/46.0.189829128 Mobile/15E216 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C153 Instagram 71.0.0.14.101 (iPhone9,1; iOS 11_2_1; es_CO; es-CO; scale=2.00; '
 'gamut=wide; 750x1334; 130735782)',
 'Outlook-iOS/696.1028740.prod.iphone (2.95.0)',
 'Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/63.0.3239.73 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/62.0.3202.70 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 Instagram 57.0.0.9.79 (iPhone9,3; iOS 11_4_1; pl_GB; pl-GB; scale=2.00; '
 'gamut=wide; 750x1334)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/36.0.169645775 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/42.0.2311.47 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) '
 'Mobile/14B100',
 'Gazetapl/3.5.12 EmbeddedBrowser (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 '
 '(KHTML, like Gecko) Mobile/15F79 DeviceUID: C8D0460C-55CF-43AC-BBBB-E20A8E702BB0',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12F70',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C114',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_1 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14A5346a Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/56.0.2924.79 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 11_1_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/63.0.3239.73 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12B440',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Mobile/14F89 [FBAN/FBIOS;FBAV/49.0.0.72.166;FBBV/22916291;FBDV/iPhone6,2;FBMD/iPhone;FBSN/iPhone '
 'OS;FBSV/10.3.2;FBSS/2; FBCR/Orange;FBID/phone;FBLC/pl_PL;FBOP/5]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Mobile/15A372',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/24.1.151204851 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; tr-tr) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8J3 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/50.0.2661.95 Mobile/13F69 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/47.0.2526.70 Mobile/13B143 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/57.0.2987.137 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/19.0.133715217 Mobile/14A403 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/18.0.130791545 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 '
 '[FBAN/FBIOS;FBAV/197.1.0.69.100;FBBV/130896868;FBDV/iPhone9,1;FBMD/iPhone;FBSN/iOS;FBSV/12.1;FBSS/2;FBCR/Avantel;FBID/phone;FBLC/en_US;FBOP/5;FBRV/131300651]',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14F5089a Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 Instagram 50.0.0.52.188 (iPhone7,2; iOS 11_4_1; es_CO; es; scale=2.00; '
 'gamut=normal; 750x1334)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/13.1.72140 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D60 '
 '[FBAN/FBIOS;FBAV/179.0.0.50.82;FBBV/116150041;FBDV/iPhone10,4;FBMD/iPhone;FBSN/iOS;FBSV/11.2.5;FBSS/2;FBCR/T-Mobile.pl;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13F69 '
 '[FBAN/FBIOS;FBAV/59.0.0.51.142;FBBV/33266808;FBRV/0;FBDV/iPhone7,1;FBMD/iPhone;FBSN/iPhone '
 'OS;FBSV/9.3.2;FBSS/3;FBCR/Telkomsel;FBID/phone;FBLC/en_US;FBOP/5]',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/69.0.3497.91 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/52.0.2743.84 Mobile/13G34 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79 '
 '[FBAN/MessengerForiOS;FBAV/170.1.0.57.96;FBBV/113832539;FBDV/iPhone10,5;FBMD/iPhone;FBSN/iOS;FBSV/11.4;FBSS/3;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/68.0.3440.83 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; da-dk) AppleWebKit/534.46.0 (KHTML, '
 'like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D100 '
 '[FBAN/FBIOS;FBAV/172.0.0.46.94;FBBV/108425359;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.2.6;FBSS/2;FBCR/OneCall;FBID/phone;FBLC/nb_NO;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) FxiOS/9.3b7374 Mobile/15A402 Safari/604.1.38',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/66.0.3359.122 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D100 '
 '[FBAN/FBIOS;FBAV/172.0.0.46.94;FBBV/108425359;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.2.6;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/41.0.2272.56 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13F72 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Mobile/11B554a',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) '
 'Mobile/9B206',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) GSA/56.0.208290612 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13E236 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/63.0.3239.73 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 '
 '[FBAN/MessengerForiOS;FBAV/164.0.0.60.91;FBBV/105889540;FBDV/iPhone10,6;FBMD/iPhone;FBSN/iOS;FBSV/11.3.1;FBSS/3;FBCR/Orange;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'FxiOS/10.6b8836 Mobile/15D60 Safari/604.5.6',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/61.0.217752169 Mobile/15B150 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.0.141836113 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13F69',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'Mobile/10B329 [Pinterest/iOS]',
 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/44.0.2403.67 Mobile/12H143 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'FxiOS/5.3 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Mobile/14C92',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 '
 '[FBAN/MessengerForiOS;FBAV/192.0.0.46.101;FBBV/131204877;FBDV/iPhone10,4;FBMD/iPhone;FBSN/iOS;FBSV/12.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/11.1.66360 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/50.2.198126961 Mobile/15E302 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 Instagram 71.0.0.14.101 (iPhone8,1; iOS 12_1; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 130735782)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/51.0.2704.64 Mobile/13F69 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 9_3_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/49.0.2623.109 Mobile/13E238 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 Instagram 65.0.0.12.86 (iPhone9,4; iOS 12_0; es_CO; es-CO; scale=2.61; gamut=wide; '
 '1080x1920; 125889668)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/FBIOS;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/TIGO;FBID/phone;FBLC/en_US;FBOP/5;FBRV/121845328]',
 'Mozilla/5.0 (iPad; CPU OS 9_2_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/11.1.66360 Mobile/13D15 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 Instagram 72.0.0.20.101 (iPhone8,1; iOS 12_1; en_CO; en-CO; scale=2.00; '
 'gamut=normal; 750x1334; 131642248)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/MessengerForiOS;FBAV/191.0.0.54.98;FBBV/130377189;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko)',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Mobile/8B117',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/43.0.185608249 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/31.0.161834491 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12B466',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Mobile/14F89 '
 '[FBAN/FBIOS;FBAV/179.0.0.50.82;FBBV/116150041;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/10.3.2;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPod touch; CPU iPhone OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like '
 'Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/MessengerForiOS;FBAV/189.0.0.41.99;FBBV/128677242;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A452 Safari/601.1 PTST/391',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.3 Mobile/14E277 Safari/603.1.30',
 'Mozilla/5.0 (iPad; CPU OS 9_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13C75',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'GSA/42.0.183854831 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'Mobile/14A456',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Mobile/15B150 '
 '[FBAN/MessengerForiOS;FBAV/147.0.0.50.87;FBBV/84235609;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.1.1;FBSS/2;FBCR/Orange;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/54.0.204505792 Mobile/15F79 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 Instagram 71.0.0.14.101 (iPhone9,3; iOS 12_1; es_CO; es-CO; scale=2.00; gamut=wide; '
 '750x1334; 130735782)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'GSA/3.2.1.25875 Mobile/11B554a Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/61.0.217752169 Mobile/16A366 Safari/604.1',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0_2 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, '
 'like Gecko) Version/3.1.1 Mobile/5C1 Safari/525.20',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'GSA/31.0.161834491 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/43.0.2357.56 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) GSA/40.1.177082287 Mobile/15B202 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 '
 '[FBAN/MessengerForiOS;FBAV/192.0.0.46.101;FBBV/131204877;FBDV/iPhone10,6;FBMD/iPhone;FBSN/iOS;FBSV/12.1;FBSS/3;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0(iPad; U; CPU OS 4_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) '
 'Version/5.0.2 Mobile/8F191 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Mobile/15A432 '
 '[FBAN/FBIOS;FBAV/146.0.0.73.91;FBBV/75938921;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/11.0.3;FBSS/2;FBCR/T-Mobile.pl;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 '
 '[FBAN/FBIOS;FBAV/189.0.0.44.93;FBBV/124150883;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/12.0;FBSS/2;FBCR/TIGO;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/125136024]',
 'Mozilla/5.0 (iPad; CPU OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 '
 '[FBAN/FBIOS;FBAV/198.0.0.57.101;FBBV/131415284;FBDV/iPad6,11;FBMD/iPad;FBSN/iOS;FBSV/12.1;FBSS/2;FBCR/;FBID/tablet;FBLC/es_LA;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Mobile/14C92 '
 '[FBAN/FBIOS;FBAV/172.0.0.46.94;FBBV/108425359;FBDV/iPhone6,2;FBMD/iPhone;FBSN/iOS;FBSV/10.2;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 Instagram 71.0.0.14.101 (iPhone7,2; iOS 12_1; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 750x1334; 130735782)',
 'Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14C89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/13.1.72140 Mobile/13E233 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D60 Instagram 33.0.0.11.96 (iPhone9,4; iOS 11_2_5; pl_PL; pl-PL; scale=2.61; '
 'gamut=wide; 1080x1920)',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/62.0.3202.70 Mobile/13G36 Safari/601.1.46',
 'Gazetapl/3.5.12 EmbeddedBrowser (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 '
 '(KHTML, like Gecko) Mobile/14G60 DeviceUID: 00000000-0000-0000-0000-000000000000',
 'Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12A365',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/52.0.2743.84 Mobile/14A456 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A452 Safari/601.1 PTST/399',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 '
 '[FBAN/MessengerForiOS;FBAV/192.0.0.46.101;FBBV/131204877;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/12.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPad; CPU OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/57.0.2987.100 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'Mercury/8.9.4 Mobile/11B554a Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'Mobile/15A432',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 '
 '[FBAN/FBIOS;FBAV/192.0.0.61.85;FBBV/126707849;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/12.0;FBSS/2;FBCR/movistar;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/127804168]',
 'Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C202',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 Instagram 31.0.0.14.97 (iPhone9,3; iOS 11_4_1; es_PL; es-PL; scale=2.00; '
 'gamut=wide; 750x1334)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Mobile/14G60 Instagram 70.1.0.15.98 (iPhone5,1; iOS 10_3_3; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 640x1136; 130350235)',
 'Mozilla/5.0 (iPad; CPU OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/66.0.3359.122 Mobile/15A432 Safari/604.1',
 'Gazetapl/3.5.12 EmbeddedBrowser (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 '
 '(KHTML, like Gecko) Mobile/15E302 DeviceUID: C5F76C2D-C109-47E0-BE12-81B5C0F1D15D',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/FBIOS;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/124134826]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/17.1.129017588 Mobile/13G34 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/59.0.3071.102 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/43.0.2357.61 Mobile/12F70 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'GSA/3.2.0.25255 Mobile/11B554a Safari/8536.25',
 'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/22.1.146053689 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Mobile/9B176',
 'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/6.0.51363 Mobile/11D201 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79 '
 '[FBAN/FBIOS;FBAV/179.0.0.50.82;FBBV/116150041;FBDV/iPhone8,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4;FBSS/3;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'FxiOS/1.1 Mobile/13B143 Safari/601.1.46',
 'Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/45.0.2454.89 Mobile/13A344 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Mobile/14F89 '
 '[FBAN/FBIOS;FBAV/98.0.0.48.70;FBBV/62465497;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/10.3.2;FBSS/2;FBCR/o2-de;FBID/phone;FBLC/de_DE;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 Instagram 65.0.0.12.86 (iPhone10,5; iOS 12_0; es_CO; es-CO; scale=2.61; '
 'gamut=wide; 1080x1920; 125889668)',
 'AppleCoreMedia/1.0.0.15G77 (iPhone; U; CPU OS 11_4_1 like Mac OS X; nl_nl)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 '
 '[FBAN/FBIOS;FBAV/173.0.0.65.96;FBBV/109978100;FBDV/iPhone8,4;FBMD/iPhone;FBSN/iOS;FBSV/11.3.1;FBSS/2;FBCR/T-Mobile.pl;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A343 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPod touch; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like '
 'Gecko) Version/10.0 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Mobile/14G60 Instagram 65.0.0.12.86 (iPhone5,1; iOS 10_3_3; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 640x1136; 125889668)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D100 '
 '[FBAN/MessengerForiOS;FBAV/171.0.0.59.94;FBBV/114465607;FBDV/iPhone10,4;FBMD/iPhone;FBSN/iOS;FBSV/11.2.6;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 '
 '[FBAN/FBIOS;FBAV/171.0.0.49.95;FBBV/107251038;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.3.1;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8J3 Safari/6533.18.5',
 'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'CriOS/47.0.2526.107 Mobile/11D257 Safari/9537.53',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/11.0.65374 Mobile/13C75 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/70.0.3538.75 Mobile/14D27 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) '
 'CriOS/56.0.2924.79 Mobile/14C92 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/MessengerForiOS;FBAV/192.0.0.46.101;FBBV/131204877;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1_2 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, '
 'like Gecko) Mobile/7D11',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 Instagram 65.0.0.12.86 (iPhone8,4; iOS 12_0; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 640x1136; 125889668)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/MessengerForiOS;FBAV/189.0.0.41.99;FBBV/128677242;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/7.0.55539 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79 '
 '[FBAN/FBIOS;FBAV/179.0.0.50.82;FBBV/116150041;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.4;FBSS/2;FBCR/Orange;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/34.1.167176684 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) '
 'CriOS/30.0.1599.12 Mobile/11A465 Safari/8536.25 (3B92C18B-D9DE-4CB7-A02A-22FD2AF17C8F)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/MessengerForiOS;FBAV/189.0.0.41.99;FBBV/128677242;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like '
 'Gecko) CriOS/69.0.3497.105 Mobile/15C153 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 '
 '[FBAN/FBIOS;FBAV/197.1.0.69.100;FBBV/130896868;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/12.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/131758933]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/52.0.2743.84 Mobile/13G35 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like '
 'Gecko) Mobile/15A432 Instagram 19.0.0.27.91 (iPhone9,4; iOS 11_0_3; pl_PL; pl-PL; scale=2.61; '
 'gamut=wide; 1080x1920)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'Mobile/14G60 '
 '[FBAN/FBIOS;FBAV/198.0.0.57.101;FBBV/131415284;FBDV/iPhone5,1;FBMD/iPhone;FBSN/iOS;FBSV/10.3.3;FBSS/2;FBCR/TIGO;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/131930380]',
 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/8.0.57838 Mobile/13A452 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/57.0.2987.137 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPod touch; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like '
 'Gecko) Version/9.0 Mobile/13D15 Safari/601.1',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like '
 'Gecko) Version/4.0 Mobile/7A341 Safari/528.16',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 Instagram 66.0.0.14.101 (iPhone8,4; iOS 12_0; es_CO; es-CO; scale=2.00; '
 'gamut=normal; 640x1136; 126719886)',
 'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/42.0.183854831 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Mobile/15B202 '
 '[FBAN/FBIOS;FBAV/155.0.0.36.93;FBBV/87992437;FBDV/iPhone10,6;FBMD/iPhone;FBSN/iOS;FBSV/11.1.2;FBSS/3;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Mobile/14C92 '
 '[FBAN/MessengerForiOS;FBAV/116.0.0.37.70;FBBV/56773907;FBDV/iPhone6,2;FBMD/iPhone;FBSN/iOS;FBSV/10.2;FBSS/2;FBCR/Orange;FBID/phone;FBLC/en_GB;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) GSA/60.0.215960477 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 '
 '[FBAN/FBIOS;FBAV/177.0.0.62.98;FBBV/114599009;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/11.3.1;FBSS/2;FBCR/Orange;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_1_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) '
 'Mobile/15B150 (Ecosia ios@3.0.1.533)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 '
 '[FBAN/FBIOS;FBAV/172.0.0.46.94;FBBV/108425359;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/11.3.1;FBSS/2;FBCR/T-Mobile.pl;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 Instagram 66.0.0.14.101 (iPhone8,4; iOS 12_0_1; en_CO; en-CO; scale=2.00; '
 'gamut=normal; 640x1136; 126719886)',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Version/4.0.5 Mobile/8B118 Safari/6531.22.7',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko; '
 'Google Page Speed Insights) Version/8.0 Mobile/12F70 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/FBIOS;FBAV/195.0.0.44.99;FBBV/128807583;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/2;FBCR/Three;FBID/phone;FBLC/en_GB;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/FBIOS;FBAV/194.0.0.38.99;FBBV/127868476;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/128532838]',
 'Mozilla/5.0 (iPad; CPU OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) '
 'Mobile/14F89 '
 '[FBAN/FBIOS;FBAV/154.0.0.34.386;FBBV/87041355;FBDV/iPad3,4;FBMD/iPad;FBSN/iOS;FBSV/10.3.2;FBSS/2;FBCR/;FBID/tablet;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/FBIOS;FBDV/iPhone10,4;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/T-Mobile.pl;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'CriOS/61.0.3163.73 Mobile/15A372 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13G35 QQ/6.5.3.410 V1_IPH_SQ_6.5.3_1_APP_A Pixel/750 Core/UIWebView NetType/2G Mem/117',
 'Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'GSA/3.2.1.25875 Mobile/11B554a Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/43.0.185608249 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13A452 Safari/601.1 PTST/395',
 'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 Instagram 66.0.0.14.101 (iPhone10,6; iOS 11_4_1; es_CO; es-CO; scale=3.00; '
 'gamut=wide; 1125x2436; 126719886)',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/46.0.2490.85 Mobile/13B143 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 '
 '[FBAN/FBIOS;FBAV/171.0.0.49.95;FBBV/107251038;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/11.3.1;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15E302 '
 '[FBAN/FBIOS;FBAV/172.0.0.46.94;FBBV/108425359;FBDV/iPhone10,4;FBMD/iPhone;FBSN/iOS;FBSV/11.3.1;FBSS/2;FBCR/T-Mobile.pl;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/33.0.164895372 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'GSA/28.0.157793287 Mobile/13G36 Safari/601.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/44.0.2403.65 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'CriOS/46.0.2490.73 Mobile/13B143 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en-us) AppleWebKit/534.46.0 (KHTML, '
 'like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'OPiOS/14.0.0.104835 Mobile/12F69 Safari/9537.53',
 'Mozilla/5.0 (iPad; CPU OS 9_0_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13A452',
 'Mozilla/5.0 (iPad; CPU OS 11_0_3 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'GSA/38.0.172903409 Mobile/15A432 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 Instagram 66.0.0.14.101 (iPhone9,3; iOS 12_0_1; en_CO; en-CO; scale=2.00; '
 'gamut=wide; 750x1334; 126719886)',
 'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/6.0.51363 Mobile/12F69 Safari/600.1.4',
 'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/66.0.3359.122 Mobile/15D60 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79 '
 '[FBAN/FBIOS;FBAV/140.0.0.63.89;FBBV/70896504;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'CriOS/62.0 Mobile/15D100 Safari/604.5.6',
 'Mozilla/5.0 (iPad; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.33.0.2 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B143 Safari/601.1',
 'Mozilla/5.0 (iPod; U; CPU iPhone OS 2_2 like Mac OS X; en-us) AppleWebKit/525.18.1 (KHTML, like '
 'Gecko) Version/3.1.1 Mobile/5G77a Safari/525.20',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B93',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C153 '
 '[FBAN/FBIOS;FBAV/162.0.0.47.94;FBBV/95649710;FBDV/iPhone10,5;FBMD/iPhone;FBSN/iOS;FBSV/11.2.1;FBSS/3;FBCR/T-Mobile.pl;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Mobile/13G36 [FBAN/FBIOS;FBAV/178.0.0.62.84;FBBV/115359828;FBDV/iPad2,1;FBMD/iPad;FBSN/iPhone '
 'OS;FBSV/9.3.5;FBSS/1;FBCR/;FBID/tablet;FBLC/es_LA;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/62.0.3202.70 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 12_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/12.0 Mobile/15E148 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 '
 '[FBAN/FBIOS;FBAV/189.0.0.44.93;FBBV/124150883;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/12.0;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/125136024]',
 'Mozilla/5.0 (iPad; CPU OS 9_3_4 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/52.0.2743.84 Mobile/13G35 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 '
 '[FBAN/FBIOS;FBAV/189.0.0.44.93;FBBV/124150883;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/12.0;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/125136024]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/69.0.3497.105 Mobile/14E304 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) GSA/28.0.157793287 Mobile/14F89 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/15G77 '
 '[FBAN/MessengerForiOS;FBAV/177.0.0.38.75;FBBV/119094790;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4.1;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) '
 'Mobile/15C153 '
 '[FBAN/FBIOS;FBAV/155.0.0.36.93;FBBV/87992437;FBDV/iPhone6,2;FBMD/iPhone;FBSN/iOS;FBSV/11.2.1;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/21.1.139288856 Mobile/14B100 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Version/11.1.2 Mobile/14E304 Safari/605.1.15',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like '
 'Gecko) CriOS/67.0.3396.87 Mobile/14B100 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.2 (KHTML, like Gecko) '
 'Version/11.0 Mobile/15D5046b Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Mobile/12B410',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'FxiOS/8.0.1b4659 Mobile/13G36 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'Version/8.0 Mobile/12A366 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) '
 'Mobile/14C92 '
 '[FBAN/FBIOS;FBAV/175.0.0.47.102;FBBV/112197024;FBDV/iPhone8,1;FBMD/iPhone;FBSN/iOS;FBSV/10.2;FBSS/2;FBCR/Play;FBID/phone;FBLC/pl_PL;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPad; CPU OS 9_3_5 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/18.0.130791545 Mobile/13G36 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16B92 '
 '[FBAN/FBIOS;FBAV/195.0.0.44.99;FBBV/128807583;FBDV/iPhone9,2;FBMD/iPhone;FBSN/iOS;FBSV/12.1;FBSS/3;FBCR/Carrier;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/129729940]',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0_2 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like '
 'Gecko) Mobile/8A400',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) '
 'Version/10.0 Mobile/14E269 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/18.0.130791545 Mobile/13G35 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/66.0.3359.122 Mobile/14G60 Safari/602.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.1.42378 Mobile/12B466 Safari/600.1.4',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; fr-fr) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/48.0.2564.87 Mobile/13D15 Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) '
 'Mobile/11D201',
 'Mozilla/5.0 (iPad; CPU OS 11_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/63.0.3239.73 Mobile/15C114 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
 'FxiOS/9.0b6052 Mobile/15A372 Safari/604.1.38',
 'Mozilla/5.0 (iPad; CPU OS 10_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/18.0.130791545 Mobile/14A456 Safari/600.1.4',
 'Mozilla/5.0 (iPad; U; CPU OS 4_3_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like '
 'Gecko) Version/5.0.2 Mobile/8G4 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) '
 'Version/9.0 Mobile/13B5110e Safari/601.1',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_1_3 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, '
 'like Gecko) Mobile/7E18',
 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 '
 'Mobile/3B48b Safari/419.3',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like '
 'Gecko) Mobile/16A404 '
 '[FBAN/FBIOS;FBAV/195.0.0.44.99;FBBV/128807583;FBDV/iPhone8,2;FBMD/iPhone;FBSN/iOS;FBSV/12.0.1;FBSS/3;FBCR/Avantel;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/0]',
 'AdsBot-Google-Mobile (+http://www.google.com/mobile/adsbot.html) Mozilla (iPhone; U; CPU iPhone '
 'OS 3 0 like Mac OS X) AppleWebKit (KHTML, like Gecko) Mobile Safari',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79 '
 '[FBAN/FBIOS;FBAV/177.0.0.62.98;FBBV/114599009;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4;FBSS/2;FBCR/fido;FBID/phone;FBLC/en_US;FBOP/5;FBRV/0]',
 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_2_1 like Mac OS X; ko-kr) AppleWebKit/533.17.9 (KHTML, '
 'like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_3 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like '
 'Gecko) CriOS/61.0.3163.73 Mobile/15A432 Safari/602.1',
 'Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) '
 'GSA/3.1.0.23513 Mobile/10B329 Safari/8536.25',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) '
 'FxiOS/10.6b8836 Mobile/14G60 Safari/603.3.8',
 'Mozilla/5.0 (iPad; CPU OS 11_4_1 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/67.0.3396.87 Mobile/15G77 Safari/604.1',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) '
 'Mobile/15D60 '
 '[FBAN/FBIOS;FBAV/189.0.0.44.93;FBBV/124150883;FBDV/iPhone6,2;FBMD/iPhone;FBSN/iOS;FBSV/11.2.5;FBSS/2;FBCR/movistar;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/125136024]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/16A366 '
 '[FBAN/FBIOS;FBAV/195.0.0.44.99;FBBV/128807583;FBDV/iPhone7,2;FBMD/iPhone;FBSN/iOS;FBSV/12.0;FBSS/2;FBCR/Claro;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/129454019]',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
 'Mobile/15F79 '
 '[FBAN/FBIOS;FBAV/196.0.0.52.95;FBBV/129677436;FBDV/iPhone6,2;FBMD/iPhone;FBSN/iOS;FBSV/11.4;FBSS/2;FBCR/TIGO;FBID/phone;FBLC/es_LA;FBOP/5;FBRV/129948386]',
 'Mozilla/5.0 (iPad; CPU OS 11_2_2 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) '
 'CriOS/64.0.3282.112 Mobile/15C202 Safari/604.1',
 'Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) '
 'CriOS/49.0.2623.109 Mobile/14A5335b Safari/601.1.46',
 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) '
 'GSA/5.4.49956 Mobile/12F70 Safari/600.1.4']

ANDRIOD_USER_AGENTS: Final[list[str]] = ['Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like '
 'Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19',
 'Mozilla/5.0 (Linux; U; Android 2.2) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile '
 'Safari/533.1',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532G Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; vivo 1713 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/53.0.2785.124 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/43.0.2357.93 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 baiduboxapp/8.6.5 (Baidu; P1 5.1.1)',
 'Mozilla/5.0 (Linux; Android 6.0.1; CPH1607 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; vivo 1603 Build/MMB29M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4A Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/60.0.3112.116 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; vivo 1606 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/53.0.2785.124 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1; vivo 1716 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L22 Build/HUAWEIMYA-L22) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX2 Build/HUAWEITRT-LX2; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L21 Build/HUAWEICAM-L21; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Dalvik/1.6.0 (Linux; U; Android 4.1.1; BroadSign Xpress 1.0.14 B- (720) Build/JRO03H)',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; BroadSign Xpress 1.0.15-6 B- (720) Build/JRO03H) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G7102 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L22 Build/HUAWEICUN-L22; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J730GM Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; HUAWEI MT7-TL00 Build/HuaweiMT7-TL00) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.3.8.909 '
 'Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; BLL-L22 Build/HUAWEIBLL-L22) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-N920C Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J710F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; CPH1723 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; GT-I9300 Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G610M Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I8190 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; vivo 1610 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/53.0.2785.124 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG GT-I9195 Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.059) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G570M Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 2.2; en-us; SCH-I800 Build/FROYO) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1 DMBrowser-BV',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J120M Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-14) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03 Build/HUAWEICAM-L03) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; ME371MG Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J111M Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG GT-I9301I Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-G900F Build/LRX21T) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.2 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5)) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L03 Build/HUAWEIMYA-L03) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-L53 Build/HUAWEITRT-L53) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 '
 '(KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7',
 'Mozilla/5.0 (Linux; U; Android 2.2.1; en-us; Nexus One Build/FRG83) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-162) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Xoom Build/IML77) AppleWebKit/535.7 (KHTML, like '
 'Gecko) CrMo/16.0.912.75 Safari/535.7',
 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/LMY48B ) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 5 Build/LMY48B; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/43.0.2357.65 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G950F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/5.2 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-152) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23 Build/HUAWEIVNS-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; WT19M-FI Build/KTU84Q)',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.063) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J710MN Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG GT-I9505 Build/LRX22C) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I9100 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Plus Build/NPNS25.137-92-14) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 6.0; DIG-L03 Build/HUAWEIDIG-L03) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play Build/OPP27.91-87) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Plus Build/NRD90M.04.026) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (4) Build/NPJS25.93-14-8.1-9) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; ALE-L23 Build/HuaweiALE-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; GT-P5210 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; Moto G (5S) Build/OPP28.65-37) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; pt-br; MZ608 Build/7.7.1-141-7-FLEM-UMTS-LA) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG GT-I9505 Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FLA-LX3 Build/HUAWEIFLA-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-L53) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; HUAWEI VNS-L23 Build/HUAWEIVNS-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; SM-T110 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0.1; MotoG3 Build/MPIS24.107-55-2-17) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J200M Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L23 Build/HuaweiALE-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T530 Build/LRX22G) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play Build/NPIS26.48-43-2) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; Lenovo-A6020l36 Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-P5110 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J106B Build/MMB29Q) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.3; Nexus 10 Build/JSS15Q) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/29.0.1547.72 Safari/537.36 DMBrowser-BV',
 'Mozilla/5.0 (Linux; Android 7.0; PRA-LX3 Build/HUAWEIPRA-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; SAMSUNG SM-J701M Build/M1AJQ) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G920F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J710MN) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G800F Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko; '
 'Google Page Speed Insights) Chrome/41.0.2272.118 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; ASUS_T00J Build/KVT49L) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L23 Build/HUAWEIMYA-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; Moto G (5)) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-T800 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.107 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L03) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-J600G Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-J600G Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI LUA-L23 Build/HUAWEILUA-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; RKM MK902 Build/KOT49H) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; BLL-L23 Build/HUAWEIBLL-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G950F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G355M Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG GT-I9515 Build/LRX22C) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; LG-X240 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L23 Build/HUAWEICUN-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Dalvik/1.6.0 (Linux; U; Android 4.0.4; opensign_x86 Build/IMM76L)',
 'Mozilla/5.0 (Linux; Android 8.0.0; FLA-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; SM-J701M Build/M1AJQ) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; ALE-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; RNE-L23 Build/HUAWEIRNE-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-J600G) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.181 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L23 Build/HUAWEICAM-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G900F Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-A520F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; XT1068 Build/MPB24.65-34-3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-J700M Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; LG-K430 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-I8200N Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.062) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J500M Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5)) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G935F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J320M Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; Nexus S Build/GRJ22) AppleWebKit/533.1 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/533.1 DMBrowser-BV',
 'Mozilla/5.0 (Linux; Android 5.0.2; vivo Y51 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/53.0.2785.124 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 2.3.1; en-us; MID Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; LDN-LX3 Build/HUAWEILDN-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-U29 Build/HUAWEICUN-U29) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (4) Build/NPJS25.93-14-18) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; LG-K350 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; Moto G (5S)) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.059) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/Orca-Android;FBAV/190.1.0.27.95;]',
 'Mozilla/5.0 (Android; Mobile; rv:38.0) Gecko/38.0 Firefox/38.0',
 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/34.0.1847.114 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/60.0.3112.116 Mobile Safari/537.36 '
 '[FB_IAB/MESSENGER;FBAV/136.0.0.8.90;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-A800I Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 5.1; XT1033 Build/LPBS23.13-56-2) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J105B Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G950F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Lenovo A2016b30 Build/MRA58K) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; SAMSUNG SM-J250M Build/NMF26X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-J120M Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J120M Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-T550 Build/MMB29M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; 4049G Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.2 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Plus) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, '
 'like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:50.0) Gecko/50.0 Firefox/50.0',
 'Mozilla/5.0 (Linux; Android 5.1.1; ASUS_X00BD Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CRO-L23 Build/HUAWEICRO-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; G735-L03 Build/HuaweiG735-L03) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-J510FN Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; LENNY3 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.85 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G (5S) Plus Build/NPSS26.116-26-18) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Android; Mobile; rv:34.0) Gecko/34.0 Firefox/34.0',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L23 Build/HUAWEICUN-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G903F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G930F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; SM-J250M Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; G3313) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; F3113 Build/33.3.A.1.97) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; RNE-L03 Build/HUAWEIRNE-L03) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G Play Build/MPIS24.241-15.3-26) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-A520F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-8-2-2) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; BLL-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5 Build/MRA58N) AppleWebKit/537.36(KHTML, like Gecko) '
 'Chrome/69.0.3464.0 Mobile Safari/537.36 Chrome-Lighthouse',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI LUA-L03 Build/HUAWEILUA-L03) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J106B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 7.0; Mobile; rv:59.0) Gecko/59.0 Firefox/59.0',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; GT-P5200 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 4.4.2; HUAWEI P7-L12 Build/HuaweiP7-L12) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; XT1033) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G (5S) Plus) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; SM-J510MN Build/NMF26X) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G935F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-J710MN Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6)) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; CHC-U23 Build/HuaweiCHC-U23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG SM-G900F Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; LG-L38C Build/GRK39F) AppleWebKit/533.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1 MMS/LG-Android-MMS-V1.0/1.2',
 'Mozilla/5.0 (Linux; Android 5.0.2; SM-G530M Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; ALE-L23 Build/HuaweiALE-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI LUA-U23 Build/HUAWEILUA-U23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J120M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android; 4.1.2; GT-I9100 Build/000000) AppleWebKit/537.22 (KHTML, like '
 'Gecko) Chrome/25.0.1234.12 Mobile Safari/537.22 OPR/14.0.123.123',
 'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; NOOK BNTV250 Build/GINGERBREAD 1.4.3) '
 'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Safari/533.1',
 'Mozilla/5.0 (Linux; Android 6.0.1; MotoG3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG SM-G800F Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ATU-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Android; Mobile; rv:40.0) Gecko/40.0 Firefox/40.0',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L03 Build/HUAWEIMYA-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 6.0; DIG-L03) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; ZTE Blade C370 Build/KOT49H) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-P5100 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; ASUS_X008DC Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; SM-T217S Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/194.0.0.42.99;]',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 4.4.2; TR10CS1 Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/30.0.0.0 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-L53 Build/HUAWEITRT-L53; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-T805 Build/MMB29K) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G900M Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-14; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; Blade A310 Build/MMB29M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; LG-M250 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L23 Build/HUAWEICUN-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J111M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; SAMSUNG SM-J510FN Build/NMF26X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG SM-T530 Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:54.0) Gecko/54.0 Firefox/54.0',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-J500FN Build/LMY48B) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T530 Build/LRX22G) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J710MN Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 7.0; G3313 Build/43.0.A.7.70) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G950F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.2 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G360T1 Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-J111M Build/LMY47V) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Dalvik/1.6.0 (Linux; U; Android 4.3.1; WT19M-FI Build/JLS36I)',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play Build/NPI26.48-43) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-N8010 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-A510F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G935F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.1.0; Mi A1 Build/OPM1.171019.026) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G955F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Android 7.0; Mobile; rv:62.0) Gecko/62.0 Firefox/62.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G930F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; LG-K240 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; PRA-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-J500FN Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G531M Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; PRA-LX3 Build/HUAWEIPRA-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 4.4.4; GT-I9060C Build/KTU84P) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto e5 plus Build/OPP27.91-41) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; LG-K580 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 4 Build/LMY48T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/40.0.2214.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; ASUS_X00BD Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 8.0.0; Mobile; rv:62.0) Gecko/62.0 Firefox/62.0',
 'Mozilla/5.0 (Linux; U; Android 2.2; fr-fr; Desire_A8181 Build/FRF91) App3leWebKit/53.1 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-L53) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; SM-G610M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Plus) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J710MN Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G925F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; ASUS_X00HD Build/NMF26F) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ATU-LX3 Build/HUAWEIATU-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-A520F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 7.0; Mobile; rv:57.0) Gecko/57.0 Firefox/57.0',
 'Mozilla/5.0 (Android 8.0.0; Mobile; rv:61.0) Gecko/61.0 Firefox/61.0',
 'Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; GT-P5210 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/Orca-Android;FBAV/192.0.0.31.101;]',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G925I Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Ilium X210 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N9005 Build/LRX21V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; LG-X220 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-A310F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 7.0; Mobile; rv:58.0) Gecko/58.0 Firefox/58.0',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.068) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G (5S) Plus) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; HUAWEI KII-L23 Build/HUAWEIKII-L23) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/Orca-Android;FBAV/190.1.0.27.95;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-T230NU Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L03 Build/HUAWEIMYA-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:62.0) Gecko/62.0 Firefox/62.0',
 'Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SCH-I545 Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-P5113 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L03 Build/HUAWEICUN-L03) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 7.0; Mobile; rv:61.0) Gecko/61.0 Firefox/61.0',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; SAMSUNG GT-I8190/I8190XXANR6 Build/JZO54K) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-L53 Build/HUAWEITRT-L53; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 6.0; HUAWEI VNS-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G355M Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; AM530 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T805 Build/LRX22G) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/3.0 Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-G900F Build/LRX21T) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; LG-K580) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.137 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-T580 Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/5.2 Chrome/51.0.2704.106 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG GT-I9515 Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G355M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; VTR-L09 Build/HUAWEIVTR-L09) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 7.0; Mobile; rv:60.0) Gecko/60.0 Firefox/60.0',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-N950U Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T800 Build/LRX22G) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/3.0 Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SM-N900T Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:57.0) Gecko/57.0 Firefox/57.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G935F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:53.0) Gecko/53.0 Firefox/53.0',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-T230 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; LG-M400 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J200M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-A510F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-gb; GT-P5110 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0; LG-X230 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J120M Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-P5210 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) Build/OPS27.82-87) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; XT1032 Build/LPBS23.13-56-2) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; HUAWEI GRA-L09 Build/HUAWEIGRA-L09) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SCH-I915 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; HTC_One Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G531H Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/Orca-Android;FBAV/192.0.0.31.101;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J110M Build/LMY48B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G531H Build/LMY48B) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; SM-J250M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; HUAWEI Y360-U03 Build/HUAWEIY360-U03) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.2.2; de-de; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 '
 '(KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-A530F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; LG-M700 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-G900T Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-L23 Build/HUAWEITAG-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/54.0.2840.85 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G930F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-15-7) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-J106B Build/MMB29Q) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; HUAWEI SCL-L03 Build/HuaweiSCL-L03) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play Build/OPP27.91-143) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; SAMSUNG SM-J510FN Build/NMF26X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.2 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG SM-T230 Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/198.0.0.53.101;]',
 'Dalvik/1.6.0 (Linux; U; Android 4.4.4; WT22M-FI Build/KTU84Q)',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G930F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.2 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J111M Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03 Build/HUAWEICAM-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-A510F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; SM-J510MN) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 8.0.0; Mobile; rv:60.0) Gecko/60.0 Firefox/60.0',
 'Mozilla/5.0 (Linux; U; Android 5.0.2; zh-CN; Redmi Note 3 Build/LRX22G) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 OPR/11.2.3.102637 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; U; Android 2.2.1; en-us; NOOK BNRV200 Build/ERD79 1.4.3) Apple WebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG GT-I9515 Build/LRX22C) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CRO-L03 Build/HUAWEICRO-L03) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-A520F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-14; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-J400M Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; LG-M400 Build/NRD90U; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/68.0.3440.85 Mobile Safari/537.36 [OBWebview/2.1.1]',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-A320FL Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SGH-T599N Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.1.0; Moto G (5S)) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G920F Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; de-de; SAMSUNG GT-I9195I Build/KTU84P) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/2.0 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:49.0) Gecko/49.0 Firefox/49.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G610M Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SM-G386T Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play Build/OPP27.91-87; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-14; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Android; Mobile; rv:36.0) Gecko/36.0 Firefox/36.0',
 'Mozilla/5.0 (Linux; Android 6.0; LG-K350) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-J110M Build/LMY48B) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/194.0.0.42.99;]',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G570M Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G900F Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; es-mx; Azumi A35CLITE Build/KTU84P) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.126 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L21 Build/HUAWEIVNS-L21) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; LDN-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; SAMSUNG GT-I9300/I9300XXUGNA5 Build/JSS15J) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.4.3; de-de; HTC_One Build/KTU84L) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Plus Build/NRD90M.04.026) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Mobile; LYF/F90M/LYF-F90M-000-02-28-130318; Android; rv:48.0) Gecko/48.0 '
 'Firefox/48.0 KAIOS/2.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-J710F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-A510F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.2 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; de-de; SAMSUNG SM-G900F Build/LRX21T) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-A300FU Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; PRA-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/Orca-Android;FBAV/191.0.0.22.98;]',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.063) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; LG-M250) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-A530F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; WAS-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G Build/MOB30M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/44.0.2403.119 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; RNE-L03) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 7.1.1; ASUS_X00ID Build/NMF26F) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-J600G Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; LG-K120 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; SM-J701M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; de-de; GT-S5830i Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'FBAndroidSDK.3.21.0',
 'Mozilla/5.0 (Linux; Android 6.0; LG-H815 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G900F Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.2 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Plus) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L03) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko; '
 'Google Page Speed Insights) Chrome/27.0.1453 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; Azumi A35C_Lite Build/KOT49H) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; SCH-S738C Build/IMM76D) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.85 Mobile Safari/537.36',
 'Mozilla/5.0 (Android; Tablet; rv:34.0) Gecko/34.0 Firefox/34.0',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-A520F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG GT-I9505 Build/LRX22C) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto e5 plus) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:52.0) Gecko/52.0 Firefox/52.0',
 'Mozilla/5.0 (Linux; Android 8.0.0; VTR-L09) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-T580 Build/MMB29K) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-A520F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.2 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; LGMS500 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; SM-A510M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 8.0.0; Mobile; rv:63.0) Gecko/63.0 Firefox/63.0',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/190.0.0.34.94;]',
 'Mozilla/5.0 (Linux; Android 5.0.1; ALE-L23 Build/HuaweiALE-L23; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-U29 Build/HUAWEICUN-U29) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-A510F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-L09 Build/HUAWEINXT-L09) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; ASUS_X00BD Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; E435 Lite Build/KOT49H) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G920I Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-J510FN Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 4.4.3; HTC_One Build/KTU84L) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G935F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03 Build/HUAWEICAM-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 4.4.2; es-us; Avvio_793 Build/KOT49H) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; TR10RS1 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/33.0.0.0 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-152; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-A320FL Build/R16NW) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03 Build/HUAWEICAM-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; Outform '
 'Build/A.0.1.82_8e41c28c6cc6907c9c8753cd72987116bdc844a5) AppleWebKit/534.30 (KHTML, like Gecko) '
 'Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J710MN Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-in; Micromax A87 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; Android 8.1.0; Mi A1) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; TA-1038 Build/O00623) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G950F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L23 Build/HUAWEICUN-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; ASUS_X008DC) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI LUA-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/194.0.0.42.99;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-T555/T555XXS1BPL1 Build/MMB29M) AppleWebKit/537.36 '
 '(KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G925I) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/51.0.2704.81 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 5.1; es-us; Ilium X210 Build/LMY47I) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23 Build/HUAWEIVNS-L23; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 6.0; 4049G Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-A500FU Build/LRX22G) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) Build/OPS27.82-72) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G925I Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; LG-K240) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; HUAWEI KII-L23 Build/HUAWEIKII-L23) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/5.0 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; Lenovo A2010-l Build/LMY47D) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (4) Build/NPJS25.93-14-8.1-9; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/198.0.0.53.101;]',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SAMSUNG-SGH-I467 Build/JZO54K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 4.4.2; HUAWEI P7-L12) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-J500M Build/LMY48B) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; DRA-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/49.0.2623.105 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; HTC Desire 10 lifestyle Build/MMB29M) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-T580 Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.2 Chrome/59.0.3071.125 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G9650 Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.3; de-de; ME302C Build/JSS15Q) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/Orca-Android;FBAV/191.0.0.22.98;]',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; de-de; GT-I9105P Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/60.0.3112.116 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; ZTE V768 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G610M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 5 Build/OPM1.171019.011) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-P5210 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T535 Build/LRX22G) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/3.2 Chrome/38.0.2125.102 Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:61.0) Gecko/61.0 Firefox/61.0',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-152; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG-SM-G900A Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36 (KHTML, '
 'like Gecko)Version/4.0 MQQBrowser/5.0 QQ-Manager Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G950F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; Moto G (5S) Build/OPP28.65-37; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; en-us; SAMSUNG SGH-M919 Build/KTU84P) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 6.0; LG-K430) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G950F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; GT-N7100 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-L53 Build/HUAWEITRT-L53; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Android; Tablet; rv:40.0) Gecko/40.0 Firefox/40.0',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto e5 Build/OPP27.91-72) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-A520F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (4) Build/NPJS25.93-14-8.1-9; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-L53 Build/HUAWEITRT-L53; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 6.0; 5044O Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; NOOK BNTV250A Build/GINGERBREAD 1.4.3) '
 'AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Safari/533.1',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-J200M Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.5 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; XT1032 Build/KXB21.14-L1.40) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; HUAWEI GRA-L09 Build/HUAWEIGRA-L09) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:55.0) Gecko/55.0 Firefox/55.0',
 'Mozilla/5.0 (Linux; Android 7.0; WAS-LX3 Build/HUAWEIWAS-LX3) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; LGMS769 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/194.0.0.42.99;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.059; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-A720F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; LG-X240) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.85 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G900M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SPH-L710 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G900F Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; F5121 Build/34.4.A.2.118) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/195.0.0.35.99;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; LIFETAB_S1036X Build/LMY47V) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/64.0.3282.137 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; BLL-L23 Build/HUAWEIBLL-L23; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Android; Tablet; rv:37.0) Gecko/37.0 Firefox/37.0',
 'Mozilla/5.0 (Linux; Android 5.0; SM-G900F Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/47.0.2526.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG SM-G900F/G900FXXU1ANE2 Build/KOT49H) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Android; Mobile; rv:37.0) Gecko/37.0 Firefox/37.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; LG-M154 Build/MXB48T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-US; B1-710 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.1 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-A720F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 7.0; Mobile; rv:56.0) Gecko/56.0 Firefox/56.0',
 'Mozilla/5.0 (Linux; Android 5.0.2; SM-G360M Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; G3123 Build/48.1.A.2.50) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G930F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L23 Build/HUAWEIMYA-L23; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; F5121) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; 7040N Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G903F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; LG-M250 Build/NRD90U; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G930F Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G900F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0; SM-G900F Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/48.0.2564.95 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; C5170 Build/IML77) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 4.4.2; T1 7.0 Build/HuaweiMediaPad) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-A520F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G950F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4) Build/MPJ24.139-64) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/58.0.3029.81 Mobile Safari/537.36 PTST/1',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L03 Build/HUAWEIMYA-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 4.4.2; CHC-U23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; G3223 Build/48.1.A.2.50) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; RNE-L21 Build/HUAWEIRNE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI NXT-L09) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto e5) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SAMSUNG-SGH-I747 Build/KOT49H) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G Play Build/NPIS26.48-43-2) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG SM-N9005 Build/KOT49H) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G900F Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Plus Build/NRD90M.04.026) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-L53 Build/HUAWEITRT-L53; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-J600G Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 7.0; G3313 Build/43.0.A.7.70; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SCH-I545 4G Build/LRX22C) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; G3313 Build/43.0.A.7.25) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; PRA-LX1 Build/HUAWEIPRA-LX1) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L23 Build/HuaweiALE-L23; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI LUA-L23 Build/HUAWEILUA-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L03 Build/HUAWEICUN-L03) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; GT-N8000 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-U29) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J111M Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; BLL-L23 Build/HUAWEIBLL-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-T580 Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; G735-L23 Build/HuaweiG735-L23) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto X Play Build/NPD26.48-24-1) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; 5042A Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; GT-N8013 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-P3110 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 4.4.4; SAMSUNG SM-J100H Build/KTU84P) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/2.0 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play Build/OPP27.91-87; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-T580 Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Kylin_5.0S Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G900F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; SAMSUNG SM-J510FN Build/NMF26X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; GT-P3113 Build/JDQ39) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-162; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; RNE-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-M830 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-J400M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; Mi A2 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L23 Build/HuaweiALE-L23; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:56.0) Gecko/56.0 Firefox/56.0',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-152) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; GT-I8190N Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.0.2; SM-G530M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G550T1 Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23 Build/HUAWEIVNS-L23; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-J320F Build/LMY47V) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.5 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; D2303 Build/18.6.A.0.182) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Android; Tablet; rv:38.0) Gecko/38.0 Firefox/38.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-N950F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.058) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; 5059A Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G531F Build/LMY48B) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SM-T210R Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-J120M Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-A520F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.4; SM-G530M Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G925F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-L53 Build/HUAWEITRT-L53; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955F Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/167.0.0.42.94;]',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-162; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; SCH-I800 Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/194.0.0.42.99;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-N910C Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; PRA-LX1 Build/HUAWEIPRA-LX1) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J320M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 4.4.2; Mobile; rv:49.0) Gecko/49.0 Firefox/49.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J500M Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/54.0.2840.85 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; G735-L03) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play Build/OPP27.91-143; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:60.0) Gecko/60.0 Firefox/60.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-J400M Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 6.0.1; Tablet; rv:50.0) Gecko/50.0 Firefox/50.0',
 'Mozilla/5.0 (Linux; Android 4.4.2; 4009A Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; de-de; SAMSUNG GT-I9100/I9100XWMS2 Build/JZO54K) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 8.0.0; FLA-LX3 Build/HUAWEIFLA-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 4.3; HUAWEI P7 mini Build/HuaweiP7Mini) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J710MN Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-152; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 7.1.1; SAMSUNG SM-J510MN Build/NMF26X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; Telekom Puls Build/LRX21M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/60.0.3112.116 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; 4047A Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J120M Build/LMY47X; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; MHA-L29 Build/HUAWEIMHA-L29) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 6.0; es-us; AVVIO Q501 Build/MRA58K; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/49.0.2623.105 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; es-us; 4009A Build/KOT49H) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SAMSUNG-SGH-I497 Build/JZO54K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G313MU Build/KOT49H) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/190.0.0.34.94;]',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23 Build/HUAWEIVNS-L23; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 7.1.1; SM-J510MN Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G903F Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; moto g(6) play Build/OPP27.91-143; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 7.0; LGMS210 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.062) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; gxq6580_weg_l Build/LMY47I) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-G903F Build/LMY47X) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; Redmi 5 Plus Build/OPM1.171019.019) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G903F/XXU1BQG1 Build/MMB29K) AppleWebKit/537.36 '
 '(KHTML, like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Android 5.0.2; Tablet; rv:45.0) Gecko/45.0 Firefox/45.0',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-gb; GT-S5830i Build/GINGERBREAD) AppleWebKit/533.1 '
 '(KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; Android 6.0; Lenovo A2016b30 Build/MRA58K) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; PRA-LX3 Build/HUAWEIPRA-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G935F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 Instagram 65.0.0.12.86 Android '
 '(24/7.0; 480dpi; 1080x1920; samsung; SM-G610M; on7xelte; samsungexynos7870; es_US; 126223536)',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G903F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; 8063 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G955F Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-A510M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J105B) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-N950F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; de-de; MD_LIFETAB_P9516 Build/IML74K) AppleWebKit/534.30 '
 '(KHTML, like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0; XT1068) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; Mi A2) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; PRA-LX3 Build/HUAWEIPRA-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:58.0) Gecko/58.0 Firefox/58.0',
 'Mozilla/5.0 (Linux; Android 5.0.1; GT-I9515 Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9301I Build/KOT49H) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.2.2; es-mx; Azumi A50c Build/JDQ39) AppleWebKit/534.30 '
 '(KHTML,like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; ALE-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-M840 Build/JZO54K) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23 Build/HUAWEIVNS-L23; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SM-T310 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) '
 'Chrome/18.0.1025.166 Safari/535.19',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G903F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G900F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/61.0.3163.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-T580 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; MotoG3 Build/MPIS24.107-55-2-17) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Lenovo TB-7304F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G570M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G (5S) Build/NPPS26.102-49-4) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; de-de; SM-T210 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G900F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955F) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; Moto G Play) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/52.0.2743.98 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G610M Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-A300FU Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/6.4 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FIG-LX3 Build/HUAWEIFIG-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/198.0.0.53.101;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570M Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Plus Build/NPNS25.137-92-14; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L21 Build/HUAWEIVNS-L21) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; LGL35G/V100) AppleWebKit/533.1 (KHTML, like Gecko) '
 'Version/4.0 Mobile Safari/533.1',
 'Mozilla/5.0 (Linux; Android 4.4.2; de-de; SAMSUNG SM-G900F/G900FXXU1ANI3 Build/KOT49H) '
 'AppleWebKit/537.36 (KHTML, like Gecko) Version/1.6 Chrome/28.0.1500.94 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; Lenovo A2016b30 Build/MRA58K) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Android; Mobile; rv:32.0) Gecko/32.0 Firefox/32.0',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-162; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; 0PCV1 Build/KOT49H) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L23 Build/HuaweiALE-L23; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; BAC-L23 Build/HUAWEIBAC-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; G8141 Build/47.1.A.5.51) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/60.0.3112.116 Mobile Safari/537.36',
 'Mozilla/5.0 (Android; Mobile; rv:35.0) Gecko/35.0 Firefox/35.0',
 'Mozilla/5.0 (Linux; Android 7.0; SM-A510M Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/64.0.3282.137 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; FLA-LX3) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03 Build/HUAWEICAM-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 7.0; BLL-L23 Build/HUAWEIBLL-L23; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G570M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX3 Build/HUAWEIWAS-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/534.30 (KHTML, like '
 'Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 6.0; Lenovo A2016b30 Build/MRA58K) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; GT-I9195L Build/KOT49H) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; DIG-L03 Build/HUAWEIDIG-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 5.1; XT1033 Build/LPBS23.13-56-2) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; HUAWEI Y520-U33 Build/HUAWEIY520-U33) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.1.0; SM-J610G) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G925F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.2 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI VNS-L23 Build/HUAWEIVNS-L23; wv) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-A300FU Build/MMB29M) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G610M Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.64 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03 Build/HUAWEICAM-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI LUA-L03 Build/HUAWEILUA-L03) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G935F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/58.0.3029.83 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; FRD-L09 Build/HUAWEIFRD-L09) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; TRT-LX3 Build/HUAWEITRT-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/Orca-Android;FBAV/190.1.0.27.95;]',
 'Mozilla/5.0 (Linux; Android 8.0.0; ANE-LX3 Build/HUAWEIANE-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/198.0.0.53.101;]',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.063) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SM-J710MN Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 7.0; SM-T580 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J200G Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/55.0.2883.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto G (5) Build/NPPS25.137-93-4) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-T555 Build/MMB29M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; LGMS210 Build/NRD90U) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI TAG-L03 Build/HUAWEITAG-L03) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-J730G Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L23 Build/HuaweiALE-L23; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-J700H Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J200M Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G800F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
 'Mozilla/5.0 (Android; Mobile; rv:39.0) Gecko/39.0 Firefox/39.0',
 'Mozilla/5.0 (Linux; Android 8.1.0; Moto G (5S) Build/OPP28.65-37; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SAMSUNG SM-G570M Build/R16NW) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/7.4 Chrome/59.0.3071.125 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; CAM-L03 Build/HUAWEICAM-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 6.0; F3313 Build/37.0.A.2.248) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0; DIG-L03 Build/HUAWEIDIG-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/196.0.0.41.95;]',
 'Mozilla/5.0 (Linux; Android 6.0; MYA-L03 Build/HUAWEIMYA-L03; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/197.0.0.46.98;]',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/195.0.0.35.99;]',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J500M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-T800 Build/MMB29K) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-J710F Build/NRD90M) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/6.2 Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; LDN-LX3 Build/HUAWEILDN-LX3; wv) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 '
 '[FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; Huawei Y301A1 Build/HuaweiY301A1) '
 'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 7.0; SM-G955F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/62.0.3202.84 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; XT1040) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SM-T217S Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J120M Build/LMY47X; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 6.0; ALE-L21 Build/HuaweiALE-L21) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.2.1; HUAWEI G610-U15 Build/HuaweiG610-U15) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; LG-F180L Build/KOT49I.F180L30b) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto G (5S) Build/NPPS26.102-49-11) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L23) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/70.0.3538.80 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; Moto E (4) Plus Build/NMA26.42-152) AppleWebKit/537.36 '
 '(KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.0.1; ALE-L23 Build/HuaweiALE-L23) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; Moto C Build/NRD90M.063; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/191.0.0.35.96;]',
 'Mozilla/5.0 (Linux; Android 7.0; HUAWEI MLA-L13 Build/HUAWEIMLA-L13) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.0; 5011A Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G355M Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SGH-T999L Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; U; Android 4.3; en-gb; GT-I9300 Build/JSS15J) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Android 7.0; Tablet; rv:59.0) Gecko/59.0 Firefox/59.0',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/63.0.3239.111 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G903F Build/MMB29K) AppleWebKit/537.36 (KHTML, '
 'like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 8.0.0; ASUS_Z012DC Build/OPR1.170623.026) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 5.1.1; SM-J111M Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) '
 'Chrome/67.0.3396.87 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 7.1.1; SM-J250M Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/193.0.0.45.101;]',
 'Mozilla/5.0 (Linux; Android 4.4.2; LG-D290 Build/KOT49I.A1423829747) AppleWebKit/537.36 (KHTML, '
 'like Gecko) Chrome/49.0.2623.105 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I605 Build/KOT49H) AppleWebKit/534.30 (KHTML, '
 'like Gecko) Version/4.0 Mobile Safari/534.30',
 'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like '
 'Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G532M Build/MMB29T; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/190.0.0.34.94;]',
 'Mozilla/5.0 (Linux; Android 6.0; LG-X240 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Version/4.0 Chrome/69.0.3497.100 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/192.0.0.34.85;]',
 'Mozilla/5.0 (Android 6.0.1; Mobile; rv:48.0) Gecko/48.0 Firefox/48.0',
 'Mozilla/5.0 (Android 7.0; Mobile; LG-M150; rv:62.0) Gecko/62.0 Firefox/62.0']

# Correctly-spelled aliases for the names in the source file.
ANDROID_BROWSER_USER_AGENTS: Final[list[str]] = ANDRIOD_BROWSER_USER_AGENTS
ANDROID_USER_AGENTS: Final[list[str]] = ANDRIOD_USER_AGENTS

USER_AGENT_CATEGORIES: Final[dict[str, list[str]]] = {
    "LATEST_USER_AGENT": LATEST_USER_AGENT,
    "IPAD_USER_AGENTS": IPAD_USER_AGENTS,
    "NEXAS5_USER_AGENTS": NEXAS5_USER_AGENTS,
    "UC_BROWSER_USER_AGENTS": UC_BROWSER_USER_AGENTS,
    "SAFARI_BROWSER_USER_AGENTS": SAFARI_BROWSER_USER_AGENTS,
    "INTERNET_EXPLORER_USER_AGENTS": INTERNET_EXPLORER_USER_AGENTS,
    "ANDRIOD_BROWSER_USER_AGENTS": ANDRIOD_BROWSER_USER_AGENTS,
    "FIREFOX_USER_AGENTS": FIREFOX_USER_AGENTS,
    "CHROME_USER_AGENTS": CHROME_USER_AGENTS,
    "LINUX_USER_AGENTS": LINUX_USER_AGENTS,
    "WINDOWS_USER_AGENTS": WINDOWS_USER_AGENTS,
    "MAC_OS_USER_AGENTS": MAC_OS_USER_AGENTS,
    "IOS_USER_AGENTS": IOS_USER_AGENTS,
    "ANDRIOD_USER_AGENTS": ANDRIOD_USER_AGENTS,
}

ALL_USER_AGENTS: Final[list[str]] = [
    *LATEST_USER_AGENT,
    *IPAD_USER_AGENTS,
    *NEXAS5_USER_AGENTS,
    *UC_BROWSER_USER_AGENTS,
    *SAFARI_BROWSER_USER_AGENTS,
    *INTERNET_EXPLORER_USER_AGENTS,
    *ANDRIOD_BROWSER_USER_AGENTS,
    *FIREFOX_USER_AGENTS,
    *CHROME_USER_AGENTS,
    *LINUX_USER_AGENTS,
    *WINDOWS_USER_AGENTS,
    *MAC_OS_USER_AGENTS,
    *IOS_USER_AGENTS,
    *ANDRIOD_USER_AGENTS,
]

# Deduplicate while preserving the original order.
UNIQUE_USER_AGENTS: Final[list[str]] = list(
    dict.fromkeys(ALL_USER_AGENTS)
)


def get_user_agents(
    category: str | None = None,
    *,
    unique: bool = True,
) -> list[str]:
    """Return a copy of all agents or a selected category."""
    if category is None:
        source = UNIQUE_USER_AGENTS if unique else ALL_USER_AGENTS
        return source.copy()

    try:
        source = USER_AGENT_CATEGORIES[category]
    except KeyError as error:
        available = ", ".join(sorted(USER_AGENT_CATEGORIES))
        raise ValueError(
            f"Unknown user-agent category: {category}. "
            f"Available categories: {available}"
        ) from error

    if unique:
        return list(dict.fromkeys(source))

    return source.copy()


def choose_user_agent(
    category: str | None = None,
    *,
    unique: bool = True,
) -> str:
    """Choose one agent for use throughout one client session."""
    agents = get_user_agents(category, unique=unique)

    if not agents:
        raise ValueError("No user agents are available")

    return SystemRandom().choice(agents)


TOTAL_USER_AGENT_COUNT: Final[int] = 4669
UNIQUE_USER_AGENT_COUNT: Final[int] = 3787
