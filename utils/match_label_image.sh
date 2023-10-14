#!/bin/bash

Help(){
    echo "./$(basename $0) [-h][-e]"
    echo ""
    echo "-e: extension for images in source directory (e.g. jpg, png)"
    exit 0
}

Run(){
    for label in $(ls "${label_path}"); do
        filename=$(basename -- "${label}")
        filename="${filename%.*}"

        # search for file in images
        image="${src_image_path}/${filename}.${img_extension}"
        (! [[ -f $image ]]) && echo "$filename not found..." && exit 1

        # copy if file was found
        cp $image $des_image_path  
        echo $image 
    done
}

readonly label_path="datasets/labels"
readonly des_image_path="datasets/images"
readonly src_image_path="images/sample"

img_extension="jpg"

while getopts ":e:" arg; do
    case $arg in
        e)
            img_extension=$OPTARG
            ;;
        *)
            Help
            ;;
    esac
done

original_path=$(pwd)
cd .. 
Run
cd $original_path