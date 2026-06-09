import random
import logging
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# ⚙️ SOZLAMALAR
# ============================================================

BOT_TOKEN   = "8731265151:AAG5lnawK64KXaE28S8QkvtOtiXmmxDLwIU"
ADMIN_ID    = 8661545898
ADMIN_PAROL = "787901"

# ============================================================
# 🌍 HIKOYALAR
# ============================================================

HIKOYALAR = [
    {
        "sarlavha": "☢️ Yadroviy Qiyomat",
        "matn": (
            "Kecha tunda yadroviy urush boshlandi. Shaharlarda portlashlar eshitildi. "
            "Radiatsiya darajasi o'limli — tashqarida 10 daqiqadan ortiq qolish mumkin emas. "
            "Bunker yagona najot. Lekin hamma sig'maydi..."
        ),
    },
    {
        "sarlavha": "🦠 Noma'lum Virus",
        "matn": (
            "Yangi virus butun qit'alarni qamrab oldi. Kasallangan odam 48 soatda o'ladi. "
            "Vaksin yo'q, davolash yo'q. Faqat izolyatsiya — bunker ichida yashab qolish mumkin. "
            "Oziq-ovqat va joy cheklangan. Kim kiradi, kim qoladi?"
        ),
    },
    {
        "sarlavha": "🌊 Mega Suv Toshqini",
        "matn": (
            "Antarktida muzliklari to'liq eridi. Dengiz sathi 80 metrga ko'tarildi. "
            "Barcha qirg'oq shaharlari suv ostida. Quruqlikning 70% yo'q bo'ldi. "
            "Bunker tog' ichida — yagona quruq joy. Resurslar cheklangan."
        ),
    },
    {
        "sarlavha": "🌋 Super Vulqon",
        "matn": (
            "Yellowstone supervulqoni otildi. Kul bulutlari quyoshni yopdi. "
            "Harorat -30 ga tushdi, ekinlar o'ldi. Oziq-ovqat zaxiralari tugayapti. "
            "Bunker — 5 yillik zaxira bilan. Lekin hamma sig'madi..."
        ),
    },
    {
        "sarlavha": "🤖 AI Isyoni",
        "matn": (
            "Sun'iy intellekt global tarmoqlarni egallab oldi. Elektr, suv, transport — hammasi o'chdi. "
            "Dronlar odamlarni kuzatyapti. Bunker — signalsiz, to'liq analog. "
            "Ichkarida yashab qolish mumkin. Lekin kimni olasiz?"
        ),
    },
    {
        "sarlavha": "☄️ Meteorit Qishi",
        "matn": (
            "Katta meteorit okean o'rtasiga tushdi. Tsunami, qorong'ulik, kislota yomg'iri. "
            "Olimlar bashorat qildi: 10 yil quyosh ko'rinmaydi. "
            "Bunkerda sun'iy yorug'lik va gidroponika bor. Faqat tanlangan odamlar kiradi."
        ),
    },
    {
        "sarlavha": "🧟 Zombie Epidemiyasi",
        "matn": (
            "Noma'lum parazit miyani egallaydi. Kasallangan odam 6 soatda o'zgaradi. "
            "Shaharlar evakuatsiya qilindi, lekin kech. 80% aholi zararlangan. "
            "Bunker — mustahkam, qulfli, xavfsiz. Kim ichkarida bo'lishga loyiq?"
        ),
    },
    {
        "sarlavha": "🌪️ Ob-havo Falokati",
        "matn": (
            "Global isish keskin tezlashdi. Har kuni yangi rekord issiqlik. "
            "Tashqarida +65 daraja — 5 daqiqa ham chidab bo'lmaydi. "
            "Bunker — sovutish tizimi bilan jihozlangan. Lekin elektr cheklangan. "
            "Kim eng zaruriy?"
        ),
    },
]

