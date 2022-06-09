
# imports
import requests
import json
import os

def get_token(user, pw, exp):
    '''Generates token for ArcGIS Online'''
    
    url = 'https://www.arcgis.com/sharing/generateToken'
    payload  = {'username':user,
            'password':pw,
            'expiration':exp,
            'referer':'www.arcgis.com',
            'f':'json'}

    r = requests.post(url, data=payload)
    t =json.loads (r.text)

    if 'token' not in t:
        msg = t['error']['details']
        raise Exception(f'Failed to get token: {msg}')
    else:
        aToken = t['token']
        return(aToken)

def geocode_addr(address, url, operation, max_return, f, tkn):
    '''Geocodes an address string'''

    get_url = f'{url}/{operation}?address={address}&maxLocations={max_return}&f={f}&token={tkn}'

    geocode_r = requests.get(get_url)
    return(geocode_r)

if __name__ == '__main__':

    # inputs
    working_fldr = os.path.abspath(os.path.dirname(__file__))
    ago_creds = open(working_fldr + r'\cfg.json').read()
    creds_json = json.loads(ago_creds)
    un = creds_json['username']
    pw = creds_json['password']

    # arcgis world geocoder
    awg_url = 'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer'

    # method
    req_op = 'findAddressCandidates'
    # params
    addr = 'Outer Banks'
    max_r = 1
    format_r = 'json'

    token = get_token(un, pw, 60)
    geocode_result = (geocode_addr(addr, awg_url, req_op, max_r, format_r, token)).json()

    if geocode_result['candidates']:
        print('Address geocoded successfully...')
        print('getting lat and long...')
        x = round(geocode_result['candidates'][0]['location']['x'], 3)
        y = round(geocode_result['candidates'][0]['location']['y'], 3)
        print(f'Address {addr} is located at {y}, {x}')

    else:
        print(f'Could not geocode string: {addr}...')
        print('Try supplying more information!')


