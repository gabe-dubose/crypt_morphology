#!/usr/bin/env python3

import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

def sliding_window_average(x, n, log, id):
    #initialize list to store binned averages
    mean_x = []

    #calculate window size
    window_size = len(x) // n
    #calculate overhang for adjustment
    overhang = len(x) % n

    window_message = f"Optimal window size: {window_size}"
    overhang_message = f"Calcualted overhang: {overhang}"

    #initialize list to store window sizes
    window_sizes = []

    start = 0
    for i in range(n):
        if i < overhang:
            window = x[start:start + window_size + 1]
            start += window_size + 1
            window_sizes.append(len(window))
        else:
            window = x[start:start + window_size]
            start += window_size
            window_sizes.append(len(window))
        
        window_average = sum(window) / len(window) if len(window) > 0 else 0
        mean_x.append(window_average)

    window_sizes_message = f"Window size distirbution: {window_sizes}"

    #write summary to log
    with open(log, 'a') as outfile:
        outfile.write(f'Summary for sample: {id}\n')
        outfile.write(f'{window_message}\n')
        outfile.write(f'{overhang_message}\n')
        outfile.write(f'{window_sizes_message}\n')
        outfile.write('\n')

    return mean_x

#A function to load the data
def load_data(dir):
    #initialize dictionary for data
    data = {}

    #load files
    files = os.listdir(dir)

    #read data
    for file in files:
        filepath = f"{dir}/{file}"
        with open(filepath, 'r', encoding='utf-8-sig') as infile:
            lines = infile.readlines()[1:]
        
        #count number of columns
        colcounter = Counter(lines[0])
        colcount = colcounter[','] + 1
        
        #add entry for file to data
        sample_id = file.strip('.csv')
        data[sample_id] = []
        #add data to data dictionary
        for i in range(colcount):
            #add entry for row in data dictionary
            data[sample_id].append([])
            #for each line in the file, extract value in ith row
            for line in lines:
                value = line.split(',')[i]
                value = value.strip()
                if value != '' and value != 'N/A':
                    value = float(value)
                    data[sample_id][i].append(value)

    return data

#A function to normalize values in a list to be between 0 and 1
def zero_one_normalize(x):
    normalixed_x = []
    for value in x:
        norm = (value-min(x))/(max(x)-min(x))
        normalixed_x.append(norm) 
    return normalixed_x

#A function to process the data
def process_data(data, n_bins, log, outfile):
    #clean duplicate files
    #delete log if present
    try:
        os.remove(log)
        print(f'Warning: Log file detected. Overwriting {log}')
    except:
        pass

    #delete outfile if present, otherwise, initialize it
    try:
        os.remove(outfile)
        print(f'Warning: Output file detected. Overwriting {outfile}')
    except:
        pass

    #initialize outfile
    with open(outfile, 'a') as out:
        header_line = "sample_id," + ",".join([f"idx{i}" for i in range(1, n_bins+1)])
        out.write(f'{header_line}\n')

    #iterate through each sample
    for sample in data:
        #interate through each replicate within a sample
        for values in data[sample]:
            #define sample_id
            sample_id = f"{sample}_{data[sample].index(values)}"
            #remove negative values
            values = [value for value in values if value > 0]
            #perform moving average smoothing
            smoothed_values = sliding_window_average(values, n_bins, log, sample_id)
            #normalize values between zero and 1
            normalized_values = zero_one_normalize(smoothed_values)
            #convert values to strings for quicker joining
            str_values = [str(value) for value in normalized_values]
            #write data to outfile
            values_line = f"{sample_id},{','.join(str_values)}\n"
            with open(outfile, 'a') as out:
                out.write(values_line)


#
data = load_data('/home/gabe/Desktop/caballaronia_col/raw_data/day3/medial')
processing_log = '/home/gabe/Desktop/caballaronia_col/docs/day3_medial_processing.log'
data_outfile = '/home/gabe/Desktop/caballaronia_col/processed_data/day3_medial_processed_data.csv'
process_data(data=data, n_bins=25, log=processing_log, outfile=data_outfile)