BUNKER_MALUMOTLARI = [
    "🏠 Sig'im: {n} kishi\n🍞 Oziq-ovqat: 2 yilga\n💧 Suv: 3 yilga\n⚡ Generator: bor\n🔫 Qurol: 2 ta miltiq",
    "🏠 Sig'im: {n} kishi\n🍞 Oziq-ovqat: 5 yilga\n💧 Suv: 2 yilga\n🌱 Gidroponik bog': bor\n🏥 Tibbiy xona: bor",
    "🏠 Sig'im: {n} kishi\n🍞 Oziq-ovqat: 1 yilga\n💧 Suv: 4 yilga\n🔬 Laboratoriya: bor\n📻 Radio aloqa: bor",
    "🏠 Sig'im: {n} kishi\n🍞 Oziq-ovqat: 3 yilga\n💧 Suv: 3 yilga\n🏥 Operatsiya xonasi: bor\n⚡ Quyosh paneli: bor",
]

KASBLAR = [
    "👨‍⚕️ Jarroh", "👩‍🔬 Mikrobiolog", "👷 Qurilishchi", "👨‍🍳 Oshpaz",
    "👩‍💻 Dasturchi", "🧑‍🌾 Dehqon", "👨‍🚒 O't o'chiruvchi", "👩‍🔧 Elektrchi",
    "🧑‍⚕️ Psixolog", "👨‍🏫 O'qituvchi", "👩‍✈️ Harbiy pilot", "🧑‍🔬 Kimyogar",
    "👨‍🌾 Veterinar", "👩‍🍳 Oziq-ovqat mutaxassisi", "🧑‍🔧 Mexanik",
    "👨‍⚖️ Huquqshunos", "👩‍🎨 Rassom", "🧑‍💼 Menejer", "🧑‍🚀 Muhandis",
    "👩‍🔒 Xavfsizlik mutaxassisi",
]
YOSHLAR_ERKAK = [
    "🧒 7 yoshli o'g'il bola",
    "👦 14 yoshli o'smir yigit",
    "👦 17 yoshli o'g'il",
    "👨 22 yoshli yigit",
    "👨 28 yoshli yigit",
    "👨 35 yoshli erkak",
    "👨 42 yoshli erkak",
    "👨 50 yoshli erkak",
    "🧓 60 yoshli keksa erkak",
    "👴 72 yoshli chol",
    "👴 80 yoshli qariya erkak",
]

YOSHLAR_AYOL = [
    "🧒 7 yoshli qiz bola",
    "👧 14 yoshli o'smir qiz",
    "👧 17 yoshli qiz",
    "👩 22 yoshli yosh ayol",
    "👩 28 yoshli ayol",
    "👩 35 yoshli ayol",
    "👩 42 yoshli ayol",
    "👩 50 yoshli ayol",
    "🧓 60 yoshli keksa ayol",
    "👵 72 yoshli kampir",
    "👵 80 yoshli qariya ayol",
    "🤰 26 yoshli homilador ayol (6 oy)",
    "🤰 31 yoshli homilador ayol (8 oy)",
]

JINSLAR = ["erkak", "ayol"]

def yosh_jins():
    """Tasodifiy jins va yosh qaytaradi"""
    jins = random.choice(JINSLAR)
    if jins == "erkak":
        yosh = random.choice(YOSHLAR_ERKAK)
        belgi = "♂️"
    else:
        yosh = random.choice(YOSHLAR_AYOL)
        belgi = "♀️"
    return f"{belgi} {yosh} ({jins})"

SOGLIK = [
    "💪 Mutlaqo sog'lom", "🤧 Yengil allergiya", "🦵 Bir oyog'i protez",
    "👁️ Ko'zi ojiz", "🧠 Psixologik muammo", "❤️ Yurak kasali",
    "🤰 Homilador (7 oy)", "💊 Doimiy dori ichadi", "🏋️ Sportchi, a'lo sog'lom",
]
KONIKMA = [
    "🔥 O't yoqishni biladi", "🌿 Dorivor o'simlik biladi",
    "🔑 Har qanday eshikni ochadi", "📻 Radio aloqa biladi",
    "🎯 Yaxshi nishon oladi", "🐟 Baliq ovlaydi",
    "🧵 Tikuvchilik qiladi", "⚙️ Mashina ta'mirlaydi",
    "📖 5 ta til biladi", "🎭 Psixologiyani o'qiydi",
    "💉 Tibbiy yordam beradi", "🌾 Dehqonchilik biladi",
]
QOSHIMCHA = [
    "🐕 Iti bor, tashlamaydi", "🤫 Katta sir yashiryapti",
    "💰 Yashirin boylik haqida biladi", "🗺️ Bunker xaritasini biladi",
    "👶 Yonida chaqalog'i bor", "😱 Qorong'ulikdan qo'rqadi",
    "🧨 Portlovchi moddalar biladi", "📡 Aloqa tizimini tuzatadi",
    "🌾 Urug'lar to'plami bor", "🎲 Qimorboz tabiatli",
]

