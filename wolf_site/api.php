<?php
declare(strict_types=1);
/* Wolf family app: single-file JSON API (PHP 8 + SQLite). */
error_reporting(E_ALL);
ini_set('display_errors', '0');
const COLS = ['ev','shop','rem','notes','chores','meals','rota'];
const LIMIT_ITEM = 6000;
const PHOTO_MAX = 7000000;
const PHOTO_CAP = 250;

function out(array $d, int $code = 200): never {
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($d, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}
function fail(string $m, int $code = 400): never { out(['ok' => false, 'error' => $m], $code); }

/* ---------- config + database (created on first run) ---------- */
$cfgFile = __DIR__ . '/config.php';
if (!is_file($cfgFile)) {
    $cfg = ['data' => 'data', 'db' => 'wolf_' . bin2hex(random_bytes(8)) . '.sqlite', 'secret' => bin2hex(random_bytes(32)),
            'support' => '', 'video' => '', 'app' => 'Wolf'];
    @mkdir(__DIR__ . '/data', 0750, true);
    @file_put_contents(__DIR__ . '/data/.htaccess', "Require all denied\nDeny from all\n");
    @file_put_contents(__DIR__ . '/data/index.html', '');
    @mkdir(__DIR__ . '/data/photos', 0750, true);
    file_put_contents($cfgFile, "<?php\nreturn " . var_export($cfg, true) . ";\n");
}
$cfg = require $cfgFile;
$DATA = __DIR__ . '/' . $cfg['data'];
if (!is_dir($DATA . '/photos')) { @mkdir($DATA . '/photos', 0750, true); }
try {
    $db = new PDO('sqlite:' . $DATA . '/' . $cfg['db']);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $db->exec('PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;');
    $db->exec("CREATE TABLE IF NOT EXISTS families(id TEXT PRIMARY KEY, code TEXT UNIQUE, created INT, ver INT DEFAULT 1, ai_key TEXT, ai_model TEXT, ics_url TEXT, ics_cache TEXT, ics_ts INT DEFAULT 0, people TEXT, tz TEXT, ai_day TEXT, ai_count INT DEFAULT 0);
    CREATE TABLE IF NOT EXISTS devices(token_hash TEXT PRIMARY KEY, fam TEXT, label TEXT, created INT, seen INT);
    CREATE TABLE IF NOT EXISTS items(id TEXT PRIMARY KEY, fam TEXT, col TEXT, data TEXT, ts INT);
    CREATE INDEX IF NOT EXISTS items_fam ON items(fam, col);
    CREATE TABLE IF NOT EXISTS attempts(ip TEXT, kind TEXT, ts INT);");
} catch (Throwable $e) { fail('Storage is not available.', 500); }

$act = $_GET['a'] ?? '';
$method = $_SERVER['REQUEST_METHOD'];
$isHttps = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https');
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';

function body(): array {
    $raw = file_get_contents('php://input');
    if ($raw === '' || $raw === false) return [];
    if (strlen($raw) > 60000) fail('Too large.', 413);
    $j = json_decode($raw, true);
    return is_array($j) ? $j : [];
}
function tooMany(PDO $db, string $ip, string $kind, int $max, int $secs): bool {
    $db->prepare('DELETE FROM attempts WHERE ts < ?')->execute([time() - 86400]);
    $st = $db->prepare('SELECT COUNT(*) FROM attempts WHERE ip=? AND kind=? AND ts>?');
    $st->execute([$ip, $kind, time() - $secs]);
    return (int)$st->fetchColumn() >= $max;
}
function note(PDO $db, string $ip, string $kind): void { $db->prepare('INSERT INTO attempts VALUES(?,?,?)')->execute([$ip, $kind, time()]); }
function newCode(PDO $db): string {
    $a = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    for ($t = 0; $t < 20; $t++) {
        $c = ''; for ($i = 0; $i < 10; $i++) $c .= $a[random_int(0, 31)];
        $st = $db->prepare('SELECT 1 FROM families WHERE code=?'); $st->execute([$c]);
        if (!$st->fetch()) return $c;
    }
    fail('Try again.', 500);
}
function giveDevice(PDO $db, string $fam, string $label, bool $https): void {
    $tok = bin2hex(random_bytes(32));
    $db->prepare('INSERT INTO devices VALUES(?,?,?,?,?)')->execute([hash('sha256', $tok), $fam, mb_substr($label, 0, 40), time(), time()]);
    setcookie('wolf_t', $tok, ['expires' => time() + 86400 * 400, 'path' => '/', 'secure' => $https, 'httponly' => true, 'samesite' => 'Lax']);
}
function who(PDO $db): ?array {
    $t = $_COOKIE['wolf_t'] ?? '';
    if (!preg_match('/^[a-f0-9]{64}$/', $t)) return null;
    $st = $db->prepare('SELECT d.fam, d.label, d.token_hash FROM devices d WHERE d.token_hash=?');
    $st->execute([hash('sha256', $t)]);
    $r = $st->fetch(PDO::FETCH_ASSOC);
    if (!$r) return null;
    return $r;
}
function bump(PDO $db, string $fam): void { $db->prepare('UPDATE families SET ver=ver+1 WHERE id=?')->execute([$fam]); }
function enc(string $s, string $secret): string {
    $key = hash('sha256', $secret, true); $iv = random_bytes(12);
    $c = openssl_encrypt($s, 'aes-256-gcm', $key, OPENSSL_RAW_DATA, $iv, $tag);
    return base64_encode($iv . $tag . $c);
}
function dec(?string $s, string $secret): string {
    if (!$s) return '';
    $b = base64_decode($s, true); if ($b === false || strlen($b) < 29) return '';
    $key = hash('sha256', $secret, true);
    $p = openssl_decrypt(substr($b, 28), 'aes-256-gcm', $key, OPENSSL_RAW_DATA, substr($b, 0, 12), substr($b, 12, 16));
    return $p === false ? '' : $p;
}
function famRow(PDO $db, string $id): array { $st = $db->prepare('SELECT * FROM families WHERE id=?'); $st->execute([$id]); return $st->fetch(PDO::FETCH_ASSOC) ?: []; }
function clean($v, int $depth = 0) {
    if ($depth > 2) return null;
    if (is_array($v)) { $o = []; $n = 0; foreach ($v as $k => $x) { if (++$n > 40) break; $o[is_int($k) ? $k : mb_substr((string)$k, 0, 20)] = clean($x, $depth + 1); } return $o; }
    if (is_string($v)) return mb_substr($v, 0, 1000);
    if (is_int($v) || is_float($v) || is_bool($v) || $v === null) return $v;
    return null;
}
function addItem(PDO $db, string $fam, string $col, array $data): string {
    $id = bin2hex(random_bytes(6));
    $j = json_encode(clean($data), JSON_UNESCAPED_UNICODE);
    if (strlen($j) > LIMIT_ITEM) fail('Too large.');
    $n = $db->prepare('SELECT COUNT(*) FROM items WHERE fam=? AND col=?'); $n->execute([$fam, $col]);
    if ((int)$n->fetchColumn() > 2000) fail('This list is full.');
    $db->prepare('INSERT INTO items VALUES(?,?,?,?,?)')->execute([$id, $fam, $col, $j, time()]);
    bump($db, $fam);
    return $id;
}
function getItems(PDO $db, string $fam, string $col): array {
    $st = $db->prepare('SELECT id,data,ts FROM items WHERE fam=? AND col=? ORDER BY ts, id'); $st->execute([$fam, $col]);
    $o = [];
    foreach ($st->fetchAll(PDO::FETCH_ASSOC) as $r) { $d = json_decode($r['data'], true) ?: []; $d['id'] = $r['id']; $d['_ts'] = (int)$r['ts']; $o[] = $d; }
    return $o;
}

/* ---------- public actions ---------- */
if ($act === 'health') out(['ok' => true, 'php' => PHP_VERSION, 'sqlite' => true, 'openssl' => function_exists('openssl_encrypt'), 'curl' => function_exists('curl_init')]);

if ($method === 'POST' && ($_SERVER['HTTP_X_WOLF'] ?? '') !== '1' && $act !== '') fail('Bad request.', 403);

if ($act === 'create' && $method === 'POST') {
    if (tooMany($db, $ip, 'create', 6, 3600)) fail('Too many new families from this connection. Try again later.', 429);
    note($db, $ip, 'create');
    $b = body(); $id = bin2hex(random_bytes(8)); $code = newCode($db);
    $db->prepare('INSERT INTO families(id,code,created,ver,people,tz) VALUES(?,?,?,?,?,?)')->execute([$id, $code, time(), 1, json_encode(['adults' => [], 'kids' => []]), 'UTC']);
    giveDevice($db, $id, (string)($b['label'] ?? 'Phone'), $isHttps);
    out(['ok' => true, 'code' => $code]);
}
if ($act === 'join' && $method === 'POST') {
    if (tooMany($db, $ip, 'join', 8, 3600)) fail('Too many tries. Wait an hour and try again.', 429);
    $b = body(); $code = strtoupper(preg_replace('/[^A-Za-z0-9]/', '', (string)($b['code'] ?? '')));
    $st = $db->prepare('SELECT id FROM families WHERE code=?'); $st->execute([$code]); $f = $st->fetch(PDO::FETCH_ASSOC);
    if (!$f) { note($db, $ip, 'join'); fail('That code was not found. Check it and try again.', 404); }
    giveDevice($db, $f['id'], (string)($b['label'] ?? 'Phone'), $isHttps);
    bump($db, $f['id']);
    out(['ok' => true]);
}

$me = who($db);
if ($act === 'me') {
    if (!$me) out(['ok' => true, 'authed' => false, 'support' => $cfg['support'] ?? '', 'video' => $cfg['video'] ?? '']);
    out(['ok' => true, 'authed' => true, 'support' => $cfg['support'] ?? '', 'video' => $cfg['video'] ?? '']);
}
if (!$me) fail('Not signed in.', 401);
$fam = $me['fam'];
$F = famRow($db, $fam);
if (!$F) fail('Family not found.', 404);
$db->prepare('UPDATE devices SET seen=? WHERE token_hash=?')->execute([time(), $me['token_hash']]);

/* ---------- calendar link (ICS) ---------- */
function okHost(string $url): bool {
    $p = parse_url($url);
    if (!$p || ($p['scheme'] ?? '') !== 'https' || empty($p['host'])) { return getenv('WOLF_TEST') === '1' && preg_match('#^http://(127\.0\.0\.1|localhost)#', $url) === 1; }
    $h = strtolower($p['host']);
    $okSuffix = ['google.com', 'outlook.live.com', 'outlook.office365.com', 'outlook.office.com', 'office365.com', 'icloud.com', 'proton.me', 'calendar.proton.me', 'fastmail.com', 'yahoo.com'];
    $ok = false; foreach ($okSuffix as $s) { if ($h === $s || str_ends_with($h, '.' . $s)) { $ok = true; break; } }
    if (!$ok) return false;
    $ips = @gethostbynamel($h) ?: [];
    foreach ($ips as $i) { if (!filter_var($i, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) return false; }
    return true;
}
function httpGet(string $url, array $headers = [], int $timeout = 8): ?string {
    $ch = curl_init($url);
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => $timeout, CURLOPT_FOLLOWLOCATION => false, CURLOPT_HTTPHEADER => $headers, CURLOPT_MAXFILESIZE => 3000000, CURLOPT_USERAGENT => 'WolfFamilyApp/1.0']);
    $r = curl_exec($ch); $code = curl_getinfo($ch, CURLINFO_RESPONSE_CODE); curl_close($ch);
    return ($r !== false && $code >= 200 && $code < 300) ? (string)$r : null;
}
function icsDate(string $val, array $params, DateTimeZone $fz): ?array {
    try {
        if (($params['VALUE'] ?? '') === 'DATE' || preg_match('/^\d{8}$/', $val)) { $d = DateTimeImmutable::createFromFormat('Ymd', $val, $fz); return $d ? [$d->setTime(0, 0), true] : null; }
        $utc = str_ends_with($val, 'Z'); $v = rtrim($val, 'Z');
        $tz = $utc ? new DateTimeZone('UTC') : (isset($params['TZID']) ? (@new DateTimeZone($params['TZID'])) : $fz);
        $d = DateTimeImmutable::createFromFormat('Ymd\THis', $v, $tz);
        return $d ? [$d->setTimezone($fz), false] : null;
    } catch (Throwable $e) { return null; }
}
function parseIcs(string $txt, DateTimeZone $fz): array {
    $txt = preg_replace("/\r?\n[ \t]/", '', $txt);
    $from = (new DateTimeImmutable('monday this week', $fz))->setTime(0, 0);
    $to = $from->modify('+80 days');
    $res = [];
    if (!preg_match_all('/BEGIN:VEVENT(.*?)END:VEVENT/s', $txt, $blocks)) return $res;
    foreach ($blocks[1] as $blk) {
        $p = [];
        foreach (preg_split('/\r?\n/', $blk) as $line) {
            if (!str_contains($line, ':')) continue;
            [$left, $val] = explode(':', $line, 2); $parts = explode(';', $left); $name = strtoupper(array_shift($parts)); $pr = [];
            foreach ($parts as $x) { if (str_contains($x, '=')) { [$k, $v] = explode('=', $x, 2); $pr[strtoupper($k)] = trim($v, '"'); } }
            if (!isset($p[$name])) $p[$name] = [$val, $pr];
        }
        if (!isset($p['DTSTART']) || ($p['STATUS'][0] ?? '') === 'CANCELLED') continue;
        $s = icsDate(trim($p['DTSTART'][0]), $p['DTSTART'][1], $fz); if (!$s) continue;
        [$start, $allDay] = $s;
        $title = trim(str_replace(['\\,', '\;', '\\n', '\\N', '\\\\'], [',', ';', ' ', ' ', '\\'], $p['SUMMARY'][0] ?? 'Event'));
        $starts = [];
        if (isset($p['RRULE'])) {
            $r = []; foreach (explode(';', $p['RRULE'][0]) as $x) { if (str_contains($x, '=')) { [$k, $v] = explode('=', $x, 2); $r[strtoupper($k)] = $v; } }
            $freq = $r['FREQ'] ?? ''; $iv = max(1, (int)($r['INTERVAL'] ?? 1)); $cnt = isset($r['COUNT']) ? (int)$r['COUNT'] : 0;
            $until = null; if (isset($r['UNTIL'])) { $u = icsDate($r['UNTIL'], [], $fz); $until = $u ? $u[0]->setTime(23, 59, 59) : null; }
            $ex = []; if (isset($p['EXDATE'])) { foreach (explode(',', $p['EXDATE'][0]) as $e) { $d = icsDate(trim($e), $p['EXDATE'][1], $fz); if ($d) $ex[$d[0]->format('Ymd')] = 1; } }
            $map = ['MO' => 1, 'TU' => 2, 'WE' => 3, 'TH' => 4, 'FR' => 5, 'SA' => 6, 'SU' => 7];
            $days = []; if (!empty($r['BYDAY'])) { foreach (explode(',', $r['BYDAY']) as $x) { $x = substr($x, -2); if (isset($map[$x])) $days[] = $map[$x]; } }
            $n = 0; $guard = 0;
            if ($freq === 'WEEKLY') {
                $wk = $start->modify('monday this week')->setTime((int)$start->format('H'), (int)$start->format('i'));
                if (!$days) $days = [(int)$start->format('N')];
                while ($guard++ < 800) {
                    foreach ($days as $dn) {
                        $occ = $wk->modify('+' . ($dn - 1) . ' days');
                        if ($occ < $start) continue;
                        if ($until && $occ > $until) break 2;
                        $n++; if ($cnt && $n > $cnt) break 2;
                        if ($occ >= $from && $occ <= $to && !isset($ex[$occ->format('Ymd')])) $starts[] = $occ;
                    }
                    $wk = $wk->modify('+' . $iv . ' weeks'); if ($wk > $to) break;
                }
            } elseif (in_array($freq, ['DAILY', 'MONTHLY', 'YEARLY'], true)) {
                $unit = ['DAILY' => 'days', 'MONTHLY' => 'months', 'YEARLY' => 'years'][$freq]; $occ = $start; $k = 0;
                while ($guard++ < 800) {
                    if ($until && $occ > $until) break;
                    $n++; if ($cnt && $n > $cnt) break;
                    if ($occ > $to) break;
                    if ($occ >= $from && !isset($ex[$occ->format('Ymd')])) $starts[] = $occ;
                    $k += $iv; $occ = $start->modify('+' . $k . ' ' . $unit);
                }
            } else { if ($start >= $from && $start <= $to) $starts[] = $start; }
        } else { if ($start >= $from && $start <= $to) $starts[] = $start; }
        foreach ($starts as $o) $res[] = ['t' => mb_substr($title, 0, 80), 'd' => $o->format('Y-m-d'), 'h' => $allDay ? '' : $o->format('H:i')];
        if (count($res) > 1500) break;
    }
    usort($res, fn($a, $b) => strcmp($a['d'] . $a['h'], $b['d'] . $b['h']));
    return $res;
}
function refreshIcs(PDO $db, array $F, string $secret): int {
    $url = dec($F['ics_url'], $secret);
    if (!$url || !okHost($url)) return -1;
    $raw = null;
    for ($hop = 0; $hop < 4; $hop++) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 8, CURLOPT_FOLLOWLOCATION => false, CURLOPT_MAXFILESIZE => 3000000, CURLOPT_USERAGENT => 'WolfFamilyApp/1.0']);
        $r = curl_exec($ch); $code = curl_getinfo($ch, CURLINFO_RESPONSE_CODE); $loc = (string)curl_getinfo($ch, CURLINFO_REDIRECT_URL); curl_close($ch);
        if ($code >= 300 && $code < 400 && $loc !== '') { $url = $loc; if (!okHost($url)) return -1; continue; }
        if ($r !== false && $code >= 200 && $code < 300) $raw = (string)$r;
        break;
    }
    if ($raw === null || !str_contains($raw, 'BEGIN:VCALENDAR')) return -1;
    try { $tz = new DateTimeZone($F['tz'] ?: 'UTC'); } catch (Throwable $e) { $tz = new DateTimeZone('UTC'); }
    $ev = parseIcs($raw, $tz);
    $db->prepare('UPDATE families SET ics_cache=?, ics_ts=?, ver=ver+1 WHERE id=?')->execute([json_encode($ev), time(), $F['id']]);
    return count($ev);
}

