import pdf2Image
from pathlib import Path
import shlex

inputDir = Path('/Users/scarpma/Downloads/SSM_paper_for_frontiers_(submission)/')
ifiles = list(inputDir.glob('*.pdf'))
ifiles += list(inputDir.glob('*.eps'))

for i in range(len(ifiles)):
    print(f'{i:4d} | {ifiles[i]}')

substrings = [
    'registrations_deformetrica_vs_ours',
    'SSM_metrics',
    'SSM_visualization',
    'loss_function',
]
outputDir = Path('images/')
outputDir.mkdir(exist_ok=False)
for i in range(len(ifiles)):
    output_file = outputDir / (ifiles[i].stem + '.jpeg')
    big_fig = any(substring in str(ifiles[i]) for substring in substrings)
    size = 180 if big_fig else 85
    arg = f'{ifiles[i]} {output_file} --size {size} --dpi 450'
    print(shlex.split(arg))
    pdf2Image.main(shlex.split(arg))


