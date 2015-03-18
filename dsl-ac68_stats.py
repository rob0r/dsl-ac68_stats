#!/usr/bin/env python
__doc__ = '''
dsl-ac68_stats.py
    Author      : rob0r - github.com/rob0r
    Description : collect DSL stats from the Asus DSL-AC68U
    Version     : 2015031801
'''

def get_by_http(router_addr, username, password, mode):
    import urllib2
    
    # setup basic auth on the root domain
    router_url = mode + '://' + router_addr + '/'
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, router_url, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    
    # get stats
    stats_url = mode + '://' + router_addr + '/Main_AdslStatus_Content.asp'
    try:
        pagehandle = urllib2.urlopen(stats_url)
    except (urllib2.HTTPError, urllib2.URLError) as error:
        print error
        quit()
    page = pagehandle.readlines()
    
    # check to see if someone else logged in
    for line in page:
        if 'You cannot Login unless logout another user first' in line:
            print 'FAILURE: Only 1 login allowed, Logout other client and try again'
            quit(1)
    
    # now logout - so other clients can login!
    logout_url = mode + '://' + router_addr + '/Logout.asp'
    urllib2.urlopen(logout_url)
    
    return page
    
def scrape_from_http(data):
    result = {}
    for line in data:
        if '<div id="up_SNR_down">' in line:
            result['snr_down'] = ((line.replace('<div id="up_SNR_down">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_SNR_up">' in line:
                result['snr_up'] = ((line.replace('<div id="up_SNR_up">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_Line_down">' in line:
            result['atten_down'] = ((line.replace('<div id="up_Line_down">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_Line_up">' in line:
            result['atten_up'] = ((line.replace('<div id="up_Line_up">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_rate_down">' in line:
            result['rate_down'] = ((line.replace('<div id="up_rate_down">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_rate_up">' in line:
            result['rate_up'] = ((line.replace('<div id="up_rate_up">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_maxrate_down">' in line:
            result['maxrate_down'] = ((line.replace('<div id="up_maxrate_down">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_maxrate_up">' in line:
            result['maxrate_up'] = ((line.replace('<div id="up_maxrate_up">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_power_down">' in line:
            result['power_down'] = ((line.replace('<div id="up_power_down">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_power_up">' in line:
            result['power_up'] = ((line.replace('<div id="up_power_up">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_CRC_down">' in line:
            result['crc_down'] = ((line.replace('<div id="up_CRC_down">', '')).replace('</div>', '')).replace('\n', '')
        elif '<div id="up_CRC_up">' in line:
            result['crc_up'] = ((line.replace('<div id="up_CRC_up">', '')).replace('</div>', '')).replace('\n', '')
    return result
    
def print_pretty_cli(data):
    # print the data returned from scrape_from_http() : beautify for cli
    pad_size = 20
    print 'rate down: '.ljust(pad_size), data['rate_down']
    print 'rate up: '.ljust(pad_size), data['rate_up']
    print 'max rate down: '.ljust(pad_size), data['maxrate_down'] + ' kbps'
    print 'max rate up: '.ljust(pad_size), data['maxrate_up'] + ' kbps'
    print 'snr down: '.ljust(pad_size), data['snr_down']
    print 'snr up: '.ljust(pad_size), data['snr_up']
    print 'attenuation down: '.ljust(pad_size), data['atten_down']
    print 'attenuation up: '.ljust(pad_size), data['atten_up']
    print 'power down: '.ljust(pad_size), data['power_down']
    print 'power up: '.ljust(pad_size), data['power_up']
    print 'CRC errors down: '.ljust(pad_size), data['crc_down']
    print 'CRC errors up: '.ljust(pad_size), data['crc_up']

def print_cacti(data):
    # print the data returned from scrape_from_http() : formatted for cacti
    print 'rate_down:' + data['rate_down'].replace(' kbps', ''), \
    'rate_up:' + data['rate_up'].replace(' kbps', ''), \
    'max_rate_down:' + data['maxrate_down'], \
    'max_rate_up:' + data['maxrate_up'], \
    'snr_down:' + data['snr_down'].replace(' dB', ''), \
    'snr_up:' + data['snr_up'].replace(' dB', ''), \
    'attenuation_down:' + data['atten_down'].replace(' dB', ''), \
    'attenuation_up:' + data['atten_up'].replace(' dB', ''), \
    'power_down:' + data['power_down'].replace(' dbm', ''), \
    'power_up:' + data['power_up'].replace(' dbm', ''), \
    'crc_error_down:' + data['crc_down'], \
    'crc_error_up:' + data['crc_up']
    
import argparse
cliopts = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    epilog = __doc__,
    )
cliopts.add_argument('-t', '--target', metavar = '',
    default = 'router.asus.com',
    help = 'Hostname or IP (DEFAULT: router.asus.com)'
    )
cliopts.add_argument('-m', '--mode', metavar = '',
    default = 'http',
    help = 'http | https (DEFAULT: http)'
    )
cliopts.add_argument('-d', '--display', metavar = '',
    default = 'cli',
    help = 'cli | cacti (DEFAULT: cli)'
    )
cliopts.add_argument('-u', '--username', metavar = '',
    default = 'admin',
    help = 'login username (DEFAULT: admin)'
    )
cliopts.add_argument('-p', '--password', metavar = '',
    default = 'admin',
    help = 'login password (DEFAULT: admin)'
    )
cliargs = cliopts.parse_args()

if cliargs.display == 'cli':
    print_pretty_cli(scrape_from_http(get_by_http(cliargs.target, cliargs.username, cliargs.password, cliargs.mode)))
elif cliargs.display == 'cacti':
    print_cacti(scrape_from_http(get_by_http(cliargs.target, cliargs.username, cliargs.password, cliargs.mode)))
