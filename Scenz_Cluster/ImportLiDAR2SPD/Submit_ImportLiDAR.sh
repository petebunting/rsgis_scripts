#!/bin/bash

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080228_RAW2 -l h_vmem=4G ImportLidar2SPD.sh LI080228_RAW2.las LI080228_RAW2_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080228_RAW3 -l h_vmem=4G ImportLidar2SPD.sh LI080228_RAW3.las LI080228_RAW3_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080228_RAW4 -l h_vmem=4G ImportLidar2SPD.sh LI080228_RAW4.las LI080228_RAW4_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080228_RAW5 -l h_vmem=4G ImportLidar2SPD.sh LI080228_RAW5.las LI080228_RAW5_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080228_RAW6 -l h_vmem=4G ImportLidar2SPD.sh LI080228_RAW6.las LI080228_RAW6_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080228_RAW7 -l h_vmem=8G ImportLidar2SPD.sh LI080228_RAW7.las LI080228_RAW7_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080228_RAW8 -l h_vmem=4G ImportLidar2SPD.sh LI080228_RAW8.las LI080228_RAW8_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080304_RAW1 -l h_vmem=4G ImportLidar2SPD.sh LI080304_RAW1.las LI080304_RAW1_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080304_RAW2 -l h_vmem=4G ImportLidar2SPD.sh LI080304_RAW2.las LI080304_RAW2_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080304_RAW3 -l h_vmem=4G ImportLidar2SPD.sh LI080304_RAW3.las LI080304_RAW3_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080304_RAW4 -l h_vmem=4G ImportLidar2SPD.sh LI080304_RAW4.las LI080304_RAW4_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080324_RAW1 -l h_vmem=4G ImportLidar2SPD.sh LI080324_RAW1.las LI080324_RAW1_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080324_RAW12 -l h_vmem=4G ImportLidar2SPD.sh LI080324_RAW12.las LI080324_RAW12_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080610_RAW1 -l h_vmem=4G ImportLidar2SPD.sh LI080610_RAW1.las LI080610_RAW1_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080228_RAW10 -l h_vmem=4G ImportLidar2SPD.sh LI080228_RAW10.las LI080228_RAW10_5m.spd

qsub -cwd -V -S /bin/bash -N Grid_sge_LI080228_RAW7_nonidx -l h_vmem=2G ImportLidar2SPDnoIdx.sh LI080228_RAW7.las LI080228_RAW7_noidx.spd
