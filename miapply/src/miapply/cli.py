#!/usr/bin/python

import time, threading, ntplib, pytz, requests

from datetime import datetime, timedelta, timezone

from micommunity import get_headers, STATE_URL, state, APPLY_URL, apply

def retry(fn):
    while True:
        try:
            return fn()
        except Exception:
            pass

get_headers()

while True:
    try:
        ms = int(input("\nEnter delay in ms before 00:00 (GMT+8)\n(e.g. 500 = 0.5s, 1000 = 1s, 3000 = 3s): "))
        break
    except ValueError:
        pass
delay = ms / 1000.0
print(f"\n[Delay]  {delay} s\n")

while True:

    session = requests.Session()
    headers = retry(lambda: get_headers(silent=True))

    status = retry(lambda: state(session.get(STATE_URL, headers=headers, timeout=15)))
    print(status.get('message'))
    if status.get('code') == 1:
        exit()

    ntp_resp = retry(lambda: ntplib.NTPClient().request("ntp1.aliyun.com", version=3))
    beijing_tz = pytz.timezone("Asia/Shanghai")
    beijing_time = datetime.fromtimestamp(ntp_resp.tx_time, timezone.utc).astimezone(beijing_tz)
    mono_ref = time.monotonic()

    target = (beijing_time + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    ) - timedelta(seconds=delay)

    print(f"\n\n[Target]: {target.strftime('%H:%M:%S.%f')} (GMT+8)")

    warmed = False
    while True:
        now  = beijing_time + timedelta(seconds=time.monotonic() - mono_ref)
        diff = (target - now).total_seconds()
        if diff <= 0:
            break
        if not warmed and diff <= 10:
            threading.Thread(
                target=lambda: session.get(STATE_URL, headers=headers, timeout=15),
                daemon=True
            ).start()
            warmed = True
        if diff > 5:
            time.sleep(min(diff - 5, 30))
        elif diff > 1:
            time.sleep(0.05)
        else:
            time.sleep(0.0001)

    send_time = beijing_time + timedelta(seconds=time.monotonic() - mono_ref)

    print(f"[Target Sent At]: {send_time.strftime('%H:%M:%S.%f')} (GMT+8)")

    response = retry(lambda: session.post(APPLY_URL, headers=headers, json={"is_retry": True}, timeout=15))

    server_ts = response.json().get('ts', 0)
    if server_ts:
        server_time = datetime.fromtimestamp(server_ts, timezone.utc).astimezone(beijing_tz)
        print(f"[Server response At]: {server_time.strftime('%H:%M:%S')} (GMT+8)\n\n")

    print(apply(response).get('message'))