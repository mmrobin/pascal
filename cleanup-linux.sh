#!/bin/bash

# count the number of relevant files
fileCount=$(find pMod*-*r.png | wc -l)

# echo $fileCount

if [ "$fileCount" -eq "0" ];
then
    echo "There are no fractal .png files. Exiting..."
    exit 0
fi

msg1="Found $fileCount fractal .png files."
msg2="Delete these files (Y/n)? "
msgY="Deleted $fileCount files. Exiting..."
msgN="No files were deleted. Exiting..."

msgE="Bad input. No files were deleted. Exiting..."

echo $msg1
echo $msg2
read yn

case $yn in
    [Yy])
        rm pMod*-*r.png
        echo $msgY
        ;;
    "")
        rm pMod*-*r.png
        echo $msgY
        ;;
    [Nn])
        echo $msgN
        exit
        ;;
    *)
        echo $msgE
        exit
        ;;
esac
    
