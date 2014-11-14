
import datetime
import glob
import utmp

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
    for fn in glob.glob('/var/log/wtmp*'):
        with open(fn, 'rb') as fd:
            for entry in utmp.read(fd.read()):
                if entry.user in ['reboot', 'shutdown']:
                    entries.append(entry)

    entries.sort(key=lambda x: x.time)

    last_reboot = None
    for entry in entries:
        if entry.user == 'shutdown' and last_reboot:
            print(last_reboot, entry.time - last_reboot)
            last_reboot = None
        elif entry.user == 'reboot':
            last_reboot = entry.time

    if last_reboot:
        now = datetime.datetime.now()
        print(last_reboot, now - last_reboot)

if __name__ == '__main__':
    main()
