# Wolf: day-one runbook (everything is ready; follow in order)

Wolf is already built, tested and packaged in `wolf_upload.zip`. Nothing needs writing on the day. If a step fails, the "If something goes wrong" table at the bottom says what to do.

## Part A. Before you start (10 minutes)
1. Buy the Hostinger plan (Unlimited, as discussed). Choose a domain name for Wolf, or use a subdomain of one you own (for example `wolf.yourdomain.com`).
2. Create a mailbox such as `support@yourdomain.com` (hPanel > Emails). Families will email this address. It keeps your personal email out of it.
3. Have the file `wolf_upload.zip` on your computer.

## Part B. Put Wolf online (about 15 minutes)
1. hPanel > **Websites** > your site > **Domains** > **Subdomains**. Create `wolf`. It gets its own folder, so it stays apart from your other sites. Do not use your main `public_html` folder.
2. hPanel > **Advanced** > **PHP Configuration**. Choose **PHP 8.2 or newer**. Tick the extensions `pdo_sqlite`, `curl`, `openssl`, `fileinfo`, `mbstring`. Set `upload_max_filesize` and `post_max_size` to `16M`. Save.
3. hPanel > **Security** > **SSL**. Make sure the subdomain shows as secure (https). Wait a few minutes if it is still being issued.
4. hPanel > **File Manager**. Open the subdomain's folder. Delete any default page.
5. **Upload** `wolf_upload.zip`, right-click it, choose **Extract**, and extract into the same folder. Check `index.html`, `api.php`, `check.php` and the `guide` and `legal` folders are directly in that folder.
6. Open `https://wolf.yourdomain.com/check.php`. Every line should be green. Fix any red line using the "Fix:" text under it, refresh, repeat.
7. When everything is green, **delete `check.php`** in File Manager.
8. Open `https://wolf.yourdomain.com/api.php?a=health`. You should see `{"ok":true,"version":"1.1.0",...}`.

## Part C. First-time setup in the owner dashboard (5 minutes)
1. In File Manager, right-click `config.php` > Edit. Copy the value on the line starting `'admin' =>`. This is your owner code. Do not share it. Close the file without changing anything.
2. Open `https://wolf.yourdomain.com/admin.html`, paste the code, and tap **Open dashboard**.
3. Under **Settings**, type your support email, paste your set-up video link when you have one, and tap **Save settings**.
4. Use **Maintenance banner** any time you want to warn families (clear it afterwards).

## Part D. Put it on your phone (2 minutes)
1. On your Android, open `https://wolf.yourdomain.com` in Chrome.
2. Type your name, tap **Create my family**, and follow the set-up guide. You will need a free Google AI key (the guide shows you where).
3. Chrome menu (three dots) > **Add to Home screen** or **Install app**.
4. Then follow `TEST_PLAN.md`. It lists every test, what you should see, and what to send back to Claude.

## Part E. Final legal text (do this before you share Wolf with anyone)
Claude Chat writes the final privacy notice and terms. Paste each into a text file and upload it over the draft:
- `legal/privacy.md` (shown at `/privacy.html`)
- `legal/terms.md` (shown at `/terms.html`)
While a file still contains the line starting `[DRAFT]`, the page shows a red DRAFT banner. Replace `{{legal_name}}`, `{{postal_address}}` and `{{support_email}}` with your real details. Do not share Wolf publicly while the DRAFT banner shows.

## Part F. Waiting list (optional, for the pre-sign-up period)
- The page is `https://wolf.yourdomain.com/waitlist.html`. Add `?s=tiktok` (or any word) to the end of the link to see where sign-ups came from. Do not share the link until Claude Chat has approved the page wording.
- Emails are listed in the owner dashboard. Download them as CSV to use in your email tool. Use the dashboard to remove an email if someone asks.

## Part G. Weekly routine (5 minutes)
1. Owner dashboard > **Download database backup**.
2. File Manager > download the `data/photos` folder and `config.php`. Keep them somewhere private.
3. Look at the **Problems on the server** box. Send anything that is not empty to Claude.

## Updating later
Upload the new `index.html`, `app.js`, `api.php` and any other changed file over the old ones. Leave `data/` and `config.php` alone. Check the version number on the Family tab or at `/api.php?a=health`.

## If something goes wrong
| What you see | What to do |
|---|---|
| A blank page or "500" on `api.php` | Open `check.php` (upload it again if you deleted it). Fix any red line. Then look in `data/error.log` and send Claude the last lines. |
| `check.php` says PHP too old | hPanel > Advanced > PHP Configuration > choose 8.2 or newer. |
| "Not signed in" keeps coming back | Make sure you open the https address. The cookie needs https. |
| Microphone does nothing | Needs https and the browser's microphone permission for the site. Use the mic on the keyboard if it is blocked. |
| Photos fail to upload | `check.php` upload limits; set both to 16M. |
| Calendar link rejected | It must be the secret or published link from Google, Outlook or iCloud, starting with https://. |
| AI says "key did not work" | The family copied the key wrongly or used the wrong Google account. Make a new key. |
| Everyone suddenly signed out | Do not delete or replace `config.php` or the `data` folder. |
| You deleted `data/` or `config.php` by mistake | See `RESTORE.md`. |
