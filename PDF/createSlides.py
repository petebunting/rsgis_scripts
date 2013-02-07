# A python script to create a tex file for a directory of PDFs with the name as the title
# from which a pdf can be created
# Dan Clewley
# 06/02/2012

import os, sys, glob

if len(sys.argv) < 3:
    print '''Not enough parameterd provided.
Usage:
    python createSlides.py inDIR outTexFile
''' 
    exit()


inDIR = sys.argv[1]
outTexFile = sys.argv[2]

outTex = open(outTexFile, 'w')

fileList = glob.glob(inDIR + '/*pdf')

header = '''\\documentclass[landscape]{slides}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{graphicx}
\\usepackage[top=1cm, bottom=1cm, left=1cm, right=1cm]{geometry}

\\usepackage{rotating} 
\\pagestyle{empty}
\\begin{document}
'''

outTex.write(header)

for file in fileList:
    baseFileName = os.path.split(file)[1].replace('.pdf','')
    baseFileName = baseFileName.replace('_','\_')
    
    slideText = ''' \\begin{slide}
    \\begin{center}
    %s\\\\
    \\includegraphics[width=\\linewidth]{%s}
    \\end{center}
    \\end{slide}
    '''%(baseFileName, file)
    
    outTex.write(slideText)

footer = '\\end{document}\n'
outTex.write(footer)

endMsg = 'Done. Create PDF using:\n\tpdflatex ' + outTex
print(endMsg)