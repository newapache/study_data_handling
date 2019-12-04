#!/usr/bin/python3
import sys
import calendar
dayofweek = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

def vehicle_cnt():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    f1 = open(input_file, 'r')
    f2 = open(output_file, 'w')
    res_dict = dict()

    for lines in f1:
        tmp = lines.rstrip().split(',')
        day = calendar.weekday(int(tmp[1].split('/')[2]), int(tmp[1].split('/')[0]), int(tmp[1].split('/')[1]))
        key = tmp[0] + ',' + dayofweek[day]
        if key not in res_dict:
            val = tmp[2] + ',' + tmp[3]
            res_dict[key] = val
        else :
            val = str(int(res_dict[key].split(',')[0]) + int(tmp[2])) + ',' + str(int(res_dict[key].split(',')[1]) + int(tmp[3]))
            res_dict[key] = val

    for k,v in res_dict.items():
        line = str(k) + ' ' + str(v) + '\n'
        f2.write(line)
    f1.close()
    f2.close()

if __name__ == '__main__':
    vehicle_cnt()
