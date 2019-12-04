#!/usr/bin/python3
import sys

def genre_count():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    f1 = open(input_file, 'r')
    f2 = open(output_file, 'w')
    res_dict = dict()

    for lines in f1:
        genres = lines.split('::')[2].rstrip().split('|')
        for genre in genres:
            if genre not in res_dict:
                res_dict[genre] = 1
            else:
                res_dict[genre] += 1

    for k,v in res_dict.items():
        line = str(k) + ' ' + str(v) + '\n'
        f2.write(line)
    f1.close()
    f2.close()

if __name__ == '__main__':
    genre_count()
