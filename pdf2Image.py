#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import pdf2image
from PIL import Image
import argparse

def open_eps(path, size_px):
        
    pic = Image.open(path)
    pic.load(scale=5)
    
    # Ensure scaling can anti-alias by converting 1-bit or paletted images
    if pic.mode in ('P', '1'):
        pic = pic.convert("RGB")
    
    # Calculate the new size, preserving the aspect ratio
    ratio = size_px / pic.size[0]
    new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
    
    # Resize to fit the target size
    pic = pic.resize(new_size, Image.Resampling.LANCZOS)
    
    return pic

def main(args=None):
    parser = argparse.ArgumentParser(
        description="Convert images from PDF to arbitrary format chosen between {jpeg, tiff, png}."
    )
    parser.add_argument(
        "input_path", type=Path, help="Input PDF file path.", metavar="INPUT_PATH"
    )
    parser.add_argument(
        "output_path", type=Path, help="Output file path.", metavar="OUTPUT_PATH"
    )
    parser.add_argument(
        "-s", "--size", type=float, help="Output image size in mm", metavar="SIZE", default=180,
    )
    parser.add_argument(
        "--dpi", type=int, help="Output image dpi", metavar="DPI", default=300,
    )
    
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)
    accepted_formats = [".jpeg", ".tiff", ".png"]
    if args.output_path.suffix not in accepted_formats:
        raise NameError(f'Output format provided ({args.output_path.suffix}) not within accepted formats')
    if args.input_path.suffix != '.pdf' and args.input_path.suffix != '.eps':
        raise NameError(f'Input format provided ({args.input_path.suffix}) not .pdf or .eps')
    
    size_mm = args.size
    size_px = 0.0393701 * size_mm * args.dpi
    
    if args.input_path.suffix == '.pdf':
        images = pdf2image.convert_from_path(
            args.input_path, #dpi=300,
            output_folder=None, first_page=None,
            last_page=None, fmt='ppm', jpegopt=None,
            strict=False, transparent=False, single_file=False,
            grayscale=False, size=(size_px,None),
        )
    else:
        images = [open_eps(args.input_path, size_px)]

    images[0].save(args.output_path)


if __name__ == "__main__":
    main()
