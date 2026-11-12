"""Generate favicon PNGs and 1200x630 share (Open Graph) images for website/.

Needs Pillow and macOS system fonts. Run from the repo root:
  /Users/liyu/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/make_share_images.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1] / 'website'
IMAGES = ROOT / 'assets' / 'images'
BG, CARD, BORDER = '#0d1117', '#161b22', '#30363d'
TEXT, TEXT2, TEXT3, BLUE, GREEN = '#f0f6fc', '#c9d1d9', '#9ba7b4', '#58a6ff', '#3fb950'
SF = '/System/Library/Fonts/SFNS.ttf'
PINGFANG = '/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData/PingFang.ttc'


def sf(size, weight='Regular'):
    font = ImageFont.truetype(SF, size)
    font.set_variation_by_name(weight)
    return font


def pingfang(size, bold=False):
    # PingFang.ttc face order: index 0 is TC Regular in this asset; semibold faces follow.
    for index in range(0, 40):
        try:
            font = ImageFont.truetype(PINGFANG, size, index=index)
        except OSError:
            break
        family, style = font.getname()
        if 'TC' in family and style == ('Semibold' if bold else 'Regular'):
            return font
    raise RuntimeError('PingFang TC face not found')


def avatar(size):
    img = Image.open(IMAGES / 'profile' / 'avatar.jpg').convert('RGB')
    img = ImageOps.fit(img, (size * 2, size * 2))
    mask = Image.new('L', img.size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, *img.size), fill=255)
    img.putalpha(mask)
    return img.resize((size, size), Image.LANCZOS)


def share_image(path, tagline, tagline_strong, sub, available, cjk):
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((40, 40, W - 40, H - 40), radius=28, fill=CARD, outline=BORDER, width=2)
    im.paste(av := avatar(132), (96, 92), av)
    body = (lambda s, b=False: pingfang(s, b)) if cjk else (lambda s, b=False: sf(s, 'Bold' if b else 'Regular'))
    d.text((256, 112), 'Li-Yu Chu', font=sf(60, 'Bold'), fill=TEXT)
    d.text((258, 190), 'Backend Engineer · Java / Spring Boot', font=sf(28, 'Semibold'), fill=BLUE)
    d.text((96, 280), tagline, font=body(50), fill=TEXT2)
    d.text((96, 350), tagline_strong, font=body(50, True), fill=TEXT)
    d.text((96, 440), sub, font=body(28), fill=TEXT3)
    d.line((96, 500, W - 96, 500), fill=BORDER, width=2)
    d.text((96, 524), 'luichu.dev', font=sf(30, 'Semibold'), fill=BLUE)
    af = body(26)
    tw = d.textlength(available, font=af)
    x = W - 96 - tw
    d.ellipse((x - 26, 536, x - 12, 550), fill=GREEN)
    d.text((x, 526), available, font=af, fill=TEXT2)
    im.save(path, optimize=True)


def favicon_png(path, size):
    scale = 4
    s = size * scale
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * 0.22), fill=BG)
    f = sf(int(s * 0.5), 'Bold')
    d.text((s / 2, s / 2 + s * 0.02), 'LC', font=f, fill=BLUE, anchor='mm')
    im.resize((size, size), Image.LANCZOS).save(path, optimize=True)


share_image(IMAGES / 'og-en.png', 'Every transaction accounted for.', 'Every AI action bounded.',
            'Three years of internet banking backend · Vancouver, BC', 'Available mid-December 2026', cjk=False)
share_image(IMAGES / 'og-zh.png', '每筆交易都對得上，', '每個 AI 動作都有邊界。',
            '三年網路銀行後端經驗 · 加拿大溫哥華', '2026 年 12 月中可到職', cjk=True)
favicon_png(ROOT / 'apple-touch-icon.png', 180)
favicon_png(ROOT / 'favicon-32.png', 32)
print('done')
