"""
Crappy phone number library.

See test_phonenumber.py for more information
"""

import re

NANP_NUMBER = re.compile("^(?P<npa>[2-9]\d\d)(?P<nxx>[2-9]\d\d)(?P<station>\d\d\d\d)$")
NANP_COUNTRIES = ('US', 'CA', 'BB', 'BM', 'JM', 'BS', 'GU', 'GD', 'PR',
                  'KN', 'MS', 'KY', 'DO', 'DM', 'LC', 'TT', 'TC', 'VC',
                  'AG', 'VG', 'AI', 'VI', 'AS')
EU_COUNTRIES = ('AT', 'BE', 'BG', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR',
                'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT',
                'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'GB')
CANADIAN_NPA = ('204', '250', '306', '403', '416', '418', '438',
                '450', '514', '519', '581', '604', '613', '647',
                '778', '289', '226', '587', '506', '705', '709',
                '807', '819', '867', '780', '902', '905')
DOMINICAN_REPUBLIC_NPA = ('809', '829', '849')
TOLL_FREE_NPA = ('800', '866', '877', '888')
IS_PREMIUM_RATE = re.compile("^1900|^1[2-9]\d\d976")
COUNTRY_DIALING_PREFIX = {
    'US': '1',
    'CA': '1',
    'KY': '1',
    'DO': '1',
    'DM': '1',
    'LC': '1',
    'TT': '1',
    'AS': '1',
    'TC': '1',
    'VC': '1',
    'AG': '1',
    'VG': '1',
    'AI': '1',
    'VI': '1',
    'BB': '1',
    'BM': '1',
    'JM': '1',
    'BS': '1',
    'GU': '1',
    'GD': '1',
    'PR': '1',
    'KN': '1',
    'MS': '1',
    'FR': '33',
    'GB': '44',
    'BE': '32',
    'IT': '39',
    'IR': '98',
    'ES': '34',
    'NL': '31',
    'MX': '52',
    'RU': '7',
    'CN': '86',
    'JP': '81',
    'LT': '370',
    'BD': '880',
    'BF': '226',
    'BG': '359',
    'WF': '681',
    'BN': '673',
    'BO': '591',
    'BH': '973',
    'BI': '257',
    'BJ': '229',
    'BT': '975',
    'BW': '267',
    'WS': '685',
    'BR': '55',
    'BY': '375',
    'BZ': '501',
    'RW': '250',
    'RE': '262',
    'TM': '993',
    'TJ': '992',
    'RO': '40',
    'TK': '690',
    'GW': '245',
    'GT': '502',
    'GR': '30',
    'GQ': '240',
    'GP': '590',
    'GY': '592',
    'GF': '594',
    'GE': '995',
    'GA': '241',
    'GN': '224',
    'GM': '220',
    'GL': '299',
    'GI': '350',
    'GH': '233',
    'OM': '968',
    'TN': '216',
    'JO': '962',
    'HT': '509',
    'HU': '36',
    'HK': '852',
    'HN': '504',
    'VE': '58',
    'PS': '970',
    'PW': '680',
    'PT': '351',
    'AF': '93',
    'IQ': '964',
    'PA': '507',
    'PF': '689',
    'PG': '675',
    'PE': '51',
    'PK': '92',
    'PH': '63',
    'PL': '48',
    'ZM': '260',
    'EE': '372',
    'EG': '20',
    'ZA': '27',
    'EC': '593',
    'VN': '84',
    'ET': '251',
    'SO': '252',
    'ZW': '263',
    'SA': '966',
    'ER': '291',
    'MD': '373',
    'MG': '261',
    'MA': '212',
    'MC': '377',
    'UZ': '998',
    'MM': '95',
    'ML': '223',
    'MO': '853',
    'MN': '976',
    'MH': '692',
    'MU': '230',
    'MT': '356',
    'MW': '265',
    'MV': '960',
    'MQ': '596',
    'PY': '595',
    'MR': '222',
    'UG': '256',
    'MY': '60',
    'IL': '972',
    'SH': '290',
    'FI': '358',
    'FJ': '679',
    'FK': '500',
    'FM': '691',
    'NI': '505',
    'NO': '47',
    'NA': '264',
    'VU': '678',
    'NC': '687',
    'NE': '227',
    'NG': '234',
    'NZ': '64',
    'NP': '977',
    'NR': '674',
    'NU': '683',
    'CK': '682',
    'CI': '225',
    'CH': '41',
    'CO': '57',
    'CM': '237',
    'CL': '56',
    'CG': '242',
    'CF': '236',
    'CD': '243',
    'CZ': '420',
    'CY': '357',
    'CR': '506',
    'CU': '53',
    'SZ': '268',
    'SY': '963',
    'KG': '996',
    'KE': '254',
    'SR': '597',
    'KI': '686',
    'KH': '855',
    'SV': '503',
    'KM': '269',
    'ST': '239',
    'SK': '421',
    'KR': '82',
    'KP': '850',
    'KW': '965',
    'SN': '221',
    'SM': '378',
    'SL': '232',
    'SC': '248',
    'SB': '677',
    'SG': '65',
    'SE': '46',
    'SD': '249',
    'DJ': '253',
    'DK': '45',
    'DE': '49',
    'YE': '967',
    'DZ': '213',
    'UY': '598',
    'LB': '961',
    'LA': '856',
    'TV': '688',
    'TW': '886',
    'TR': '90',
    'LK': '94',
    'LI': '423',
    'LV': '371',
    'TO': '676',
    'TL': '670',
    'LU': '352',
    'LR': '231',
    'LS': '266',
    'TH': '66',
    'TG': '228',
    'TD': '235',
    'LY': '218',
    'VA': '379',
    'AC': '247',
    'AE': '971',
    'AD': '376',
    'IS': '354',
    'AM': '374',
    'AL': '355',
    'AO': '244',
    'AN': '599',
    'AR': '54',
    'AU': '61',
    'AT': '43',
    'AW': '297',
    'IN': '91',
    'TZ': '255',
    'AZ': '994',
    'IE': '353',
    'ID': '62',
    'QA': '974',
    'MZ': '258',
    'UA': '380',
    'CS': '381',
    'HR': '385',
    'SI': '386',
    'BA': '387',
    'MK': '389',
}

def i_said_ascii_god_damnit(s):
    if not s:
        return ''
    if isinstance(s, str):
        s = s.decode('utf-8', 'ignore')
    assert isinstance(s, unicode)
    return s.encode('ascii', 'ignore')

class InvalidPSTNNumber(ValueError):
    def __init__(self, phoneno=None):
        self.phoneno = phoneno

    __str__  = lambda self: "%s" % (self.phoneno)
    __repr__ = lambda self: "<%s: %s>" % (self.__class__.__name__, self)

def e164_to_country(phoneno, default=None):
    """Falls back to 'US' if not sure.  Don't pass naked e164"""
    if not phoneno:
        return default
    (cdp, number) = e164_split(phoneno)
    if not cdp:
        return default
    if cdp == '1':
        if len(number) != 10:
            return 'US'
        if is_canadian(phoneno):
            return 'CA'
        if is_dominican_republic(phoneno):
            return 'DO'
        return 'US'
    for country, cdp2 in COUNTRY_DIALING_PREFIX.items():
        if cdp == cdp2:
            return country
    return default

def strip_prefixes(phoneno):
    phoneno = phoneno.lstrip('+')
    if phoneno.startswith('011'):
        phoneno = phoneno[3:]
    if phoneno.startswith('00'):
        phoneno = phoneno[2:]
    return phoneno

def e164_split(phoneno):
    """
    Heuristic to take a phone number and return a tuple with the
    country dialing prefix and digits after the country prefix.
    Returns (None, None) if it gets confused.

    Supports naked e164, even if it is prefixed with: +/011/00

    Examples:

      assert e164_split('12036660420') == ('1', '2036660420')
      assert e164_split('+12036660420') == ('1', '2036660420')
      assert e164_split('01144123456789') == ('44', '123456789')
      assert e164_split('44123456789') == ('44', '123456789')

    """
    if not phoneno:
        return (None, None)
    if phoneno.startswith("+"):
        phoneno = phoneno[1:]
    phoneno = re.sub(r"\D", "", phoneno)
    if len(phoneno) < 5:
        return (None, None)
    if phoneno.startswith('011'):
        phoneno = phoneno[3:]
    if phoneno.startswith('00'):
        phoneno = phoneno[2:]
    if len(phoneno) < 5 or phoneno[0] == '0':
        return (None, None)
    if int(phoneno[0]) in (1, 7): # 1st and 2nd world
        return (phoneno[0], phoneno[1:])
    if int(phoneno[:2]) in ( # all 2 digit country dialing codes
        20, 27, 30, 31, 32, 33, 34, 36, 39, 40, 41, 43, 44, 45, 46, 47, 48,
        49, 51, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 64, 65, 66, 81,
        82, 84, 86, 90, 91, 92, 93, 94, 95, 98):
        return (phoneno[:2], phoneno[2:])
    else:
        return (phoneno[:3], phoneno[3:])

def e164_format(phoneno, country=None, text_names=True):
    """
    If the number doesn't appear sane, this function will spit it back
    as is.  If the number is for a country we don't know about, we
    shuold show the number in i18n format with a + prefix and country
    code.

    Country is the country code for the user.  When formatting numbers
    for this user's country we will exclude the country code.  We only
    take out the country code when we have a really good grasp on the
    formatting for a particular country.
    """
    phoneno = i_said_ascii_god_damnit(phoneno)
    if not phoneno:
        return u'Unavailable'
    if text_names and phoneno.strip().lower() in ('', 'unavailable', 'unknown'):
        return u'Unavailable'
    if text_names and phoneno.strip().lower() in ('anonymous', 'withheld', 'private'):
        return u'Anonymous'

    (cc, number) = e164_split(phoneno)
    if not cc or not number:
        return phoneno
    res = None
    trunk = None
    include_cc = True

    if cc == '1': # NANP: +1 (203) 666-1234 or 203-666-1234
        if country and country in NANP_COUNTRIES:
            include_cc = False
        m = NANP_NUMBER.search(number)
        if m: res = "%s-%s-%s" % (m.group('npa'), m.group('nxx'), m.group('station'))
    elif cc == '44': # UK: http://en.wikipedia.org/wiki/Telephone_numbers_in_the_United_Kingdom
        if country and country == 'GB':
            include_cc = False
        m = re.search("^(?P<area>1\d1|11\d|8\d\d)(?P<area2>\d{3})(?P<station>\d+)$", number)
        if m:
            res = "%s %s %s" % (m.group('area'), m.group('area2'), m.group('station'))
        else:
            m = re.search("^(?P<area>[17]\d\d\d)(?P<station>\d+)$", number)
            if m: res = "%s %s" % (m.group('area'), m.group('station'))
            m = re.search("^(?P<area>[235]\d)(?P<area2>\d{4})(?P<station>\d+)$", number)
            if m: res = "%s %s %s" % (m.group('area'), m.group('area2'), m.group('station'))
        if res:
            trunk = '0'
    elif cc == '33': # France: +33 09 12 34 56 78
        if country and country == 'FR':
            include_cc = False
        if len(number) == 9 and number[0] != '0':
            trunk = '0'
            res = "%s %s %s %s %s" % (number[0], number[1:3], number[3:5], number[5:7], number[7:9])

    if res is None:
        return "+%s %s" % (cc, number)
    if include_cc:
        if trunk is not None:
            res = "(%s)%s" % (trunk, res)
        return "+%s %s" % (cc, res)
    else:
        if trunk is not None:
            return "%s%s" % (trunk, res)
        else:
            return res

def parse_pstn_number(phoneno, country=None):
    """Returns a naked e164 number or raises hell"""
    if not phoneno:
        raise InvalidPSTNNumber(phoneno)
    phoneno = i_said_ascii_god_damnit(phoneno)
    phoneno = re.sub(r"[^+0-9]", "", phoneno)
    if len(phoneno) > 32:
        raise InvalidPSTNNumber(phoneno)
    if phoneno.startswith('+1'):
        phoneno = phoneno[1:]
    if phoneno.startswith('+'):
        phoneno = '011' + phoneno[1:]
    if '+' in phoneno:
        raise InvalidPSTNNumber(phoneno)
    if phoneno.startswith('011') or phoneno.startswith('00'):
        # International, or is it?
        if phoneno.startswith('001'):
            phoneno = phoneno[2:]
        elif phoneno.startswith('0111'):
            phoneno = phoneno[3:]
        else:
            (cdp, no) = e164_split(phoneno)
            if cdp is not None and len(no) >= 5:
                if no[0] == '0': # they left in the trunk prefix *sigh*
                    if cdp != '39': # italy is a weird exception
                        no = no[1:]
                return "%s%s" % (cdp, no)
    if phoneno.startswith('1') and re.search("^1[2-9]\d\d[2-9]\d{6}$", phoneno):
        return phoneno
    if phoneno.startswith('0') and country:
        # non-nanp natl dialing
        cdp = prefix_for_country(country)
        if cdp != '1' and len(phoneno[1:]) >= 5:
            if cdp == '39': # italy keeps trunk prefix
                return '%s%s' % (cdp, phoneno)
            else:
                return '%s%s' % (cdp, phoneno[1:])
    if country and country in NANP_COUNTRIES and re.search("^[2-9]\d\d[2-9]\d{6}$", phoneno):
        # nanp natl dialing w/o 1
        return "1%s" % (phoneno)
    raise InvalidPSTNNumber(phoneno)

def parse_caller_id(cid, country=None):
    try:
        return parse_pstn_number(cid, country)
    except InvalidPSTNNumber:
        return ''

def easy_parse(number, country='US'):
    try:
        return add_plus(parse_pstn_number(number, country))
    except InvalidPSTNNumber:
        return number

def country_in_nanp(country):
    assert len(country) == 2
    assert country == country.upper()
    return country.upper() in NANP_COUNTRIES

def cdp(phoneno):
    (cdp, number) = e164_split(phoneno)
    return cdp

def npa(phoneno):
    """10 digit numbers only"""
    return phoneno[0:3]

def nxx(phoneno):
    """10 digit numbers only"""
    return phoneno[3:6]

def is_toll_free(phoneno):
    """Only supports NANP for now"""
    (cdp, number) = e164_split(phoneno)
    return (cdp == '1' and npa(number) in TOLL_FREE_NPA)

def is_premium_rate(phoneno):
    """Only supports NANP for now"""
    (cdp, number) = e164_split(phoneno)
    return (cdp == '1' and bool(re.search(IS_PREMIUM_RATE, cdp + number)))

def is_canadian(phoneno):
    (cdp, number) = e164_split(phoneno)
    return (cdp == '1' and npa(number) in CANADIAN_NPA)

def is_dominican_republic(phoneno):
    (cdp, number) = e164_split(phoneno)
    return (cdp == '1' and npa(number) in DOMINICAN_REPUBLIC_NPA)

def prefix_for_country(country, default=None):
    return COUNTRY_DIALING_PREFIX.get(country, default)

def e164_to_nanp(phoneno):
    if not phoneno:
        return phoneno
    phoneno = phoneno.lstrip('+')
    if phoneno.startswith('1'):
        return phoneno
    else:
        return '011' + phoneno

def add_plus(phoneno):
    if not phoneno:
        return phoneno
    return '+' + phoneno.lstrip('+')
