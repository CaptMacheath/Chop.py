import csv
import sys
from bisect import bisect_left

# Source: https://stackoverflow.com/a/12141511
def pick_closest(target, options):
    options.sort()
    pos = bisect_left(options, target)
    if pos == 0:
        return options[0]
    if pos == len(options):
        return options[-1]
    before = options[pos - 1]
    after = options[pos]
    if after - target < target - before:
        return after
    else:
        return before

# Initialize variables from command line arguments
if len(sys.argv) < 2:
    print('No input file provided, exiting')
    quit
file_path = sys.argv[1]
if len(sys.argv) < 3:
    num_buckets = 10
else:
    num_buckets = int(sys.argv[2])

# Read model from file and make initial calculations about its size
model = []
model_size = 0
with open(file_path, 'r') as f:
    reader = csv.reader(f)
    for _, line in enumerate(reader):
        model.append([line[0], int(line[1])])
        model_size += int(line[1])
bucket_size = model_size / num_buckets

# Main algorithm: load the model's entries into the appropriate "buckets"
chopped_model = []
ideal_size_read = 0     # A value representing the ideal size read into 'chopped_model' for each bucket
actual_size_read = 0    # Total number of units loaded into the 'chopped_model' so far
next = 0
for b in range(0, num_buckets):
    ideal_size_read = ideal_size_read + bucket_size
    bucket = []
    for e in range(next, len(model)):
        possible_size_read = actual_size_read + model[e][1]
        # If the bucket will not overflow with this next entry...
        if possible_size_read <= ideal_size_read:
            bucket.append(model[e])
            actual_size_read = possible_size_read
            next += 1
        # Else if it WILL overflow with this next entry but stay close enough to the ideal size...
        elif pick_closest(ideal_size_read, [actual_size_read, possible_size_read]) == possible_size_read:
            bucket.append(model[e])
            actual_size_read = possible_size_read
            next += 1
        # Otherwise...
        else:
            break
    chopped_model.append(bucket)

# Display results
percentage_displayed = 0
for b in range(0, len(chopped_model)):
    percentage_displayed += 100 / num_buckets
    print('{0}% of model:'.format(percentage_displayed))
    for name, num_units in chopped_model[b]:
        print('{0} [{1} units]'.format(name, num_units))
    print()
