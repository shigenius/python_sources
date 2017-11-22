#!/bin/sh
ls -lTU |sed -E 's/\ +/\ /g'  | cut -d ' ' -f6-10 | grep -E '\.mov|\.MOV' |sed -E 's/:/ /g' | awk '{print $6, $1, $2, $3, $4, $5, $7}' | gawk '{dst=mktime(sprintf("%s %s %s %s %s %s",$1,$2,$3,$4,$5,$6));command=sprintf("mv %s %s.mov",$7,dst);system(command)}'