/* ---------- authed actions ---------- */
if ($act === 'sync') {
    $since = (int)($_GET['since'] ?? 0);
    $tz = (string)($_GET['tz'] ?? '');
    if ($tz !== '' && $tz !== $F['tz'] && @timezone_open($tz)) { $db->prepare('UPDATE families SET tz=? WHERE id=?')->execute([$tz, $fam]); $F['tz'] = $tz; }
    if ($F['ics_url'] && time() - (int)$F['ics_ts'] > 1800) { refreshIcs($db, $F, $cfg['secret']); $F = famRow($db, $fam); }
    if ($since === (int)$F['ver']) out(['ok' => true, 'same' => true]);
    $data = []; foreach (COLS as $c) $data[$c] = getItems($db, $fam, $c);
    $photos = getItems($db, $fam, 'photos');
    $mc = $db->prepare('SELECT label,created FROM devices WHERE fam=?'); $mc->execute([$fam]);
    out(['ok' => true, 'ver' => (int)$F['ver'], 'data' => $data, 'photos' => $photos, 'ics' => json_decode($F['ics_cache'] ?: '[]', true), 'members' => $mc->fetchAll(PDO::FETCH_ASSOC),
         'code' => $F['code'], 'people' => json_decode($F['people'] ?: '{}', true), 'hasKey' => (bool)$F['ai_key'], 'model' => $F['ai_model'], 'hasIcs' => (bool)$F['ics_url'], 'icsTs' => (int)$F['ics_ts'], 'me' => $me['label']]);
}
if ($act === 'put' && $method === 'POST') {
    $b = body(); $c = (string)($b['col'] ?? ''); if (!in_array($c, COLS, true)) fail('Unknown list.');
    $o = is_array($b['obj'] ?? null) ? $b['obj'] : fail('Nothing to add.'); unset($o['id']); $o['by'] = $me['label'];
    out(['ok' => true, 'id' => addItem($db, $fam, $c, $o)]);
}
if ($act === 'upd' && $method === 'POST') {
    $b = body(); $c = (string)($b['col'] ?? ''); $id = (string)($b['id'] ?? ''); if (!in_array($c, COLS, true)) fail('Unknown list.');
    $st = $db->prepare('SELECT data FROM items WHERE id=? AND fam=? AND col=?'); $st->execute([$id, $fam, $c]); $r = $st->fetch(PDO::FETCH_ASSOC);
    if (!$r) fail('Not found.', 404);
    $d = array_merge(json_decode($r['data'], true) ?: [], is_array($b['patch'] ?? null) ? clean($b['patch']) : []); unset($d['id']);
    $j = json_encode($d, JSON_UNESCAPED_UNICODE); if (strlen($j) > LIMIT_ITEM) fail('Too large.');
    $db->prepare('UPDATE items SET data=? WHERE id=? AND fam=?')->execute([$j, $id, $fam]); bump($db, $fam); out(['ok' => true]);
}
if ($act === 'del' && $method === 'POST') {
    $b = body(); $c = (string)($b['col'] ?? ''); $id = (string)($b['id'] ?? '');
    if (!in_array($c, array_merge(COLS, ['photos']), true)) fail('Unknown list.');
    if ($c === 'photos') {
        $st = $db->prepare('SELECT data FROM items WHERE id=? AND fam=? AND col=?'); $st->execute([$id, $fam, 'photos']); $r = $st->fetch(PDO::FETCH_ASSOC);
        if ($r) { $d = json_decode($r['data'], true); if (!empty($d['file']) && preg_match('/^[a-f0-9]{32}\.(jpg|png|webp|gif)$/', $d['file'])) @unlink($DATA . '/photos/' . $fam . '_' . $d['file']); }
    }
    $db->prepare('DELETE FROM items WHERE id=? AND fam=? AND col=?')->execute([$id, $fam, $c]); bump($db, $fam); out(['ok' => true]);
}
if ($act === 'photo' && $method === 'POST') {
    if (empty($_FILES['f']) || $_FILES['f']['error'] !== UPLOAD_ERR_OK) fail('The photo did not upload.');
    $f = $_FILES['f']; if ($f['size'] > PHOTO_MAX) fail('That photo is too big.');
    $fi = new finfo(FILEINFO_MIME_TYPE); $mime = $fi->file($f['tmp_name']);
    $ext = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/webp' => 'webp', 'image/gif' => 'gif'][$mime] ?? null;
    if (!$ext || !@getimagesize($f['tmp_name'])) fail('Only photos can be added.');
    $n = $db->prepare('SELECT COUNT(*) FROM items WHERE fam=? AND col=?'); $n->execute([$fam, 'photos']);
    if ((int)$n->fetchColumn() >= PHOTO_CAP) fail('Family storage is full. Delete some photos first.');
    $name = bin2hex(random_bytes(16)) . '.' . $ext;
    if (!move_uploaded_file($f['tmp_name'], $DATA . '/photos/' . $fam . '_' . $name)) fail('Could not save the photo.', 500);
    out(['ok' => true, 'id' => addItem($db, $fam, 'photos', ['file' => $name, 'by' => $me['label'], 'ts' => time() * 1000])]);
}
if ($act === 'img') {
    $id = (string)($_GET['id'] ?? '');
    $st = $db->prepare('SELECT data FROM items WHERE id=? AND fam=? AND col=?'); $st->execute([$id, $fam, 'photos']); $r = $st->fetch(PDO::FETCH_ASSOC);
    $d = $r ? json_decode($r['data'], true) : null;
    if (!$d || !preg_match('/^[a-f0-9]{32}\.(jpg|png|webp|gif)$/', $d['file'] ?? '')) { http_response_code(404); exit; }
    $p = $DATA . '/photos/' . $fam . '_' . $d['file']; if (!is_file($p)) { http_response_code(404); exit; }
    header('Content-Type: ' . ['jpg' => 'image/jpeg', 'png' => 'image/png', 'webp' => 'image/webp', 'gif' => 'image/gif'][pathinfo($p, PATHINFO_EXTENSION)]);
    header('Cache-Control: private, max-age=86400'); header('X-Content-Type-Options: nosniff'); header('Content-Length: ' . filesize($p)); readfile($p); exit;
}
if ($act === 'people' && $method === 'POST') {
    $b = body(); $l = fn($x) => array_values(array_slice(array_filter(array_map(fn($s) => mb_substr(trim((string)$s), 0, 24), is_array($x) ? $x : []), 'strlen'), 0, 8));
    $db->prepare('UPDATE families SET people=? WHERE id=?')->execute([json_encode(['adults' => $l($b['adults'] ?? []), 'kids' => $l($b['kids'] ?? [])]), $fam]); bump($db, $fam); out(['ok' => true]);
}
function aiBase(): string { return rtrim(getenv('WOLF_AI_BASE') ?: 'https://generativelanguage.googleapis.com', '/'); }
function pickModel(string $key): ?string {
    $raw = httpGet(aiBase() . '/v1beta/models?pageSize=200', ['x-goog-api-key: ' . $key], 10); if ($raw === null) return null;
    $j = json_decode($raw, true); $best = null; $bv = -1.0; $any = null;
    foreach (($j['models'] ?? []) as $m) {
        $n = preg_replace('#^models/#', '', $m['name'] ?? ''); if (!in_array('generateContent', $m['supportedGenerationMethods'] ?? [], true)) continue;
        if (preg_match('/(preview|exp|image|tts|audio|live|embed|thinking|vision|8b|lite)/i', $n)) continue;
        if (preg_match('/^gemini-(\d+(?:\.\d+)?)-flash$/', $n, $mm)) { if ((float)$mm[1] > $bv) { $bv = (float)$mm[1]; $best = $n; } }
        elseif (str_contains($n, 'flash') && !$any) $any = $n;
    }
    return $best ?: $any;
}
if ($act === 'settings' && $method === 'POST') {
    $b = body(); $msg = [];
    if (isset($b['ai_key'])) {
        $k = trim((string)$b['ai_key']);
        if ($k === '') { $db->prepare('UPDATE families SET ai_key=NULL, ai_model=NULL WHERE id=?')->execute([$fam]); }
        else {
            if (!preg_match('/^[A-Za-z0-9_\-]{20,80}$/', $k)) fail('That does not look like an AI key. Copy it again, with nothing else.');
            $m = pickModel($k); if (!$m) fail('That key did not work. Check you copied all of it, then try again.');
            $db->prepare('UPDATE families SET ai_key=?, ai_model=? WHERE id=?')->execute([enc($k, $cfg['secret']), $m, $fam]); $msg[] = 'AI key works.';
        }
    }
    if (isset($b['ics_url'])) {
        $u = trim((string)$b['ics_url']);
        if ($u === '') { $db->prepare('UPDATE families SET ics_url=NULL, ics_cache=NULL, ics_ts=0 WHERE id=?')->execute([$fam]); }
        else {
            if (!okHost($u)) fail('That link is not a calendar link we can read. It should start with https:// and come from Google, Outlook or iCloud.');
            if (!empty($b['tz']) && @timezone_open((string)$b['tz'])) $db->prepare('UPDATE families SET tz=? WHERE id=?')->execute([(string)$b['tz'], $fam]);
            $db->prepare('UPDATE families SET ics_url=?, ics_ts=0 WHERE id=?')->execute([enc($u, $cfg['secret']), $fam]);
            $n = refreshIcs($db, famRow($db, $fam), $cfg['secret']);
            if ($n < 0) { $db->prepare('UPDATE families SET ics_url=NULL WHERE id=?')->execute([$fam]); fail('We could not read that calendar link. Copy the whole link again.'); }
            $msg[] = 'Calendar connected: ' . $n . ' upcoming events found.';
        }
    }
    bump($db, $fam); out(['ok' => true, 'message' => implode(' ', $msg)]);
}
if ($act === 'wipe' && $method === 'POST') {
    foreach (glob($DATA . '/photos/' . $fam . '_*') ?: [] as $p) @unlink($p);
    foreach (['items', 'devices'] as $t) $db->prepare("DELETE FROM $t WHERE fam=?")->execute([$fam]);
    $db->prepare('DELETE FROM families WHERE id=?')->execute([$fam]);
    setcookie('wolf_t', '', ['expires' => 1, 'path' => '/']); out(['ok' => true]);
}
if ($act === 'leave' && $method === 'POST') { $db->prepare('DELETE FROM devices WHERE token_hash=?')->execute([$me['token_hash']]); setcookie('wolf_t', '', ['expires' => 1, 'path' => '/']); bump($db, $fam); out(['ok' => true]); }
if ($act === 'newcode' && $method === 'POST') { $c = newCode($db); $db->prepare('UPDATE families SET code=? WHERE id=?')->execute([$c, $fam]); bump($db, $fam); out(['ok' => true, 'code' => $c]); }

