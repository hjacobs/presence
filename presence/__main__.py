
import datetime
import glob
import gzip

MONTHS = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12
}

def main():
    entries = []
    for fn in glob.glob('/var/log/syslog*'):
        openfun = open
        if fn.endswith('.gz'):
            openfun = gzip.open
        last_uptime = 0
        with openfun(fn, mode='rt', encoding='utf-8') as fd:
            for line in fd:
                if line.startswith('\x00'):
                    continue
                parts = line.split()
                mon = MONTHS[parts[0].lower()]
                now = datetime.datetime.now()
                hour, minute, second = parts[2].split(':')
                dt = datetime.datetime(year=now.year, month=mon, day=int(parts[1]), hour=int(hour), minute=int(minute), second=int(second))
                if 'kernel:' in line:
                    last_uptime = float(' '.join(parts[5:(7 if parts[5] == '[' else 6)]).strip(' []'))
                    entries.append((dt, last_uptime))
                else:
                    entries.append((dt, last_uptime))


    last_uptime = 0
    last_ts = None
    last_start = None
    for ts, uptime in sorted(entries):
        if uptime < last_uptime:
            print(last_start, '--', last_ts, uptime, last_uptime, ts)
            last_start = ts
        last_uptime = uptime
        last_ts = ts


if __name__ == '__main__':
    main()
