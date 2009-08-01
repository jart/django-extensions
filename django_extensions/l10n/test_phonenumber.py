# -*- coding: utf-8 -*-

import py.test
from django_extensions.l10n.phonenumber import *

def acceptable_prefixes(x):
    yield x
    yield '+' + x
    yield '00' + x
    yield '011' + x
    yield e164_to_nanp(x)

def test_prefix_for_country():
    assert 'US' in NANP_COUNTRIES
    assert 'CA' in NANP_COUNTRIES
    assert prefix_for_country('US') == '1'
    assert prefix_for_country('CA') == '1'
    assert prefix_for_country('FR') == '33'
    assert prefix_for_country('IT') == '39'

def test_e164_to_country():
    for x in acceptable_prefixes('12036660420'):
        assert e164_to_country(x) == 'US'
    for x in acceptable_prefixes('12046660420'):
        assert e164_to_country(x) == 'CA'
    for x in acceptable_prefixes('446660420'):
        assert e164_to_country(x) == 'GB'
    for x in acceptable_prefixes('396660420'):
        assert e164_to_country(x) == 'IT'
    for x in acceptable_prefixes('336660420'):
        assert e164_to_country(x) == 'FR'
    for x in acceptable_prefixes('7336660420'):
        assert e164_to_country(x) == 'RU'
    assert e164_to_country(parse_pstn_number("023456789", 'GB')) == 'GB'
    assert e164_to_country('666') == None
    assert e164_to_country('111') == None

def test_e164_split():
    assert e164_split('') == (None, None)
    assert e164_split('0') == (None, None)
    assert e164_split('12036660420')    == ('1', '2036660420')
    assert e164_split('+12036660420')   == ('1', '2036660420')
    assert e164_split('01144123456789') == ('44', '123456789')
    assert e164_split('44123456789')    == ('44', '123456789')

def test_is_canadian():
    for x in acceptable_prefixes('12036660420'):
        assert not is_canadian(x)
    for x in acceptable_prefixes('12046660420'):
        assert is_canadian(x)

def test_is_premium_rate():
    for x in acceptable_prefixes('12036660420'):
        assert not is_premium_rate(x)
    for x in acceptable_prefixes('19002223333'):
        assert is_premium_rate(x)
    for x in acceptable_prefixes('12039763333'):
        assert is_premium_rate(x)

def test_is_toll_free():
    for x in acceptable_prefixes('12036660420'):
        assert not is_toll_free(x)
    for x in acceptable_prefixes('18226660420'):
        assert not is_toll_free(x)
    for x in acceptable_prefixes('4423456789'):
        assert not is_toll_free(x)
    for x in acceptable_prefixes('18006660420'):
        assert is_toll_free(x)
    for x in acceptable_prefixes('18776660420'):
        assert is_toll_free(x)
    for x in acceptable_prefixes('18666660420'):
        assert is_toll_free(x)
    for x in acceptable_prefixes('18886660420'):
        assert is_toll_free(x)

def test_parse_pstn_number():
    assert parse_pstn_number("12036660420", 'US')    == "12036660420"
    assert parse_pstn_number("+12036660420", 'US')   == "12036660420"
    assert parse_pstn_number("01112036660420", 'US') == "12036660420"
    assert parse_pstn_number("0012036660420", 'US')  == "12036660420"
    assert parse_pstn_number("2036660420", 'US')     == "12036660420"
    assert parse_pstn_number(u"20366集60420\u96C6", 'US') == "12036660420"
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number("2036660420"))
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number("2036660420", 'GB'))
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number("+1+2036660420"))
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number("++2036660420"))
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number("CLOWN"))
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number("unavailable"))
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number("0"))
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number(""))

    assert parse_pstn_number("12036660420", 'GB') == "12036660420"
    assert parse_pstn_number("+12036660420", 'GB') == "12036660420"
    assert parse_pstn_number("01112036660420", 'GB') == "12036660420"
    assert parse_pstn_number("0012036660420", 'GB') == "12036660420"
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number("2036660420", 'GB'))

    assert parse_pstn_number("023456789", 'GB') == "4423456789"
    py.test.raises(InvalidPSTNNumber, lambda: parse_pstn_number("023456789"))
    assert parse_pstn_number("00 33 (0)2 34 56 78", 'IR') == "332345678"
    assert parse_pstn_number("(0)2 34 56 78", 'FR') == "332345678"
    assert parse_pstn_number("00 33 (0)2 34 56 78", 'US') == "332345678"
    assert parse_pstn_number("00 44023456789", 'IT') == "4423456789"
    assert parse_pstn_number("023456789", 'IT') == "39023456789"
    assert parse_pstn_number("011 39 023456789") == "39023456789"
    assert parse_pstn_number("00 39023456789") == "39023456789"
    assert parse_pstn_number(" +39023456789 ") == "39023456789"
    assert parse_pstn_number("+44 02 3456789", 'US') == "4423456789"
    assert parse_pstn_number("+39 02 3456789", 'US') == "39023456789"
    assert parse_pstn_number(u"MOP\u01e2 +39 02 3456789", 'US') == "39023456789"
    assert isinstance(parse_pstn_number(u"MOP\u01e2 +39 02 3456789", 'US'), str)

