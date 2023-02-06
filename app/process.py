from .ppe_detector.pkd_checkin import pkd_checkin
import os.path

# return if ppe is detected
def process(location, id, dir):
    print("processing image at " + location)
    pkd_checkin(id, 0.6, location, dir)
    return verify_checkin() == "SUCCESS"

def verify_checkin(loc = '.tmp/checkin_records.txt'):
    with open(loc, 'r') as f:
        data = f.readlines()[-1].split(';')[-1]
    return data[:-1]

