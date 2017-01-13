#!/usr/bin/env python
import sys, os

cue_sheet = open(sys.argv[1]).read().split('\n')
input_file, offset = cue_sheet[0].split()
segments = {}
n = int(offset)
for segment in cue_sheet[1:]:
    segment = segment.strip()
    # Skip blank lines
    if not segment: continue
    # Skip comments
    if segment.startswith('#'): continue
    segment_start, segment_end, segment_title = segment.split(' ', 2)
    os.system("ffmpeg -i {} -c copy -ss {} -to {} tmp.mov"
              .format(input_file, segment_start, segment_end))
    if segment_title not in segments:
        # New segment; easy case
        n += 1
        filename = "{:03} - {}.mov".format(n, segment_title)
        segments[segment_title] = filename
        os.rename("tmp.mov", filename)
    else:
        # Segment already exists; do fancy concat
        with open("tmp.txt", "w") as f:
            f.write("file '{}'\n".format(segments[segment_title]))
            f.write("file 'tmp.mov'\n")
        os.system("ffmpeg -f concat -i tmp.txt -c copy tmp2.mov")
        os.unlink("tmp.mov")
        os.unlink(segments[segment_title])
        os.rename("tmp2.mov", segments[segment_title])