# ============================================================
# HOLAT
# ============================================================

games        = {}   # chat_id -> game
banned_users = {}   # user_id -> True
all_users    = {}   # user_id -> info
bot_stats    = {"jami_oyinlar": 0, "boshlangan": datetime.now().strftime("%Y-%m-%d %H:%M")}
admin_sessions = {} # user_id -> {"step": ..., "verified": bool}

# ============================================================
# YORDAMCHI
# ============================================================

def is_admin(uid):   return uid == ADMIN_ID
def is_banned(uid):  return uid in banned_users

def track(user):
    if user.id not in all_users:
        all_users[user.id] = {
            "ism": user.first_name,
            "username": user.username or "-",
            "vaqt": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

def new_card():
    return {
        "kasb":    random.choice(KASBLAR),
        "yosh":    yosh_jins(),
        "soglik":  random.choice(SOGLIK),
        "konikma": random.choice(KONIKMA),
        "fakt":    random.choice(QOSHIMCHA),
    }

def card_text(card, name):
    return (
        f"🎴 *{name}ning kartochkasi:*\n"
        f"├ 👔 {card['kasb']}\n"
        f"├ 🧬 {card['yosh']}\n"
        f"├ 🏥 {card['soglik']}\n"
        f"├ ⭐ {card['konikma']}\n"
        f"└ 🔮 {card['fakt']}"
    )

# ============================================================
# O'YIN OQIMI (async loop)
# ============================================================

async def game_loop(chat_id: int, app):
    """Asosiy o'yin oqimi: mulohaza → kartochkalar → ovoz → takrorlash"""
    game = games.get(chat_id)
    if not game:
        return

    bot = app.bot
    players = list(game["players"].values())
    sigim   = game["sigim"]

    while True:
        game = games.get(chat_id)
        if not game or not game.get("active"):
            return

        living = [p for p in game["players"].values()]
        if len(living) <= sigim:
            # O'yin tugadi
            winners = "\n".join(f"🏆 {p['ism']}" for p in living)
            await bot.send_message(
                chat_id,
                f"🎉 *O'YIN TUGADI!*\n\nBunkerga kirganlar:\n{winners}",
                parse_mode="Markdown"
            )
            game["active"] = False
            return

        # ── 1. MULOHAZA (30 sek) ──────────────────────────────
        await bot.send_message(
            chat_id,
            "🤔 *30 SONIYA MULOHAZA!*\n\nHar bir o'yinchi o'z kartochkasini taqdim etsin.",
            parse_mode="Markdown"
        )
        for i in range(30, 0, -10):
            await asyncio.sleep(10)
            if i > 10:
                await bot.send_message(chat_id, f"⏳ {i-10} soniya qoldi...")
        await asyncio.sleep(10)

        game = games.get(chat_id)
        if not game or not game.get("active"):
            return

        # ── 2. KARTOCHKALARNI BIRMA-BIR OCHISH (20 sek/har biri) ─
        await bot.send_message(
            chat_id,
            "🎴 *KARTOCHKALAR OCHILDI!*\n\nHar 20 soniyada 1 ta kartochka ko'rsatiladi.",
            parse_mode="Markdown"
        )
        await asyncio.sleep(3)

        current_players = list(games.get(chat_id, {}).get("players", {}).values())
        for idx, player in enumerate(current_players):
            game = games.get(chat_id)
            if not game or not game.get("active"):
                return

            await bot.send_message(
                chat_id,
                f"👤 *{idx+1}/{len(current_players)} o'yinchi:*\n\n"
                + card_text(player["kartochka"], player["ism"]),
                parse_mode="Markdown"
            )

            if idx < len(current_players) - 1:
                await asyncio.sleep(20)

        # ── 3. OVOZ BERISH (30 sek) ──────────────────────────────
        game = games.get(chat_id)
        if not game or not game.get("active"):
            return

        current_players = list(game["players"].values())
        keyboard = [
            [InlineKeyboardButton(f"🚪 {p['ism']}", callback_data=f"vote_{p['uid']}_{chat_id}")]
            for p in current_players
        ]

        game["votes"] = {}
        game["voting"] = True

        vote_msg = await bot.send_message(
            chat_id,
            "🗳️ *OVOZ BERISH — 30 SONIYA!*\n\nKimni bunkerdan chiqarasiz?",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        game["vote_msg_id"] = vote_msg.message_id

        # Countdown
        for i in range(30, 0, -10):
            await asyncio.sleep(10)
            if i > 10:
                await bot.send_message(chat_id, f"⏳ Ovoz berishga {i-10} soniya qoldi...")

        await asyncio.sleep(10)

        game = games.get(chat_id)
        if not game or not game.get("active"):
            return

        game["voting"] = False

        # Natijalar
        votes = game.get("votes", {})
        if not votes:
            await bot.send_message(chat_id, "😶 Hech kim ovoz bermadi. Davom etamiz!")
            continue

        # Eng ko'p ovoz olganini chiqaramiz
        count = {}
        for voted_uid in votes.values():
            count[voted_uid] = count.get(voted_uid, 0) + 1

        max_votes = max(count.values())
        kicked_uid = max(count, key=lambda x: count[x])

        if kicked_uid not in game["players"]:
            await bot.send_message(chat_id, "⚠️ Natija aniqlanmadi. Keyingi tur!")
            continue

        kicked = game["players"][kicked_uid]
        game["chiqarilganlar"].append(kicked["ism"])
        del game["players"][kicked_uid]

        # ovoz xulosasi (result_lines da ko'rinadi)
        vote_summary = ", ".join(
            f"{all_users.get(uid, {}).get('ism', str(uid))}"
            for uid in votes.keys()
        )

        result_lines = "\n".join(
            f"• {all_users.get(uid, {}).get('ism', f'ID:{uid}')}: {cnt} ovoz"
            for uid, cnt in sorted(count.items(), key=lambda x: -x[1])
        )

        await bot.send_message(
            chat_id,
            f"🚪 *{kicked['ism']} bunkerdan chiqarildi!*\n\n"
            f"📊 Ovozlar:\n{result_lines}\n\n"
            f"{card_text(kicked['kartochka'], kicked['ism'])}\n\n"
            f"👥 Qolganlar: {len(game['players'])} kishi\n"
            f"🏠 Kerak: {sigim} kishi",
            parse_mode="Markdown"
        )

        await asyncio.sleep(5)

# ============================================================
# KOMANDALAR
# ============================================================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    track(user)
    if is_banned(user.id):
        await update.message.reply_text("🚫 Siz botdan bloklangansiz!")
        return
    badge = "👑 *ADMIN*\n" if is_admin(user.id) else ""
    text = (
        f"{badge}🏚️ *BUNKER O'YINIGA XUSH KELIBSIZ!*\n\n"
        "Apokalipsis yuz berdi. Hammaga joy yo'q.\n"
        "Kim bunkerga kiradi — jamoat hal qiladi!\n\n"
        "📋 *Komandalar:*\n"
        "/newgame — Yangi o'yin boshlash\n"
        "/join — O'yinga qo'shilish\n"
        "/startgame — O'yinni boshlash (host)\n"
        "/mycard — Kartochkangni ko'rish\n"
        "/bunker — Bunker va stsenariy\n"
        "/endgame — O'yinni tugatish (host)"
    )
    if is_admin(user.id):
        text += "\n\n🔧 *Admin:* /admin"
    await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user    = update.effective_user
    track(user)
    if is_banned(user.id):
        await update.message.reply_text("🚫 Siz botdan bloklangansiz!")
        return

    hikoya = random.choice(HIKOYALAR)
    sigim  = random.randint(2, 4)
    bunker = random.choice(BUNKER_MALUMOTLARI).format(n=sigim)

    games[chat_id] = {
        "host":           user.id,
        "host_name":      user.first_name,
        "players":        {},
        "started":        False,
        "active":         False,
        "hikoya":         hikoya,
        "bunker":         bunker,
        "sigim":          sigim,
        "chiqarilganlar": [],
        "votes":          {},
        "voting":         False,
        "vaqt":           datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    bot_stats["jami_oyinlar"] += 1

    await update.message.reply_text(
        f"🎮 *Yangi o'yin boshlandi!*\n"
        f"👑 Host: {user.first_name}\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🌍 *{hikoya['sarlavha']}*\n\n"
        f"{hikoya['matn']}\n"
        f"━━━━━━━━━━━━━━━━\n\n"
        f"{bunker}\n\n"
        f"⚠️ Bunkerga faqat *{sigim} kishi* sig'adi!\n\n"
        f"Qo'shilish uchun: /join",
        parse_mode="Markdown"
    )


async def cmd_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user    = update.effective_user
    track(user)
    logger.info(f"JOIN: user={user.id} chat={chat_id} games_keys={list(games.keys())}")
    if is_banned(user.id):
        await update.message.reply_text("🚫 Siz botdan bloklangansiz!")
        return
    if chat_id not in games:
        await update.message.reply_text(
            f"❌ Bu guruhda faol o'yin yo'q!\n"
            f"Yangi o'yin boshlash uchun: /newgame"
        )
        return
    game = games[chat_id]
    if game["started"]:
        await update.message.reply_text("❌ O'yin allaqachon boshlangan!")
        return
    if user.id in game["players"]:
        await update.message.reply_text(f"⚠️ {user.first_name}, siz allaqachon qo'shilgansiz!")
        return

    game["players"][user.id] = {
        "uid":      user.id,
        "ism":      user.first_name,
        "kartochka": new_card(),
        "username": user.username or user.first_name,
    }
    await update.message.reply_text(
        f"✅ *{user.first_name}* qo'shildi!\n"
        f"👥 Jami: {len(game['players'])} kishi\n"
        f"Kartochkangiz: /mycard",
        parse_mode="Markdown"
    )


async def cmd_startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user    = update.effective_user
    logger.info(f"STARTGAME: user={user.id} chat={chat_id} games_keys={list(games.keys())}")
    if chat_id not in games:
        await update.message.reply_text("❌ Avval /newgame bilan o'yin boshlang!")
        return
    game = games[chat_id]
    if user.id != game["host"] and not is_admin(user.id):
        await update.message.reply_text(
            f"❌ Faqat host boshlaya oladi!\n"
            f"Host: {game['host_name']}"
        )
        return
    if len(game["players"]) < 2:
        await update.message.reply_text("❌ Kamida 2 o'yinchi kerak!")
        return
    if game["started"]:
        await update.message.reply_text("❌ O'yin allaqachon boshlangan!")
        return

    game["started"] = True
    game["active"]  = True

    royxat = "\n".join(f"• {p['ism']}" for p in game["players"].values())
    await update.message.reply_text(
        f"🚨 *O'YIN BOSHLANDI!*\n\n"
        f"👥 O'yinchilar:\n{royxat}\n\n"
        f"🏠 Maqsad: {game['sigim']} kishi bunkerga kiradi\n\n"
        f"🤔 30 soniya mulohaza vaqti boshlanmoqda...",
        parse_mode="Markdown"
    )

    asyncio.create_task(game_loop(chat_id, context.application))


async def cmd_mycard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user    = update.effective_user
    if chat_id not in games or user.id not in games[chat_id]["players"]:
        await update.message.reply_text("❌ Siz o'yinda emassiz!")
        return
    p = games[chat_id]["players"][user.id]
    await update.message.reply_text(card_text(p["kartochka"], p["ism"]), parse_mode="Markdown")


async def cmd_bunker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in games:
        await update.message.reply_text("❌ Faol o'yin yo'q!")
        return
    g = games[chat_id]
    await update.message.reply_text(
        f"🌍 *{g['hikoya']['sarlavha']}*\n\n{g['hikoya']['matn']}\n\n"
        f"━━━━━━━━━━━━\n{g['bunker']}",
        parse_mode="Markdown"
    )


async def cmd_endgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user    = update.effective_user
    if chat_id not in games:
        await update.message.reply_text("❌ Faol o'yin yo'q!")
        return
    if user.id != games[chat_id]["host"] and not is_admin(user.id):
        await update.message.reply_text("❌ Faqat host yoki admin tugatishi mumkin!")
        return
    games[chat_id]["active"] = False
    del games[chat_id]
    await update.message.reply_text("🏁 O'yin tugatildi! /newgame bilan yangi o'yin boshlang.")


# ============================================================
# OVOZ BERISH CALLBACK
# ============================================================

async def vote_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user  = query.from_user
    data  = query.data  # vote_{uid}_{chat_id}

    parts   = data.split("_")
    voted_uid = int(parts[1])
    chat_id   = int(parts[2])

    game = games.get(chat_id)
    if not game or not game.get("voting"):
        await query.answer("⏰ Ovoz berish vaqti tugadi!", show_alert=True)
        return

    if user.id not in game["players"]:
        await query.answer("❌ Siz bu o'yinchi emassiz!", show_alert=True)
        return

    if user.id == voted_uid:
        await query.answer("❌ O'zingizga ovoz bera olmaysiz!", show_alert=True)
        return

    if user.id in game["votes"]:
        await query.answer("⚠️ Siz allaqachon ovoz bergansiz!", show_alert=True)
        return

    if voted_uid not in game["players"]:
        await query.answer("❌ Bu o'yinchi topilmadi!", show_alert=True)
        return

    game["votes"][user.id] = voted_uid
    voted_name = game["players"][voted_uid]["ism"]
    await query.answer(f"✅ {voted_name} ga ovoz berdingiz!", show_alert=False)


# ============================================================
# 👑 ADMIN PANEL
# ============================================================

async def cmd_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    # Guruhda yozilsa — xabarni o'chir va PM ga yo'naltir
    if chat.type in ("group", "supergroup"):
        try:
            await update.message.delete()
        except Exception:
            pass
        try:
            await context.bot.send_message(
                user.id,
                "🔐 Admin panel faqat shaxsiy xabarda ochiladi!\n\nMenga yozing: /admin"
            )
        except Exception:
            pass
        return

    if not is_admin(user.id):
        await update.message.reply_text("❌ Bu buyruq faqat admin uchun!")
        return

    # Parol tekshirish
    session = admin_sessions.get(user.id, {})
    if not session.get("verified"):
        admin_sessions[user.id] = {"step": "parol", "verified": False}
        await update.message.reply_text(
            "🔐 *Admin paneliga kirish*\n\nParolni kiriting:",
            parse_mode="Markdown"
        )
        return

    await show_admin_panel(update.message, context)


async def show_admin_panel(msg, context):
    keyboard = [
        [
            InlineKeyboardButton("📊 Statistika",        callback_data="adm_stats"),
            InlineKeyboardButton("👥 Foydalanuvchilar",  callback_data="adm_users"),
        ],
        [
            InlineKeyboardButton("🎮 Faol o'yinlar",     callback_data="adm_games"),
            InlineKeyboardButton("🚫 Banlist",           callback_data="adm_banlist"),
        ],
        [
            InlineKeyboardButton("📢 Xabar yuborish",    callback_data="adm_broadcast"),
            InlineKeyboardButton("🛑 O'yinni to'xtatish",callback_data="adm_stopgame"),
        ],
        [
            InlineKeyboardButton("🔒 Chiqish",           callback_data="adm_logout"),
        ],
    ]
    await msg.reply_text(
        "👑 *ADMIN PANEL*\n\nNimani ko'rmoqchisiz?",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def adm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user  = query.from_user

    if not is_admin(user.id):
        await query.answer("❌ Ruxsat yo'q!", show_alert=True)
        return

    session = admin_sessions.get(user.id, {})
    if not session.get("verified"):
        await query.answer("🔐 Avval /admin bilan kiring!", show_alert=True)
        return

    await query.answer()
    data = query.data

    back_btn = [[InlineKeyboardButton("🔙 Orqaga", callback_data="adm_back")]]

    if data == "adm_stats":
        faol  = len(games)
        jami_o = sum(len(g["players"]) for g in games.values())
        text = (
            f"📊 *STATISTIKA*\n\n"
            f"👥 Foydalanuvchilar: *{len(all_users)}*\n"
            f"🎮 Jami o'yinlar: *{bot_stats['jami_oyinlar']}*\n"
            f"🟢 Faol o'yinlar: *{faol}*\n"
            f"🕹️ Hozir o'ynayotganlar: *{jami_o}*\n"
            f"🚫 Banlangan: *{len(banned_users)}*\n"
            f"⏰ Bot yoqilgan: {bot_stats['boshlangan']}"
        )
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(back_btn))

    elif data == "adm_users":
        if not all_users:
            text = "👥 *FOYDALANUVCHILAR*\n\nHali hech kim yo'q."
        else:
            text = f"👥 *FOYDALANUVCHILAR* ({len(all_users)} ta)\n\n"
            for uid, d in list(all_users.items())[:20]:
                b = "🚫" if uid in banned_users else "✅"
                text += f"{b} *{d['ism']}* | @{d['username']} | `{uid}`\n"
            if len(all_users) > 20:
                text += f"\n... va yana {len(all_users)-20} ta"
        kb = [
            [InlineKeyboardButton("🚫 Ban",    callback_data="adm_ban_input"),
             InlineKeyboardButton("✅ Unban",  callback_data="adm_unban_input")],
            *back_btn
        ]
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(kb))

    elif data == "adm_games":
        if not games:
            text = "🎮 *FAOL O'YINLAR*\n\nHozir hech qanday o'yin yo'q."
        else:
            text = f"🎮 *FAOL O'YINLAR* ({len(games)} ta)\n\n"
            for cid, g in games.items():
                text += (
                    f"📍 Chat: `{cid}`\n"
                    f"👑 Host: {g['host_name']}\n"
                    f"👥 O'yinchilar: {len(g['players'])}\n"
                    f"🟢 Boshlangan: {'Ha' if g['started'] else 'Yoq'}\n"
                    f"⏰ {g['vaqt']}\n\n"
                )
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(back_btn))

    elif data == "adm_banlist":
        if not banned_users:
            text = "🚫 *BANLANGAN*\n\nRo'yxat bo'sh."
        else:
            text = f"🚫 *BANLANGAN* ({len(banned_users)} ta)\n\n"
            for uid in banned_users:
                d = all_users.get(uid, {})
                text += f"• *{d.get('ism','?')}* @{d.get('username','-')} `{uid}`\n"
        kb = [
            [InlineKeyboardButton("✅ Unban", callback_data="adm_unban_input")],
            *back_btn
        ]
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=InlineKeyboardMarkup(kb))

    elif data == "adm_broadcast":
        context.user_data["adm_mode"] = "broadcast"
        await query.edit_message_text(
            "📢 *HAMMAGA XABAR*\n\nXabar matnini yozing:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(back_btn)
        )

    elif data == "adm_ban_input":
        context.user_data["adm_mode"] = "ban"
        await query.edit_message_text(
            "🚫 *BAN*\n\nFoydalanuvchi ID sini yozing:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(back_btn)
        )

    elif data == "adm_unban_input":
        context.user_data["adm_mode"] = "unban"
        await query.edit_message_text(
            "✅ *UNBAN*\n\nFoydalanuvchi ID sini yozing:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(back_btn)
        )

    elif data == "adm_stopgame":
        context.user_data["adm_mode"] = "stopgame"
        await query.edit_message_text(
            "🛑 *O'YINNI TO'XTATISH*\n\nChat ID sini yozing:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(back_btn)
        )

    elif data == "adm_logout":
        admin_sessions.pop(user.id, None)
        context.user_data.pop("adm_mode", None)
        await query.edit_message_text("🔒 Admin paneldan chiqdingiz.")

    elif data == "adm_back":
        context.user_data.pop("adm_mode", None)
        keyboard = [
            [
                InlineKeyboardButton("📊 Statistika",        callback_data="adm_stats"),
                InlineKeyboardButton("👥 Foydalanuvchilar",  callback_data="adm_users"),
            ],
            [
                InlineKeyboardButton("🎮 Faol o'yinlar",     callback_data="adm_games"),
                InlineKeyboardButton("🚫 Banlist",           callback_data="adm_banlist"),
            ],
            [
                InlineKeyboardButton("📢 Xabar yuborish",    callback_data="adm_broadcast"),
                InlineKeyboardButton("🛑 O'yinni to'xtatish",callback_data="adm_stopgame"),
            ],
            [InlineKeyboardButton("🔒 Chiqish",             callback_data="adm_logout")],
        ]
        await query.edit_message_text(
            "👑 *ADMIN PANEL*\n\nNimani ko'rmoqchisiz?",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()

    # ── Parol tekshirish ──────────────────────────────────────
    if is_admin(user.id):
        session = admin_sessions.get(user.id, {})
        if session.get("step") == "parol":
            if text == ADMIN_PAROL:
                admin_sessions[user.id] = {"step": None, "verified": True}
                await update.message.reply_text("✅ Parol to'g'ri! Admin panelga xush kelibsiz.")
                await show_admin_panel(update.message, context)
            else:
                admin_sessions.pop(user.id, None)
                await update.message.reply_text("❌ Noto'g'ri parol!")
            return

    # ── Admin rejim (broadcast/ban/unban/stopgame) ────────────
    if is_admin(user.id) and admin_sessions.get(user.id, {}).get("verified"):
        mode = context.user_data.get("adm_mode")
        if mode:
            context.user_data.pop("adm_mode", None)

            if mode == "broadcast":
                sent = 0
                for uid in all_users:
                    try:
                        await context.bot.send_message(
                            uid,
                            f"📢 *Admin xabari:*\n\n{text}",
                            parse_mode="Markdown"
                        )
                        sent += 1
                    except Exception:
                        pass
                await update.message.reply_text(f"✅ {sent} ta foydalanuvchiga yuborildi.")

            elif mode == "ban":
                try:
                    uid = int(text)
                    if uid == ADMIN_ID:
                        await update.message.reply_text("❌ O'zingizni ban qila olmaysiz!")
                        return
                    banned_users[uid] = True
                    ism = all_users.get(uid, {}).get("ism", "Noma'lum")
                    await update.message.reply_text(f"🚫 *{ism}* (`{uid}`) banlandi!", parse_mode="Markdown")
                except ValueError:
                    await update.message.reply_text("❌ Noto'g'ri ID!")

            elif mode == "unban":
                try:
                    uid = int(text)
                    if uid in banned_users:
                        del banned_users[uid]
                        ism = all_users.get(uid, {}).get("ism", "Noma'lum")
                        await update.message.reply_text(f"✅ *{ism}* bandan chiqarildi!", parse_mode="Markdown")
                    else:
                        await update.message.reply_text("⚠️ Bu foydalanuvchi banlangan emas.")
                except ValueError:
                    await update.message.reply_text("❌ Noto'g'ri ID!")

            elif mode == "stopgame":
                try:
                    cid = int(text)
                    if cid in games:
                        games[cid]["active"] = False
                        del games[cid]
                        await update.message.reply_text(f"🛑 Chat `{cid}` o'yini to'xtatildi!", parse_mode="Markdown")
                        try:
                            await context.bot.send_message(cid, "🛑 Admin tomonidan o'yin to'xtatildi.")
                        except Exception:
                            pass
                    else:
                        await update.message.reply_text("❌ Bu chat ID da faol o'yin yo'q.")
                except ValueError:
                    await update.message.reply_text("❌ Noto'g'ri Chat ID!")
            return


# ============================================================
# MAIN
# ============================================================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Guruh va shaxsiy xabarlarda ham ishlaydi
    app.add_handler(CommandHandler("start",     cmd_start,     filters=None))
    app.add_handler(CommandHandler("newgame",   cmd_newgame,   filters=None))
    app.add_handler(CommandHandler("join",      cmd_join,      filters=None))
    app.add_handler(CommandHandler("startgame", cmd_startgame, filters=None))
    app.add_handler(CommandHandler("mycard",    cmd_mycard,    filters=None))
    app.add_handler(CommandHandler("bunker",    cmd_bunker,    filters=None))
    app.add_handler(CommandHandler("endgame",   cmd_endgame,   filters=None))
    app.add_handler(CommandHandler("admin",     cmd_admin,     filters=None))

    app.add_handler(CallbackQueryHandler(vote_callback, pattern=r"^vote_"))
    app.add_handler(CallbackQueryHandler(adm_callback,  pattern=r"^adm_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    print("🤖 Bunker boti ishga tushdi!")
    print(f"👑 Admin ID: {ADMIN_ID}")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
