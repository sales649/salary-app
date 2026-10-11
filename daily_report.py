"""التقرير المالي اليومي - بيشتغل لوحده من GitHub Actions الساعة 9 مساءً بتوقيت السعودية.
مستقل تماماً عن Streamlit/Render (مش محتاج حد يفتح البرنامج). الأسرار بتتقرا من GitHub Secrets."""
import os, sys
from datetime import datetime, timedelta
import requests
from supabase import create_client

AR_MONTHS = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']

def env(name):
    v = os.environ.get(name, '').strip()
    if not v:
        print(f"ناقص السر: {name}")
        sys.exit(1)
    return v

def num(x):
    try:
        return float(x or 0)
    except Exception:
        return 0.0

def net(box, opening):
    tin = sum(num(t.get('amount')) for t in box if isinstance(t, dict) and 'قبض' in str(t.get('type', '')))
    tout = sum(num(t.get('amount')) for t in box if isinstance(t, dict) and 'صرف' in str(t.get('type', '')))
    return num(opening) + tin - tout

def saman_balance(drivers):
    if not isinstance(drivers, list):
        return 0.0
    recs = [d for d in drivers if isinstance(d, dict) and ('سمان' in str(d.get('driver_name') or d.get('driver') or '') or d.get('driver_name') is None)]
    cust = {}
    for r in recs:
        g = num(r.get('given_amt') or r.get('amount'))
        if g > 0 and r.get('type') != 'تصفية_جزئية':
            cust[f"#{r.get('id')}"] = [g, 0.0]
    for r in recs:
        tid = r.get('target_custody_id')
        s = num(r.get('spent_amt') or r.get('spent'))
        if tid and tid in cust and s > 0:
            cust[tid][1] += s
    open_rem = sum(max(0.0, g - s) for g, s in cust.values())
    excess = sum(num(r.get('excess_amt')) for r in recs if r.get('type') == 'زيادة_فواتير')
    return open_rem - excess

def main():
    sb = create_client(env('SUPABASE_URL'), env('SUPABASE_KEY'))
    def get(key, default):
        r = sb.table('app_stores').select('data_val').eq('store_key', key).execute()
        return r.data[0]['data_val'] if r.data else default

    now = datetime.utcnow() + timedelta(hours=3)
    month = f"{AR_MONTHS[now.month - 1]} {now.year}"
    cash = get('cashbox_data', {})
    m = cash.get(month)
    if not isinstance(m, dict):
        print(f"مفيش شهر {month} في الصندوق - هوقف بدل ما أبعت أرقام غلط")
        sys.exit(1)
    main_net = net(m.get('transactions', []), m.get('opening', 0))
    acc_net = net(m.get('acc_transactions', []), m.get('acc_opening', 0))
    saman = saman_balance(get('driver_custody', []))
    total = main_net + acc_net
    today = now.strftime('%Y-%m-%d')

    html = (f"<b>📊 التقرير المالي اليومي - شركة ميم الخماسية</b>\n🗓 <b>التاريخ:</b> <code>{today}</code> ({month})\n\n"
            f"───────────────\n🏦 <b>الخزينة الرئيسية (Wahbi):</b>\n💵 <code>{main_net:,.2f} ر.س</code>\n\n"
            f"💼 <b>عُهدة المحاسب (Omar):</b>\n💵 <code>{acc_net:,.2f} ر.س</code>\n\n"
            f"🚚 <b>المتبقي بذمة (سمان السواق):</b>\n💵 <code>{saman:,.2f} ر.س</code>\n───────────────\n"
            f"💰 <b>إجمالي نقدية الشركة:</b>\n💎 <code>{total:,.2f} ر.س</code>\n───────────────")
    wa = (f"📊 *التقرير المالي اليومي - شركة ميم الخماسية*\n🗓 *التاريخ:* {today} ({month})\n\n"
          f"───────────────\n🏦 *الخزينة الرئيسية (Wahbi):*\n💵 {main_net:,.2f} ر.س\n\n"
          f"💼 *عُهدة المحاسب (Omar):*\n💵 {acc_net:,.2f} ر.س\n\n"
          f"🚚 *المتبقي بذمة (سمان السواق):*\n💵 {saman:,.2f} ر.س\n───────────────\n"
          f"💰 *إجمالي نقدية الشركة:*\n💎 {total:,.2f} ر.س\n───────────────")

    ok = True
    r = requests.post(f"https://api.telegram.org/bot{env('TELEGRAM_BOT_TOKEN')}/sendMessage",
                      json={"chat_id": env('TELEGRAM_CHAT_ID'), "text": html, "parse_mode": "HTML"}, timeout=30)
    print("telegram:", r.status_code, r.text[:200])
    ok &= r.status_code == 200
    r = requests.post(f"https://api.ultramsg.com/{env('ULTRAMSG_INSTANCE_ID')}/messages/chat",
                      data={"token": env('ULTRAMSG_TOKEN'), "to": env('MANAGER_PHONE_NUMBER'), "body": wa, "priority": "10"}, timeout=30)
    print("whatsapp:", r.status_code, r.text[:200])
    ok &= r.status_code == 200
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
