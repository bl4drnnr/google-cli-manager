import sys
import socket
import ssl
import json
import httplib2
import time
import random

import google.oauth2.id_token
import googleapiclient
import googleapiclient.discovery
import googleapiclient.errors

from src.common.print_text import print_text

extra_args = {'prettyPrint': False}


def _backoff(n, retries, reason, stdscr=None):
    wait_on_fail = (2 ** n) if (2 ** n) < 60 else 60
    randomness = float(random.randint(1, 1000)) / 1000
    wait_on_fail += randomness
    if n > 3:
        print_text('\nTemp error %s. Backing off %s seconds...'
                   % (reason, int(wait_on_fail)), stdscr)
    time.sleep(wait_on_fail)
    if n > 3:
        print_text('attempt %s/%s\n' % (n + 1, retries), stdscr)


def call_api(
        service,
        function,
        soft_errors=False,
        throw_reasons=None,
        retry_reasons=None,
        stdscr=None,
        **kwargs
):
    if retry_reasons is None:
        retry_reasons = []
    if throw_reasons is None:
        throw_reasons = []

    retries = 10
    parameters = kwargs.copy()
    parameters.update(extra_args)
    for n in range(1, retries + 1):
        try:
            if function:
                method = getattr(service, function)(**parameters)
            else:
                method = service

            return method.execute()
        except googleapiclient.errors.MediaUploadSizeError as e:
            print_text('ERROR: %s' % e, stdscr)
            if soft_errors:
                print_text(' - Giving up.', stdscr)
                return
            else:
                sys.exit()
        except (OSError,
                socket.timeout,
                socket.gaierror,
                ssl.SSLEOFError,
                httplib2.error.ServerNotFoundError) as e:
            _backoff(n, retries, e, stdscr)
            continue
        except googleapiclient.errors.HttpError as e:
            try:
                error = json.loads(e.content.decode('utf-8'))
                reason = error['error']['status']
                message = error['error']['message']
                http_status = error['error']['code']
            except (KeyError, json.decoder.JSONDecodeError):
                http_status = int(e.resp['status'])
                reason = http_status
                message = e.content
            if reason in throw_reasons:
                raise
            if n != retries and (http_status >= 500 or
                                 reason in ['rateLimitExceeded', 'userRateLimitExceeded', 'backendError'] or
                                 reason in retry_reasons):
                _backoff(n, retries, reason, stdscr)
                continue
            print_text('\n%s: %s - %s' % (http_status, message, reason), stdscr)
            if soft_errors:
                print_text(' - Giving up.', stdscr)
                return
            else:
                return
        except google.auth.exceptions.RefreshError as e:
            print_text('Error: Authentication Token Error - %s' % e, stdscr)
            sys.exit(403)


def call_api_pages(service, function, items='items',
                   next_page_token='nextPageToken', page_message=None, message_attribute=None, stdscr=None,
                   **kwargs):
    page_token = None
    all_pages = list()
    total_items = 0
    while True:
        this_page = call_api(service, function, pageToken=page_token, **kwargs)
        if not this_page:
            this_page = {items: []}
        try:
            page_items = len(this_page[items])
        except KeyError:
            page_items = 0
        total_items += page_items
        if page_message:
            show_message = page_message
            try:
                show_message = show_message.replace('%%num_items%%', str(page_items))
            except (IndexError, KeyError):
                show_message = show_message.replace('%%num_items%%', '0')
            try:
                show_message = show_message.replace('%%total_items%%',
                                                    str(total_items))
            except (IndexError, KeyError):
                show_message = show_message.replace('%%total_items%%', '0')
            if message_attribute:
                try:
                    show_message = show_message.replace('%%first_item%%',
                                                        str(this_page[items][0][message_attribute]))
                    show_message = show_message.replace('%%last_item%%',
                                                        str(this_page[items][-1][message_attribute]))
                except (IndexError, KeyError):
                    show_message = show_message.replace('%%first_item%%', '')
                    show_message.replace('%%last_item%%', '')
        try:
            all_pages += this_page[items]
            page_token = this_page[next_page_token]
            if page_token == '':
                return all_pages
        except (IndexError, KeyError):
            if page_message:
                print_text('\n', stdscr)
            return all_pages
