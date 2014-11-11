
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
    for fn in glob.glob('/var/log/syslog*'):
        openfun = open
        if fn.endswith('.gz'):
            openfun = gzip.open
        with openfun(fn, mode='rt', encoding='utf-8') as fd:
            for line in fd:
                if 'kernel:' in line:
                    parts = line.split()
                    mon = MONTHS[parts[0].lower()]
                    now = datetime.datetime.now()
                    hour, minute, second = parts[2].split(':')
                    dt = datetime.datetime(year=now.year, month=mon, day=int(parts[1]), hour=int(hour), minute=int(minute), second=int(second))
                    print(dt, parts[6])


if __name__ == '__main__':
    main()
