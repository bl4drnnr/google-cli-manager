import os
import sys
import curses
import requests

from urllib.parse import urlencode
from src.common.variables import LOGO


def pad_refresh(pad, pad_pos, height, width):
    pad.refresh(pad_pos, 0, 0, 0, height - 1, width)


def navigation_control(pad, y, height, width):
    key_up, key_down = 'AB'

    for c in iter(pad.getkey, 'q'):
        if c in '\x1b\x5b':
            continue
        y -= (c == key_up)
        y += (c == key_down)
        pad_refresh(pad, y, height, width)


def print_raw_input(stdscr, prompt_string):
    curses.echo()
    stdscr.addstr(prompt_string)
    stdscr.refresh()
    user_input = stdscr.getstr()
    return user_input.decode('utf-8')


def print_logo(stdscr, color_pair_id):
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(LOGO):
        x = w // 2 - len(row) // 2
        stdscr.addstr(idx, x, row, curses.color_pair(color_pair_id))


def rewrite_line(mystring, h, stdscr=None):
    if stdscr is not None:
        win = curses.newwin(1, 54, h + 1, 0)
        win.addstr(f'{mystring}')
        win.refresh()
    else:
        print(' ' * 80, end='\r')
        print(mystring, end='\r')


def check_client_id_and_secret(client_id, client_secret):
    error_msg = ''

    url = 'https://www.googleapis.com/oauth2/v4/token'
    post_data = {'client_id': client_id, 'client_secret': client_secret,
                 'code': 'ThisIsAnInvalidCodeOnlyBeingUsedToTestIfClientAndSecretAreValid',
                 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob', 'grant_type': 'authorization_code'}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    content = requests.post(url, urlencode(post_data), headers=headers)

    try:
        content = content.json()
    except ValueError:
        error_msg = 'Unknown error: %s' % content

    if 'error' not in content or 'error_description' not in content:
        error_msg = 'Unknown error: %s' % content
    if content['error'] == 'invalid_grant':
        return error_msg
    if content['error_description'] == 'The OAuth client was not found.':
        error_msg = '\nERROR!ERROR!ERROR!\n\nNot a valid client ID. Please make sure you are following the\n' \
                    'directions exactly and that there are no extra spaces in your client ID.'
        return error_msg
    if content['error_description'] == 'Unauthorized':
        error_msg = '\nERROR!ERROR!ERROR!\n\nNot a valid client secret. Please make sure you are following\n' \
                    'the directions exactly and that there are no extra spaces in your client secret.'
        return error_msg
    error_msg = 'Unknown error: %s' % content
    return error_msg


def print_text(text, stdscr=None, error=False):
    if stdscr is not None:
        if error:
            stdscr.addstr(f'\n{text}', curses.A_BOLD | curses.color_pair(3))
        else:
            stdscr.addstr(f'\n{text}')
    else:
        print(text)


def read_file(filename, mode='r'):
    try:
        with open(os.path.expanduser(filename), mode) as f:
            return f.read()
    except IOError as e:
        print(e)
        sys.exit()
    except (LookupError, UnicodeDecodeError, UnicodeError) as e:
        print(e)
        sys.exit()
