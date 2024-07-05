# sbpicture
a zlib compressed image format in python made for fun

### What does SBP/sbpicture stand for?
It stands for Stacking Books Picture. A picture format made by me.

### How does it work?
It is a string, where each line, is a column (Y) of RGBA hex colors. It is then compressed with ZLIB and with a SBP added in the front of the file (magic number).

### Should I use it?
No, It was made entirely for fun.

### How do I use it?

```sbp.py -to <png,jpg,tiff,...>```
Convert an image to a format that can be read by the Pillow library

```sbp.py -view myimage.sbp```
View a SBP file

```sbp.py -from myimage.sbp <png,tiff,webp>```
Convert a SBP file to a file format.
