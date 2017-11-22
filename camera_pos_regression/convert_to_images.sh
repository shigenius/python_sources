#!/bin/sh
#dependence : ffmpeg

flame=2 #per sec
for mov in $(ls ./ | grep -E '\.m4v|\.mp4|\.mov|\.MOV');do 
  dir=$(echo $mov | sed -E 's/\.mp4|\.m4v|\.mov|\.MOV//g')
  echo $mov
  echo $dir
  if [ ! -d $mov$dir ]; 
    then mkdir ./$dir
  fi;

  ffmpeg -i $mov -r $flame ./$dir/image_%04d.jpg
done
