def time_to_seconds(timestr):
    if not timestr or not isinstance(timestr, str):
        return 0  # 如果传入 None 或非字符串，返回 0 或抛出异常

    timestr = timestr.strip()  # 去除两端空格

    if ':' not in timestr:
        # 如果没有冒号，假设已经是秒数
        return float(timestr)

    parts = timestr.split(':')
    if len(parts) == 2:
        # 格式为 "分:秒"
        minutes = int(parts[0])
        seconds = int(parts[1])
        return minutes * 60 + seconds
    elif len(parts) == 3:
        # 格式为 "时:分:秒"
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return hours * 3600 + minutes * 60 + seconds

    return 0  # 如果格式不正确，返回 0 或抛出异常