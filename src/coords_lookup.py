import csv

# Simple lookup table for known launch sites and coordinates
LAUNCH_SITE_COORDS = {
    'CCAFS LC-40': (28.5618571, -80.577366),
    'CCAFS SLC-40': (28.5618571, -80.577366),
    'KSC LC-39A': (28.608058, -80.603956),
    'VAFB SLC-4E': (34.632093, -120.610829),
    'Kwajalein Atoll': (8.720, 167.733),
}


def lookup(site_name):
    return LAUNCH_SITE_COORDS.get(site_name)


if __name__ == '__main__':
    print('Available sites:', list(LAUNCH_SITE_COORDS.keys()))
