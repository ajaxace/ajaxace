# Restoring Wolf from a backup

Your backup has two parts: the database file (`wolf-backup-DATE.sqlite`) and `config.php` (holds the secret key that unlocks families' saved AI keys and calendar links). Photos are in `data/photos`.

## If the site still works but data is lost
1. File Manager > open the `data` folder.
2. Find the current database file named like `wolf_xxxxxxxx.sqlite` (its exact name is the `'db'` line in `config.php`).
3. Rename it to `old-wolf.sqlite` (do not delete it yet).
4. Upload your backup and rename it to the exact name from the `'db'` line.
5. Open the Wolf address. Families should be back. Keep `old-wolf.sqlite` until you are sure.

## If the whole folder is lost
1. Re-upload `wolf_upload.zip` and extract it.
2. Upload your saved `config.php` over the new one, and your saved `data` folder (database and photos).
3. Open the address.

Without your original `config.php`, families' saved AI keys and calendar links cannot be read. They would need to paste them again. Everything else still works.