/* ---------- AI chat (uses the family's own free key) ---------- */
function dueAt(string $local, string $tz): int { try { $d = new DateTimeImmutable($local, new DateTimeZone($tz)); return $d->getTimestamp() * 1000; } catch (Throwable $e) { return 0; } }
if ($act === 'ai' && $method === 'POST') {
    $key = dec($F['ai_key'], $cfg['secret']); if (!$key) fail('no_key', 409);
    $today = gmdate('Y-m-d'); if ($F['ai_day'] !== $today) { $db->prepare('UPDATE families SET ai_day=?, ai_count=0 WHERE id=?')->execute([$today, $fam]); $F['ai_count'] = 0; }
    if ((int)$F['ai_count'] >= 300) fail('That is a lot of messages for today. Try again tomorrow, or use your own paid AI plan.', 429);
    $db->prepare('UPDATE families SET ai_count=ai_count+1 WHERE id=?')->execute([$fam]);
    $b = body(); $msg = mb_substr(trim((string)($b['message'] ?? '')), 0, 800); if ($msg === '') fail('Say something first.');
    $tzs = (string)($b['tz'] ?? $F['tz'] ?: 'UTC'); if (!@timezone_open($tzs)) $tzs = 'UTC';
    $now = new DateTimeImmutable('now', new DateTimeZone($tzs));
    $ppl = json_decode($F['people'] ?: '{}', true) ?: [];
    $brief = function (string $c, callable $f) use ($db, $fam) { return json_encode(array_map($f, getItems($db, $fam, $c)), JSON_UNESCAPED_UNICODE); };
    $ics = array_slice(json_decode($F['ics_cache'] ?: '[]', true) ?: [], 0, 60);
    $sys = "You are Wolf, a friendly family assistant. Answer in 1 to 3 short sentences, plain text, UK English, no markdown. Local date and time: " . $now->format('l j F Y, H:i') . " (" . $tzs . "). Today is " . $now->format('Y-m-d') . ". Adults: " . implode(', ', $ppl['adults'] ?? []) . ". Children: " . implode(', ', $ppl['kids'] ?? []) . ". "
         . "Family events: " . $brief('ev', fn($e) => ['id' => $e['id'], 'title' => $e['t'] ?? '', 'date' => $e['d'] ?? '', 'time' => $e['h'] ?? '']) . ". Linked calendar (read only): " . json_encode($ics, JSON_UNESCAPED_UNICODE) . ". Shopping list: " . $brief('shop', fn($e) => $e['t'] ?? '') . ". Reminders: " . $brief('rem', fn($e) => $e['t'] ?? '') . ". Notes: " . $brief('notes', fn($e) => $e['t'] ?? '') . ". Chores: " . $brief('chores', fn($e) => ($e['who'] ?? '') . ': ' . ($e['t'] ?? '')) . ". Dinners: " . $brief('meals', fn($e) => ($e['day'] ?? '') . ': ' . ($e['t'] ?? '')) . ". School run (0=Mon): " . $brief('rota', fn($e) => ($e['day'] ?? '') . ': ' . ($e['who'] ?? '')) . ". "
         . "Use the tools to add events, shopping items, reminders, notes, chores, dinners or school-run cover when asked. Convert words like tomorrow or Friday to YYYY-MM-DD from the date above, and times to 24-hour HH:MM. You have no live data for trains, taxis, cinemas, weather or traffic and you cannot book anything or promise a pickup; say so plainly. Never invent calendar entries. After using a tool, confirm in one short sentence.";
    $S = ['type' => 'STRING'];
    $tools = [['functionDeclarations' => [
        ['name' => 'add_event', 'description' => 'Add an event to the family calendar', 'parameters' => ['type' => 'OBJECT', 'properties' => ['title' => $S, 'date' => ['type' => 'STRING', 'description' => 'YYYY-MM-DD'], 'time' => ['type' => 'STRING', 'description' => 'HH:MM 24 hour, or empty']], 'required' => ['title', 'date']]],
        ['name' => 'remove_event', 'description' => 'Remove a family event by id', 'parameters' => ['type' => 'OBJECT', 'properties' => ['id' => $S], 'required' => ['id']]],
        ['name' => 'add_shopping', 'description' => 'Add an item to the shopping list', 'parameters' => ['type' => 'OBJECT', 'properties' => ['item' => $S], 'required' => ['item']]],
        ['name' => 'add_reminder', 'description' => 'Add a reminder', 'parameters' => ['type' => 'OBJECT', 'properties' => ['text' => $S, 'at' => ['type' => 'STRING', 'description' => 'Local YYYY-MM-DDTHH:MM, or empty']], 'required' => ['text']]],
        ['name' => 'add_note', 'description' => 'Post a shared family note', 'parameters' => ['type' => 'OBJECT', 'properties' => ['text' => $S], 'required' => ['text']]],
        ['name' => 'add_chore', 'description' => 'Add a chore for a child with a pocket money reward', 'parameters' => ['type' => 'OBJECT', 'properties' => ['title' => $S, 'who' => $S, 'pounds' => ['type' => 'NUMBER']], 'required' => ['title', 'who']]],
        ['name' => 'set_meal', 'description' => 'Set dinner for a weekday', 'parameters' => ['type' => 'OBJECT', 'properties' => ['day' => ['type' => 'STRING', 'description' => 'Mon, Tue, Wed, Thu, Fri, Sat or Sun'], 'meal' => $S, 'ingredients' => $S], 'required' => ['day', 'meal']]],
        ['name' => 'set_pickup', 'description' => 'Set who has the school run on a weekday', 'parameters' => ['type' => 'OBJECT', 'properties' => ['day' => $S, 'who' => $S], 'required' => ['day', 'who']]],
    ]]];
    $days = ['mon' => 0, 'tue' => 1, 'wed' => 2, 'thu' => 3, 'fri' => 4, 'sat' => 5, 'sun' => 6];
    $exec = function (string $n, array $a) use ($db, $fam, $me, $tzs, $days): string {
        $by = $me['label'];
        switch ($n) {
            case 'add_event': addItem($db, $fam, 'ev', ['t' => (string)($a['title'] ?? 'Event'), 'd' => (string)($a['date'] ?? ''), 'h' => (string)($a['time'] ?? ''), 'by' => 'Wolf']); return 'Added';
            case 'remove_event': $db->prepare("DELETE FROM items WHERE id=? AND fam=? AND col='ev'")->execute([(string)($a['id'] ?? ''), $fam]); bump($db, $fam); return 'Removed';
            case 'add_shopping': addItem($db, $fam, 'shop', ['t' => (string)($a['item'] ?? ''), 'x' => 0, 'by' => 'Wolf']); return 'Added';
            case 'add_reminder': addItem($db, $fam, 'rem', ['t' => (string)($a['text'] ?? ''), 'at' => !empty($a['at']) ? dueAt((string)$a['at'], $tzs) : 0, 'x' => 0, 'by' => 'Wolf']); return 'Added';
            case 'add_note': addItem($db, $fam, 'notes', ['t' => (string)($a['text'] ?? ''), 'ts' => time() * 1000, 'by' => 'Wolf']); return 'Added';
            case 'add_chore': addItem($db, $fam, 'chores', ['t' => (string)($a['title'] ?? ''), 'who' => (string)($a['who'] ?? ''), 'v' => (int)round(((float)($a['pounds'] ?? 0)) * 100), 'x' => 0, 'paid' => 0, 'by' => 'Wolf']); return 'Added';
            case 'set_meal': $d = $days[strtolower(substr((string)($a['day'] ?? ''), 0, 3))] ?? null; if ($d === null) return 'Unknown day';
                $st = $db->prepare("SELECT id FROM items WHERE fam=? AND col='meals' AND json_extract(data,'$.day')=?"); $st->execute([$fam, $d]); $id = $st->fetchColumn();
                $dat = json_encode(['day' => $d, 't' => mb_substr((string)($a['meal'] ?? ''), 0, 80), 'ing' => mb_substr((string)($a['ingredients'] ?? ''), 0, 300)], JSON_UNESCAPED_UNICODE);
                if ($id) { $db->prepare('UPDATE items SET data=? WHERE id=?')->execute([$dat, $id]); bump($db, $fam); } else addItem($db, $fam, 'meals', json_decode($dat, true)); return 'Set';
            case 'set_pickup': $d = $days[strtolower(substr((string)($a['day'] ?? ''), 0, 3))] ?? null; if ($d === null || $d > 4) return 'Weekdays only';
                $st = $db->prepare("SELECT id FROM items WHERE fam=? AND col='rota' AND json_extract(data,'$.day')=?"); $st->execute([$fam, $d]); $id = $st->fetchColumn();
                $dat = json_encode(['day' => $d, 'who' => mb_substr((string)($a['who'] ?? ''), 0, 24)]);
                if ($id) { $db->prepare('UPDATE items SET data=? WHERE id=?')->execute([$dat, $id]); bump($db, $fam); } else addItem($db, $fam, 'rota', json_decode($dat, true)); return 'Set';
        }
        return 'Unknown tool';
    };
    $model = $F['ai_model'] ?: 'gemini-2.5-flash'; $contents = [['role' => 'user', 'parts' => [['text' => $msg]]]]; $reply = '';
    for ($round = 0; $round < 4; $round++) {
        $payload = json_encode(['systemInstruction' => ['parts' => [['text' => $sys]]], 'contents' => $contents, 'tools' => $tools]);
        $ch = curl_init(aiBase() . '/v1beta/models/' . rawurlencode($model) . ':generateContent');
        curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $payload, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 40, CURLOPT_HTTPHEADER => ['Content-Type: application/json', 'x-goog-api-key: ' . $key]]);
        $raw = curl_exec($ch); $code = curl_getinfo($ch, CURLINFO_RESPONSE_CODE); curl_close($ch);
        if ($raw === false) fail('Could not reach the AI service. Try again.', 502);
        if ($code === 429) fail('Your free AI limit is used up for now. Try again later, or use your own paid AI plan.', 429);
        if ($code === 400 || $code === 403) fail('The AI service refused the request. Check your AI key in Set-up.', 400);
        if ($code < 200 || $code >= 300) fail('The AI service had a problem. Try again.', 502);
        $j = json_decode($raw, true); $parts = $j['candidates'][0]['content']['parts'] ?? [];
        $calls = []; $txt = ''; foreach ($parts as $p) { if (isset($p['functionCall'])) $calls[] = $p['functionCall']; if (isset($p['text'])) $txt .= $p['text']; }
        if (!$calls) { $reply = trim($txt); break; }
        $contents[] = ['role' => 'model', 'parts' => $parts]; $resp = [];
        foreach ($calls as $c) $resp[] = ['functionResponse' => ['name' => $c['name'], 'response' => ['result' => $exec((string)$c['name'], is_array($c['args'] ?? null) ? $c['args'] : [])]]];
        $contents[] = ['role' => 'user', 'parts' => $resp]; if ($txt !== '') $reply = trim($txt);
    }
    out(['ok' => true, 'reply' => $reply !== '' ? $reply : 'Done.']);
}
fail('Unknown request.', 404);
