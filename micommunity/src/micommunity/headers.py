import re, json
from migate import get_passtoken, get_service
from urllib.request import urlopen

VERSION_NAME = None
VERSION_CODE = None

def get_version():
    try:
        url = "https://play.google.com/store/apps/details?id=com.mi.global.bbs&hl=en&gl=us"
        dom = urlopen(url).read().decode("UTF-8")

        for match in re.finditer(r"AF_initDataCallback[\s\S]*?</script", dom):
            if re.search(r"(ds:5)'", match.group()):
                value_match = re.search(r"data:([\s\S]*?), sideChannel: {}}\);<\/", match.group())
                if value_match:
                    v_name = json.loads(value_match.group(1))[1][2][140][0][0][0]
                    major, minor, patch = v_name.split(".")
                    v_code = int(major) * 100000 + int(minor) * 100 + int(patch)
                    return v_name, v_code
    except:
        pass

    return "5.4.11", 500411


def get_headers(silent=False):
    sid = '18n_bbs_global'
    params = {"sid": sid}
    
    if silent:
        passToken = get_passtoken(params, silent=True)
    else:
        passToken = get_passtoken(params)

    service = get_service(passToken, params)
    token = service['cookies']['new_bbs_serviceToken']
    device_id = service['servicedata']['deviceId']

    global VERSION_NAME, VERSION_CODE
    
    if VERSION_NAME is None or VERSION_CODE is None:
        print("\nFetching latest version...")
        VERSION_NAME, VERSION_CODE = get_version()
        print(f"\nversion: '{VERSION_NAME}'")

    headers = {
        'User-Agent': "okhttp/4.12.0",
        'Accept': "application/json",
        'Accept-Encoding': "gzip",
        'content-type': "application/json; charset=utf-8",
        'Cookie': f"new_bbs_serviceToken={token};versionCode={VERSION_CODE};versionName={VERSION_NAME};deviceId={device_id};"
    }

    return headers