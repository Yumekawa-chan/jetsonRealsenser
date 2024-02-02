#!/bin/bash
python3 src/inner_para.py
python3 src/getRGBD.py

source ./configs/config.sh

DIRECTORY="./para"

find "$DIRECTORY" -name "*.npy" -exec sh -c '
    file={};
    echo "Sending '$file' to remote server";
    sshpass -p "$REMOTE_PASS" scp "$file" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_BASE_DIR/matrix/$(basename "$file")"
' \;

