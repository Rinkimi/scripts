@echo off
set /p au=Enter ip 
plink.exe -L 5938:%au%:5938 -ssh svp-stream-ssk-01.svp.prod -i ssk.ppk -l ssk_operator
