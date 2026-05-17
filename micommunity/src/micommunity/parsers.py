def check_code_response(code, default_msg):
    error_map = {
        100001: "参数错误",
        100002: "csrf token 验证失败",
        100003: "操作失败",
        100004: "登录",
        100005: "命中关键词（话题）",
        100008: "错误码 100008",
        100009: "You have been banned from posting contents",
        100010: "没有编辑权限",
        100011: "用户名已经被占用",
        100012: "用户已经修改过用户名",
        100013: "没有新增权限",
        700001: "delete account wait",
        700002: "delete data done",
        700003: "delete account done",
        1010020006: "私信用户被拉黑"
    }
    return error_map.get(code, default_msg)



def info(response):
    response_json = response.json()
    code = response_json.get('code')
    if code != 0:
        return {"code": -1, "message": check_code_response(code, response_json.get('msg'))}

    data = response_json.get("data")
    return data


def state(response):
    response_json = response.json()
    code = response_json.get('code')
    if code != 0:
        return {"code": -1, "message": check_code_response(code, response_json.get('msg'))}

    data = response_json.get("data")
    is_pass = data.get("is_pass")
    button_state = data.get("button_state")
    deadline_format = data.get("deadline_format", "")

    if is_pass == 1:
        message = f"You have been granted access to unlock until Beijing time {deadline_format} (mm/dd/yyyy)"
        return {"code": 1, "message": message, "response_json": response_json}
    else:
        if button_state == 1:
            message = "Apply for unlocking"
            return {"code": 2, "message": message, "response_json": response_json}
        elif button_state == 2:
            message = f"Account Error Please try again after {deadline_format} (mm/dd)"
            return {"code": 3, "message": message, "response_json": response_json}
        else:
            message = "Account must be registered over 30 days"
            return {"code": 4, "message": message, "response_json": response_json}


def apply(response):
    response_json = response.json()
    code = response_json.get('code')
    if code != 0:
        return {"code": -1, "message": check_code_response(code, response_json.get('msg'))}

    data = response_json.get("data")
    apply_result = data.get("apply_result")
    deadline_format = data.get("deadline_format", "")

    if apply_result == 1:
        message = "Application Successful"
        return {"code": 1, "message": message}
    elif apply_result in (2, 4):
        message = f"Account Error Please try again after {deadline_format} (mm/dd)"
        return {"code": 2, "message": message}
    elif apply_result == 3:
        if deadline_format:
            parts = deadline_format.split(' ', 1)
            d_date = parts[0]
            d_time = parts[1] if len(parts) > 1 else "00:00"
        else:
            d_date, d_time = "", "00:00"
        message = f"Application quota limit reached,please try again after {d_date} (mm/dd) {d_time} (GMT+8)"
        return {"code": 3, "message": message}
    elif apply_result == 5:
        message = "Sorry, application failed Please try again later"
        return {"code": 4, "message": message}
    elif apply_result == 6:
        message = "Please try again in a minute"
        return {"code": 5, "message": message}
    elif apply_result == 7:
        message = "Please try again later"
        return {"code": 6, "message": message}