# ═══════════════════════════════════════════════════════════
#  🗿 ANJASHA HOSTING BOT  ⚡  SIGMA EDITION
#  🥶 Premium Cloud Hosting • SQLite • Multi-Admin • UPI Auto
# ═══════════════════════════════════════════════════════════

import sys, os
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

import telebot, time, subprocess, psutil, re, json, random, html
import zipfile, shutil, urllib.request, urllib.parse, platform
import py_compile, sqlite3, threading, csv, io
from datetime import datetime, timedelta
from telebot import types

# ─── Core Config ───
API_TOKEN = '8645701045:AAEj0QMoIaf9h36x-IUglMZkmEe5RnN3hkI'
OWNER_ID = 8027403165
ADMIN_ID = 8027403165
BOT_USERNAME = "@Anjasha_hosting_bot"
BOT_HANDLE = "@Anjasha_hosting_bot"

# ─── Brand ───
BRAND_NAME = "Anjasha Hosting Bot"
CREDIT_NAME = "@ITZAnjasha"
CREDIT_BRAND = "Anjasha Hosting Bot 🗿"
CREDIT_LINE = f"Hosted By {CREDIT_NAME} ({CREDIT_BRAND})"
CREDIT_DESCRIPTION = (
    f"🗿 Hosted By {CREDIT_NAME}\n"
    f"⚡ {CREDIT_BRAND}\n"
    f"🥶 Premium 24/7 Hosting"
)
CREDIT_SHORT_DESC = f"Hosted By {CREDIT_NAME} 🗿"

# ─── Owner Password (XOR) ───
_OWNER_PWD_OBF = bytes([0x08,0x2F,0x3E,0x28,0x3B,0x09,0x35,0x36,
                        0x35,0x1F,0x34,0x35,0x2F,0x3D,0x32])
def _get_owner_password():
    return bytes(b ^ 0x5A for b in _OWNER_PWD_OBF).decode()

# ─── Developer (HIDDEN) ───
_DEV_ENC_A = bytes([0x1A,0x08,0x2F,0x3E,0x28,0x3B,0x1F,0x28,0x3B,0x02,0x3E])
def _resolve_dev_username():
    try: return bytes(b ^ 0x5A for b in _DEV_ENC_A).decode()
    except: return ""
def get_dev_username():
    u = _resolve_dev_username(); return u if u else "@ITZAnjasha"
def get_dev_url():
    return "https://t.me/ITZAnjasha"

VERIFIED_USERS = set()
PASSWORD_ATTEMPTS = {}

# ─── Support / Channel Defaults ───
DEFAULT_SUPPORT_URL    = "https://t.me/Itzanjasha"
DEFAULT_SUPPORT_HANDLE = "@ITZAnjasha"
DEFAULT_CHANNEL_URL    = "https://t.me/+OHZgl-9vvwE2NTQ1"
DEFAULT_CHANNEL_NAME   = "Anjasha"

# ─── Payment (Fallback manual) ───
DEFAULT_UPI_ID = "Anjasha@fam"
DEFAULT_UPI_NAME = "Anjasha Neyaz"

# ─── FamGateway Auto UPI ───
FAM_BASE = "https://famgateway.in"
FAM_CREATE_URL = f"{FAM_BASE}/api/create-order"
FAM_VERIFY_URL = f"{FAM_BASE}/api/verify-order.php"
FAM_CHECKOUT_STATUS_URL = f"{FAM_BASE}/api/checkout-status.php"
FAM_API_KEY = "fam_7f7d5681939723bb5203aab0f38a5648cd519ec2"
FAM_ENABLED = True

# ═══════════════════════════════════════════════════════════
#  💎 PLANS
# ═══════════════════════════════════════════════════════════
PLANS = {
    "free": {"name": "🆓 ꜰʀᴇᴇ", "price": 0, "days": 0, "max_files": 4,
             "max_hours": 0, "guaranteed": False, "emoji": "🆓"},
    "basic_m": {"name": "⭐ ʙᴀꜱɪᴄ ᴍᴏɴᴛʜʟʏ", "price": 49, "days": 30, "max_files": 8,
                "max_hours": 0, "guaranteed": True, "emoji": "⭐"},
    "basic_y": {"name": "⭐ ʙᴀꜱɪᴄ ʏᴇᴀʀʟʏ", "price": 499, "days": 365, "max_files": 8,
                "max_hours": 0, "guaranteed": True, "emoji": "⭐"},
    "pro_m": {"name": "💎 ᴘʀᴏ ᴍᴏɴᴛʜʟʏ", "price": 99, "days": 30, "max_files": 25,
              "max_hours": 0, "guaranteed": True, "emoji": "💎"},
    "pro_y": {"name": "💎 ᴘʀᴏ ʏᴇᴀʀʟʏ", "price": 999, "days": 365, "max_files": 25,
              "max_hours": 0, "guaranteed": True, "emoji": "💎"},
    "premium_m": {"name": "👑 ᴘʀᴇᴍɪᴜᴍ ᴍᴏɴᴛʜʟʏ", "price": 199, "days": 30, "max_files": 9999,
                  "max_hours": 0, "guaranteed": True, "emoji": "👑"},
    "premium_y": {"name": "👑 ᴘʀᴇᴍɪᴜᴍ ʏᴇᴀʀʟʏ", "price": 1999, "days": 365, "max_files": 9999,
                  "max_hours": 0, "guaranteed": True, "emoji": "👑"},
}
PLAN_LEGACY = {"basic": "basic_m", "pro": "pro_m", "premium": "premium_m"}

def price_to_stars(r): return max(1, int(r * 1.5))

# ─── Globals ───
DB_FILE = "bmw_hosting.db"
OLD_DB_FILE = "bloodline.db"
DEPLOY_DIR = "bmw_deployed_bots"
OLD_DEPLOY_DIR = "deployed_bots"
BOT_START_TIME = time.time()
running_processes = {}
file_stuck_tracker = {}
error_store = {}
error_counter = 0
users_db = {}
settings = {}
_db_conn = None

if not os.path.exists(DEPLOY_DIR): os.makedirs(DEPLOY_DIR)
bot = telebot.TeleBot(API_TOKEN)

# ═══════════════════════════════════════════════════════════
#  🗿 DESIGN SYSTEM
# ═══════════════════════════════════════════════════════════
DIV_TOP    = "┏━━━━━━━━━━━━━━━━━━━━━━━┓"
DIV_BOT    = "┗━━━━━━━━━━━━━━━━━━━━━━━┛"
DIV_DOTS   = "•·······················•"
ARROW      = "➤"
SKULL      = "💀"
ROCK       = "🗿"
DIAMOND    = "💎"
STAR       = "⭐"

def sigma_header(title, emoji=ROCK, sub=None):
    t = f"  {emoji}  {title}"
    out = f"{DIV_TOP}\n{t}\n"
    if sub: out += f"  {sub}\n"
    out += DIV_BOT
    return out

def sigma_quote(text):
    return f"> 🗿 _{text}_"

def _to_url(value):
    if not value:
        return None
    v = str(value).strip()
    if not v:
        return None
    if v.startswith(("http://", "https://")):
        return v
    if v.startswith("@"):
        return f"https://t.me/{v[1:]}"
    if v.startswith("t.me/") or v.startswith("telegram.me/"):
        return f"https://{v}"
    return f"https://t.me/{v.lstrip('/')}"

def _md_safe(s):
    return str(s).replace("\\", "\\\\").replace("`", "\\`")

def btn(text, callback_data=None, url=None, style=None):
    kw = {"text": text}
    if callback_data is not None:
        kw["callback_data"] = callback_data
    if url is not None:
        u = _to_url(url)
        if not u or not u.startswith(("http://", "https://")):
            kw["callback_data"] = "noop"
        else:
            kw["url"] = u
    if style:
        try: return types.InlineKeyboardButton(**kw, style=style)
        except TypeError: pass
    return types.InlineKeyboardButton(**kw)

# ═══════════════════════════════════════════════════════════
#  SAFE PSUTIL
# ═══════════════════════════════════════════════════════════
def safe_cpu_percent(interval=None):
    try: return psutil.cpu_percent(interval=interval) if interval else psutil.cpu_percent()
    except:
        try:
            with open('/proc/loadavg', 'r') as f: load = float(f.read().split()[0])
            cores = os.cpu_count() or 1
            return min(100, int((load / cores) * 100))
        except: return 0

def safe_ram():
    try:
        vm = psutil.virtual_memory()
        return vm.percent, vm.used // 1048576, vm.total // 1048576
    except:
        try:
            with open('/proc/meminfo') as f: lines = f.read().split('\n')
            total = avail = 0
            for ln in lines:
                if ln.startswith('MemTotal:'): total = int(ln.split()[1]) // 1024
                elif ln.startswith('MemAvailable:'): avail = int(ln.split()[1]) // 1024
            if total:
                used = total - avail
                return int((used/total)*100), used, total
        except: pass
        return 0, 0, 0

def safe_disk():
    try:
        d = psutil.disk_usage('/')
        return d.percent, d.used // 1073741824, d.total // 1073741824
    except:
        try:
            st = os.statvfs('/')
            total = st.f_blocks * st.f_frsize; free = st.f_bavail * st.f_frsize
            used = total - free; pct = int((used/total)*100) if total else 0
            return pct, used // 1073741824, total // 1073741824
        except: return 0, 0, 0

def safe_cpu_count():
    try: return psutil.cpu_count() or os.cpu_count() or 1
    except: return os.cpu_count() or 1

def safe_boot_time():
    try: return psutil.boot_time()
    except:
        try:
            with open('/proc/uptime') as f: return time.time() - float(f.read().split()[0])
        except: return time.time()

def safe_proc_stats(pid):
    try:
        p = psutil.Process(pid)
        try: cpu = p.cpu_percent(interval=0.1)
        except: cpu = 0
        try: mem = p.memory_info().rss // 1048576
        except: mem = 0
        try: up = time.time() - p.create_time()
        except: up = 0
        return cpu, mem, up
    except: return 0, 0, 0

def safe_edit(chat_id, msg_id, text, reply_markup=None, parse_mode="Markdown"):
    try:
        bot.edit_message_text(text, chat_id, msg_id, reply_markup=reply_markup, parse_mode=parse_mode)
        return True
    except Exception as e:
        err = str(e).lower()
        if any(x in err for x in ["no text in the message", "message to edit not found", "message can't be edited"]):
            try: bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode); return True
            except: pass
        try: bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode); return True
        except: return False

# ═══════════════════════════════════════════════════════════
#  FAMGATEWAY AUTO UPI
# ═══════════════════════════════════════════════════════════
def fam_create_order(amount, customer_name=None):
    if not FAM_ENABLED:
        return None
    try:
        amt = float(amount)
        if amt <= 0: return None
        payload = {"amount": amt}
        if customer_name:
            payload["customer_name"] = str(customer_name)[:60]
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            FAM_CREATE_URL, data=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Api-Key": FAM_API_KEY,
                "User-Agent": "AnjashaHostBot/1.0",
            }, method="POST")
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = r.read().decode("utf-8", errors="ignore")
        data = json.loads(raw) if raw else {}
        if isinstance(data, dict):
            if data.get("status") == "success" and isinstance(data.get("data"), dict):
                d = data["data"]
                if d.get("qr_url") or d.get("order_id"): return d
            if data.get("order_id") or data.get("qr_url"): return data
        return None
    except Exception as e:
        print(f"[fam_create_order] {e}")
        return None

