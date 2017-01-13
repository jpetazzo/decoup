# Decoup

Decoup is a script to cut a long video into multiple chapters.

It is very simple (and honestly doesn't really deserve its own
GitHub repository!) but I personally find this workflow super
convenient, and wanted to share it, so that others could use
it if they found it useful.


## Use case

I often record my workshops and tutorials using screen capture.
The result is one (or multiple) really long video files (a few
hours each).

I want to share these workshops with a small community, but
sharing a 2 hours video is not very useful; I want to:

- add a nice table of contents so that people can know what's
  in the whole thing, and jump to any chapter or section
  easily;
- remove useless sections (e.g. coffee breaks, questions
  specific to the venue where the video was recorded, etc);
- sometimes rearrange some sections in a different order.

But I don't want to spend hours with a video editing software
to do all that.


## Pre-requirements

You need Python, ffmpeg, and I also recommend MPlayer and VLC.
They are all installable with APT, brew, or whatever is your
favorite package manager.

I recommend that you add the following line to `~/.mplayer/input.conf`
(create the file if it doesn't already exist):

```
BS seek -1
```

This creates a keyboard shortcut to seek back 1 second when you
press backspace in MPlayer. This will be useful later.


## Workflow

1. Record your video (e.g. with QuickTime screen capture, or
   any similar tool). Let's say it's `capture-1.mov`.
2. Using MPlayer, write down "start" and "end" times of each
   chapter of your video. (More on this later.)
3. Create a "cue file" listing each chapter with its start
   and end time (More on this later.)
   Let's say that this file is `capture-1.txt`.
4. Run `python decoup.py capture-1.txt`. The script will
   use ffmpeg to slice and dice the video accordingly, and
   create a bunch of numbered files corresponding to
   each chapter. (The original file is left untouched.)
5. Do whatever you want with the numbered files. For instance,
   I upload them as a YouTube playlist; it's very easy
   (and the numbering makes it easy to keep ordering).


## Cue file format

The cue file is a simple text file. On the first line,
there should be the name of the video file, and an index.
The index will be a relative offset for all the chapters
in the cue file.

Then each line describes a chapter. A chapter has a start
time, end time, and title; all separated by spaces. The
times are in seconds, and can be decimal. The chapter title
can contain spaces.

For each chapter, a separate file will be created, named
`NNN XXX XXX XXX.mov` where `NNN` is the chapter number
(starting at the relative offset + 1) and `XXX XXX XXX`
is the title specified in the cue sheet.

If multiple chapters have the same title, then the corresponding
segments will automatically be concatanated in the output files.

Short example:

```
capture-1.mov 0
4.2 55.2 introduction
58.9 164.3 part one
166.3 320.5 part two
325.5 399.1 part two
398.5 450.4 thanks
```

This will create files named:

```
001 introduction.mov
002 part one.mov
003 part two.mov
004 thanks.mov
```

"Part two" will be the concatenation of two video segments.

The concatenation is made using ffmpeg's [concat demuxer](
https://trac.ffmpeg.org/wiki/Concatenate), which I found perfect
when working on screen captures made with QuickTime, but your
mileage may vary.

See also `lisa-1.txt` and `lisa-1.out` for a more complex
example.


## Using MPlayer to write down start/end times

This is very easy to do, with the following technique.

1. Make sure that you have setup `input.conf` as described
   above. This will let you go back by 1 second when viewing
   videos with MPlayer.
2. Open a text editor for the "cue file."
3. On the same screen, open a terminal window, and use the
   terminal to play the video with MPlayer
   (i.e. `mplayer capture.mov`).
4. Make sure to have on screen, side by side, the text editor,
   the video, and the terminal where you started MPlayer.

At this point, you can seek around the video using MPlayer's
keyboard shortcuts:

- left and right arrows seek by 10 seconds
- up and down arrows seek by 1 minute
- backspace seeks back 1 second (I find this super useful!)
- space will pause the playback

In the terminal window, you will see the seek position; e.g.:
```
A:5770.8 V:5770.8 A-V:  0.000 ct:  0.000   0/   0  4%  5%  1.2% 0 0
```
The "A" and "V" numbers are the position within the audio
and video streams, in seconds. They should be equal (or really
close) unless your video capture file is damaged. This
number is exactly what you want to put in your cue sheet.

So I play the video, seek forward in increments of 10 seconds,
locate my cut point; then I find the exact position of the cut
point, pause the video at the cut point, unpause it; and if
I'm satisfied by this exact cut point, I write down the
position in the cue sheet file. (When you hit pause/play,
MPlayer will add a line break, so the exact position of the
cue point will be shown in the terminal.)


## Quality control

After running `decoup.py`, I suggest to load all the videos in VLC
and check the first and last seconds of each segment. I found the
VLC interface to be particularly efficient for that specific task,
since I can let the first few seconds of the video play out, then
click to the right end of the seek bar, see the last instants of
the video, and let VLC automatically load the next one, and repeat.


## Last words

Before using this technique, cutting a long video in chapters
took me ~2 days, and I was only half-satisfied with the accuracy
of the cut points (I was using the "trim" feature of QuickTime).
With this technique, I was able to process a longer video
in half a day, and was happier with the result. So yay.

