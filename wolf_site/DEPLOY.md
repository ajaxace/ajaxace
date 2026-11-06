# Wolf: put it on Hostinger (separate from your other sites)

You need: a Hostinger web hosting plan with PHP 8.2 or newer, and a subdomain (for example `wolf.yourdomain.com`) that points at its own empty folder. Nothing else on your hosting is touched.

## One-time set-up
1. hPanel > Websites > your site > **Domains > Subdomains**. Create the subdomain. Note the folder it points to.
2. hPanel > **Advanced > PHP Configuration**. Choose PHP 8.2 or newer. Make sure these extensions are ticked: `pdo_sqlite`, `curl`, `openssl`, `fileinfo`, `mbstring`.
3. hPanel > **Security > SSL**. Make sure the subdomain has SSL (https). Wolf needs https for the microphone and install-to-home-screen.
4. hPanel > **File Manager**. Open the subdomain's folder.
5. Upload these files from `wolf_site/`: `index.html`, `guide.html`, the `guide/` folder, `app.js`, `api.php`, `sw.js`, `manifest.webmanifest`, `.htaccess`, `icon-192.png`, `icon-512.png`, `apple-touch-icon.png`. Do NOT upload `src/`, `build.py`, `DEPLOY.md`.
6. Open `https://your-subdomain/api.php?a=health`. You should see `{"ok":true,...}`. If you see an error, tell Claude what it says.
7. Open `https://your-subdomain/` on your phone. Tap **Create my family** and follow the set-up guide.

The first visit creates a `data` folder (database and photos) and a `config.php` (a secret key). Never delete or share them. Back them up from File Manager once a week: download `data/` and `config.php`.

## Optional
- Put your support email and set-up video link in `config.php` after the first run: change `'support' => ''` to `'support' => 'you@example.com'` and `'video' => ''` to the video's address. They then show in the set-up guide.
- Screenshots: put images in a `guide/` folder next to `index.html`, named as in `SETUP_VIDEO_SHOTLIST.md`. Any missing image simply doesn't show.

## Updating later
Upload the new `index.html`, `app.js` and `api.php` over the old ones. Leave `data/` and `config.php` alone.

## Telling families about maintenance
Open `config.php` in File Manager and set `'notice' => 'Planned maintenance Sunday 2am to 3am (UK). Wolf may be unavailable.'`. A banner appears on every open Wolf within about 15 seconds. Set it back to `''` to remove it.

## Free automatic checks (so you don't have to watch it)
1. Sign up for a free uptime monitor (for example UptimeRobot).
2. Add a monitor for `https://wolf.yourdomain.com/api.php?a=health`, checking every 5 minutes, and send alerts to your email.
3. In hPanel, turn on auto-renew only after you've decided you want to keep paying. Put the renewal date in your calendar 60 days ahead.
