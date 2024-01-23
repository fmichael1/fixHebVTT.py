import argparse
import re

class VTTLine:
    def __init__(self, timing, text):
        self.timing = timing
        self.text = text

class VTTDecodeError(Exception): pass

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    return parser.parse_args(args)

def get_file_lines(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except UnicodeDecodeError as e:
        raise VTTDecodeError("File decoding failed.") from e

class VTTParser:
    def __init__(self):
        self.lines = []

    def parse_lines(self, lines):
        current_timing = ""
        current_text = []

        for line in lines:
            if line.startswith("WEBVTT"):
                continue
            if "-->" in line:
                if current_text:
                    self.lines.append(VTTLine(current_timing, current_text))
                    current_text = []
                current_timing = line
            else:
                current_text.append(line)

        if current_text:
            self.lines.append(VTTLine(current_timing, current_text))

        return self.lines

class VTTWriter:
    def __init__(self, file):
        self.file = open(file, "w", encoding="utf-8")

    def write_lines(self, lines):
        self.file.write("WEBVTT\n\n")
        for line in lines:
            self.file.write(line.timing + "\n")
            self.file.write("\n".join(line.text) + "\n\n")

    def close(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

def fix_line(line):
    special_chars = r'.,:;\'()\-?!+=*&$^%#@~`"'
    prefix_match = re.search(f"^([{special_chars}]*)", line)
    suffix_match = re.search(f"[^{special_chars}]([{special_chars}]*)$", line)
    prefix = prefix_match.group(1) if prefix_match else ""
    suffix = suffix_match.group(1) if suffix_match else ""

    # Reverse the placement of special characters
    return suffix + line[len(prefix):len(line)-len(suffix)] + prefix

def fix_subtitles(subtitles):
    new_subtitles = []
    for subtitle_line in subtitles:
        new_text = [fix_line(text_line) for text_line in subtitle_line.text]
        new_subtitles.append(VTTLine(subtitle_line.timing, new_text))
    return new_subtitles

def main(args):
    lines = get_file_lines(args.file)
    vtt_parser = VTTParser()
    subtitles = vtt_parser.parse_lines(lines)

    modified_subtitles = fix_subtitles(subtitles)
    with VTTWriter(args.file[:-4] + ".fixed.vtt") as vtt_writer:
        vtt_writer.write_lines(modified_subtitles)

if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    main(args)
