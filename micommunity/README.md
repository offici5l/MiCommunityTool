<div align="center">

---

[![Version](https://img.shields.io/pypi/v/micommunity?label=Version&labelColor=black&color=brightgreen)](https://pypi.org/project/micommunity/)
[![Changelog](https://img.shields.io/badge/Changelog-blue?style=flat&logoColor=white)](CHANGELOG.md)

---

</div>


## Library

### Install

```
pip install micommunity
```

### get_headers

Handles login and returns the headers required for all requests.

```python
from micommunity import get_headers

headers = get_headers()
```

To skip the "already logged in" prompt:

```python
headers = get_headers(silent=True)
```

### info

```python
import requests
from micommunity import INFO_URL, info

response = requests.get(INFO_URL, headers=headers)
result = info(response)
```

### state

```python
import requests
from micommunity import STATE_URL, state

response = requests.get(STATE_URL, headers=headers)
result = state(response)
```

### apply

```python
import requests
from micommunity import APPLY_URL, apply

response = requests.post(APPLY_URL, json={"is_retry": True}, headers=headers)
result = apply(response)
```

---

### result return {"code": *, "message": *}


# state 

| result['code'] | result['message'] |
|---|---|
| -1 | API Error |
| 1 | You have been granted access to unlock until Beijing time {deadline_format} (mm/dd/yyyy) |
| 2 | Apply for unlocking |
| 3 | Account Error Please try again after {deadline_format} (mm/dd) |
| 4 | Account must be registered over 30 days |

---

# apply 

| result['code'] | result['message'] |
|---|---|
| -1 | API Error |
| 1 | Application Successful |
| 2 | Account Error Please try again after {deadline_format} (mm/dd) |
| 3 | Application quota limit reached,please try again after {d_date} (mm/dd) {d_time} (GMT+8) |
| 4 | Sorry, application failed Please try again later |
| 5 | Please try again in a minute |
| 6 | Please try again later |

---

# info 

| result['code'] | result['message'] |
|---|---|
| -1 | API Error |
| 0 | Success (returns data directly) |


