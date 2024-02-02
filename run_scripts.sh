#!/bin/bash
source ./configs/config.sh
DIRECTORY="./para"

python3 src/inner_para.py

find "$DIRECTORY" -name "*.npy" -exec sh -c '
    file={};
    echo "Sending '$file' to remote server";
    sshpass -p "$REMOTE_PASS" scp "$file" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_MATRIX_DIR/$(basename "$file")"
' \;

python3 src/getRGBD.py
