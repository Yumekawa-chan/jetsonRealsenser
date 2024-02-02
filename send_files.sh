#!/bin/bash

source ./configs/config.sh

DIRECTORIES=("image" "matrix")

for DIR in "${DIRECTORIES[@]}"
do
    if [ "$DIR" == "matrix" ]; then
        inotifywait -m "$DIR" -e create -e moved_to --format '%w%f' |
            while read file; do
                if [[ $file == *.npy ]]; then
                    echo "The file '$file' appeared in directory '$DIR' via 'create/moved_to'"
                    sshpass -p "$REMOTE_PASS" scp "$file" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_BASE_DIR$DIR/"
                fi
            done
    else
        inotifywait -m "$DIR" -e create -e moved_to --format '%w%f' |
            while read file; do
                echo "The file '$file' appeared in directory '$DIR' via 'create/moved_to'"
                sshpass -p "$REMOTE_PASS" scp "$file" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_BASE_DIR$DIR/"
            done
    fi
done