def test_add_plus():
    assert add_plus('33333333') == '+33333333'
    assert add_plus('+33333333') == '+33333333'

def test_e164_to_nanp():
    assert e164_to_nanp(parse_pstn_number("023456789", 'GB')) == "0114423456789"
    assert e164_to_nanp(parse_pstn_number("2046660420", 'CA')) == "12046660420"
    assert e164_to_nanp(parse_pstn_number("12046660420")) == "12046660420"

def test_parse_caller_id():
    assert parse_caller_id("666", 'US') == ""
    assert parse_caller_id("12039931234", 'US') == "12039931234"
    assert parse_caller_id("2039931234", 'US') == "12039931234"
    assert e164_to_nanp(parse_caller_id("0")) == ""
    assert e164_to_nanp(parse_caller_id("unavailable")) == ""
    assert e164_to_nanp(add_plus(parse_caller_id("0"))) == ""
    assert e164_to_nanp(add_plus(parse_caller_id("unavailable"))) == ""

def test_e164_format_uk():
    for x in acceptable_prefixes('441194442222'):
        assert e164_format(x) == '+44 (0)119 444 2222'
    assert e164_format('011441914442222') == '+44 (0)191 444 2222'
    assert e164_format('01144191444222') == '+44 (0)191 444 222'
    assert e164_format('011448004442222') == '+44 (0)800 444 2222'
    assert e164_format('01144122') == '+44 122'
    assert e164_format('011441222') == '+44 1222'
    assert e164_format('0114412223') == '+44 (0)1222 3'
    assert e164_format('01144122233') == '+44 (0)1222 33'
    assert e164_format('011441222333') == '+44 (0)1222 333'

    for x in acceptable_prefixes('441194442222'):
        assert e164_format(x, 'GB') == '0119 444 2222'
    assert e164_format('011441914442222', 'GB') == '0191 444 2222'
    assert e164_format('01144191444222', 'GB') == '0191 444 222'
    assert e164_format('011448004442222', 'GB') == '0800 444 2222'
    assert e164_format('01144122', 'GB') == '+44 122'
    assert e164_format('011441222', 'GB') == '+44 1222'
    assert e164_format('0114412223', 'GB') == '01222 3'
    assert e164_format('01144122233', 'GB') == '01222 33'
    assert e164_format('011441222333', 'GB') == '01222 333'

def test_e164_format_fr():
    assert e164_format('+33934567890') == '+33 (0)9 34 56 78 90'
    assert e164_format('+33934567890', 'FR') == '09 34 56 78 90'
    assert e164_format('+33934567890', 'US') == '+33 (0)9 34 56 78 90'

def test_e164_format_us():
    assert e164_format('12039931234') == '+1 203-993-1234'
    assert e164_format('12039931234', 'US') == '203-993-1234'
    assert e164_format('12039931234', 'CA') == '203-993-1234'
    assert e164_format('12039931234', 'PR') == '203-993-1234'
    assert e164_format('', 'US') == 'Unavailable'
    assert e164_format('unavailable', 'US') == 'Unavailable'
