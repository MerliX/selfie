if [ ! -f /data/base.db ]; then
    python recreate_db.py
fi

cd /selfie/src
nginx & python selfie.py