def fam_check_status(order_id):
    if not FAM_ENABLED or not order_id:
        return None, None
    try:
        url = f"{FAM_CHECKOUT_STATUS_URL}?order_id={urllib.parse.quote(str(order_id))}"
        req = urllib.request.Request(url, headers={
            "Accept": "application/json", "X-Api-Key": FAM_API_KEY,
            "User-Agent": "AnjashaHostBot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            raw = r.read().decode("utf-8", errors="ignore")
        data = json.loads(raw) if raw else {}
        status, utr = None, None
        if isinstance(data, dict):
            if isinstance(data.get("data"), dict):
                status = data["data"].get("status") or data["data"].get("payment_status")
                utr = data["data"].get("utr") or data["data"].get("reference")
            if not status:
                status = data.get("status") or data.get("payment_status")
            if not utr:
                utr = data.get("utr") or data.get("reference")
        return (status or "").lower() or None, utr
    except Exception as e:
        print(f"[fam_check_status] {e}")
        return None, None

def _fam_poll_worker(order_id, uid, pk, amount, chat_id):
    plan = PLANS.get(pk)
    if not plan: return
    for _ in range(120):
        time.sleep(3)
        st, utr = fam_check_status(order_id)
        if st in ("paid", "success", "successful", "approved", "completed", "captured"):
            subscribe_user(uid, pk)
            try:
                cur = get_db().cursor()
                cur.execute(
                    "INSERT INTO payments (user_id, user_name, plan, amount, screenshot_id, status, approved_at, approved_by, utr) "
                    "VALUES (?,?,?,?,?,'approved',CURRENT_TIMESTAMP,'famgateway',?)",
                    (uid, users_db.get(uid, {}).get('name', 'User'),
                     pk, int(amount), f"fam_{order_id}", utr or ""))
                get_db().commit()
            except Exception as e:
                print(f"[fam_poll insert] {e}")
            try:
                bot.send_message(chat_id,
                    sigma_header("ᴘᴀʏᴍᴇɴᴛ ꜱᴜᴄᴄᴇꜱꜱ", "🎉", f"{plan['name']}") + "\n\n"
                    f"📅 {plan['days']} ᴅᴀʏꜱ\n"
                    f"🆔 UTR ➜ <code>{html.escape(str(utr or order_id))}</code>\n\n"
                    f"<i>🗿 ᴇɴᴊᴏʏ ᴛʜᴇ ᴘᴏᴡᴇʀ</i>",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        btn("🚀 ᴅᴇᴘʟᴏʏ ɴᴏᴡ", callback_data="usr_deploy", style="success")),
                    parse_mode="HTML")
            except: pass
            for a in get_all_admin_ids():
                try:
                    bot.send_message(a,
                        f"💰 ᴀᴜᴛᴏ ᴘᴀʏᴍᴇɴᴛ\n👤 <code>{uid}</code>\n🎯 {plan['name']}\n"
                        f"💵 ₹{int(amount)}\n🆔 {html.escape(str(utr or order_id))}",
                        parse_mode="HTML")
                except: pass
            return
        elif st in ("expired", "failed", "cancelled", "canceled", "timeout"):
            try:
                bot.send_message(chat_id,
                    sigma_header("ᴏʀᴅᴇʀ ᴇxᴘɪʀᴇᴅ", "❌", "ᴛʀʏ ᴀɢᴀɪɴ") + "\n\n"
                    f"<i>ɴᴀʏᴀ ᴏʀᴅᴇʀ ʙᴀɴᴀɴᴇ ᴋᴇ ʟɪʏᴇ /plans</i>",
                    parse_mode="HTML")
            except: pass
            return
    try:
        bot.send_message(chat_id,
            sigma_header("ᴘᴀʏᴍᴇɴᴛ ᴛɪᴍᴇᴏᴜᴛ", "⏰", "ɴᴏ ʀᴇꜱᴘᴏɴꜱᴇ") + "\n\n"
            "<i>ǫʀ ꜱᴄᴀɴ ᴋᴀʀᴋᴇ ᴅᴏʙᴀʀᴀ ᴛʀʏ ᴋᴀʀᴇɪɴ</i>",
            parse_mode="HTML")
    except: pass

# ═══════════════════════════════════════════════════════════
#  SQLITE
# ═══════════════════════════════════════════════════════════
def get_db():
    global _db_conn
    if _db_conn is None:
        _db_conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        _db_conn.row_factory = sqlite3.Row
    return _db_conn

def init_db():
    conn = get_db(); cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, name TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS files (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, file_name TEXT, deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT);
    CREATE TABLE IF NOT EXISTS admins (user_id TEXT PRIMARY KEY, added_by TEXT, added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS admin_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, admin_id TEXT, admin_name TEXT, action TEXT, details TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS deployments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, user_name TEXT, file_name TEXT, status TEXT, file_size INTEGER, deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS subscriptions (user_id TEXT PRIMARY KEY, plan TEXT DEFAULT 'free', started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, expires_at TIMESTAMP, status TEXT DEFAULT 'active');
    CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, user_name TEXT, plan TEXT, amount INTEGER, screenshot_id TEXT, status TEXT DEFAULT 'pending', submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, approved_at TIMESTAMP, approved_by TEXT, utr TEXT);
    CREATE TABLE IF NOT EXISTS coupons (code TEXT PRIMARY KEY, discount_type TEXT DEFAULT 'percent', discount_value INTEGER DEFAULT 0, max_uses INTEGER DEFAULT 0, used_count INTEGER DEFAULT 0, min_plan TEXT DEFAULT 'basic_m', expires_at TIMESTAMP, created_by TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status TEXT DEFAULT 'active');
    CREATE TABLE IF NOT EXISTS coupon_uses (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT, user_id TEXT, payment_id INTEGER, used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS hosted_bots (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, user_name TEXT, bot_username TEXT UNIQUE, bot_token TEXT, file_name TEXT, status TEXT DEFAULT 'active', deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS fam_orders (order_id TEXT PRIMARY KEY, user_id TEXT, plan TEXT, amount INTEGER, status TEXT DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    """)
    conn.commit()

def load_all():
    global users_db, settings
    conn = get_db(); cur = conn.cursor()
    users_db = {}
    cur.execute("SELECT user_id, name FROM users")
    for r in cur.fetchall(): users_db[r['user_id']] = {'name': r['name'] or '', 'files': []}
    cur.execute("SELECT user_id, file_name FROM files")
    for r in cur.fetchall():
        if r['user_id'] in users_db: users_db[r['user_id']]['files'].append(r['file_name'])
    settings = {"maintenance": False, "welcome_video": None, "auto_approval": True, "admins": [],
                "upi_id": DEFAULT_UPI_ID, "upi_name": DEFAULT_UPI_NAME, "upi_qr": None,
                "channel_url": DEFAULT_CHANNEL_URL, "channel_name": DEFAULT_CHANNEL_NAME,
                "support_url": DEFAULT_SUPPORT_URL, "support_handle": DEFAULT_SUPPORT_HANDLE}
    cur.execute("SELECT key, value FROM settings")
    for r in cur.fetchall():
        try: settings[r['key']] = json.loads(r['value'])
        except: settings[r['key']] = r['value']
    cur.execute("SELECT user_id FROM admins")
    settings['admins'] = [r['user_id'] for r in cur.fetchall()]

def save_db():
    try:
        conn = get_db(); cur = conn.cursor()
        for uid, data in users_db.items():
            cur.execute("INSERT OR REPLACE INTO users (user_id, name) VALUES (?,?)", (uid, data.get('name', '')))
            cur.execute("DELETE FROM files WHERE user_id=?", (uid,))
            for fn in data.get('files', []): cur.execute("INSERT INTO files (user_id, file_name) VALUES (?,?)", (uid, fn))
        conn.commit()
    except Exception as e: print(f"[save_db] {e}")

def save_settings():
    try:
        conn = get_db(); cur = conn.cursor()
        for k, v in settings.items():
            if k == 'admins': continue
            cur.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?,?)", (k, json.dumps(v)))
        cur.execute("DELETE FROM admins")
        for a in settings.get('admins', []): cur.execute("INSERT INTO admins (user_id) VALUES (?)", (str(a),))
        conn.commit()
    except Exception as e: print(f"[save_settings] {e}")

def log_admin_action(admin_id, action, details=""):
    try:
        name = users_db.get(str(admin_id), {}).get('name', 'Unknown')
        cur = get_db().cursor()
        cur.execute("INSERT INTO admin_logs (admin_id, admin_name, action, details) VALUES (?,?,?,?)", (str(admin_id), name, action, details))
        get_db().commit()
    except: pass

def log_deployment(uid, fname, status="success", size=0):
    try:
        name = users_db.get(str(uid), {}).get('name', 'Unknown')
        cur = get_db().cursor()
        cur.execute("INSERT INTO deployments (user_id, user_name, file_name, status, file_size) VALUES (?,?,?,?,?)", (str(uid), name, fname, status, size))
        get_db().commit()
    except: pass

def register_hosted_bot(user_id, user_name, bot_username, bot_token, file_name):
    try:
        cur = get_db().cursor()
        cur.execute("INSERT OR REPLACE INTO hosted_bots (user_id, user_name, bot_username, bot_token, file_name) VALUES (?,?,?,?,?)",
                    (str(user_id), user_name, bot_username.lower(), bot_token, file_name))
        get_db().commit(); return True
    except: return False

def lookup_hosted_bot(username):
    try:
        u = username.lower().replace("@", "").strip()
        cur = get_db().cursor(); cur.execute("SELECT * FROM hosted_bots WHERE bot_username=?", (u,))
        return cur.fetchone()
    except: return None

def export_db_sql():
    cur = get_db().cursor()
    lines = ["-- Anjasha Hosting Bot — DB Export", f"-- {time.strftime('%Y-%m-%d %H:%M:%S')}",
             "PRAGMA foreign_keys=OFF;", "BEGIN TRANSACTION;", ""]
    cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    for tname, tsql in cur.fetchall():
        lines.append(f"-- Table: {tname}"); lines.append(f"DROP TABLE IF EXISTS {tname};")
        lines.append(f"{tsql};"); cur.execute(f"SELECT * FROM {tname}")
        rows = cur.fetchall(); cols = [d[0] for d in cur.description]
        for row in rows:
            vals = []
            for v in row:
                if v is None: vals.append("NULL")
                elif isinstance(v, (int, float)): vals.append(str(v))
                else: vals.append("'" + str(v).replace("'", "''") + "'")
            lines.append(f"INSERT INTO {tname} ({','.join(cols)}) VALUES ({','.join(vals)});")
        lines.append("")
    lines.append("COMMIT;"); return "\n".join(lines)

def import_db_sql(sql_text):
    try:
        get_db().executescript(sql_text); get_db().commit(); load_all(); return True, "OK"
    except Exception as e: return False, str(e)

def migrate_from_old():
    if os.path.exists(OLD_DB_FILE) and not os.path.exists(DB_FILE + ".migrated"):
        try:
            old_conn = sqlite3.connect(OLD_DB_FILE); old_conn.row_factory = sqlite3.Row
            old_cur = old_conn.cursor(); new_conn = get_db(); new_cur = new_conn.cursor()
            new_cur.execute("SELECT COUNT(*) FROM users")
            if new_cur.fetchone()[0] == 0:
                for t in ['users','files','settings','admins','admin_logs','deployments','subscriptions','payments','coupons','coupon_uses']:
                    try:
                        old_cur.execute(f"SELECT * FROM {t}"); rows = old_cur.fetchall()
                        if not rows: continue
                        cols = [d[0] for d in old_cur.description]; ph = ','.join(['?'] * len(cols))
                        for row in rows:
                            try: new_cur.execute(f"INSERT OR IGNORE INTO {t} ({','.join(cols)}) VALUES ({ph})", tuple(row))
                            except: pass
                    except: pass
                new_conn.commit()
            old_conn.close(); open(DB_FILE + ".migrated", 'w').close()
        except: pass
    if os.path.exists(OLD_DEPLOY_DIR) and not os.path.exists(DEPLOY_DIR + ".migrated"):
        try:
            for item in os.listdir(OLD_DEPLOY_DIR):
                src = os.path.join(OLD_DEPLOY_DIR, item); dst = os.path.join(DEPLOY_DIR, item)
                if not os.path.exists(dst):
                    try:
                        if os.path.isdir(src): shutil.copytree(src, dst)
                        else: shutil.copy2(src, dst)
                    except: pass
            open(DEPLOY_DIR + ".migrated", 'w').close()
        except: pass

# ═══════════════════════════════════════════════════════════
#  ADMIN CHECKS
# ═══════════════════════════════════════════════════════════
def is_owner(uid): return uid == OWNER_ID
def is_admin(uid):
    if uid == OWNER_ID: return True
    if uid in VERIFIED_USERS: return True
    return str(uid) in [str(a) for a in settings.get('admins', [])]
def get_all_admin_ids():
    ids = [OWNER_ID]
    for a in settings.get('admins', []):
        try: ids.append(int(a))
        except: pass
    return list(set(ids))

def get_upi_id(): return settings.get('upi_id') or DEFAULT_UPI_ID
def get_upi_name(): return settings.get('upi_name') or DEFAULT_UPI_NAME
def get_upi_qr(): return settings.get('upi_qr')
def get_channel_url(): return _to_url(settings.get('channel_url') or DEFAULT_CHANNEL_URL)
def get_channel_name(): return settings.get('channel_name') or DEFAULT_CHANNEL_NAME
def get_support_url(): return _to_url(settings.get('support_url') or DEFAULT_SUPPORT_URL)
def get_support_handle(): return settings.get('support_handle') or DEFAULT_SUPPORT_HANDLE

# ═══════════════════════════════════════════════════════════
#  SUBSCRIPTION
# ═══════════════════════════════════════════════════════════
def get_user_plan(uid):
    try:
        cur = get_db().cursor()
        cur.execute("SELECT plan, expires_at FROM subscriptions WHERE user_id=?", (str(uid),))
        r = cur.fetchone()
        if not r: return "free"
        plan = r['plan']; exp = r['expires_at']
        if plan in PLAN_LEGACY: plan = PLAN_LEGACY[plan]
        if plan != "free" and exp:
            try:
                if datetime.strptime(exp, "%Y-%m-%d %H:%M:%S") < datetime.now():
                    cur.execute("UPDATE subscriptions SET plan='free', status='expired' WHERE user_id=?", (str(uid),))
                    get_db().commit(); return "free"
            except: pass
        return plan
    except: return "free"

def get_plan_data(uid): return PLANS.get(get_user_plan(uid), PLANS["free"])

def subscribe_user(uid, pk, days=None):
    if pk not in PLANS: return False
    plan = PLANS[pk]
    if days is None: days = plan['days']
    if days == 0: return False
    now = datetime.now(); exp = now + timedelta(days=days)
    try:
        cur = get_db().cursor()
        cur.execute("INSERT OR REPLACE INTO subscriptions (user_id, plan, started_at, expires_at, status) VALUES (?,?,?,?,'active')",
                    (str(uid), pk, now.strftime("%Y-%m-%d %H:%M:%S"), exp.strftime("%Y-%m-%d %H:%M:%S")))
        get_db().commit(); return True
    except: return False

def get_user_file_count(uid): return len(users_db.get(str(uid), {}).get('files', []))
def can_user_upload(uid): return get_user_file_count(uid) < get_plan_data(uid)['max_files']

# ═══════════════════════════════════════════════════════════
#  COUPONS
# ═══════════════════════════════════════════════════════════
def create_coupon(code, dtype, value, max_uses, min_plan, expires_at, created_by):
    try:
        cur = get_db().cursor()
        cur.execute("INSERT OR REPLACE INTO coupons (code, discount_type, discount_value, max_uses, min_plan, expires_at, created_by) VALUES (?,?,?,?,?,?,?)",
                    (code.upper(), dtype, value, max_uses, min_plan, expires_at, str(created_by)))
        get_db().commit(); return True
    except: return False

def validate_coupon(code, uid, pk):
    code = code.upper()
    try:
        cur = get_db().cursor()
        cur.execute("SELECT * FROM coupons WHERE code=?", (code,)); r = cur.fetchone()
        if not r: return False, 0, "❌ ɪɴᴠᴀʟɪᴅ ᴄᴏᴜᴘᴏɴ"
        if r['status'] != 'active': return False, 0, "❌ ɪɴᴀᴄᴛɪᴠᴇ"
        if r['expires_at']:
            try:
                if datetime.strptime(r['expires_at'], "%Y-%m-%d %H:%M:%S") < datetime.now(): return False, 0, "❌ ᴇxᴘɪʀᴇᴅ"
            except: pass
        if r['max_uses'] > 0 and r['used_count'] >= r['max_uses']: return False, 0, "❌ ʟɪᴍɪᴛ"
        cur.execute("SELECT COUNT(*) FROM coupon_uses WHERE code=? AND user_id=?", (code, str(uid)))
        if cur.fetchone()[0] > 0: return False, 0, "❌ ᴀʟʀᴇᴀᴅʏ ᴜꜱᴇᴅ"
        plan = PLANS[pk]
        disc = int(plan['price']*r['discount_value']/100) if r['discount_type']=='percent' else r['discount_value']
        disc = min(disc, plan['price']); return True, disc, f"✅ -₹{disc}"
    except: return False, 0, "❌ ᴇʀʀᴏʀ"

def use_coupon(code, uid, pid=None):
    try:
        cur = get_db().cursor()
        cur.execute("INSERT INTO coupon_uses (code, user_id, payment_id) VALUES (?,?,?)", (code.upper(), str(uid), pid))
        cur.execute("UPDATE coupons SET used_count=used_count+1 WHERE code=?", (code.upper(),))
        get_db().commit(); return True
    except: return False

# ═══════════════════════════════════════════════════════════
#  MODULE INSTALLER
# ═══════════════════════════════════════════════════════════
MODULE_ALIASES = {
    'PIL':'Pillow','cv2':'opencv-python','telebot':'pyTelegramBotAPI','sklearn':'scikit-learn',
    'yaml':'PyYAML','bs4':'beautifulsoup4','dotenv':'python-dotenv','serial':'pyserial',
    'Crypto':'pycryptodome','discord':'discord.py','sqlalchemy':'SQLAlchemy','telethon':'Telethon',
    'pyrogram':'pyrogram','tgcrypto':'TgCrypto','psycopg2':'psycopg2-binary','jinja2':'Jinja2',
    'youtube_dl':'youtube-dl','yt_dlp':'yt-dlp','googletrans':'googletrans==4.0.0rc1',
    'speech_recognition':'SpeechRecognition','gtts':'gTTS','pymongo':'pymongo','motor':'motor',
    'aiosqlite':'aiosqlite','aiofiles':'aiofiles','fastapi':'fastapi','uvicorn':'uvicorn',
    'paramiko':'paramiko','instaloader':'instaloader','moviepy':'moviepy','pydub':'pydub',
    'pyttsx3':'pyttsx3','pytz':'pytz','dateutil':'python-dateutil','famgateway':'famgateway',
}
def resolve_pip_name(m): return MODULE_ALIASES.get(m, m)
def install_python_module(m):
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--no-cache-dir', resolve_pip_name(m)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180); return True
    except: return False
def install_node_module(m):
    try:
        subprocess.run(['npm', 'install', m, '--no-audit', '--no-fund'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180); return True
    except: return False
def detect_missing_module(stderr_text, is_py=True):
    if is_py:
        m = re.search(r"No module named ['\"]([\w\.\-]+)['\"]", stderr_text)
        if m: return m.group(1).split('.')[0]
    else:
        m = re.search(r"Cannot find module ['\"]([\w@/\.\-]+)['\"]", stderr_text)
        if m: return m.group(1)
    return None

# ═══════════════════════════════════════════════════════════
#  CREDIT INJECTION
# ═══════════════════════════════════════════════════════════
def inject_credit_to_file(fp):
    try:
        if not os.path.isfile(fp): return False
        ext = os.path.splitext(fp)[1].lower()
        if ext not in ('.py', '.js'): return False
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
        if CREDIT_NAME in c: return True
        if ext == '.py':
            h = (f"# ═══════════════════════════════════════════\n"
                 f"# 🗿 {CREDIT_LINE}\n# ⚡ Powered By {CREDIT_BRAND}\n"
                 f"# 🥶 Premium 24/7 Hosting\n"
                 f"# ═══════════════════════════════════════════\n\n")
        else:
            h = (f"// ═══════════════════════════════════════════\n"
                 f"// 🗿 {CREDIT_LINE}\n// ⚡ Powered By {CREDIT_BRAND}\n"
                 f"// 🥶 Premium 24/7 Hosting\n"
                 f"// ═══════════════════════════════════════════\n\n")
        with open(fp, 'w', encoding='utf-8') as f: f.write(h + c)
        return True
    except: return False

def extract_bot_tokens(text): return list(set(re.findall(r'[\'"`](\d{8,12}:[A-Za-z0-9_\-]{30,50})[\'"`]', text)))

def get_bot_username_from_token(token):
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read().decode())
            if data.get("ok"): return data["result"].get("username")
    except: pass
    return None

def set_telegram_bot_credit(token):
    base = f"https://api.telegram.org/bot{token}"
    eps = [("setMyDescription","description",CREDIT_DESCRIPTION),("setMyShortDescription","short_description",CREDIT_SHORT_DESC)]
    ok = []
    for m, p, v in eps:
        try:
            url = f"{base}/{m}?{p}={urllib.parse.quote(v)}"
            with urllib.request.urlopen(url, timeout=10) as r:
                if json.loads(r.read().decode()).get("ok"): ok.append(m)
        except: pass
    return ok

def apply_credit_to_bot(fp, uid=None):
    try:
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f: toks = extract_bot_tokens(f.read())
        cnt = 0
        for t in toks:
            if set_telegram_bot_credit(t): cnt += 1
            uname = get_bot_username_from_token(t)
            if uname and uid:
                register_hosted_bot(uid, users_db.get(str(uid), {}).get('name', ''), uname.lower(), t, os.path.basename(fp))
        return cnt
    except: return 0

# ═══════════════════════════════════════════════════════════
#  ERROR FIXERS
# ═══════════════════════════════════════════════════════════
def register_error(uid, fname, fpath, err):
    global error_counter
    error_counter += 1
    eid = str(error_counter)
    error_store[eid] = {'uid': int(uid), 'fname': fname, 'fpath': fpath, 'error': err, 'attempts': 0}
    return eid

def auto_fix_error(fpath, err):
    fixes = []
    try:
        if os.path.isdir(fpath): return False, "📁 ZIP — manual fix"
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f: orig = f.read()
    except Exception as e: return False, f"Cannot read: {e}"
    src = orig; is_py = fpath.endswith('.py')

    if 'UnicodeEncodeError' in err or 'charmap' in err:
        if 'sys.stdout.reconfigure' not in src:
            patch = ("import sys as _sys\n"
                     "try:\n"
                     "    _sys.stdout.reconfigure(encoding='utf-8')\n"
                     "    _sys.stderr.reconfigure(encoding='utf-8')\n"
                     "except Exception: pass\n")
            src = patch + src
            fixes.append("🔧 UTF-8 console fix")

    m = re.search(r"No module named ['\"]([\w\.\-]+)['\"]", err)
    if m:
        mod = m.group(1).split('.')[0]
        if install_python_module(mod): fixes.append(f"📦 Installed: `{mod}`")
        else: return False, f"❌ Cannot install `{mod}`"
    m = re.search(r"Cannot find module ['\"]([\w@/\.\-]+)['\"]", err)
    if m and not is_py:
        if install_node_module(m.group(1)): fixes.append(f"📦 Installed: `{m.group(1)}`")
    if 'TabError' in err or 'inconsistent use of tabs' in err:
        if '\t' in src: src = src.replace('\t', '    '); fixes.append("🔧 Tabs fixed")
    if 'IndentationError' in err or 'unexpected indent' in err:
        m = re.search(r'line (\d+)', err)
        if m:
            ln = int(m.group(1)) - 1; ls = src.split('\n')
            if 0 <= ln < len(ls):
                fl = ls[ln].lstrip()
                if ls[ln] != fl: ls[ln] = fl; src = '\n'.join(ls); fixes.append(f"🔧 Line {ln+1}")
    m = re.search(r"No such file or directory: ['\"]([^'\"]+)['\"]", err)
    if m:
        miss = m.group(1)
        if not os.path.isabs(miss):
            full = os.path.join(os.path.dirname(fpath), miss)
            try:
                os.makedirs(os.path.dirname(full), exist_ok=True)
                open(full, 'w').close(); fixes.append(f"📄 Created: `{miss}`")
            except: pass
    if "Missing parentheses in call to 'print'" in err:
        pat = re.compile(r'^(\s*)print\s+([^\(\n].*)$', re.MULTILINE)
        if pat.search(src): src = pat.sub(r'\1print(\2)', src); fixes.append("🔧 print()")
    if src != orig:
        try:
            with open(fpath + '.bak', 'w', encoding='utf-8') as f: f.write(orig)
            with open(fpath, 'w', encoding='utf-8') as f: f.write(src)
            fixes.append("💾 Backup")
        except Exception as e: return False, f"Write failed: {e}"
    return (True, "\n".join(fixes)) if fixes else (False, "❌ No auto-fix")

def run_user_file(fpath, uid, fname):
    ext = os.path.splitext(fname)[1].lower(); is_py = ext == '.py'
    max_try = 3; att = 0
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    while att < max_try:
        att += 1
        cmd = [sys.executable, fpath] if is_py else ['node', fpath]
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True, encoding='utf-8', errors='replace', env=env)
            running_processes[fpath] = proc; time.sleep(4)
            if proc.poll() is not None:
                _, stderr = proc.communicate()
                stderr = stderr or "Unknown error"
                miss = detect_missing_module(stderr, is_py)
                if miss and att < max_try:
                    bot.send_message(uid, f"⚡ ꜰɪxɪɴɢ `{miss}` ({att}/{max_try})...")
                    ok = install_python_module(miss) if is_py else install_node_module(miss)
                    if ok:
                        bot.send_message(uid, f"✅ `{miss}` ɪɴꜱᴛᴀʟʟᴇᴅ")
                        continue
                    break
                eid = register_error(uid, fname, fpath, stderr)
                mk = types.InlineKeyboardMarkup()
                mk.add(btn("💀 ꜰɪx ᴇʀʀᴏʀ", callback_data=f"fix_{eid}", style="primary"))
                safe_stderr = html.escape(stderr[:2000])
                safe_fname  = html.escape(str(fname))
                safe_credit = html.escape(CREDIT_NAME)
                try:
                    bot.send_message(uid,
                        sigma_header("ʀᴜɴᴛɪᴍᴇ ᴇʀʀᴏʀ", SKULL, "ᴄʀᴀꜱʜ ᴅᴇᴛᴇᴄᴛᴇᴅ") + "\n\n"
                        f"📄 <code>{safe_fname}</code>\n\n"
                        f"<pre>{safe_stderr}</pre>\n\n"
                        f"🗿 <i>{safe_credit} ᴡɪʟʟ ꜰɪx ɪᴛ</i>",
                        reply_markup=mk, parse_mode="HTML")
                except Exception as _e:
                    try: bot.send_message(uid, f"💀 ᴇʀʀᴏʀ ʀᴇɴᴅᴇʀɪɴɢ ᴛʀᴀᴄᴇʙᴀᴄᴋ: {str(_e)[:200]}")
                    except: pass
                if fpath in running_processes: del running_processes[fpath]
                return False
            return True
        except Exception as e:
            try: bot.send_message(uid, f"❌ {e}")
            except: pass
            return False
    if fpath in running_processes: del running_processes[fpath]
    return False

def deep_fix_file(fp):
    log = []; tot = 0
    try:
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f: src = f.read()
    except Exception as e: return False, f"❌ {e}", 0
    is_py = fp.endswith('.py'); orig = src
    if '\t' in src: src = src.replace('\t','    '); log.append("🔧 Tabs"); tot += 1
    ls = src.split('\n'); cl = [l.rstrip() for l in ls]
    if cl != ls: src = '\n'.join(cl); log.append("🧹 Whitespace"); tot += 1
    pat = re.compile(r'^(\s*)print\s+([^\(\n].*)$', re.MULTILINE)
    if pat.search(src): src = pat.sub(r'\1print(\2)', src); log.append("🔧 print()"); tot += 1
    if is_py:
        std = {'os','sys','time','json','re','math','random','datetime','asyncio','threading','subprocess','pathlib','typing','collections','itertools','functools','io','base64','hashlib','uuid','shutil','logging','traceback','socket','ssl','urllib','http','html','xml','csv','sqlite3','zipfile','platform','py_compile','telebot','psutil'}
        libs = set(re.findall(r'^\s*(?:import|from)\s+([\w\.]+)', src, re.MULTILINE))
        ins = []
        for lib in libs:
            top = lib.split('.')[0]
            if top in std: continue
            try: __import__(top)
            except ImportError:
                if install_python_module(top): ins.append(top)
        if ins: log.append(f"📦 {', '.join(ins)}"); tot += len(ins)
    for ob, cb in [('(',')'),('[',']'),('{','}')]:
        o, c = src.count(ob), src.count(cb)
        if 0 < (o-c) <= 3: src = src.rstrip() + cb*(o-c); log.append(f"🔧 Closed"); tot += 1
    try:
        with open(fp,'w',encoding='utf-8') as f: f.write(src)
    except Exception as e: return False, f"❌ {e}", tot
    if is_py:
        try:
            r = subprocess.run([sys.executable,'-m','py_compile',fp], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
            if r.returncode == 0: log.append("✅ Syntax OK")
            else: log.append(f"⚠️ {r.stderr[:250]}")
        except: pass
    return True, "\n".join(log) if log else "ℹ️ No fixes", tot

def fix_host_syntax():
    hf = os.path.abspath(__file__); log = []
    try: py_compile.compile(hf, doraise=True); return True, "✅ ꜱʏɴᴛᴀx ᴏᴋ", 0
    except py_compile.PyCompileError as e: log.append(f"⚠️ {str(e)[:300]}")
    try:
        with open(hf,'r',encoding='utf-8') as f: src = f.read()
    except Exception as e: return False, f"❌ {e}", 0
    orig = src; fx = 0
    if '\t' in src: src = src.replace('\t','    '); log.append("🔧 Tabs"); fx += 1
    for ob, cb in [('(',')'),('[',']'),('{','}')]:
        o, c = src.count(ob), src.count(cb)
        if 0 < (o-c) <= 3: src = src.rstrip() + cb*(o-c); log.append(f"🔧 Closed"); fx += 1
    if src != orig:
        try:
            with open(hf+'.bak','w',encoding='utf-8') as f: f.write(orig)
            with open(hf,'w',encoding='utf-8') as f: f.write(src)
        except Exception as e: return False, f"❌ {e}", fx
    try:
        py_compile.compile(hf, doraise=True); log.append("✅ Syntax OK"); return True, "\n".join(log), fx
    except py_compile.PyCompileError as e: log.append(f"❌ {str(e)[:200]}"); return False, "\n".join(log), fx

def fix_host_all():
    hf = os.path.abspath(__file__); log = []; tot = 0
    try:
        with open(hf,'r',encoding='utf-8') as f: src = f.read()
    except Exception as e: return False, f"❌ {e}", 0
    orig = src
    std = {'os','sys','time','json','re','math','random','datetime','asyncio','threading','subprocess','pathlib','typing','collections','itertools','functools','io','base64','hashlib','uuid','shutil','logging','traceback','socket','ssl','urllib','http','html','xml','csv','sqlite3','zipfile','platform','py_compile','psutil','telebot'}
    libs = set(re.findall(r'^\s*(?:import|from)\s+([\w\.]+)', src, re.MULTILINE))
    ins = []
    for lib in libs:
        top = lib.split('.')[0]
        if top in std: continue
        try: __import__(top)
        except ImportError:
            if install_python_module(top): ins.append(top)
    if ins: log.append(f"📦 {', '.join(ins)}"); tot += len(ins)
    if '\t' in src: src = src.replace('\t','    '); log.append("🔧 Tabs"); tot += 1
    for ob, cb in [('(',')'),('[',']'),('{','}')]:
        o, c = src.count(ob), src.count(cb)
        if 0 < (o-c) <= 3: src = src.rstrip() + cb*(o-c); log.append(f"🔧 Closed"); tot += 1
    if src != orig:
        try:
            with open(hf+'.bak','w',encoding='utf-8') as f: f.write(orig)
            with open(hf,'w',encoding='utf-8') as f: f.write(src)
        except Exception as e: return False, f"❌ {e}", tot
    try: py_compile.compile(hf, doraise=True); log.append("✅ Syntax OK")
    except py_compile.PyCompileError as e: log.append(f"⚠️ {str(e)[:200]}")
    if not log: log.append("ℹ️ Nothing to fix")
    return True, "\n".join(log), tot

def restart_host_bot():
    try:
        for fp, proc in list(running_processes.items()):
            try: proc.terminate()
            except: pass
        running_processes.clear()
        subprocess.Popen([sys.executable]+sys.argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        time.sleep(1); os._exit(0)
    except Exception as e:
        try: bot.send_message(OWNER_ID, f"❌ {e}")
        except: pass

# ═══════════════════════════════════════════════════════════
#  WELCOME TEXT
# ═══════════════════════════════════════════════════════════
def get_welcome_text(message):
    u = message.from_user
    plan_key = get_user_plan(u.id)
    plan = PLANS.get(plan_key, PLANS['free'])
    status = "🟢 ᴀᴄᴛɪᴠᴇ" if not settings.get('maintenance') else "🔴 ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ"
    files = get_user_file_count(u.id)
    maxf = plan['max_files'] if plan['max_files']<9999 else '∞'
    host_tag = "⚡ ɢᴜᴀʀᴀɴᴛᴇᴇᴅ ²⁴/⁷" if plan.get('guaranteed') else "💀 ꜰʀᴇᴇ ᴛɪᴇʀ"

    return (
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n"
        "    🗿 Anjasha Hosting Bot 🗿\n"
        "    🥶 ꜱɪɢᴍᴀ ᴄʟᴏᴜᴅ ʜᴏꜱᴛɪɴɢ ꜱᴇʀᴠɪᴄᴇ\n"
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n\n"
        "╭──────────────────────────╮\n"
        f"│  💀 *ᴜꜱᴇʀ* ➜  {u.first_name[:15].upper()}\n"
        f"│  ⚡ *ɪᴅ*   ➜  `{u.id}`\n"
        f"│  💎 *ᴘʟᴀɴ* ➜  {plan['name']}\n"
        f"│  🎯 *ꜱʟᴏᴛꜱ* ➜  {files}/{maxf}\n"
        f"│  🔥 *ꜱᴛᴀᴛᴜꜱ* ➜  {status}\n"
        f"│  🥶 *ʜᴏꜱᴛ*  ➜  {host_tag}\n"
        "╰──────────────────────────╯\n\n"
        "┏━〔 ⚡ ᴘᴏᴡᴇʀꜰᴜʟ ꜰᴇᴀᴛᴜʀᴇꜱ 〕━┓\n"
        "┃ 🗿 ᴅᴇᴘʟᴏʏ .ᴘʏ • .ᴊꜱ • .ᴢɪᴘ\n"
        "┃ 💀 ᴀᴜᴛᴏ ᴍᴏᴅᴜʟᴇ ꜰɪx\n"
        "┃ 🥶 ᴀᴜᴛᴏ ᴇʀʀᴏʀ ʀᴇᴘᴀɪʀ\n"
        "┃ 🎯 ᴘʀᴇᴍɪᴜᴍ ²⁴/⁷ ʜᴏꜱᴛɪɴɢ\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"{sigma_quote('ᴄʜᴏᴏꜱᴇ ᴛᴏ ᴅᴏᴍɪɴᴀᴛᴇ')}\n"
        f"☟ ☟ ☟"
    )

# ═══════════════════════════════════════════════════════════
#  KEYBOARDS
# ═══════════════════════════════════════════════════════════
def main_keyboard(user_id):
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(btn("📢 ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=get_channel_url(), style="primary"),
           btn("👨‍💻 ꜱᴜᴘᴘᴏʀᴛ", url=get_support_url(), style="success"))
    mk.add(btn("🚀 ᴅᴇᴘʟᴏʏ ꜰɪʟᴇ", callback_data="usr_deploy", style="success"),
           btn("📂 ᴍʏ ꜰɪʟᴇꜱ", callback_data="usr_myfiles", style="primary"))
    mk.add(btn("⚡ ꜱᴛᴀᴛꜱ", callback_data="usr_stats", style="primary"),
           btn("🥶 ꜱᴘᴇᴇᴅ", callback_data="usr_speed", style="success"))
    mk.add(btn("💀 ʜᴇʟᴘ", callback_data="usr_help", style="primary"),
           btn("🎯 ꜱᴇʀᴠᴇʀ", callback_data="usr_serverinfo", style="primary"))
    mk.add(btn("💎 ᴘʀᴇᴍɪᴜᴍ ᴢᴏɴᴇ", callback_data="usr_show_plans", style="success"))
    mk.add(btn("📞 ꜱᴜᴘᴘᴏʀᴛ", url=get_support_url(), style="primary"))
    if is_admin(user_id):
        mk.add(btn("👑 ᴏᴡɴᴇʀ ᴘᴀɴᴇʟ", callback_data="adm_page_main", style="danger"))
    return mk

def admin_keyboard(user_id=None):
    mk = types.InlineKeyboardMarkup(row_width=2)
    mt = "🔴 ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴏɴ" if settings['maintenance'] else "🟢 ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴏꜰꜰ"
    ms = "danger" if settings['maintenance'] else "success"
    at = "✅ ᴀᴜᴛᴏᴀᴘᴘʀᴏᴠᴇ ᴏɴ" if settings.get('auto_approval',True) else "⛔ ᴀᴜᴛᴏᴀᴘᴘʀᴏᴠᴇ ᴏꜰꜰ"
    as_ = "success" if settings.get('auto_approval',True) else "danger"
    mk.add(btn(mt, callback_data="adm_toggle_maint", style=ms), btn(at, callback_data="adm_toggle_autoapproval", style=as_))
    us = "✅" if settings.get('upi_id') else "⚠️"; qs = "✅" if settings.get('upi_qr') else "❌"
    mk.add(btn(f"{us} ᴜᴘɪ", callback_data="adm_set_upi", style="primary"),
           btn(f"{qs} Qʀ", callback_data="adm_set_qr", style="success"))
    mk.add(btn("👁 ᴘᴀʏᴍᴇɴᴛ", callback_data="adm_view_payment", style="primary"),
           btn("🗑 ʀᴍ Qʀ", callback_data="adm_del_qr", style="danger"))
    cs = "✅" if settings.get('channel_url') else "⚠️"
    mk.add(btn(f"{cs} ᴄʜᴀɴɴᴇʟ", callback_data="adm_set_channel", style="primary"),
           btn("🔧 ꜱᴜᴘᴘᴏʀᴛ", callback_data="adm_set_support", style="success"))
    mk.add(btn("👁 ᴠɪᴇᴡ ʟɪɴᴋꜱ", callback_data="adm_view_links", style="primary"),
           btn("🗿 ʙᴏᴛ ʟᴏᴏᴋᴜᴘ", callback_data="adm_lookup_bot", style="success"))
    mk.add(btn("📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ", callback_data="adm_broadcast", style="primary"),
           btn("⚡ ꜱᴛᴀᴛꜱ", callback_data="adm_stats", style="primary"))
    pend = 0
    try:
        cur = get_db().cursor(); cur.execute("SELECT COUNT(*) FROM payments WHERE status='pending'"); pend = cur.fetchone()[0]
    except: pass
    pt = f"💰 ᴘᴀʏᴍᴇɴᴛꜱ ({pend})" if pend else "💰 ᴘᴀʏᴍᴇɴᴛꜱ"
    mk.add(btn(pt, callback_data="adm_payments", style="danger"),
           btn("👥 ꜱᴜʙꜱ", callback_data="adm_subs_list", style="primary"))
    mk.add(btn("🎁 ᴄᴏᴜᴘᴏɴꜱ", callback_data="adm_coupons", style="primary"),
           btn("➕ ɴᴇᴡ ᴄᴏᴜᴘᴏɴ", callback_data="adm_new_coupon", style="success"))
    mk.add(btn("📊 ᴘᴀʏ ꜱᴛᴀᴛꜱ", callback_data="adm_paystats", style="success"))
    fam_lbl = "🟢 ꜰᴀᴍ ᴀᴜᴛᴏ" if FAM_ENABLED else "🔴 ꜰᴀᴍ ᴏꜰꜰ"
    mk.add(btn(fam_lbl, callback_data="adm_toggle_fam", style="primary"))
    mk.add(btn("🎥 ꜱᴇᴛ ᴠɪᴅᴇᴏ", callback_data="adm_set_video", style="primary"),
           btn("🔧 ꜰɪx ꜰɪʟᴇꜱ", callback_data="adm_fixfile", style="success"))
    if settings.get('welcome_video'): mk.add(btn("❌ ʀᴍ ᴠɪᴅᴇᴏ", callback_data="adm_del_video", style="danger"))
    if user_id is None or is_owner(user_id):
        mk.add(btn("➕ ᴀᴅᴅ ᴀᴅᴍɪɴ", callback_data="adm_add_admin", style="success"),
               btn("➖ ʀᴍ ᴀᴅᴍɪɴ", callback_data="adm_remove_admin", style="danger"))
    mk.add(btn("👥 ᴀᴅᴍɪɴ ʟɪꜱᴛ", callback_data="adm_list_admins", style="primary"))
    mk.add(btn("🔎 ꜱᴇᴀʀᴄʜ ᴜꜱᴇʀ", callback_data="adm_search_user", style="primary"),
           btn("📜 ʟᴏɢꜱ", callback_data="adm_logs", style="primary"))
    mk.add(btn("📤 ᴇxᴘᴏʀᴛ ᴅʙ", callback_data="adm_export_sql", style="success"),
           btn("📥 ɪᴍᴘᴏʀᴛ ᴅʙ", callback_data="adm_import_sql", style="primary"))
    mk.add(btn("📂 ꜰɪʟᴇ ᴄᴛʀʟ ➡️", callback_data="adm_page_files", style="primary"))
    mk.add(btn("🔧 ꜰɪx ᴄᴛʀʟ", callback_data="adm_fixmenu", style="success"))
    return mk

def admin_files_keyboard():
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(btn("📂 ᴀʟʟ ꜰɪʟᴇꜱ", callback_data="adm_all_files", style="primary"),
           btn("🔍 ᴄʜᴇᴄᴋ", callback_data="adm_check_whole", style="primary"))
    mk.add(btn("▶️ ʀᴜɴ ᴀʟʟ", callback_data="adm_run_all", style="success"),
           btn("⏸ ꜱᴛᴏᴘ ᴀʟʟ", callback_data="adm_stop_all", style="danger"))
    mk.add(btn("🎯 ꜱᴛᴏᴘ ᴏɴᴇ", callback_data="adm_stop_specific", style="danger"))
    mk.add(btn("🔄 ʀᴇꜰʀᴇꜱʜ", callback_data="adm_refresh_files", style="primary"))
    mk.add(btn("⬅️ ʙᴀᴄᴋ", callback_data="adm_page_main", style="primary"))
    return mk

def fix_menu_keyboard():
    mk = types.InlineKeyboardMarkup(row_width=1)
    mk.add(btn("🔧 ꜰɪx ꜱʏɴᴛᴀx", callback_data="fix_syntax", style="primary"))
    mk.add(btn("💀 ꜰɪx ᴀʟʟ", callback_data="fix_allerrors", style="danger"))
    mk.add(btn("🔄 ʀᴇꜱᴛᴀʀᴛ ʜᴏꜱᴛ", callback_data="fix_restart", style="success"))
    mk.add(btn("⬅️ ʙᴀᴄᴋ", callback_data="adm_page_main", style="primary"))
    return mk

def plans_keyboard():
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(btn("⭐ ʙᴀꜱɪᴄ ᴍᴏ", callback_data="plan_buy_basic_m", style="primary"),
           btn("⭐ ʙᴀꜱɪᴄ ʏʀ", callback_data="plan_buy_basic_y", style="primary"))
    mk.add(btn("💎 ᴘʀᴏ ᴍᴏ", callback_data="plan_buy_pro_m", style="success"),
           btn("💎 ᴘʀᴏ ʏʀ", callback_data="plan_buy_pro_y", style="success"))
    mk.add(btn("👑 ᴘʀᴇᴍ ᴍᴏ", callback_data="plan_buy_premium_m", style="danger"),
           btn("👑 ᴘʀᴇᴍ ʏʀ", callback_data="plan_buy_premium_y", style="danger"))
    mk.add(btn("👤 ᴍʏ ꜱᴜʙ", callback_data="usr_mysub", style="primary"))
    mk.add(btn("⬅️ ʙᴀᴄᴋ", callback_data="usr_back", style="primary"))
    return mk

def owner_keyboard():
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(btn("🟢 ꜱᴛᴀᴛᴜꜱ", callback_data="own_status", style="success"),
           btn("📊 ꜱᴛᴀᴛꜱ", callback_data="own_stats", style="primary"))
    mk.add(btn("📂 ꜰɪʟᴇꜱ", callback_data="adm_all_files", style="primary"),
           btn("🔄 ʀᴜɴ ᴀʟʟ", callback_data="adm_run_all", style="success"))
    mk.add(btn("⏸ ꜱᴛᴏᴘ ᴀʟʟ", callback_data="adm_stop_all", style="danger"),
           btn("🧹 ᴄʟᴇᴀɴ", callback_data="own_clean", style="primary"))
    mk.add(btn("👥 ᴜꜱᴇʀꜱ", callback_data="own_users", style="primary"),
           btn("💰 ᴘᴀʏᴍᴇɴᴛꜱ", callback_data="adm_payments", style="success"))
    mk.add(btn("🗿 ʙᴏᴛ ʟᴏᴏᴋᴜᴘ", callback_data="adm_lookup_bot", style="success"))
    mk.add(btn("📜 ʟᴏɢꜱ", callback_data="adm_logs", style="primary"),
           btn("📢 ʙʀᴏᴀᴅᴄᴀꜱᴛ", callback_data="adm_broadcast", style="primary"))
    mk.add(btn("📤 ᴇxᴘᴏʀᴛ", callback_data="adm_export_sql", style="success"),
           btn("📥 ɪᴍᴘᴏʀᴛ", callback_data="adm_import_sql", style="primary"))
    mk.add(btn("👑 ꜰᴜʟʟ ᴀᴅᴍɪɴ", callback_data="adm_page_main", style="primary"))
    mk.add(btn("💀 ꜱᴛᴏᴘ ʜᴏꜱᴛ", callback_data="own_stop_host", style="danger"))
    mk.add(btn("☠️ ᴅᴇʟᴇᴛᴇ ᴀʟʟ", callback_data="own_delete_all", style="danger"))
    return mk

# ═══════════════════════════════════════════════════════════
#  OWNER COMMAND
# ═══════════════════════════════════════════════════════════
@bot.message_handler(commands=['owner', 'Owner', 'OWNER'])
def owner_cmd(message):
    uid = message.from_user.id
    if is_admin(uid): return _send_owner_panel(message.chat.id, uid)
    if uid in VERIFIED_USERS: return _send_owner_panel(message.chat.id, uid)
    PASSWORD_ATTEMPTS[uid] = 0
    msg = bot.send_message(message.chat.id,
        sigma_header("ᴘᴀꜱꜱᴡᴏʀᴅ ɴᴇᴇᴅᴇᴅ", "🔐", "ᴘʀɪᴠᴀᴛᴇ ᴢᴏɴᴇ ᴅᴇᴛᴇᴄᴛᴇᴅ") + "\n\n"
        f"🗿 ᴘᴀꜱꜱᴡᴏʀᴅ ʙʜᴇᴊᴏ\n"
        f"💀 ᴄᴀɴᴄᴇʟ ➜ /cancel\n"
        f"☠️ ᴡʀᴏɴɢ × 3 = ʙʟᴏᴄᴋᴇᴅ",
        parse_mode="Markdown")
    bot.register_next_step_handler(msg, _owner_password_check)

def _owner_password_check(message):
    uid = message.from_user.id
    text = (message.text or "").strip()
    if text == "/cancel":
        try: return bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ")
        except: return
    if text == _get_owner_password():
        VERIFIED_USERS.add(uid); PASSWORD_ATTEMPTS.pop(uid, None)
        try: bot.delete_message(message.chat.id, message.message_id)
        except: pass
        bot.send_message(message.chat.id,
            sigma_header("ᴀᴄᴄᴇꜱꜱ ɢʀᴀɴᴛᴇᴅ", ROCK, "ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ ᴋɪɴɢ 👑"),
            parse_mode="Markdown")
        return _send_owner_panel(message.chat.id, uid)
    PASSWORD_ATTEMPTS[uid] = PASSWORD_ATTEMPTS.get(uid, 0) + 1
    att = PASSWORD_ATTEMPTS[uid]
    try: bot.delete_message(message.chat.id, message.message_id)
    except: pass
    if att >= 3:
        bot.send_message(message.chat.id, f"{SKULL} 3 ᴡʀᴏɴɢ ᴀᴛᴛᴇᴍᴘᴛꜱ\n🔒 ʙʟᴏᴄᴋᴇᴅ")
        try: bot.send_message(OWNER_ID, f"⚠️ ꜱᴜꜱᴘɪᴄɪᴏᴜꜱ\n👤 {message.from_user.first_name}\n🆔 `{uid}`", parse_mode="Markdown")
        except: pass
        return
    msg = bot.send_message(message.chat.id, f"💀 ᴡʀᴏɴɢ\n⚙️ {att}/3")
    bot.register_next_step_handler(msg, _owner_password_check)

@bot.message_handler(commands=['cancel'])
def cancel_cmd(message):
    try: bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ")
    except: pass

def _send_owner_panel(chat_id, uid):
    name = users_db.get(str(uid), {}).get('name', 'User')
    flag = "👑 ᴋɪɴɢ" if uid == OWNER_ID else "🔐 ᴠᴇʀɪꜰɪᴇᴅ"
    tf = sum(len(u.get('files', [])) for u in users_db.values())
    bot.send_message(chat_id,
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n"
        "    👑 𝗢𝗪𝗡𝗘𝗥 𝗣𝗔𝗡𝗘𝗟 🗿\n"
        "    🥶 ꜱɪɢᴍᴀ ᴄᴏɴᴛʀᴏʟ ʀᴏᴏᴍ\n"
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n\n"
        "╭──────────────────────────╮\n"
        f"│  💀 ɴᴀᴍᴇ ➜ {name}\n"
        f"│  ⚡ ɪᴅ   ➜ `{uid}`\n"
        f"│  👑 ʀᴏʟᴇ ➜ {flag}\n"
        "╰──────────────────────────╯\n\n"
        "┏━〔 📊 ʟɪᴠᴇ ꜱᴛᴀᴛꜱ 〕━┓\n"
        f"┃ 👥 ᴜꜱᴇʀꜱ ➜ *{len(users_db)}*\n"
        f"┃ 🎯 ʀᴜɴɴɪɴɢ ➜ *{len(running_processes)}*\n"
        f"┃ 📂 ꜰɪʟᴇꜱ ➜ *{tf}*\n"
        "┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"{sigma_quote('ᴡɪᴛʜ ɢʀᴇᴀᴛ ᴘᴏᴡᴇʀ ᴄᴏᴍᴇꜱ ɢʀᴇᴀᴛ ʀᴇꜱᴘᴏɴꜱɪʙɪʟɪᴛʏ')}",
        reply_markup=owner_keyboard(), parse_mode="Markdown")

# ═══════════════════════════════════════════════════════════
#  COMMANDS
# ═══════════════════════════════════════════════════════════
@bot.message_handler(commands=['start'])
def start(message):
    uid = str(message.from_user.id)
    if settings['maintenance'] and message.from_user.id != OWNER_ID:
        try:
            return bot.send_message(message.chat.id,
                "┏━━━━━━━━━━━━━━━━━━━━━━━┓\n"
                "  🔴  ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ\n"
                "  ᴡᴇ'ʟʟ ʙᴇ ʙᴀᴄᴋ ꜱᴏᴏɴ\n"
                "┗━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                f"💌 <code>{html.escape(get_support_url() or '')}</code>",
                parse_mode="HTML")
        except: return
    if uid not in users_db:
        users_db[uid] = {'files': [], 'name': message.from_user.first_name}
    else:
        users_db[uid]['name'] = message.from_user.first_name
    save_db()
    caption = get_welcome_text(message)
    video = settings.get('welcome_video')
    kb = main_keyboard(message.from_user.id)
    if video:
        try: bot.send_video(message.chat.id, video, caption=caption, reply_markup=kb, parse_mode="Markdown")
        except: bot.send_message(message.chat.id, caption, reply_markup=kb, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, caption, reply_markup=kb, parse_mode="Markdown")

@bot.message_handler(commands=['admin', 'panel'])
def show_admin_panel(message):
    if not is_admin(message.from_user.id): return bot.send_message(message.chat.id, "🚫 ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ")
    bot.send_message(message.chat.id,
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n"
        "    👑 𝗔𝗗𝗠𝗜𝗡 𝗖𝗢𝗡𝗧𝗥𝗢𝗟 🗿\n"
        "    🥶 ꜱɪɢᴍᴀ ᴅᴀꜱʜʙᴏᴀʀᴅ\n"
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄",
        reply_markup=admin_keyboard(message.from_user.id), parse_mode="Markdown")

@bot.message_handler(commands=['plans'])
def show_plans(message):
    uid = str(message.from_user.id)
    pk = get_user_plan(uid); plan = PLANS[pk]
    mx = plan['max_files'] if plan['max_files']<9999 else '∞'
    text = (
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n"
        "    💎 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗭𝗢𝗡𝗘 💎\n"
        "    🗿 ᴜɴʟᴏᴄᴋ ᴘʀᴇᴍɪᴜᴍ ᴘᴏᴡᴇʀ 🥶\n"
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n\n"
        "╭── ❖ ᴄᴜʀʀᴇɴᴛ ᴛɪᴇʀ ❖ ──╮\n"
        f"│ 🎯 ᴘʟᴀɴ ➜ {plan['name']}\n"
        f"│ 📂 ᴜꜱᴇᴅ ➜ {get_user_file_count(uid)}/{mx}\n"
        "╰───────────────────────╯\n\n"
        "┏━〔 🆓 ꜰʀᴇᴇ ᴛɪᴇʀ 〕━┓\n"
        "┃ 💀 4 ꜰɪʟᴇꜱ ᴏɴʟʏ\n"
        "┃ 🥶 ɴᴏɴ-ɢᴜᴀʀᴀɴᴛᴇᴇᴅ ʜᴏꜱᴛɪɴɢ\n"
        "┗━━━━━━━━━━━━━━━━━━━┛\n\n"
        "┏━〔 ⭐ ʙᴀꜱɪᴄ ᴛɪᴇʀ 〕━┓\n"
        "┃ 💎 8 ꜰɪʟᴇꜱ\n"
        "┃ ⚡ ɢᴜᴀʀᴀɴᴛᴇᴇᴅ ²⁴/⁷\n"
        "┃ 💰 ₹49/ᴍᴏ | ₹499/ʏʀ\n"
        "┗━━━━━━━━━━━━━━━━━━━┛\n\n"
        "┏━〔 💎 ᴘʀᴏ ᴛɪᴇʀ 〕━┓\n"
        "┃ 🎯 25 ꜰɪʟᴇꜱ\n"
        "┃ 🔥 ᴘʀɪᴏʀɪᴛʏ ʜᴏꜱᴛɪɴɢ\n"
        "┃ 💰 ₹99/ᴍᴏ | ₹999/ʏʀ\n"
        "┗━━━━━━━━━━━━━━━━━━━┛\n\n"
        "┏━〔 👑 ᴘʀᴇᴍɪᴜᴍ ᴛɪᴇʀ 〕━┓\n"
        "┃ 🗿 ᴜɴʟɪᴍɪᴛᴇᴅ ꜰɪʟᴇꜱ\n"
        "┃ 🥶 ᴠɪᴘ ʟᴇᴠᴇʟ ʜᴏꜱᴛɪɴɢ\n"
        "┃ 💰 ₹199/ᴍᴏ | ₹1999/ʏʀ\n"
        "┗━━━━━━━━━━━━━━━━━━━┛"
    )
    bot.send_message(message.chat.id, text, reply_markup=plans_keyboard(), parse_mode="Markdown")

@bot.message_handler(commands=['mysub'])
def my_subscription(message):
    uid = str(message.from_user.id)
    pk = get_user_plan(uid); plan = PLANS[pk]
    st = "—"; exp = "—"
    try:
        cur = get_db().cursor()
        cur.execute("SELECT started_at, expires_at FROM subscriptions WHERE user_id=?", (uid,))
        r = cur.fetchone()
        if r: st = r['started_at'] or "—"; exp = r['expires_at'] or "—"
    except: pass
    mx = plan['max_files'] if plan['max_files']<9999 else '∞'
    host = "⚡ ɢᴜᴀʀᴀɴᴛᴇᴇᴅ" if plan.get('guaranteed') else "💀 ꜰʀᴇᴇ"
    bot.send_message(message.chat.id,
        sigma_header("ᴍʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ", DIAMOND, f"{plan['name']}") + "\n\n"
        f"📅 ꜱᴛᴀʀᴛ ➜ `{st}`\n⏳ ᴇxᴘɪʀᴇ ➜ `{exp}`\n"
        f"📂 ꜰɪʟᴇꜱ ➜ {get_user_file_count(uid)}/{mx}\n"
        f"🎯 ʜᴏꜱᴛ ➜ {host}",
        parse_mode="Markdown")

# ═══════════════════════════════════════════════════════════
#  FILE / USER / BOT HANDLERS
# ═══════════════════════════════════════════════════════════
def start_deployment_cb(call):
    msg = bot.send_message(call.message.chat.id,
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n"
        "    🚀 𝗗𝗘𝗣𝗟𝗢𝗬 𝗭𝗢𝗡𝗘 🗿\n"
        "    🥶 ꜱᴇɴᴅ ᴜꜱ ʏᴏᴜʀ ꜰɪʟᴇ\n"
        "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n\n"
        "┏━〔 📂 ꜱᴜᴘᴘᴏʀᴛᴇᴅ ꜰɪʟᴇꜱ 〕━┓\n"
        "┃ ⚡ `.ᴘʏ`  ➜ ᴘʏᴛʜᴏɴ ʙᴏᴛ\n"
        "┃ 🗿 `.ᴊꜱ`  ➜ ɴᴏᴅᴇ ʙᴏᴛ\n"
        "┃ 💀 `.ᴢɪᴘ` ➜ ᴢɪᴘ ᴘᴀᴄᴋᴀɢᴇ\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"{sigma_quote('ᴅᴇᴘʟᴏʏ ᴀɴᴅ ᴅᴏᴍɪɴᴀᴛᴇ')}",
        parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_upload)

def show_my_files_cb(call):
    uid = str(call.from_user.id)
    files = users_db.get(uid, {}).get('files', [])
    plan = get_plan_data(uid)
    mx = plan['max_files'] if plan['max_files']<9999 else '∞'
    if not files:
        mk = types.InlineKeyboardMarkup()
        mk.add(btn("🚀 ᴅᴇᴘʟᴏʏ ɴᴏᴡ", callback_data="usr_deploy", style="success"),
               btn("⬅️ ʙᴀᴄᴋ", callback_data="usr_back", style="primary"))
        return bot.send_message(call.message.chat.id,
            sigma_header("ɴᴏ ꜰɪʟᴇꜱ ʏᴇᴛ", SKULL, f"ꜱʟᴏᴛꜱ: 0/{mx}") + "\n\n"
            f"{sigma_quote('ꜱᴛᴀʀᴛ ᴅᴇᴘʟᴏʏɪɴɢ ɴᴏᴡ')}",
            reply_markup=mk, parse_mode="Markdown")
    bot.send_message(call.message.chat.id,
        sigma_header(f"ʏᴏᴜʀ ꜰɪʟᴇꜱ ({len(files)}/{mx})", "📂", "ᴍᴀɴᴀɢᴇ ʏᴏᴜʀ ʙᴏᴛꜱ"),
        parse_mode="Markdown")
    for f_name in files:
        fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{uid}_{f_name}"))
        running = fp in running_processes and running_processes[fp].poll() is None
        st = "🟢 ᴀᴄᴛɪᴠᴇ" if running else "🔴 ꜱᴛᴏᴘᴘᴇᴅ"
        try:
            if os.path.isfile(fp): size = f"{os.path.getsize(fp)//1024} ᴋʙ"
            elif os.path.isdir(fp):
                ts = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(fp) for f in fs)
                size = f"{ts//1024} ᴋʙ"
            else: size = "—"
        except: size = "—"

        mk = types.InlineKeyboardMarkup(row_width=2)
        mk.add(btn("▶️ ʀᴜɴ", callback_data=f"run_{f_name}_{uid}", style="success"),
               btn("⏸ ꜱᴛᴏᴘ", callback_data=f"stop_{f_name}_{uid}", style="danger"))
        mk.add(btn("🔄 ʀᴇꜱᴛᴀʀᴛ", callback_data=f"restart_{f_name}_{uid}", style="primary"),
               btn("⚡ ꜱᴘᴇᴇᴅ", callback_data=f"speed_{f_name}_{uid}", style="success"))
        mk.add(btn("📥 ᴅᴏᴡɴʟᴏᴀᴅ", callback_data=f"down_{f_name}_{uid}", style="primary"),
               btn("🗑 ᴅᴇʟᴇᴛᴇ", callback_data=f"del_{f_name}_{uid}", style="danger"))

        bot.send_message(call.message.chat.id,
            "╭───────────────────────────╮\n"
            f"│  📄 `{_md_safe(f_name)}`\n"
            f"│  📶 {st}  •  📦 {size}\n"
            "╰───────────────────────────╯",
            reply_markup=mk, parse_mode="Markdown")

    nav = types.InlineKeyboardMarkup()
    nav.add(btn("🚀 ᴅᴇᴘʟᴏʏ", callback_data="usr_deploy", style="success"),
            btn("⬅️ ʙᴀᴄᴋ", callback_data="usr_back", style="primary"))
    bot.send_message(call.message.chat.id, "🗿", reply_markup=nav)

def show_stats_cb(call):
    try:
        upl = len([u for u in users_db if len(users_db[u].get('files',[]))>0])
        mk = types.InlineKeyboardMarkup().add(btn("⬅️ ʙᴀᴄᴋ", callback_data="usr_back", style="primary"))
        bot.send_message(call.message.chat.id,
            sigma_header("ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ", "📊", "ꜱɪɢᴍᴀ ɴᴇᴛᴡᴏʀᴋ") + "\n\n"
            f"👥 ᴜꜱᴇʀꜱ ➜ *{len(users_db)}*\n"
            f"📤 ᴜᴘʟᴏᴀᴅᴇʀꜱ ➜ *{upl}*\n"
            f"🎯 ʀᴜɴɴɪɴɢ ➜ *{len(running_processes)}*\n\n"
            f"{sigma_quote('ɴᴜᴍʙᴇʀꜱ ᴅᴏɴᴛ ʟɪᴇ')}",
            reply_markup=mk, parse_mode="Markdown")
    except: pass

def show_speed_cb(call):
    try:
        uid = str(call.from_user.id)
        files = users_db.get(uid, {}).get('files', [])
        run = sum(1 for f in files if os.path.normpath(os.path.join(DEPLOY_DIR,f"{uid}_{f}")) in running_processes
                  and running_processes[os.path.normpath(os.path.join(DEPLOY_DIR,f"{uid}_{f}"))].poll() is None)
        cpu = safe_cpu_percent(interval=0.3); rp, ru, rt = safe_ram()
        t0 = time.time()
        try: bot.get_me(); ping = int((time.time()-t0)*1000)
        except: ping = -1
        rt_str = "🟢 ʙʟᴀᴢɪɴɢ" if ping<100 else "🟡 ꜰᴀꜱᴛ" if ping<300 else "🟠 ɴᴏʀᴍᴀʟ" if ping<700 else "🔴 ꜱʟᴏᴡ"
        mk = types.InlineKeyboardMarkup()
        mk.add(btn("🔄 ʀᴇᴛᴇꜱᴛ", callback_data="usr_speed", style="success"),
               btn("⬅️ ʙᴀᴄᴋ", callback_data="usr_back", style="primary"))
        bot.send_message(call.message.chat.id,
            sigma_header("ꜱᴘᴇᴇᴅ ᴛᴇꜱᴛ", "🥶", "ʟᴏᴡ ʟᴀᴛᴇɴᴄʏ ᴢᴏɴᴇ") + "\n\n"
            f"🏓 ᴘɪɴɢ ➜ *{ping}ᴍꜱ* {rt_str}\n"
            f"⚙️ ᴄᴘᴜ ➜ *{cpu}%*\n"
            f"🧠 ʀᴀᴍ ➜ *{rp}%* ({ru}/{rt}ᴍʙ)\n\n"
            f"🎯 ᴀᴄᴛɪᴠᴇ ➜ *{run}/{len(files)}*",
            reply_markup=mk, parse_mode="Markdown")
    except: pass

def show_help_cb(call):
    mk = types.InlineKeyboardMarkup()
    mk.add(btn("🚀 ᴅᴇᴘʟᴏʏ", callback_data="usr_deploy", style="success"),
           btn("⬅️ ʙᴀᴄᴋ", callback_data="usr_back", style="primary"))
    support_url = get_support_url() or ""
    text = (
        "┏━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "  💀  ʜᴇʟᴘ ᴄᴇɴᴛʀᴇ\n"
        "  ʀᴇᴀᴅ ᴛʜɪꜱ\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "┏━〔 🚀 ᴅᴇᴘʟᴏʏ 〕━┓\n"
        "┃ ⚡ <code>.ᴘʏ .ᴊꜱ .ᴢɪᴘ</code> ꜱᴇɴᴅ ᴋᴀʀᴏ\n"
        "┃ 💀 ᴀᴜᴛᴏ ᴍᴏᴅᴜʟᴇ ɪɴꜱᴛᴀʟʟ ✅\n"
        "┗━━━━━━━━━━━━━━━━┛\n\n"
        "┏━〔 📂 ᴍʏ ꜰɪʟᴇꜱ 〕━┓\n"
        "┃ 🎯 ʀᴜɴ • ꜱᴛᴏᴘ • ʀᴇꜱᴛᴀʀᴛ\n"
        "┃ 🥶 ᴅᴏᴡɴʟᴏᴀᴅ • ᴅᴇʟᴇᴛᴇ\n"
        "┗━━━━━━━━━━━━━━━━━┛\n\n"
        "┏━〔 🔧 ᴇʀʀᴏʀ 〕━┓\n"
        "┃ 🗿 ᴀᴜᴛᴏ-ꜰɪx ᴀᴠᴀɪʟᴀʙʟᴇ\n"
        "┗━━━━━━━━━━━━━━┛\n\n"
        f"📞 ꜱᴜᴘᴘᴏʀᴛ ➜ <code>{html.escape(support_url)}</code>"
    )
    bot.send_message(call.message.chat.id, text, reply_markup=mk, parse_mode="HTML")

def show_server_info_cb(call):
    try:
        cpu = safe_cpu_percent(interval=0.3); rp, ru, rt = safe_ram()
        dp, du, dt = safe_disk(); cc = safe_cpu_count()
        bt = time.time() - safe_boot_time(); h, m = int(bt//3600), int((bt%3600)//60)
        bu = int(time.time() - BOT_START_TIME); bh, bm = bu//3600, (bu%3600)//60
        mk = types.InlineKeyboardMarkup()
        mk.add(btn("🔄 ʀᴇꜰʀᴇꜱʜ", callback_data="usr_serverinfo", style="success"),
               btn("⬅️ ʙᴀᴄᴋ", callback_data="usr_back", style="primary"))
        bot.send_message(call.message.chat.id,
            sigma_header("ꜱᴇʀᴠᴇʀ ɪɴꜰᴏ", "🎯", "ꜱʏꜱᴛᴇᴍ ᴍᴏɴɪᴛᴏʀ") + "\n\n"
            "┏━〔 🖥 ꜱʏꜱᴛᴇᴍ 〕━┓\n"
            f"┃ 💻 ᴏꜱ ➜ `{platform.system()} {platform.release()}`\n"
            f"┃ 🐍 ᴘʏ ➜ `{platform.python_version()}`\n"
            f"┃ 🗿 ᴄᴘᴜ ➜ *{cpu}%* ({cc} ᴄᴏʀᴇꜱ)\n"
            f"┃ 🥶 ʀᴀᴍ ➜ *{rp}%*\n"
            f"┃ 💾 ᴅɪꜱᴋ ➜ *{dp}%*\n"
            "┗━━━━━━━━━━━━━━━━━┛\n\n"
            "┏━〔 ⏱ ᴜᴘᴛɪᴍᴇ 〕━┓\n"
            f"┃ 🖥 ꜱᴇʀᴠᴇʀ ➜ *{h}ʜ {m}ᴍ*\n"
            f"┃ 🤖 ʙᴏᴛ ➜ *{bh}ʜ {bm}ᴍ*\n"
            f"┃ 🎯 ʀᴜɴɴɪɴɢ ➜ *{len(running_processes)}*\n"
            "┗━━━━━━━━━━━━━━━━━┛",
            reply_markup=mk, parse_mode="Markdown")
    except: pass

# ═══════════════════════════════════════════════════════════
#  DEPLOY
# ═══════════════════════════════════════════════════════════
def process_upload(message):
    if not message.document: return
    uid = str(message.from_user.id)
    if not can_user_upload(uid):
        plan = get_plan_data(uid)
        mx = plan['max_files'] if plan['max_files']<9999 else '∞'
        return bot.send_message(message.chat.id,
            sigma_header("ꜰɪʟᴇ ʟɪᴍɪᴛ ʀᴇᴀᴄʜᴇᴅ", SKULL, f"{plan['name']}") + "\n\n"
            f"📂 ᴜꜱᴇᴅ ➜ {get_user_file_count(uid)}/{mx}\n\n"
            f"{sigma_quote('ᴜᴘɢʀᴀᴅᴇ ꜰᴏʀ ᴜɴʟɪᴍɪᴛᴇᴅ ᴘᴏᴡᴇʀ')}",
            reply_markup=types.InlineKeyboardMarkup().add(
                btn("💎 ᴜᴘɢʀᴀᴅᴇ", callback_data="usr_show_plans", style="success")),
            parse_mode="Markdown")

    f_name = message.document.file_name
    f_path = os.path.normpath(os.path.join(DEPLOY_DIR, f"{uid}_{f_name}"))
    prog = bot.send_message(message.chat.id, "⚡ ᴅᴇᴘʟᴏʏɪɴɢ...")
    try:
        f_info = bot.get_file(message.document.file_id)
        content = bot.download_file(f_info.file_path)
        with open(f_path, 'wb') as f: f.write(content)

        if not settings.get('auto_approval', True):
            if f_name not in users_db[uid]['files']: users_db[uid]['files'].append(f_name)
            save_db()
            safe_edit(message.chat.id, prog.message_id,
                sigma_header("ᴀᴡᴀɪᴛɪɴɢ ᴀᴘᴘʀᴏᴠᴀʟ", "⏳", f_name))
            try: size = os.path.getsize(f_path)
            except: size = 0
            log_deployment(int(uid), f_name, "pending", size)
            for a in get_all_admin_ids():
                try:
                    mk = types.InlineKeyboardMarkup(row_width=2)
                    mk.add(btn("✅ ᴀᴘᴘʀᴏᴠᴇ", callback_data=f"run_{f_name}_{uid}", style="success"),
                           btn("🗑 ʀᴇᴊᴇᴄᴛ", callback_data=f"del_{f_name}_{uid}", style="danger"))
                    mk.add(btn("📥 ᴅᴏᴡɴʟᴏᴀᴅ", callback_data=f"down_{f_name}_{uid}", style="primary"))
                    bot.send_message(a,
                        sigma_header("ɴᴇᴡ ᴜᴘʟᴏᴀᴅ", "🔔", "ᴘᴇɴᴅɪɴɢ ᴀᴘᴘʀᴏᴠᴀʟ") + "\n\n"
                        f"👤 `{uid}` ({users_db.get(uid,{}).get('name','—')})\n📄 `{_md_safe(f_name)}`\n📦 `{size//1024} ᴋʙ`",
                        reply_markup=mk, parse_mode="Markdown")
                    if os.path.isfile(f_path):
                        try:
                            with open(f_path, 'rb') as f: bot.send_document(a, f, visible_file_name=f_name)
                        except: pass
                except: pass
            return

        if f_name.endswith('.zip'):
            ed = os.path.join(DEPLOY_DIR, f"{uid}_{f_name.replace('.zip','')}")
            try:
                with zipfile.ZipFile(f_path, 'r') as z: z.extractall(ed)
                os.remove(f_path); f_path = ed
            except Exception as e:
                return safe_edit(message.chat.id, prog.message_id, f"❌ ZIP: {e}")
            entry = None
            for root, _, files in os.walk(ed):
                for fn in files:
                    if fn in ('main.py','app.py','bot.py','index.js','main.js','app.js'):
                        entry = os.path.join(root,fn); break
                if entry: break
            if not entry:
                for root, _, files in os.walk(ed):
                    for fn in files:
                        if fn.endswith(('.py','.js')): entry = os.path.join(root,fn); break
                    if entry: break
            if entry: f_path = entry; f_name = os.path.basename(entry)
            req = os.path.join(ed, 'requirements.txt')
            if os.path.exists(req):
                safe_edit(message.chat.id, prog.message_id, "⚡ ɪɴꜱᴛᴀʟʟɪɴɢ ʀᴇǫᴜɪʀᴇᴍᴇɴᴛꜱ...")
                subprocess.run([sys.executable,'-m','pip','install','-r',req,'--no-cache-dir'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        safe_edit(message.chat.id, prog.message_id, "🗿 ᴀᴅᴅɪɴɢ ᴄʀᴇᴅɪᴛ...")
        if os.path.isdir(f_path):
            for root, _, fs in os.walk(f_path):
                for fn in fs:
                    if fn.endswith(('.py','.js')):
                        fp = os.path.join(root, fn)
                        inject_credit_to_file(fp); apply_credit_to_bot(fp, message.from_user.id)
        else:
            inject_credit_to_file(f_path); apply_credit_to_bot(f_path, message.from_user.id)

        ok = run_user_file(f_path, int(uid), f_name)
        if ok:
            if f_name not in users_db[uid]['files']: users_db[uid]['files'].append(f_name)
            save_db()
            plan = get_plan_data(uid)
            host_note = "⚡ ɢᴜᴀʀᴀɴᴛᴇᴇᴅ ²⁴/⁷" if plan.get('guaranteed') else "💀 ꜰʀᴇᴇ ᴛɪᴇʀ (ɴᴏɴ-ɢᴜᴀʀᴀɴᴛᴇᴇᴅ)"
            safe_edit(message.chat.id, prog.message_id,
                sigma_header("ᴅᴇᴘʟᴏʏ ꜱᴜᴄᴄᴇꜱꜱ", "🚀", "ʙᴏᴛ ɪꜱ ʟɪᴠᴇ! 🗿") + "\n\n"
                f"📄 `{_md_safe(f_name)}`\n🎯 ᴘʟᴀɴ ➜ {plan['name']}\n{host_note}\n\n"
                f"{sigma_quote('ʟᴇᴛ ɪᴛ ʀɪᴅᴇ')}")
        else:
            safe_edit(message.chat.id, prog.message_id,
                sigma_header("ᴅᴇᴘʟᴏʏ ꜰᴀɪʟᴇᴅ", SKULL, "ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴏᴅᴇ"))
        try: size = os.path.getsize(f_path) if os.path.isfile(f_path) else 0
        except: size = 0
        log_deployment(int(uid), f_name, "success" if ok else "failed", size)
    except Exception as e:
        try: bot.send_message(message.chat.id, f"❌ ᴇʀʀᴏʀ: {e}")
        except: pass

# ═══════════════════════════════════════════════════════════
#  ADMIN HELPERS
# ═══════════════════════════════════════════════════════════
def broadcast_logic(message):
    count = 0
    for u in users_db:
        try:
            bot.send_message(int(u),
                sigma_header("ᴀɴɴᴏᴜɴᴄᴇᴍᴇɴᴛ", "📢", "ꜰʀᴏᴍ ᴛʜᴇ ᴛᴏᴘ 🗿") + f"\n\n{message.text}\n\n◆ {CREDIT_NAME}")
            count += 1
        except: pass
    bot.send_message(message.chat.id, f"✅ ꜱᴇɴᴛ ᴛᴏ *{count}* ᴜꜱᴇʀꜱ", parse_mode="Markdown")

def save_video_logic(message):
    if message.video:
        settings['welcome_video'] = message.video.file_id; save_settings()
        bot.send_message(message.chat.id, "✅ ᴠɪᴅᴇᴏ ꜱᴇᴛ 🗿")
    else: bot.send_message(message.chat.id, "❌ ɴᴏᴛ ᴀ ᴠɪᴅᴇᴏ")

def _admin_stop_specific(message):
    try:
        p = message.text.strip().split()
        if len(p) < 2: return bot.send_message(message.chat.id, "❌ `uid filename`", parse_mode="Markdown")
        tu, fn = p[0], "_".join(p[1:])
        fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{tu}_{fn}"))
        if fp in running_processes:
            running_processes[fp].terminate(); del running_processes[fp]
            bot.send_message(message.chat.id, f"⏸ ꜱᴛᴏᴘᴘᴇᴅ `{_md_safe(fn)}`", parse_mode="Markdown")
        else: bot.send_message(message.chat.id, "⚠️ ɴᴏᴛ ʀᴜɴɴɪɴɢ")
    except Exception as e:
        try: bot.send_message(message.chat.id, f"❌ {e}")
        except: pass

def _admin_search_user(message):
    q = message.text.strip(); res = []
    if q.isdigit():
        if q in users_db: res.append((q, users_db[q]))
    else:
        for uid, d in users_db.items():
            if q.lower() in d.get('name','').lower(): res.append((uid, d))
    if not res: return bot.send_message(message.chat.id, f"❌ ɴᴏᴛ ꜰᴏᴜɴᴅ `{_md_safe(q)}`", parse_mode="Markdown")
    for uid, d in res[:15]:
        files = d.get('files', [])
        run = sum(1 for f in files if os.path.normpath(os.path.join(DEPLOY_DIR,f"{uid}_{f}")) in running_processes
                  and running_processes[os.path.normpath(os.path.join(DEPLOY_DIR,f"{uid}_{f}"))].poll() is None)
        mk = types.InlineKeyboardMarkup(row_width=2)
        mk.add(btn("📂 ꜰɪʟᴇꜱ", callback_data=f"adm_userfiles_{uid}", style="primary"),
               btn("🗑 ᴅᴇʟ", callback_data=f"adm_deluser_{uid}", style="danger"))
        bot.send_message(message.chat.id,
            f"╭── ❖ 𝗨𝗦𝗘𝗥 ❖ ──╮\n"
            f"│ 👤 {d.get('name','—')}\n│ 🆔 `{uid}`\n│ 📂 {len(files)}\n│ 🟢 {run} ʀᴜɴɴɪɴɢ\n"
            "╰────────────────╯",
            reply_markup=mk, parse_mode="Markdown")

def _admin_add_admin(message):
    if not is_owner(message.from_user.id): return
    try: new_id = int(message.text.strip())
    except: return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ ɪᴅ")
    if new_id == OWNER_ID: return bot.send_message(message.chat.id, "❌ ᴏᴡɴᴇʀ ᴀʟʀᴇᴀᴅʏ")
    adm = settings.get('admins', [])
    if str(new_id) in [str(a) for a in adm]: return bot.send_message(message.chat.id, "⚠️ ᴀʟʀᴇᴀᴅʏ ᴀᴅᴍɪɴ")
    adm.append(new_id); settings['admins'] = adm; save_settings()
    bot.send_message(message.chat.id, f"✅ ᴀᴅᴍɪɴ ᴀᴅᴅᴇᴅ: `{new_id}` 👑", parse_mode="Markdown")

def _admin_bot_lookup(message):
    if not is_admin(message.from_user.id): return
    q = message.text.strip().lower().replace("@", "")
    if not q: return bot.send_message(message.chat.id, "❌ ᴜꜱᴇʀɴᴀᴍᴇ ʙʜᴇᴊᴏ")
    row = lookup_hosted_bot(q)
    if not row:
        return bot.send_message(message.chat.id,
            f"💀 <b>ʙᴏᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ</b>\n\n<code>{html.escape('@'+q)}</code>",
            parse_mode="HTML")

    uid = row['user_id']
    user_name = row['user_name'] or users_db.get(str(uid), {}).get('name', '—')
    plan_key = get_user_plan(uid)
    plan = PLANS.get(plan_key, PLANS['free'])
    fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{uid}_{row['file_name']}"))
    is_running = fp in running_processes and running_processes[fp].poll() is None
    st_icon = "🟢 ᴀᴄᴛɪᴠᴇ" if is_running else "🔴 ꜱᴛᴏᴘᴘᴇᴅ"

    try:
        if os.path.isfile(fp): size = f"{os.path.getsize(fp)//1024} ᴋʙ"
        elif os.path.isdir(fp):
            ts = sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(fp) for f in fs)
            size = f"{ts//1024} ᴋʙ"
        else: size = "—"
    except: size = "—"

    deploy_count = 0
    try:
        cur = get_db().cursor()
        cur.execute("SELECT COUNT(*) FROM deployments WHERE user_id=?", (uid,))
        deploy_count = cur.fetchone()[0] or 0
    except: pass

    text = (
        sigma_header("ʙᴏᴛ ʟᴏᴏᴋᴜᴘ", "🗿", "ꜰᴜʟʟ ᴅᴇᴛᴀɪʟꜱ") + "\n\n"
        "┏━〔 🤖 ʙᴏᴛ ɪɴꜰᴏ 〕━┓\n"
        f"┃ 🆔 @{q}\n"
        f"┃ 📄 `{_md_safe(row['file_name'])}`\n"
        f"┃ 📊 {st_icon}\n"
        f"┃ 📦 {size}\n"
        "┗━━━━━━━━━━━━━━━━━━━┛\n\n"
        "┏━〔 👤 ᴏᴡɴᴇʀ 〕━┓\n"
        f"┃ 💀 {user_name}\n"
        f"┃ ⚡ `{uid}`\n"
        f"┃ 💎 {plan['name']}\n"
        "┗━━━━━━━━━━━━━━━┛\n\n"
        "┏━〔 📊 ꜱᴛᴀᴛꜱ 〕━┓\n"
        f"┃ 📤 ᴅᴇᴘʟᴏʏꜱ ➜ {deploy_count}\n"
        f"┃ 📅 `{row['deployed_at']}`\n"
        "┗━━━━━━━━━━━━━━━┛"
    )

    mk = types.InlineKeyboardMarkup(row_width=2)
    safe_f = row['file_name'].replace(' ', '_')
    mk.add(btn("▶️ ʀᴜɴ", callback_data=f"run_{safe_f}_{uid}", style="success"),
           btn("⏸ ꜱᴛᴏᴘ", callback_data=f"stop_{safe_f}_{uid}", style="danger"))
    mk.add(btn("🔄 ʀᴇꜱᴛᴀʀᴛ", callback_data=f"restart_{safe_f}_{uid}", style="primary"),
           btn("⚡ ꜱᴘᴇᴇᴅ", callback_data=f"speed_{safe_f}_{uid}", style="success"))
    mk.add(btn("📥 ᴅᴏᴡɴʟᴏᴀᴅ", callback_data=f"down_{safe_f}_{uid}", style="primary"),
           btn("🗑 ᴅᴇʟᴇᴛᴇ", callback_data=f"del_{safe_f}_{uid}", style="danger"))
    mk.add(btn("👤 ᴜꜱᴇʀ ᴅᴇᴛᴀɪʟꜱ", callback_data=f"adm_userfiles_{uid}", style="primary"))

    bot.send_message(message.chat.id, text, reply_markup=mk, parse_mode="Markdown")

def _admin_set_upi_step1(message):
    if not is_admin(message.from_user.id): return
    t = message.text.strip()
    if not t or "@" not in t or len(t) > 60: return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ")
    settings['upi_id'] = t; save_settings()
    msg = bot.send_message(message.chat.id, "✅ ꜱᴀᴠᴇᴅ\n📝 ɴᴀᴍᴇ ʙʜᴇᴊᴏ:\n⏭ `/skip`")
    bot.register_next_step_handler(msg, _admin_set_upi_step2)

def _admin_set_upi_step2(message):
    if not is_admin(message.from_user.id): return
    t = message.text.strip()
    if not t.startswith("/skip") and len(t) <= 40:
        settings['upi_name'] = t; save_settings()
    bot.send_message(message.chat.id, "✅ ᴜᴘɪ ꜱᴇᴛ 🗿",
                     reply_markup=types.InlineKeyboardMarkup().add(btn("✅ ᴅᴏɴᴇ", callback_data="adm_page_main", style="primary")))

def _admin_set_qr_step1(message):
    if not is_admin(message.from_user.id): return
    if not message.photo: return bot.send_message(message.chat.id, "❌ ᴘʜᴏᴛᴏ ɴᴀʜɪ")
    settings['upi_qr'] = message.photo[-1].file_id; save_settings()
    bot.send_message(message.chat.id, "✅ Qʀ ꜱᴇᴛ 🗿",
                     reply_markup=types.InlineKeyboardMarkup().add(btn("✅ ᴅᴏɴᴇ", callback_data="adm_page_main", style="primary")))

def _admin_set_channel_step1(message):
    if not is_admin(message.from_user.id): return
    url = message.text.strip()
    if url.startswith("@"): url = f"https://t.me/{url[1:]}"
    if not url.startswith(("https://t.me/", "http://t.me/")): return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ")
    settings['channel_url'] = url; save_settings()
    msg = bot.send_message(message.chat.id, "✅ ʟɪɴᴋ ꜱᴀᴠᴇᴅ\n📝 ɴᴀᴍᴇ:\n⏭ `/skip`")
    bot.register_next_step_handler(msg, _admin_set_channel_step2)

def _admin_set_channel_step2(message):
    if not is_admin(message.from_user.id): return
    t = message.text.strip()
    if not t.startswith("/skip") and len(t) <= 60:
        settings['channel_name'] = t; save_settings()
    bot.send_message(message.chat.id, "✅ ᴄʜᴀɴɴᴇʟ ꜱᴇᴛ",
                     reply_markup=types.InlineKeyboardMarkup().add(btn("✅ ᴅᴏɴᴇ", callback_data="adm_page_main", style="primary")))

def _admin_set_support_step1(message):
    if not is_admin(message.from_user.id): return
    url = message.text.strip()
    if url.startswith("@"): url = f"https://t.me/{url[1:]}"
    if not url.startswith(("https://t.me/", "http://t.me/")): return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ")
    settings['support_url'] = url
    settings['support_handle'] = "@" + url.rstrip("/").split("/")[-1].replace("@", "")
    save_settings()
    bot.send_message(message.chat.id, f"✅ ꜱᴜᴘᴘᴏʀᴛ ꜱᴇᴛ 🗿\n{settings['support_handle']}",
                     reply_markup=types.InlineKeyboardMarkup().add(btn("✅ ᴅᴏɴᴇ", callback_data="adm_page_main", style="primary")))

def _admin_fixfile_handler(message):
    if not is_admin(message.from_user.id): return
    if not message.document: return bot.send_message(message.chat.id, "❌ ꜰɪʟᴇ ɴᴀʜɪ")
    fn = message.document.file_name
    wd = os.path.join(DEPLOY_DIR, "_admin_fix"); os.makedirs(wd, exist_ok=True)
    sp = os.path.join(wd, fn)
    prog = bot.send_message(message.chat.id, "⏳ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
    try:
        fi = bot.get_file(message.document.file_id)
        with open(sp, 'wb') as f: f.write(bot.download_file(fi.file_path))
    except Exception as e: return safe_edit(message.chat.id, prog.message_id, f"❌ {e}")
    safe_edit(message.chat.id, prog.message_id, "🔍 ꜱᴄᴀɴ..."); time.sleep(1)
    ok, log, cnt = deep_fix_file(sp)
    base, ext = os.path.splitext(fn); fxd = f"Fixed_{base}{ext}"
    cap = (sigma_header("ꜰɪxᴇᴅ", "🗿", f"{cnt} ꜰɪxᴇꜱ") + "\n\n"
           f"📄 <code>{html.escape(fxd)}</code>\n\n"
           f"<pre>{html.escape(log[:1200])}</pre>")
    with open(sp,'rb') as f:
        try:
            bot.send_document(message.chat.id, f, visible_file_name=fxd, caption=cap, parse_mode="HTML")
        except Exception:
            bot.send_document(message.chat.id, f, visible_file_name=fxd)
    try: os.remove(sp)
    except: pass
    safe_edit(message.chat.id, prog.message_id, "✅ ᴅᴏɴᴇ 🗿")

def _admin_import_sql(message):
    if not is_admin(message.from_user.id): return
    if not message.document: return bot.send_message(message.chat.id, "❌ .sql ɴᴀʜɪ")
    prog = bot.send_message(message.chat.id, "⏳ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...")
    try:
        fi = bot.get_file(message.document.file_id)
        content = bot.download_file(fi.file_path).decode('utf-8', errors='ignore')
    except Exception as e: return safe_edit(message.chat.id, prog.message_id, f"❌ {e}")
    safe_edit(message.chat.id, prog.message_id, "⚙️ ɪᴍᴘᴏʀᴛɪɴɢ...")
    try:
        ts = time.strftime("%Y%m%d_%H%M%S"); bp = f"anjasha_backup_{ts}.db"
        shutil.copy(DB_FILE, bp)
        with open(bp,'rb') as f:
            bot.send_document(message.chat.id, f, visible_file_name=bp, caption="💾 ʙᴀᴄᴋᴜᴘ")
    except: pass
    ok, err = import_db_sql(content)
    if ok: safe_edit(message.chat.id, prog.message_id, f"✅ ɪᴍᴘᴏʀᴛᴇᴅ ({len(users_db)} ᴜꜱᴇʀꜱ)")
    else: safe_edit(message.chat.id, prog.message_id, f"❌ {err[:300]}")

def _payment_screenshot_handler(message, pk):
    if not message.photo and not message.document: return bot.send_message(message.chat.id, "❌ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ɴᴀʜɪ")
    fid = message.photo[-1].file_id if message.photo else message.document.file_id
    plan = PLANS[pk]; uid = str(message.from_user.id)
    name = users_db.get(uid, {}).get('name', 'User')
    coupon = None; disc = 0
    if hasattr(bot, '_tmp_coupons') and uid in bot._tmp_coupons:
        c = bot._tmp_coupons[uid]
        if c['plan'] == pk: coupon = c['code']; disc = c['discount']
    final = plan['price'] - disc
    try:
        cur = get_db().cursor()
        cur.execute("INSERT INTO payments (user_id, user_name, plan, amount, screenshot_id, status) VALUES (?,?,?,?,?,'pending')",
                    (uid, name, pk, final, fid))
        get_db().commit(); pid = cur.lastrowid
    except Exception as e:
        try: return bot.send_message(message.chat.id, f"❌ {e}")
        except: return
    if coupon: use_coupon(coupon, uid)
    if hasattr(bot, '_tmp_coupons') and uid in bot._tmp_coupons: del bot._tmp_coupons[uid]
    bot.send_message(message.chat.id,
        sigma_header("ᴘᴀʏᴍᴇɴᴛ ꜱᴇɴᴛ", "✅", f"ᴘᴀʏ ɪᴅ #{pid}") + f"\n\n"
        f"🎯 {plan['name']}\n💰 ₹{final}\n\n⏳ ᴀᴅᴍɪɴ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ɪɴ ᴘʀᴏɢʀᴇꜱꜱ",
        parse_mode="Markdown")
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(btn("✅ ᴀᴘᴘʀᴏᴠᴇ", callback_data=f"pay_appr_{pid}", style="success"),
           btn("❌ ʀᴇᴊᴇᴄᴛ", callback_data=f"pay_rej_{pid}", style="danger"))
    for a in get_all_admin_ids():
        try:
            bot.send_photo(a, fid,
                caption=sigma_header("ɴᴇᴡ ᴘᴀʏᴍᴇɴᴛ", "💰", f"ᴘᴀʏ #{pid}") + f"\n\n"
                f"👤 {name} (`{uid}`)\n🎯 {plan['name']}\n💰 ₹{final}",
                reply_markup=mk, parse_mode="Markdown")
        except: pass

# ═══════════════════════════════════════════════════════════
#  BACKGROUND WORKERS
# ═══════════════════════════════════════════════════════════
def free_tier_random_stuck_worker():
    while True:
        try:
            time.sleep(1800)
            for fp, proc in list(running_processes.items()):
                if proc.poll() is not None: continue
                base = os.path.basename(fp)
                if "_" not in base: continue
                uid = base.split("_")[0]
                if not uid.isdigit(): continue
                plan = get_plan_data(uid)
                if plan.get('guaranteed'): continue
                if random.random() < 0.25:
                    try: proc.terminate()
                    except: pass
                    running_processes.pop(fp, None)
                    file_stuck_tracker[uid] = file_stuck_tracker.get(uid, 0) + 1
                    try:
                        bot.send_message(int(uid),
                            sigma_header("ꜰʀᴇᴇ ᴛɪᴇʀ ʟɪᴍɪᴛ", "💀", "ʙᴏᴛ ꜱᴛᴏᴘᴘᴇᴅ ʀᴀɴᴅᴏᴍʟʏ") + "\n\n"
                            "🥶 ꜰʀᴇᴇ ᴜꜱᴇʀꜱ ᴋᴇ ʟɪʏᴇ ɴᴏɴ-ɢᴜᴀʀᴀɴᴛᴇᴇᴅ ʜᴏꜱᴛɪɴɢ ʜᴀɪ\n\n"
                            f"{sigma_quote('ᴜᴘɢʀᴀᴅᴇ ꜰᴏʀ ⚡ ɢᴜᴀʀᴀɴᴛᴇᴇᴅ ²⁴/⁷')}",
                            reply_markup=types.InlineKeyboardMarkup().add(
                                btn("💎 ᴜᴘɢʀᴀᴅᴇ", callback_data="usr_show_plans", style="success")),
                            parse_mode="Markdown")
                    except: pass
        except Exception as e: print(f"[stuck] {e}")

def subscription_reminder_worker():
    while True:
        try:
            time.sleep(3600)
            cur = get_db().cursor()
            cur.execute("SELECT user_id, plan, expires_at FROM subscriptions WHERE plan != 'free' AND status='active' AND expires_at IS NOT NULL")
            for r in cur.fetchall():
                try:
                    exp = datetime.strptime(r['expires_at'], "%Y-%m-%d %H:%M:%S")
                    diff = exp - datetime.now(); d_left = diff.days
                    if d_left in [7, 3, 1]:
                        try:
                            bot.send_message(int(r['user_id']),
                                sigma_header("ᴇxᴘɪʀʏ ᴀʟᴇʀᴛ", "⏰", f"{d_left} ᴅᴀʏꜱ ʟᴇꜰᴛ") + "\n\n"
                                f"{sigma_quote('ʀᴇɴᴇᴡ ɴᴏᴡ ᴛᴏ ꜱᴛᴀʏ ᴏɴʟɪɴᴇ')}",
                                reply_markup=types.InlineKeyboardMarkup().add(
                                    btn("💎 ʀᴇɴᴇᴡ", callback_data="usr_show_plans", style="success")),
                                parse_mode="Markdown")
                        except: pass
                except: pass
        except Exception as e: print(f"[reminder] {e}")

def subscription_expiry_worker():
    while True:
        try:
            time.sleep(1800)
            conn = get_db(); cur = conn.cursor()
            cur.execute("SELECT user_id, plan FROM subscriptions WHERE plan != 'free' AND status='active' AND expires_at < CURRENT_TIMESTAMP")
            for r in cur.fetchall():
                cur.execute("UPDATE subscriptions SET plan='free', status='expired' WHERE user_id=?", (r['user_id'],))
                conn.commit()
                for f in users_db.get(r['user_id'], {}).get('files', []):
                    fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{r['user_id']}_{f}"))
                    if fp in running_processes:
                        try: running_processes[fp].terminate()
                        except: pass
                        running_processes.pop(fp, None)
                try:
                    bot.send_message(int(r['user_id']),
                        sigma_header("ᴘʟᴀɴ ᴇxᴘɪʀᴇᴅ", "💀", "ᴛɪᴍᴇ ɪꜱ ᴜᴘ") + "\n\n"
                        f"{sigma_quote('ʀᴇɴᴇᴡ ꜰᴏʀ ᴜɴʟɪᴍɪᴛᴇᴅ ᴘᴏᴡᴇʀ')}",
                        reply_markup=types.InlineKeyboardMarkup().add(btn("💎 ʀᴇɴᴇᴡ", callback_data="usr_show_plans", style="success")),
                        parse_mode="Markdown")
                except: pass
        except Exception as e: print(f"[expiry] {e}")

# ═══════════════════════════════════════════════════════════
#  CALLBACK HANDLER
# ═══════════════════════════════════════════════════════════
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global FAM_ENABLED
    uid = str(call.from_user.id)
    data = call.data

    if data == "noop":
        try: bot.answer_callback_query(call.id)
        except: pass
        return

    # USER
    if data == "usr_deploy":
        try: bot.answer_callback_query(call.id)
        except: pass
        return start_deployment_cb(call)
    if data == "usr_myfiles":
        try: bot.answer_callback_query(call.id)
        except: pass
        return show_my_files_cb(call)
    if data == "usr_stats":
        try: bot.answer_callback_query(call.id)
        except: pass
        return show_stats_cb(call)
    if data == "usr_speed":
        try: bot.answer_callback_query(call.id)
        except: pass
        return show_speed_cb(call)
    if data == "usr_help":
        try: bot.answer_callback_query(call.id)
        except: pass
        return show_help_cb(call)
    if data == "usr_serverinfo":
        try: bot.answer_callback_query(call.id)
        except: pass
        return show_server_info_cb(call)
    if data == "usr_back":
        try: bot.answer_callback_query(call.id)
        except: pass
        return send_welcome(call.message.chat.id, call.from_user.id)
    if data == "usr_show_plans":
        try: bot.answer_callback_query(call.id)
        except: pass
        return show_plans(call.message)
    if data == "usr_mysub":
        try: bot.answer_callback_query(call.id)
        except: pass
        return my_subscription(call.message)

    # AUTO FIX
    if data.startswith("fix_") and not data.startswith(("fix_syntax","fix_allerrors","fix_restart")):
        eid = data.split("_", 1)[1]
        info = error_store.get(eid)
        if not info:
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        if call.from_user.id != info['uid'] and not is_admin(call.from_user.id):
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        info['attempts'] += 1; att = info['attempts']
        if att > 3:
            try: bot.answer_callback_query(call.id, "⚠️ Max 3", show_alert=True)
            except: pass
            return
        try: bot.answer_callback_query(call.id, "🔧")
        except: pass
        fixed, log = auto_fix_error(info['fpath'], info['error'])
        if fixed:
            bot.send_message(call.message.chat.id, sigma_header("ꜰɪxᴇᴅ", "🗿", "ᴀᴜᴛᴏ-ʀᴇᴘᴀɪʀᴇᴅ") + f"\n\n{log}", parse_mode="Markdown")
            run_user_file(info['fpath'], info['uid'], info['fname'])
        else:
            bot.send_message(call.message.chat.id, f"💀 ꜰᴀɪʟᴇᴅ\n`{log[:400]}`", parse_mode="Markdown")
        return

    if data.startswith("show_myfiles_"):
        t_uid = data.split("_", 2)[2]
        files = users_db.get(t_uid, {}).get('files', [])
        if not files:
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        try: bot.answer_callback_query(call.id)
        except: pass
        for f_name in files:
            fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{t_uid}_{f_name}"))
            st = "🟢" if (fp in running_processes and running_processes[fp].poll() is None) else "🔴"
            mk = types.InlineKeyboardMarkup(row_width=2)
            mk.add(btn("▶️", callback_data=f"run_{f_name}_{t_uid}", style="success"),
                   btn("⏸", callback_data=f"stop_{f_name}_{t_uid}", style="danger"),
                   btn("📥", callback_data=f"down_{f_name}_{t_uid}", style="primary"),
                   btn("🗑", callback_data=f"del_{f_name}_{t_uid}", style="danger"))
            bot.send_message(call.message.chat.id, f"📄 `{_md_safe(f_name)}` {st}", reply_markup=mk, parse_mode="Markdown")
        return

    # PER-FILE
    if "_" in data and not data.startswith(("adm_","usr_","fix_","show_myfiles_","plan_","pay_","own_")):
        parts = data.split("_")
        action = parts[0]; f_name = "_".join(parts[1:-1]); t_uid = parts[-1]
        fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{t_uid}_{f_name}"))
        if call.from_user.id != OWNER_ID and str(call.from_user.id) != t_uid and not is_admin(call.from_user.id):
            try: bot.answer_callback_query(call.id, "🚫")
            except: pass
            return
        if action == "run":
            ok = run_user_file(fp, int(t_uid), f_name)
            try: bot.answer_callback_query(call.id, "▶️" if ok else "❌")
            except: pass
            return
        if action == "stop":
            if fp in running_processes:
                try: running_processes[fp].terminate()
                except: pass
                del running_processes[fp]
            try: bot.answer_callback_query(call.id, "⏸")
            except: pass
            return
        if action == "restart":
            if fp in running_processes:
                try: running_processes[fp].terminate()
                except: pass
                del running_processes[fp]
            try: bot.answer_callback_query(call.id, "🔄")
            except: pass
            run_user_file(fp, int(t_uid), f_name); return
        if action == "speed":
            if fp not in running_processes or running_processes[fp].poll() is not None:
                try: bot.answer_callback_query(call.id, "🔴", show_alert=True)
                except: pass
                return
            try:
                cpu, mem, up = safe_proc_stats(running_processes[fp].pid)
                bot.answer_callback_query(call.id, "⚡")
                bot.send_message(call.message.chat.id,
                    f"⚡ `{_md_safe(f_name)}`\n⚙️ ᴄᴘᴜ {cpu}% • 🧠 {mem}ᴍʙ • ⏱ {int(up//3600)}ʜ", parse_mode="Markdown")
            except: pass
            return
        if action == "down":
            if not os.path.exists(fp):
                try: bot.answer_callback_query(call.id, "❌", show_alert=True)
                except: pass
                return
            try: bot.answer_callback_query(call.id, "📥")
            except: pass
            if os.path.isfile(fp):
                with open(fp,'rb') as f: bot.send_document(call.message.chat.id, f, visible_file_name=f_name)
            elif os.path.isdir(fp):
                try:
                    tz = os.path.join(DEPLOY_DIR, f"_dl_{t_uid}_{int(time.time())}.zip")
                    with zipfile.ZipFile(tz, 'w', zipfile.ZIP_DEFLATED) as z:
                        for root, _, files in os.walk(fp):
                            for fn in files:
                                full = os.path.join(root, fn); z.write(full, os.path.relpath(full, fp))
                    with open(tz,'rb') as f: bot.send_document(call.message.chat.id, f, visible_file_name=f"{f_name}.zip")
                    os.remove(tz)
                except: pass
            return
        if action == "del":
            if fp in running_processes:
                try: running_processes[fp].terminate()
                except: pass
                del running_processes[fp]
            if os.path.exists(fp):
                if os.path.isdir(fp): shutil.rmtree(fp, ignore_errors=True)
                else:
                    try: os.remove(fp)
                    except: pass
            if f_name in users_db.get(t_uid,{}).get('files',[]):
                users_db[t_uid]['files'].remove(f_name); save_db()
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            try: bot.answer_callback_query(call.id, "🗑")
            except: pass
            return

    # OWNER SPECIAL
    if data == "own_status":
        try: bot.answer_callback_query(call.id)
        except: pass
        cpu = safe_cpu_percent(); rp, _, _ = safe_ram()
        up = int(time.time() - BOT_START_TIME); h, m = up // 3600, (up % 3600) // 60
        bot.send_message(call.message.chat.id,
            sigma_header("ʟɪᴠᴇ ꜱᴛᴀᴛᴜꜱ", "🟢", "ꜱʏꜱᴛᴇᴍ ᴍᴏɴɪᴛᴏʀ") + "\n\n"
            f"⚡ ᴄᴘᴜ ➜ *{cpu}%*\n🧠 ʀᴀᴍ ➜ *{rp}%*\n"
            f"🤖 ᴜᴘᴛɪᴍᴇ ➜ *{h}ʜ {m}ᴍ*\n🎯 ʀᴜɴɴɪɴɢ ➜ *{len(running_processes)}*",
            parse_mode="Markdown")
        return
    if data == "own_stats":
        try: bot.answer_callback_query(call.id)
        except: pass
        try:
            cur = get_db().cursor()
            cur.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='approved'")
            total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM subscriptions WHERE plan != 'free' AND status='active'")
            paid = cur.fetchone()[0]
        except: total = paid = 0
        bot.send_message(call.message.chat.id,
            sigma_header("ᴏᴡɴᴇʀ ꜱᴛᴀᴛꜱ", "📊", "ꜰᴜʟʟ ʀᴇᴘᴏʀᴛ") + "\n\n"
            f"👥 ᴜꜱᴇʀꜱ ➜ *{len(users_db)}*\n💎 ᴘᴀɪᴅ ➜ *{paid}*\n💰 ʀᴇᴠᴇɴᴜᴇ ➜ *₹{total}*",
            parse_mode="Markdown")
        return
    if data == "own_users":
        try: bot.answer_callback_query(call.id)
        except: pass
        txt = sigma_header(f"ᴜꜱᴇʀꜱ ({len(users_db)})", "👥") + "\n\n"
        for u, ud in list(users_db.items())[:20]:
            plan = get_user_plan(u); pd = PLANS.get(plan, PLANS['free'])
            txt += f"• `{u}` {ud.get('name','—')[:15]} {pd['emoji']}\n"
        bot.send_message(call.message.chat.id, txt[:4000], parse_mode="Markdown")
        return
    if data == "own_clean":
        try: bot.answer_callback_query(call.id)
        except: pass
        try:
            removed = 0
            for root, _, files in os.walk(DEPLOY_DIR):
                for f in files:
                    if f.endswith(('.bak', '.tmp', '.log')):
                        try: os.remove(os.path.join(root, f)); removed += 1
                        except: pass
            bot.send_message(call.message.chat.id, f"🧹 {removed} ꜰɪʟᴇꜱ ʀᴇᴍᴏᴠᴇᴅ")
        except: pass
        return
    if data == "own_stop_host":
        try: bot.answer_callback_query(call.id)
        except: pass
        mk = types.InlineKeyboardMarkup()
        mk.add(btn("✅ ʏᴇꜱ", callback_data="own_stop_confirm", style="danger"),
               btn("❌ ᴄᴀɴᴄᴇʟ", callback_data="own_back", style="primary"))
        bot.send_message(call.message.chat.id,
            sigma_header("ꜱᴛᴏᴘ ʜᴏꜱᴛ?", SKULL, "ᴛʜɪꜱ ᴋɪʟʟꜱ ᴛʜᴇ ʙᴏᴛ") + "\n\n"
            f"{sigma_quote('ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ?')}",
            reply_markup=mk, parse_mode="Markdown")
        return
    if data == "own_stop_confirm":
        try: bot.answer_callback_query(call.id)
        except: pass
        for fp, proc in list(running_processes.items()):
            try: proc.terminate()
            except: pass
        running_processes.clear()
        try: bot.send_message(call.message.chat.id, sigma_header("ꜱᴛᴏᴘᴘᴇᴅ", "💀", "ɢᴏᴏᴅʙʏᴇ 🗿"), parse_mode="Markdown")
        except: pass
        time.sleep(1); os._exit(0); return
    if data == "own_delete_all":
        try: bot.answer_callback_query(call.id)
        except: pass
        mk = types.InlineKeyboardMarkup()
        mk.add(btn("✅ ᴅᴇʟᴇᴛᴇ ᴀʟʟ", callback_data="own_del_confirm", style="danger"),
               btn("❌ ᴄᴀɴᴄᴇʟ", callback_data="own_back", style="primary"))
        bot.send_message(call.message.chat.id,
            sigma_header("ᴅᴇʟᴇᴛᴇ ᴀʟʟ?", "☠️", "ɪʀʀᴇᴠᴇʀꜱɪʙʟᴇ ᴀᴄᴛɪᴏɴ") + "\n\n"
            f"{sigma_quote('ᴛʜᴇʀᴇ ɪꜱ ɴᴏ ɢᴏɪɴɢ ʙᴀᴄᴋ')}",
            reply_markup=mk, parse_mode="Markdown")
        return
    if data == "own_del_confirm":
        try: bot.answer_callback_query(call.id)
        except: pass
        for fp, proc in list(running_processes.items()):
            try: proc.terminate()
            except: pass
        running_processes.clear()
        try: os.remove(DB_FILE)
        except: pass
        try: shutil.rmtree(DEPLOY_DIR, ignore_errors=True)
        except: pass
        try: bot.send_message(call.message.chat.id, sigma_header("ᴀʟʟ ᴅᴇʟᴇᴛᴇᴅ", "☠️", "ᴄʟᴇᴀɴ ᴡɪᴘᴇ"), parse_mode="Markdown")
        except: pass
        time.sleep(2); os._exit(0); return
    if data == "own_back":
        try: bot.answer_callback_query(call.id)
        except: pass
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        return _send_owner_panel(call.message.chat.id, call.from_user.id)

    # PLANS
    if data.startswith("plan_buy_"):
        pk = data.replace("plan_buy_", "")
        if pk not in PLANS:
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        plan = PLANS[pk]; stars = price_to_stars(plan['price'])
        try: bot.answer_callback_query(call.id, "💳")
        except: pass
        text = (sigma_header("ᴄʜᴏᴏꜱᴇ ᴘᴀʏᴍᴇɴᴛ", "💳", f"{plan['name']}") + "\n\n"
                f"💰 ₹{plan['price']}\n⭐ {stars} ꜱᴛᴀʀꜱ\n📅 {plan['days']} ᴅᴀʏꜱ\n\n"
                f"{sigma_quote('ᴄʜᴏᴏꜱᴇ ʏᴏᴜʀ ᴍᴇᴛʜᴏᴅ')}")
        mk = types.InlineKeyboardMarkup(row_width=1)
        mk.add(btn("🎁 ᴀᴘᴘʟʏ ᴄᴏᴜᴘᴏɴ", callback_data=f"plan_coupon_{pk}", style="primary"))
        upi_label = "💳 ᴀᴜᴛᴏ ᴜᴘɪ" if FAM_ENABLED else f"💳 ᴜᴘɪ — ₹{plan['price']}"
        mk.add(btn(upi_label, callback_data=f"plan_upi_{pk}", style="primary"))
        mk.add(btn(f"⭐ ꜱᴛᴀʀꜱ — {stars}⭐", callback_data=f"plan_stars_{pk}", style="success"))
        mk.add(btn("⬅️ ʙᴀᴄᴋ", callback_data="usr_show_plans", style="primary"))
        bot.send_message(call.message.chat.id, text, reply_markup=mk, parse_mode="Markdown")
        return

    if data.startswith("plan_coupon_"):
        pk = data.replace("plan_coupon_", "")
        if pk not in PLANS:
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        try: bot.answer_callback_query(call.id)
        except: pass
        msg = bot.send_message(call.message.chat.id, "🎁 ᴄᴏᴜᴘᴏɴ ᴄᴏᴅᴇ ʙʜᴇᴊᴏ:\n❌ `/cancel`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, lambda m: _apply_coupon_step(m, pk)); return

    if data.startswith("plan_upi_"):
        pk = data.replace("plan_upi_", "")
        if pk not in PLANS:
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        plan = PLANS[pk]; final = plan['price']; coupon = None
        if hasattr(bot, '_tmp_coupons') and uid in bot._tmp_coupons:
            c = bot._tmp_coupons[uid]
            if c['plan'] == pk: coupon = c['code']; final = plan['price'] - c['discount']

        if FAM_ENABLED:
            order = fam_create_order(final, users_db.get(uid, {}).get('name', 'User'))
            if order:
                order_id = order.get("order_id") or order.get("id")
                qr_url = order.get("qr_url") or order.get("qr")
                upi_intent = order.get("upi_intent") or order.get("intent") or ""
                try:
                    cur = get_db().cursor()
                    cur.execute("INSERT OR REPLACE INTO fam_orders (order_id, user_id, plan, amount, status) VALUES (?,?,?,?,'pending')",
                                (str(order_id), uid, pk, int(final)))
                    get_db().commit()
                except: pass
                try: bot.answer_callback_query(call.id, "💳")
                except: pass
                c_line = f"\n🎁 ᴄᴏᴜᴘᴏɴ: <code>{html.escape(coupon)}</code> (-₹{plan['price']-final})" if coupon else ""
                cap = (sigma_header("ᴀᴜᴛᴏ ᴜᴘɪ", "💳", f"{plan['name']}") + "\n\n"
                       f"💰 <b>₹{final}</b>"
                       + (f" <s>₹{plan['price']}</s>" if coupon else "") + "\n"
                       f"📅 {plan['days']} ᴅᴀʏꜱ" + c_line + "\n\n"
                       f"🆔 ᴏʀᴅᴇʀ ➜ <code>{html.escape(str(order_id))}</code>\n\n"
                       f"📱 ϙʀ ꜱᴄᴀɴ ᴋᴀʀᴇɪɴ ᴋɪ ᴘᴀʏᴍᴇɴᴛ ᴀᴜᴛᴏ ᴄᴏɴꜰɪʀᴍ ʜᴏɢᴀ ✅")
                mk = types.InlineKeyboardMarkup(row_width=1)
                if upi_intent:
                    mk.add(btn("📲 ᴏᴘᴇɴ ᴜᴘɪ ᴀᴘᴘ", url=upi_intent, style="success"))
                mk.add(btn("🔄 sᴛᴀᴛᴜꜱ ᴄʜᴇᴄᴋ", callback_data=f"famchk_{order_id}", style="primary"))
                mk.add(btn("⬅️ ʙᴀᴄᴋ", callback_data=f"plan_buy_{pk}", style="primary"))
                try:
                    bot.send_photo(call.message.chat.id, qr_url, caption=cap,
                                   reply_markup=mk, parse_mode="HTML")
                except Exception as _e:
                    print(f"[fam photo] {_e}")
                    try:
                        bot.send_message(call.message.chat.id, cap, reply_markup=mk, parse_mode="HTML")
                    except: pass
                threading.Thread(target=_fam_poll_worker,
                                 args=(order_id, uid, pk, final, call.message.chat.id),
                                 daemon=True).start()
                return

        try: bot.answer_callback_query(call.id, "💳")
        except: pass
        c_line = f"\n🎁 ᴄᴏᴜᴘᴏɴ: `{_md_safe(coupon)}` (-₹{plan['price']-final})" if coupon else ""
        cap = (sigma_header("ᴜᴘɪ ᴘᴀʏᴍᴇɴᴛ", "💳", f"{plan['name']}") + "\n\n"
               f"💰 *₹{final}*" + (f" ~~₹{plan['price']}~~" if coupon else "") + "\n"
               f"📅 {plan['days']} ᴅᴀʏꜱ" + c_line + "\n\n"
               f"💳 ᴜᴘɪ ➜ `{get_upi_id()}`\n👤 ɴᴀᴍᴇ ➜ {get_upi_name()}\n\n"
               f"{sigma_quote(f'ᴘᴀʏ ₹{final} ᴛʜᴇɴ ꜱᴇɴᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ')}")
        mk = types.InlineKeyboardMarkup(row_width=1)
        mk.add(btn("📤 ꜱᴇɴᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ", callback_data=f"plan_ss_{pk}", style="success"))
        mk.add(btn("⬅️ ʙᴀᴄᴋ", callback_data=f"plan_buy_{pk}", style="primary"))
        qr = get_upi_qr()
        if qr:
            try: bot.send_photo(call.message.chat.id, qr, caption=cap, reply_markup=mk, parse_mode="Markdown"); return
            except: pass
        bot.send_message(call.message.chat.id, cap, reply_markup=mk, parse_mode="Markdown")
        return

    if data.startswith("famchk_"):
        order_id = data.replace("famchk_", "")
        try: bot.answer_callback_query(call.id, "🔄")
        except: pass
        st, utr = fam_check_status(order_id)
        if st in ("paid", "success", "successful", "approved", "completed", "captured"):
            try:
                cur = get_db().cursor()
                cur.execute("SELECT * FROM fam_orders WHERE order_id=?", (order_id,))
                fo = cur.fetchone()
                if fo and fo['status'] != 'paid':
                    subscribe_user(fo['user_id'], fo['plan'])
                    cur.execute("UPDATE fam_orders SET status='paid' WHERE order_id=?", (order_id,))
                    get_db().commit()
            except: pass
            bot.send_message(call.message.chat.id,
                sigma_header("ᴘᴀʏᴍᴇɴᴛ ᴘᴀɪᴅ", "✅", f"ᴜᴛʀ: {utr or '—'}") + "\n\n"
                f"<i>ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴀᴄᴛɪᴠᴇ 🗿</i>",
                parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id,
                sigma_header("sᴛᴀᴛᴜꜱ", "⏳", f"{st or 'ᴘᴇɴᴅɪɴɢ'}") + "\n\n"
                f"<i>ᴘᴀʏᴍᴇɴᴛ ᴋᴀ ɪɴᴛᴇᴢᴀᴀʀ ʜᴀɪ...</i>",
                parse_mode="HTML")
        return

    if data.startswith("plan_ss_"):
        pk = data.replace("plan_ss_", "")
        if pk not in PLANS:
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        try: bot.answer_callback_query(call.id, "📸")
        except: pass
        msg = bot.send_message(call.message.chat.id, sigma_header("ꜱᴇɴᴅ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ", "📸") + "\n\nᴘᴀʏᴍᴇɴᴛ ᴋᴀ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ʙʜᴇᴊᴏ", parse_mode="Markdown")
        bot.register_next_step_handler(msg, lambda m: _payment_screenshot_handler(m, pk))
        return

    if data.startswith("plan_stars_"):
        pk = data.replace("plan_stars_", "")
        if pk not in PLANS:
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        plan = PLANS[pk]; final = plan['price']
        if hasattr(bot, '_tmp_coupons') and uid in bot._tmp_coupons:
            c = bot._tmp_coupons[uid]
            if c['plan'] == pk: final = plan['price'] - c['discount']
        stars = price_to_stars(final)
        try: bot.answer_callback_query(call.id, "⭐")
        except: pass
        try:
            bot.send_invoice(chat_id=call.message.chat.id, title=f"{plan['name']} — {plan['days']} ᴅᴀʏꜱ",
                description=f"ᴘʟᴀɴ: {plan['name']} | ꜰɪɴᴀʟ: ₹{final}",
                invoice_payload=f"plan_{pk}_{uid}", provider_token="", currency="XTR",
                prices=[types.LabeledPrice(label=plan['name'], amount=stars)], start_parameter=f"plan_{pk}")
        except Exception as e:
            try: bot.send_message(call.message.chat.id, f"❌ {e}")
            except: pass
        return

    # ADMIN ONLY
    if not is_admin(call.from_user.id): return

    if data == "adm_page_main":
        try: bot.answer_callback_query(call.id)
        except: pass
        safe_edit(call.message.chat.id, call.message.message_id,
            "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n"
            "    👑 𝗔𝗗𝗠𝗜𝗡 𝗖𝗢𝗡𝗧𝗥𝗢𝗟 🗿\n"
            "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄",
            reply_markup=admin_keyboard(call.from_user.id))
        return

    if data == "adm_page_files":
        try: bot.answer_callback_query(call.id)
        except: pass
        safe_edit(call.message.chat.id, call.message.message_id,
            sigma_header("ꜰɪʟᴇ ᴄᴏɴᴛʀᴏʟ", "📂", "ɢʟᴏʙᴀʟ ᴄᴏᴍᴍᴀɴᴅ ᴄᴇɴᴛʀᴇ"),
            reply_markup=admin_files_keyboard())
        return

    if data == "adm_toggle_maint":
        settings['maintenance'] = not settings['maintenance']; save_settings()
        try: bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=admin_keyboard(call.from_user.id))
        except: pass
        try: bot.answer_callback_query(call.id, "🔴 ON" if settings['maintenance'] else "🟢 OFF")
        except: pass
        return

    if data == "adm_toggle_autoapproval":
        settings['auto_approval'] = not settings.get('auto_approval', True); save_settings()
        try: bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=admin_keyboard(call.from_user.id))
        except: pass
        try: bot.answer_callback_query(call.id, "✅ ON" if settings['auto_approval'] else "⛔ OFF")
        except: pass
        return

    if data == "adm_toggle_fam":
        FAM_ENABLED = not FAM_ENABLED
        try: bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=admin_keyboard(call.from_user.id))
        except: pass
        try: bot.answer_callback_query(call.id, "🟢 ON" if FAM_ENABLED else "🔴 OFF")
        except: pass
        return

    if data == "adm_set_upi":
        try: bot.answer_callback_query(call.id, "💳")
        except: pass
        msg = bot.send_message(call.message.chat.id, f"💳 ᴄᴜʀʀᴇɴᴛ: `{get_upi_id()}`\n\nɴᴀʏᴀ ʙʜᴇᴊᴏ:", parse_mode="Markdown")
        bot.register_next_step_handler(msg, _admin_set_upi_step1); return

    if data == "adm_set_qr":
        try: bot.answer_callback_query(call.id, "📸")
        except: pass
        msg = bot.send_message(call.message.chat.id, "📸 Qʀ ᴘʜᴏᴛᴏ ʙʜᴇᴊᴏ:")
        bot.register_next_step_handler(msg, _admin_set_qr_step1); return

    if data == "adm_view_payment":
        try: bot.answer_callback_query(call.id)
        except: pass
        txt = (f"💳 <code>{html.escape(get_upi_id() or '')}</code>\n"
               f"👤 {html.escape(get_upi_name() or '')}\n"
               f"📸 {'✅' if get_upi_qr() else '❌'}\n\n"
               f"🤖 ꜰᴀᴍ ᴀᴜᴛᴏ: {'🟢 ᴏɴ' if FAM_ENABLED else '🔴 ᴏꜰꜰ'}")
        qr = get_upi_qr()
        if qr:
            try: bot.send_photo(call.message.chat.id, qr, caption=txt, parse_mode="HTML"); return
            except: pass
        bot.send_message(call.message.chat.id, txt, parse_mode="HTML"); return

    if data == "adm_del_qr":
        if not settings.get('upi_qr'):
            try: bot.answer_callback_query(call.id, "❌", show_alert=True)
            except: pass
            return
        settings['upi_qr'] = None; save_settings()
        try: bot.answer_callback_query(call.id, "🗑")
        except: pass
        try: bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=admin_keyboard(call.from_user.id))
        except: pass
        return

    if data == "adm_set_channel":
        try: bot.answer_callback_query(call.id, "📢")
        except: pass
        msg = bot.send_message(call.message.chat.id, f"📢 ᴄᴜʀʀᴇɴᴛ: {get_channel_url()}\n\nɴᴀʏᴀ ʟɪɴᴋ ʙʜᴇᴊᴏ:")
        bot.register_next_step_handler(msg, _admin_set_channel_step1); return

    if data == "adm_set_support":
        try: bot.answer_callback_query(call.id, "🔧")
        except: pass
        msg = bot.send_message(call.message.chat.id, f"🔧 ᴄᴜʀʀᴇɴᴛ: {get_support_url()}\n\nɴᴀʏᴀ ʟɪɴᴋ ʙʜᴇᴊᴏ:")
        bot.register_next_step_handler(msg, _admin_set_support_step1); return

    if data == "adm_view_links":
        try: bot.answer_callback_query(call.id)
        except: pass
        bot.send_message(call.message.chat.id,
            f"📢 ᴄʜᴀɴɴᴇʟ: <code>{html.escape(get_channel_url() or '')}</code>\n"
            f"🔧 ꜱᴜᴘᴘᴏʀᴛ: <code>{html.escape(get_support_url() or '')}</code>\n"
            f"👨‍💻 ᴅᴇᴠ: <code>{html.escape(get_dev_url() or '')}</code>\n"
            f"🤖 ʙᴏᴛ: <code>{html.escape(BOT_USERNAME)}</code>",
            parse_mode="HTML")
        return

    if data == "adm_lookup_bot":
        try: bot.answer_callback_query(call.id, "🗿")
        except: pass
        msg = bot.send_message(call.message.chat.id,
            sigma_header("ʙᴏᴛ ʟᴏᴏᴋᴜᴘ", "🗿", "ᴜꜱᴇʀɴᴀᴍᴇ ʙʜᴇᴊᴏ") + "\n\n"
            f"{sigma_quote('ᴇx: mybot')}",
            parse_mode="Markdown")
        bot.register_next_step_handler(msg, _admin_bot_lookup); return

    if data == "adm_broadcast":
        msg = bot.send_message(call.message.chat.id, "📝 ᴍᴇꜱꜱᴀɢᴇ ʙʜᴇᴊᴏ:")
        bot.register_next_step_handler(msg, broadcast_logic); return

    if data == "adm_set_video":
        msg = bot.send_message(call.message.chat.id, "📹 ᴠɪᴅᴇᴏ ʙʜᴇᴊᴏ:")
        bot.register_next_step_handler(msg, save_video_logic); return

    if data == "adm_del_video":
        settings['welcome_video'] = None; save_settings()
        try: bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=admin_keyboard(call.from_user.id))
        except: pass
        try: bot.answer_callback_query(call.id, "❌")
        except: pass
        return

    if data == "adm_stats":
        cpu = safe_cpu_percent(); rp, _, _ = safe_ram(); dp, _, _ = safe_disk()
        try: bot.answer_callback_query(call.id)
        except: pass
        bot.send_message(call.message.chat.id,
            sigma_header("ꜱᴇʀᴠᴇʀ ꜱᴛᴀᴛꜱ", "⚡") + "\n\n"
            f"⚡ ᴄᴘᴜ ➜ {cpu}%\n🧠 ʀᴀᴍ ➜ {rp}%\n💾 ᴅɪꜱᴋ ➜ {dp}%\n"
            f"🤖 ʙᴏᴛꜱ ➜ {len(running_processes)}\n👥 ᴜꜱᴇʀꜱ ➜ {len(users_db)}",
            parse_mode="Markdown")
        return

    if data == "adm_all_files":
        try: bot.answer_callback_query(call.id)
        except: pass
        tot = 0
        for tu, ud in users_db.items():
            for fn in ud.get('files', []):
                tot += 1
                fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{tu}_{fn}"))
                st = "🟢" if (fp in running_processes and running_processes[fp].poll() is None) else "🔴"
                mk = types.InlineKeyboardMarkup(row_width=2)
                mk.add(btn("▶️", callback_data=f"run_{fn}_{tu}", style="success"),
                       btn("⏸", callback_data=f"stop_{fn}_{tu}", style="danger"),
                       btn("📥", callback_data=f"down_{fn}_{tu}", style="primary"),
                       btn("🗑", callback_data=f"del_{fn}_{tu}", style="danger"))
                bot.send_message(call.message.chat.id,
                    f"👤 {ud.get('name','—')}\n📄 `{_md_safe(fn)}` {st}\n`{tu}`", reply_markup=mk, parse_mode="Markdown")
        if tot == 0: bot.send_message(call.message.chat.id, "📭 ɴᴏ ꜰɪʟᴇꜱ")
        return

    if data == "adm_check_whole":
        try: bot.answer_callback_query(call.id)
        except: pass
        r = s = m = 0
        for tu, ud in users_db.items():
            for fn in ud.get('files', []):
                fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{tu}_{fn}"))
                if not os.path.exists(fp): m += 1; continue
                if fp in running_processes and running_processes[fp].poll() is None: r += 1
                else: s += 1
        bot.send_message(call.message.chat.id,
            sigma_header("ꜰɪʟᴇ ʀᴇᴘᴏʀᴛ", "🔍") + "\n\n"
            f"🟢 ʀᴜɴɴɪɴɢ ➜ {r}\n🔴 ꜱᴛᴏᴘᴘᴇᴅ ➜ {s}\n❌ ᴍɪꜱꜱɪɴɢ ➜ {m}",
            parse_mode="Markdown")
        return

    if data == "adm_run_all":
        try: bot.answer_callback_query(call.id)
        except: pass
        ok = fail = 0; msg = bot.send_message(call.message.chat.id, "⚡...")
        for tu, ud in users_db.items():
            for fn in ud.get('files', []):
                fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{tu}_{fn}"))
                if not os.path.exists(fp): continue
                if fp in running_processes and running_processes[fp].poll() is None: continue
                try:
                    if run_user_file(fp, int(tu), fn): ok += 1
                    else: fail += 1
                except: fail += 1
        safe_edit(call.message.chat.id, msg.message_id, f"✅ {ok} • ❌ {fail}"); return

    if data == "adm_stop_all":
        try: bot.answer_callback_query(call.id)
        except: pass
        cnt = 0
        for fp, p in list(running_processes.items()):
            try: p.terminate(); cnt += 1
            except: pass
            running_processes.pop(fp, None)
        bot.send_message(call.message.chat.id, f"⏸ ꜱᴛᴏᴘᴘᴇᴅ {cnt}"); return

    if data == "adm_stop_specific":
        msg = bot.send_message(call.message.chat.id, "🎯 `uid filename`", parse_mode="Markdown")
        bot.register_next_step_handler(msg, _admin_stop_specific); return

    if data == "adm_search_user":
        msg = bot.send_message(call.message.chat.id, "🔎 ɪᴅ ᴏʀ ɴᴀᴍᴇ:")
        bot.register_next_step_handler(msg, _admin_search_user); return

    if data == "adm_add_admin":
        if not is_owner(call.from_user.id):
            try: bot.answer_callback_query(call.id, "🚫")
            except: pass
            return
        try: bot.answer_callback_query(call.id)
        except: pass
        msg = bot.send_message(call.message.chat.id, "👤 ᴜꜱᴇʀ ɪᴅ ʙʜᴇᴊᴏ:")
        bot.register_next_step_handler(msg, _admin_add_admin); return

    if data == "adm_remove_admin":
        if not is_owner(call.from_user.id):
            try: bot.answer_callback_query(call.id, "🚫")
            except: pass
            return
        adm = settings.get('admins', [])
        if not adm:
            try: bot.answer_callback_query(call.id, "❌ ɴᴏɴᴇ", show_alert=True)
            except: pass
            return
        mk = types.InlineKeyboardMarkup(row_width=1)
        for a in adm:
            n = users_db.get(str(a), {}).get('name', '—')
            mk.add(btn(f"❌ {a} ({n})", callback_data=f"adm_rmadmin_{a}", style="danger"))
        mk.add(btn("⬅️ ʙᴀᴄᴋ", callback_data="adm_page_main", style="primary"))
        try: bot.answer_callback_query(call.id)
        except: pass
        bot.send_message(call.message.chat.id, "🗑 ʀᴇᴍᴏᴠᴇ ᴋɪꜱᴇ?", reply_markup=mk); return

    if data.startswith("adm_rmadmin_"):
        if not is_owner(call.from_user.id): return
        t = data.split("_", 2)[2]
        adm = settings.get('admins', [])
        if t in [str(a) for a in adm]:
            settings['admins'] = [a for a in adm if str(a) != t]; save_settings()
            try: bot.answer_callback_query(call.id, "✅")
            except: pass
            safe_edit(call.message.chat.id, call.message.message_id, f"✅ ʀᴇᴍᴏᴠᴇᴅ `{t}`")
        return

    if data == "adm_list_admins":
        try: bot.answer_callback_query(call.id)
        except: pass
        on = users_db.get(str(OWNER_ID), {}).get('name', '—')
        txt = sigma_header("ᴀᴅᴍɪɴ ʟɪꜱᴛ", "👑", "ᴛʜᴇ ᴘᴏᴡᴇʀ ʜᴏʟᴅᴇʀꜱ") + "\n\n"
        txt += f"👑 ᴏᴡɴᴇʀ: `{OWNER_ID}` ({on})\n\n"
        adm = settings.get('admins', [])
        if adm:
            for i, a in enumerate(adm, 1):
                n = users_db.get(str(a), {}).get('name', '—')
                txt += f"{i}. `{a}` ({n})\n"
        else: txt += "👥 ɴᴏ ᴀᴅᴍɪɴꜱ"
        bot.send_message(call.message.chat.id, txt, parse_mode="Markdown"); return

    if data == "adm_logs":
        try: bot.answer_callback_query(call.id)
        except: pass
        try:
            cur = get_db().cursor()
            cur.execute("SELECT admin_name, action, details, timestamp FROM admin_logs ORDER BY id DESC LIMIT 20")
            rows = cur.fetchall()
            if not rows: return bot.send_message(call.message.chat.id, "📜 ɴᴏ ʟᴏɢꜱ")
            txt = sigma_header("ᴀᴄᴛɪᴏɴ ʟᴏɢꜱ", "📜", "ʀᴇᴄᴇɴᴛ ᴇᴠᴇɴᴛꜱ") + "\n\n"
            for r in rows:
                txt += f"👤 {r['admin_name']} → `{_md_safe(r['action'])}`\n   🕐 `{r['timestamp']}`\n\n"
            bot.send_message(call.message.chat.id, txt[:4000], parse_mode="Markdown")
        except: pass
        return

    if data == "adm_export_sql":
        try: bot.answer_callback_query(call.id, "📤")
        except: pass
        try:
            dump = export_db_sql(); ts = time.strftime("%Y%m%d_%H%M%S"); fn = f"anjasha_backup_{ts}.sql"
            with open(fn, 'w', encoding='utf-8') as f: f.write(dump)
            with open(fn, 'rb') as f:
                bot.send_document(call.message.chat.id, f, visible_file_name=fn,
                                  caption=sigma_header("ᴅʙ ᴇxᴘᴏʀᴛ", "📤", f"{len(users_db)} ᴜꜱᴇʀꜱ"),
                                  parse_mode="Markdown")
            try: os.remove(fn)
            except: pass
        except Exception as e:
            try: bot.send_message(call.message.chat.id, f"❌ {e}")
            except: pass
        return

    if data == "adm_import_sql":
        try: bot.answer_callback_query(call.id, "📥")
        except: pass
        msg = bot.send_message(call.message.chat.id, sigma_header("ɪᴍᴘᴏʀᴛ ᴅʙ", "📥") + "\n\n.ꜱQʟ ꜰɪʟᴇ ʙʜᴇᴊᴏ", parse_mode="Markdown")
        bot.register_next_step_handler(msg, _admin_import_sql); return

    if data == "adm_fixmenu":
        try: bot.answer_callback_query(call.id)
        except: pass
        bot.send_message(call.message.chat.id, sigma_header("ꜰɪx ᴄᴏɴᴛʀᴏʟ", "🔧"), reply_markup=fix_menu_keyboard(), parse_mode="Markdown"); return

    if data == "fix_syntax":
        try: bot.answer_callback_query(call.id)
        except: pass
        msg = bot.send_message(call.message.chat.id, "⚡ ꜱᴄᴀɴɴɪɴɢ...")
        time.sleep(2)
        try:
            ok, log, cnt = fix_host_syntax()
            safe_edit(call.message.chat.id, msg.message_id, f"{'✅' if ok else '❌'} {cnt} ꜰɪxᴇꜱ\n\n{log[:1800]}")
        except Exception as e: safe_edit(call.message.chat.id, msg.message_id, f"❌ {e}")
        return

    if data == "fix_allerrors":
        try: bot.answer_callback_query(call.id)
        except: pass
        msg = bot.send_message(call.message.chat.id, "🗿 ꜱᴄᴀɴ...")
        time.sleep(3)
        try:
            ok, log, cnt = fix_host_all()
            safe_edit(call.message.chat.id, msg.message_id, f"{'✅' if ok else '❌'} {cnt} ꜰɪxᴇꜱ\n\n{log[:1800]}")
        except Exception as e: safe_edit(call.message.chat.id, msg.message_id, f"❌ {e}")
        return

    if data == "fix_restart":
        try: bot.answer_callback_query(call.id)
        except: pass
        mk = types.InlineKeyboardMarkup()
        mk.add(btn("✅ ʏᴇꜱ", callback_data="fix_restart_confirm", style="danger"),
               btn("❌ ᴄᴀɴᴄᴇʟ", callback_data="adm_fixmenu", style="primary"))
        bot.send_message(call.message.chat.id, "🔄 ʀᴇꜱᴛᴀʀᴛ ʜᴏꜱᴛ?", reply_markup=mk); return

    if data == "fix_restart_confirm":
        try: bot.answer_callback_query(call.id)
        except: pass
        safe_edit(call.message.chat.id, call.message.message_id, "🔄 ʀᴇꜱᴛᴀʀᴛɪɴɢ...")
        time.sleep(1)
        try: restart_host_bot()
        except: pass
        return

    if data == "adm_fixfile":
        try: bot.answer_callback_query(call.id)
        except: pass
        msg = bot.send_message(call.message.chat.id, "🔧 ʙʀᴏᴋᴇɴ ꜰɪʟᴇ ʙʜᴇᴊᴏ")
        bot.register_next_step_handler(msg, _admin_fixfile_handler); return

    if data.startswith("adm_userfiles_"):
        tu = data.split("_", 2)[2]
        files = users_db.get(tu, {}).get('files', [])
        if not files:
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        try: bot.answer_callback_query(call.id)
        except: pass
        for fn in files:
            fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{tu}_{fn}"))
            st = "🟢" if (fp in running_processes and running_processes[fp].poll() is None) else "🔴"
            mk = types.InlineKeyboardMarkup(row_width=2)
            mk.add(btn("▶️", callback_data=f"run_{fn}_{tu}", style="success"),
                   btn("⏸", callback_data=f"stop_{fn}_{tu}", style="danger"),
                   btn("📥", callback_data=f"down_{fn}_{tu}", style="primary"),
                   btn("🗑", callback_data=f"del_{fn}_{tu}", style="danger"))
            bot.send_message(call.message.chat.id, f"📄 `{_md_safe(fn)}` {st}", reply_markup=mk, parse_mode="Markdown")
        return

    if data.startswith("adm_deluser_"):
        tu = data.split("_", 2)[2]
        if tu not in users_db:
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            return
        mk = types.InlineKeyboardMarkup()
        mk.add(btn("✅ ᴅᴇʟ", callback_data=f"adm_deluserok_{tu}", style="danger"),
               btn("❌ ᴄᴀɴᴄᴇʟ", callback_data="adm_page_main", style="primary"))
        try: bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=mk)
        except: pass
        return

    if data.startswith("adm_deluserok_"):
        tu = data.split("_", 2)[2]
        for fn in users_db.get(tu, {}).get('files', []):
            fp = os.path.normpath(os.path.join(DEPLOY_DIR, f"{tu}_{fn}"))
            if fp in running_processes:
                try: running_processes[fp].terminate()
                except: pass
                del running_processes[fp]
            try:
                if os.path.isdir(fp): shutil.rmtree(fp, ignore_errors=True)
                elif os.path.exists(fp): os.remove(fp)
            except: pass
        users_db.pop(tu, None); save_db()
        try: bot.answer_callback_query(call.id, "✅")
        except: pass
        safe_edit(call.message.chat.id, call.message.message_id, f"✅ ᴅᴇʟᴇᴛᴇᴅ `{tu}`")
        return

    # PAYMENTS
    if data == "adm_payments":
        try: bot.answer_callback_query(call.id)
        except: pass
        try:
            cur = get_db().cursor()
            cur.execute("SELECT * FROM payments WHERE status='pending' ORDER BY id DESC LIMIT 20")
            rows = cur.fetchall()
            if not rows: return bot.send_message(call.message.chat.id, "💰 ɴᴏ ᴘᴇɴᴅɪɴɢ")
            bot.send_message(call.message.chat.id, f"💰 *{len(rows)} ᴘᴇɴᴅɪɴɢ*", parse_mode="Markdown")
            for r in rows:
                plan = PLANS.get(r['plan'], PLANS['basic_m'])
                mk = types.InlineKeyboardMarkup(row_width=2)
                mk.add(btn("✅ ᴀᴘᴘʀᴏᴠᴇ", callback_data=f"pay_appr_{r['id']}", style="success"),
                       btn("❌ ʀᴇᴊᴇᴄᴛ", callback_data=f"pay_rej_{r['id']}", style="danger"))
                cap = f"🆔 `#{r['id']}`\n👤 {r['user_name']}\n🎯 {plan['name']}\n💰 ₹{r['amount']}"
                try: bot.send_photo(call.message.chat.id, r['screenshot_id'], caption=cap, reply_markup=mk, parse_mode="Markdown")
                except: bot.send_message(call.message.chat.id, cap, reply_markup=mk, parse_mode="Markdown")
        except: pass
        return

    if data.startswith("pay_appr_"):
        pid = data.split("_", 2)[2]
        try:
            conn = get_db(); cur = conn.cursor()
            cur.execute("SELECT * FROM payments WHERE id=?", (pid,))
            r = cur.fetchone()
            if not r:
                try: bot.answer_callback_query(call.id, "❌")
                except: pass
                return
            if r['status'] != 'pending':
                try: bot.answer_callback_query(call.id, f"⚠️ {r['status']}")
                except: pass
                return
            subscribe_user(r['user_id'], r['plan'])
            cur.execute("UPDATE payments SET status='approved', approved_at=CURRENT_TIMESTAMP, approved_by=? WHERE id=?",
                        (str(call.from_user.id), pid))
            conn.commit()
            try: bot.answer_callback_query(call.id, "✅")
            except: pass
            safe_edit(call.message.chat.id, call.message.message_id, f"✅ #{pid} ᴀᴘᴘʀᴏᴠᴇᴅ")
            try:
                p = PLANS[r['plan']]
                bot.send_message(int(r['user_id']),
                    sigma_header("ᴘʟᴀɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ", "🎉", f"{p['name']}") + "\n\n"
                    f"📅 {p['days']} ᴅᴀʏꜱ\n\n{sigma_quote('ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴛᴏᴘ 🗿')}",
                    parse_mode="Markdown")
            except: pass
        except Exception as e:
            try: bot.send_message(call.message.chat.id, f"❌ {e}")
            except: pass
        return

    if data.startswith("pay_rej_"):
        pid = data.split("_", 2)[2]
        try:
            cur = get_db().cursor()
            cur.execute("SELECT * FROM payments WHERE id=?", (pid,))
            r = cur.fetchone()
            if not r:
                try: bot.answer_callback_query(call.id, "❌")
                except: pass
                return
            cur.execute("UPDATE payments SET status='rejected', approved_by=? WHERE id=?",
                        (str(call.from_user.id), pid))
            get_db().commit()
            try: bot.answer_callback_query(call.id, "❌")
            except: pass
            safe_edit(call.message.chat.id, call.message.message_id, f"❌ #{pid} ʀᴇᴊᴇᴄᴛᴇᴅ")
        except: pass
        return

    if data == "adm_subs_list":
        try: bot.answer_callback_query(call.id)
        except: pass
        try:
            cur = get_db().cursor()
            cur.execute("SELECT user_id, plan, expires_at FROM subscriptions WHERE plan != 'free' AND status='active' ORDER BY expires_at ASC LIMIT 30")
            rows = cur.fetchall()
            if not rows: return bot.send_message(call.message.chat.id, "👥 ɴᴏ ᴘᴀɪᴅ ᴜꜱᴇʀꜱ")
            txt = sigma_header(f"ᴘᴀɪᴅ ᴜꜱᴇʀꜱ ({len(rows)})", "💎") + "\n\n"
            for r in rows:
                p = PLANS.get(r['plan'], PLANS['basic_m'])
                n = users_db.get(r['user_id'], {}).get('name', '—')
                txt += f"{p['emoji']} `{r['user_id']}` ({n})\n   📅 `{r['expires_at']}`\n\n"
            bot.send_message(call.message.chat.id, txt[:4000], parse_mode="Markdown")
        except: pass
        return

    # COUPONS
    if data == "adm_coupons":
        try: bot.answer_callback_query(call.id)
        except: pass
        try:
            cur = get_db().cursor()
            cur.execute("SELECT * FROM coupons ORDER BY created_at DESC LIMIT 20")
            rows = cur.fetchall()
            if not rows: return bot.send_message(call.message.chat.id, "🎁 ɴᴏ ᴄᴏᴜᴘᴏɴꜱ")
            txt = sigma_header(f"ᴄᴏᴜᴘᴏɴꜱ ({len(rows)})", "🎁") + "\n\n"
            for r in rows:
                ic = "🟢" if r['status']=='active' else "🔴"
                dt = f"{r['discount_value']}%" if r['discount_type']=='percent' else f"₹{r['discount_value']}"
                txt += f"{ic} `{_md_safe(r['code'])}` — {dt}\n   ᴜꜱᴇꜱ: {r['used_count']}/{r['max_uses'] or '∞'}\n\n"
            mk = types.InlineKeyboardMarkup().add(
                btn("➕ ɴᴇᴡ", callback_data="adm_new_coupon", style="success"),
                btn("⬅️ ʙᴀᴄᴋ", callback_data="adm_page_main", style="primary"))
            bot.send_message(call.message.chat.id, txt[:4000], reply_markup=mk, parse_mode="Markdown")
        except: pass
        return

    if data == "adm_new_coupon":
        try: bot.answer_callback_query(call.id)
        except: pass
        if not hasattr(bot, '_tmp_coupon'): bot._tmp_coupon = {}
        bot._tmp_coupon[call.from_user.id] = {}
        msg = bot.send_message(call.message.chat.id, "🎁 ᴄᴏᴅᴇ ʙʜᴇᴊᴏ (ꜱᴛᴇᴘ 1/4):")
        bot.register_next_step_handler(msg, _coupon_step1); return

    if data == "cp_type_percent":
        bot._tmp_coupon[call.from_user.id]['type'] = 'percent'
        try: bot.answer_callback_query(call.id)
        except: pass
        msg = bot.send_message(call.message.chat.id, "ᴠᴀʟᴜᴇ (1-100):")
        bot.register_next_step_handler(msg, _coupon_step2_value); return

    if data == "cp_type_fixed":
        bot._tmp_coupon[call.from_user.id]['type'] = 'fixed'
        try: bot.answer_callback_query(call.id)
        except: pass
        msg = bot.send_message(call.message.chat.id, "₹ ᴠᴀʟᴜᴇ (1-500):")
        bot.register_next_step_handler(msg, _coupon_step2_value); return

    if data == "adm_paystats":
        try: bot.answer_callback_query(call.id)
        except: pass
        try:
            cur = get_db().cursor()
            cur.execute("SELECT COALESCE(SUM(amount),0) FROM payments WHERE status='approved'")
            total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM payments WHERE status='pending'")
            pend = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM payments WHERE status='approved'")
            appr = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM coupon_uses")
            cu = cur.fetchone()[0]
        except: total = pend = appr = cu = 0
        bot.send_message(call.message.chat.id,
            sigma_header("ᴘᴀʏᴍᴇɴᴛ ʀᴇᴘᴏʀᴛ", "📊", "ꜰɪɴᴀɴᴄɪᴀʟ ʟᴏɢ") + "\n\n"
            f"💰 ᴛᴏᴛᴀʟ ➜ *₹{total}*\n✅ ᴀᴘᴘʀᴏᴠᴇᴅ ➜ *{appr}*\n⏳ ᴘᴇɴᴅɪɴɢ ➜ *{pend}*\n"
            f"🎁 ᴄᴏᴜᴘᴏɴꜱ ➜ *{cu}*",
            parse_mode="Markdown")
        return

def _apply_coupon_step(message, pk):
    uid = str(message.from_user.id)
    if not message.text:
        try: return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ")
        except: return
    code = message.text.strip().upper()
    if code == "/CANCEL":
        try: return bot.send_message(message.chat.id, "❌ ᴄᴀɴᴄᴇʟʟᴇᴅ")
        except: return
    valid, disc, msg = validate_coupon(code, uid, pk)
    if not valid:
        try: return bot.send_message(message.chat.id, f"{msg}")
        except: return
    plan = PLANS[pk]; np_ = plan['price'] - disc; stars = price_to_stars(np_)
    if not hasattr(bot, '_tmp_coupons'): bot._tmp_coupons = {}
    bot._tmp_coupons[uid] = {'code': code, 'discount': disc, 'plan': pk}
    try:
        bot.send_message(message.chat.id,
            sigma_header("ᴄᴏᴜᴘᴏɴ ᴀᴘᴘʟɪᴇᴅ", "🎁", f"-₹{disc}") + "\n\n"
            f"📊 ᴏʟᴅ ➜ ~~₹{plan['price']}~~\n✨ ɴᴇᴡ ➜ *₹{np_}*\n⭐ ꜱᴛᴀʀꜱ ➜ *{stars}*",
            reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                btn(f"💳 ᴜᴘɪ — ₹{np_}", callback_data=f"plan_upi_{pk}", style="primary"),
                btn(f"⭐ ꜱᴛᴀʀꜱ — {stars}⭐", callback_data=f"plan_stars_{pk}", style="success"),
                btn("🗑 ʀᴍ", callback_data=f"plan_rmcoupon_{pk}", style="danger"),
                btn("⬅️ ʙᴀᴄᴋ", callback_data=f"plan_buy_{pk}", style="primary")),
            parse_mode="Markdown")
    except: pass

def _coupon_step1(message):
    if not message.text: return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ")
    code = message.text.strip().upper()
    if not code or len(code) > 20 or " " in code: return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ")
    if not hasattr(bot, '_tmp_coupon'): bot._tmp_coupon = {}
    bot._tmp_coupon[message.from_user.id] = bot._tmp_coupon.get(message.from_user.id, {})
    bot._tmp_coupon[message.from_user.id]['code'] = code
    bot.send_message(message.chat.id, f"✅ `{_md_safe(code)}`\n\nꜱᴛᴇᴘ 2/4: ᴛʏᴘᴇ:",
        reply_markup=types.InlineKeyboardMarkup(row_width=2).add(
            btn("📊 %", callback_data="cp_type_percent", style="primary"),
            btn("💰 ₹", callback_data="cp_type_fixed", style="success")),
        parse_mode="Markdown")

def _coupon_step2_value(message):
    try: v = int(message.text.strip())
    except: return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ")
    bot._tmp_coupon[message.from_user.id]['value'] = v
    msg = bot.send_message(message.chat.id, f"✅ {v}\n\nꜱᴛᴇᴘ 3/4: ᴍᴀx ᴜꜱᴇꜱ:")
    bot.register_next_step_handler(msg, _coupon_step3)

def _coupon_step3(message):
    try: m = int(message.text.strip())
    except: return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ")
    bot._tmp_coupon[message.from_user.id]['max_uses'] = m
    msg = bot.send_message(message.chat.id, f"✅ {m}\n\nꜱᴛᴇᴘ 4/4: ᴠᴀʟɪᴅ ᴅᴀʏꜱ (0=ɴᴇᴠᴇʀ):")
    bot.register_next_step_handler(msg, _coupon_step4)

def _coupon_step4(message):
    try: d = int(message.text.strip())
    except: return bot.send_message(message.chat.id, "❌ ɪɴᴠᴀʟɪᴅ")
    data = bot._tmp_coupon.get(message.from_user.id, {})
    exp = None
    if d > 0: exp = (datetime.now() + timedelta(days=d)).strftime("%Y-%m-%d %H:%M:%S")
    ok = create_coupon(data['code'], data.get('type','percent'), data['value'], data['max_uses'], 'basic_m', exp, message.from_user.id)
    if ok: bot.send_message(message.chat.id, f"✅ ᴄᴏᴜᴘᴏɴ ᴄʀᴇᴀᴛᴇᴅ\n🎁 `{_md_safe(data['code'])}`")
    else: bot.send_message(message.chat.id, "❌ ꜰᴀɪʟᴇᴅ")
    if hasattr(bot, '_tmp_coupon'): bot._tmp_coupon.pop(message.from_user.id, None)

# ═══════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════
def send_welcome(chat_id, uid):
    try:
        bot.send_message(chat_id,
            f"🗿 <b>ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ</b>\n\n✦ ɪᴅ: <code>{uid}</code>\n"
            f"✦ ᴘʟᴀɴ: {PLANS[get_user_plan(uid)]['name']}\n\n▸ ᴄʜᴏᴏꜱᴇ 👇",
            reply_markup=main_keyboard(uid), parse_mode="HTML")
    except: pass

@bot.message_handler(commands=['clearkb'])
def clearkb(message):
    try: bot.send_message(message.chat.id, "🧹 ᴄʟᴇᴀʀᴇᴅ", reply_markup=types.ReplyKeyboardRemove())
    except: pass

@bot.message_handler(commands=['fixbuttons', 'fixmenu'])
def fix_buttons_menu(message):
    if not is_admin(message.from_user.id): return
    try:
        bot.send_message(message.chat.id,
            sigma_header("ꜰɪx ᴄᴏɴᴛʀᴏʟ", "🔧", "ꜱᴇʟꜰ-ʜᴇᴀʟɪɴɢ ᴍᴏᴅᴇ"),
            reply_markup=fix_menu_keyboard(), parse_mode="Markdown")
    except: pass

@bot.message_handler(commands=['admins'])
def list_admins_cmd(message):
    if not is_admin(message.from_user.id): return
    on = users_db.get(str(OWNER_ID), {}).get('name', '—')
    text = f"👑 ᴏᴡɴᴇʀ: `{OWNER_ID}` ({on})\n\n"
    adm = settings.get('admins', [])
    if adm:
        for i, a in enumerate(adm, 1):
            n = users_db.get(str(a), {}).get('name', '—')
            text += f"{i}. `{a}` ({n})\n"
    else: text += "👥 ɴᴏɴᴇ"
    try: bot.send_message(message.chat.id, text, parse_mode="Markdown")
    except: pass

# ═══════════════════════════════════════════════════════════
#  STAR PAYMENT
# ═══════════════════════════════════════════════════════════
@bot.pre_checkout_query_handler(func=lambda q: True)
def pre_checkout(query):
    try: bot.answer_pre_checkout_query(query.id, ok=True)
    except: pass

@bot.message_handler(content_types=['successful_payment'])
def successful_payment_handler(message):
    try:
        payload = message.successful_payment.invoice_payload
        parts = payload.split("_")
        if len(parts) < 3: return
        pk = parts[1]; uid = str(message.from_user.id)
        if pk not in PLANS: return
        plan = PLANS[pk]
        subscribe_user(uid, pk)
        stars_amt = message.successful_payment.total_amount
        try:
            cur = get_db().cursor()
            cur.execute("INSERT INTO payments (user_id, user_name, plan, amount, screenshot_id, status, approved_at, approved_by) VALUES (?,?,?,?,?,'approved',CURRENT_TIMESTAMP,'stars')",
                        (uid, users_db.get(uid, {}).get('name', 'User'), pk, plan['price'], f"stars_{stars_amt}"))
            get_db().commit()
        except: pass
        bot.send_message(message.chat.id,
            sigma_header("ᴘᴀʏᴍᴇɴᴛ ꜱᴜᴄᴄᴇꜱꜱ", "🎉", f"{stars_amt} ꜱᴛᴀʀꜱ") + "\n\n"
            f"🎯 {plan['name']}\n📅 {plan['days']} ᴅᴀʏꜱ\n\n{sigma_quote('ᴇɴᴊᴏʏ ᴛʜᴇ ᴘᴏᴡᴇʀ 🗿')}",
            reply_markup=types.InlineKeyboardMarkup().add(
                btn("🚀 ᴅᴇᴘʟᴏʏ ɴᴏᴡ", callback_data="usr_deploy", style="success")),
            parse_mode="Markdown")
        for a in get_all_admin_ids():
            try:
                bot.send_message(a,
                    f"💰 ꜱᴛᴀʀꜱ ᴘᴀʏᴍᴇɴᴛ\n👤 `{uid}`\n🎯 {plan['name']}\n⭐ {stars_amt}",
                    parse_mode="Markdown")
            except: pass
    except: pass

# ═══════════════════════════════════════════════════════════
#  STARTUP
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        print(
            "\n▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n"
            "  🗿 Anjasha Hosting Bot  ⚡\n"
            "  🥶 SIGMA EDITION — ONLINE 🗿\n"
            "▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n"
        )
    except: pass
    init_db()
    migrate_from_old()
    load_all()
    try: print(f"✅ DB ready: {len(users_db)} users | FamGateway: {'ON' if FAM_ENABLED else 'OFF'}")
    except: pass

    threading.Thread(target=free_tier_random_stuck_worker, daemon=True).start()
    threading.Thread(target=subscription_reminder_worker, daemon=True).start()
    threading.Thread(target=subscription_expiry_worker, daemon=True).start()

    while True:
        try:
            bot.infinity_polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            try: print(f"[polling] {e}")
            except: pass
            time.sleep(3)