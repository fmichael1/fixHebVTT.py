# fixHebVTT.py: Hebrew Subtitles RTL Fixer

`fixHebVTT.py` is a Python utility designed to address Right-to-Left (RTL) text direction issues in Hebrew subtitles within WebVTT (.vtt) files. This script automates the correction of common RTL formatting problems, ensuring proper display and readability of Hebrew subtitles.

## Features

- **RTL Adjustment**: Automatically adjusts the RTL text direction for Hebrew subtitles, resolving display issues.  
- **WebVTT Compatibility**: Works exclusively with .vtt subtitle files, commonly used in online streaming platforms.

## Dependencies

- Python 3.x: The script is written in Python and requires Python 3.x to run.

## Installation

No additional installation is required, other than having Python 3.x installed on your system.

## Usage

To use `fixHebVTT.py`, simply run it from the command line with the path to the .vtt file as an argument. The script will process the file and create a new .vtt file with corrected Hebrew subtitles.

```bash
python fixHebVTT.py path_to_your_subtitle_file.vtt
```

The output will be a new file with the same name as the original, appended with `.fixed`, containing the corrected subtitles.

