# Set password. Password is in sha256 hex format e.g.
# hashlib.sha256(b"desired password").hexdigest()
# if password is empty, there won't be any auth
PASSWORD = ""

# TELEGRAM BOT TOKEN
TELEGRAM_ACCESS_TOKEN = ""

# TELEGRAM URL
TELEGRAM_API_URL = 'https://api.telegram.org/bot{token}/{method}'.format

# TELEGRAM NOTIFY/CHANNEL
TELEGRAM_NOTIFY_CHANNEL = ""