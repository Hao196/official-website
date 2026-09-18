# -*- coding: utf-8 -*-
"""
i18n builder: generate en/ and ja/ mirrors for all 122 pages.
Shared chrome (nav/footer/buttons/breadcrumb/switch/lang/title) is
translated via dictionaries; page bodies via body_en/body_ja maps.
"""
import glob, os, re, sys, json, io, html as _html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = "F:/做一个官网网页/"
OUT = {"en": ROOT + "en/", "ja": ROOT + "ja/"}

for d in OUT.values():
    os.makedirs(d, exist_ok=True)

def load_json(p, default):
    if os.path.exists(p):
        return json.load(io.open(p, encoding="utf-8"))
    return default

# ---------- shared dictionaries ----------
NAV = ["首页", "关于我们", "产品中心", "成功案例", "新闻动态",
       "视频中心", "下载中心", "招聘人才", "联系我们"]
NAV_TR = {
    "en": ["Home", "About Us", "Products", "Case Studies", "News",
           "Videos", "Downloads", "Careers", "Contact Us"],
    "ja": ["ホーム", "会社概要", "製品センター", "導入事例", "ニュース",
           "ビデオ", "ダウンロード", "採用情報", "お問い合わせ"],
}
BTN = {"en": "Contact Us", "ja": "お問い合わせ"}

# footer
FOOTER_COLS = {
    "en": {"brand_suffix": "Dongguan Qingfeng Electrical Machinery Co., Ltd.",
           "intro": "Founded in 2000, a high-tech enterprise dedicated to the R&D, manufacturing and service of wire, cable and optical cable machinery worldwide.",
           "col1": "Quick Links",
           "col2": "Product Series",
           "col3": "Contact Us",
           "series": ["Extrusion Lines", "Stranding & Cabling", "Shielding Series", "Optical Cable Series", "Auxiliary Equipment"],
           "labels": ["Mobile", "HK Office", "Email", "Address"]},
    "ja": {"brand_suffix": "東莞市慶豊電工機械有限公司",
           "intro": "2000年設立。電線・ケーブル・光ケーブル機械の研究開発・製造・サービスをグローバルに提供するハイテク企業です。",
           "col1": "クイックナビ",
           "col2": "製品シリーズ",
           "col3": "お問い合わせ",
           "series": ["押出機シリーズ", "撚線・成ケーブルシリーズ", "シールドシリーズ", "光ケーブルシリーズ", "補助設備シリーズ"],
           "labels": ["携帯", "香港オフィス", "メール", "住所"]},
}
FTR_MISC = {
    "en": ("Dongguan Qingfeng Electrical Machinery Co., Ltd. All Rights Reserved.",
           "Professional extrusion machines, stranding machines, irradiation equipment and high-frequency cable taping machines."),
    "ja": ("東莞市慶豊電工機械有限公司　無断転載禁止。",
           "押出機・撚線機・放射線架橋設備・高周波ケーブル巻回機の専門メーカー。"),
}

# common button/UI strings
UI = {
    "en": {"back": "Back to Products", "details": "View Details",
           "learn": "Learn More", "viewall": "View All Products",
           "home": "Home", "news_category": "Industry & Company News"},
    "ja": {"back": "製品一覧に戻る", "details": "詳細を見る",
           "learn": "詳細を見る", "viewall": "全製品を見る",
           "home": "ホーム", "news_category": "業界情報・企業ニュース"},
}

BRAND_CN = "庆丰电工机械"
BRAND_EN = "Qingfeng Electrical Machinery"
BRAND_JA = "慶豊電工機械"
FULL_CN = "东莞市庆丰电工机械有限公司"

# common phrases applied to every page (back links, category labels)
COMMON = {
    "en": [
        ("返回产品中心", "Back to Products"),
        ("返回新闻动态", "Back to News"),
        ("返回成功案例", "Back to Cases"),
        ("辐照交联束下设备系列", "Irradiation Cross-linking Under-beam Series"),
        ("轴转式框绞机", "Shaft-Type Rigid Frame Strander"),
        ("绞线及成缆系列", "Stranding &amp; Cabling Series"),
        ("立式极细单双层包带机", "Vertical Ultra-fine Single/Double-layer Taping Machine"),
        ("卧式单层双层三层包带机", "Horizontal Single/Double/Triple-layer Taping Machine"),
        ("卧式单层/双层/三层包带机", "Horizontal Single/Double/Triple-layer Taping Machine"),
        ("1000牵引轮外置式旋臂单绞机", "1000 External Capstan Arm-Type Single Twister"),
        ("高速旋臂单绞机", "High-Speed Arm-Type Single Twister"),
        ("1250高速绞线机", "1250 High-Speed Stranding Machine"),
        ("高速双绞机", "High-Speed Double Twister"),
        ("高速绞线机", "High-Speed Stranding Machine"),
        ("行星式笼绞机", "Planetary Cage Strander"),
        ("扁平排线及电梯扁平电线押出生产线", "Flat Ribbon &amp; Elevator Flat Cable Extrusion Line"),
        ("汽车线,建筑线,低烟无卤线押出生产线", "Automotive, Building &amp; LSZH Wire Extrusion Line"),
        ("护套线及电力电缆押出生产线", "Sheathing &amp; Power Cable Extrusion Line"),
        ("绝缘芯线押出生产线", "Insulated Core Wire Extrusion Line"),
        ("化学发泡押出生产线", "Chemical Foaming Extrusion Line"),
        ("物理发泡押出生产线", "Physical Foaming Extrusion Line"),
        ("摇盘机", "Coil Winder"),
        ("甩桶放线架", "Barrel Payoff Stand"),
        ("卷取机", "Take-up Machine"),
        ("成套设备系列", "Complete Line Series"),
        ("行星笼绞式复合光缆成缆机", "Planetary Cage Composite Optical Cable Strander"),
        ("光纤二次塑套押出生产线", "Optical Fiber Secondary Jacketing Extrusion Line"),
        ("光缆护套押出生产线", "Optical Cable Sheathing Extrusion Line"),
        ("50单双芯及皮线光缆生产线", "50 Single/Dual-core &amp; Drop Cable Production Line"),
        ("30紧包光纤押出生产线", "30 Tight-Buffered Fiber Extrusion Line"),
        ("USB3.1,Type-C 芯线成缆设备", "USB3.1/Type-C Core Wire Cabling Equipment"),
        ("新能源充电桩电缆设备", "New-Energy Charging Pile Cable Equipment"),
        ("行业新闻", "Industry News"),
        ("企业新闻", "Company News"),
        ("技术文章", "Technical Articles"),
        # h1 variants that differ from category label
        ("轴转式绞线机", "Shaft-Type Stranding Machine"),
        ("1000牵引轮外置式单绞机", "1000 External Capstan Single Twister"),
        ("1250弓型高速双次绞线机", "1250 Bow-Type High-Speed Double Twister"),
        ("扁平排线押出生产线", "Flat Ribbon Extrusion Line"),
        ("外披护套押出生产线", "Sheath/Jacket Extrusion Line"),
        ("QF-50单芯，双芯，皮线光缆生产线", "QF-50 Single/Dual-core &amp; Drop Cable Production Line"),
        ("50单芯，双芯，皮线光缆生产线", "50 Single/Dual-core &amp; Drop Cable Production Line"),
        ("USB3.1,Type-C 挤出生产线", "USB3.1/Type-C Extrusion Line"),
        ("电动汽车（充电桩）线缆绞线设备", "EV (Charging Pile) Cable Stranding Machine"),
        ("高频线缆包带机", "High-Frequency Cable Taping Machine"),
        ("立式笼绞机", "Vertical Cage Strander"),
        # breadcrumbs
        ("/ 首页", "/ Home"),
        ("/ 关于我们", "/ About Us"),
        ("/ 产品中心", "/ Products"),
        ("/ 成功案例", "/ Case Studies"),
        ("/ 新闻动态", "/ News"),
        ("/ 视频中心", "/ Videos"),
        ("/ 下载中心", "/ Downloads"),
        ("/ 招聘人才", "/ Careers"),
        ("/ 联系我们", "/ Contact Us"),
        ("/ 在线留言", "/ Message"),
        # generic page headings
        ("产品中心", "Products"),
        ("成功案例", "Case Studies"),
        ("视频中心", "Videos"),
        ("下载中心", "Downloads"),
        ("招聘人才", "Careers"),
        ("在线留言", "Leave a Message"),
        # contact info labels/values
        ("手机热线", "Mobile Hotline"),
        ("香港办公室电话", "Hong Kong Office"),
        ("传真", "Fax"),
        ("电子邮箱", "Email"),
        ("公司地址", "Company Address"),
        ("服务区域", "Service Regions"),
        ("北部及其它大区 / 东部大区 / 西部及南部大区",
         "North &amp; Other Regions / East Region / West &amp; South Region"),
        ("香港中环砵典乍街30号金明街502室",
         "Room 502, 30 Pottinger Street, Central, Hong Kong"),
        # remaining category labels
        ("70多芯(软光缆及布线)光缆押出生产线", "70+ Core (Soft Optical Cable &amp; Wiring) Optical Cable Extrusion Line"),
        ("300卧式缠绕双包一体屏蔽机 (USB3.1,Type-C)", "300 Horizontal Winding &amp; Double-taping Integrated Shielding Machine (USB3.1, Type-C)"),
        ("新能源(光伏,风能,充电桩等),智能化机器 (工业4.0)线缆押出生产线",
         "New Energy (PV, Wind, Charging Pile) &amp; Smart Industry 4.0 Cable Extrusion Line"),
        ("铁氟龙(USB3.1,Type-C 同轴线及高温线) 押出生线",
         "PTFE (USB3.1, Type-C Coaxial &amp; High-Temperature Wire) Extrusion Line"),
        ("辐照束下设备", "Irradiation Under-beam Equipment"),
        ("300卧式缠绕双包一体屏蔽机", "300 Horizontal Winding &amp; Double-taping Integrated Shielding Machine"),
        ("行业信息", "Industry Info"),
        ("行业资讯与专业技术分享", "Industry news and technical insights"),
        ("1,500万+", "&yen;15M+"),
        ("庆丰电工机械工厂", "Qingfeng Electrical Machinery Factory"),
        ("机械传动示意", "Mechanical drive schematic"),
        ("宋体", "SimSun"),
        ("我们希望有更多的专业人才加入我们事业的行列", "We hope more professionals will join our team"),
        ("更多的人关注庆丰的发展", "more people to follow Qingfeng's development"),
        ("更多的人关注Qingfeng的发展", "more people to follow Qingfeng's development"),
        ("庆丰", "Qingfeng"),
        ("新闻动态", "News"),
        ("成功案例", "Case Studies"),
        ("行业技术", "Technology"),
        ("展会活动", "Exhibitions &amp; Events"),
        ("电线电缆设备制造商", "Wire and Cable Equipment Manufacturer"),
    ],
    "ja": [
        ("返回产品中心", "製品一覧に戻る"),
        ("返回新闻动态", "ニュース一覧に戻る"),
        ("返回成功案例", "導入事例一覧に戻る"),
        ("辐照交联束下设备系列", "放射線架橋アンダービームシリーズ"),
        ("轴转式框绞机", "軸回転式リジッドフレーム撚線機"),
        ("绞线及成缆系列", "撚線・成ケーブルシリーズ"),
        ("立式极细单双层包带机", "縦型極細単層・二層テープ巻機"),
        ("卧式单层双层三层包带机", "横型単層・二層・三層テープ巻機"),
        ("卧式单层/双层/三层包带机", "横型単層・二層・三層テープ巻機"),
        ("1000牵引轮外置式旋臂单绞机", "1000 キャプスタン外置型アーム式単撚機"),
        ("高速旋臂单绞机", "高速アーム式単撚機"),
        ("1250高速绞线机", "1250 高速撚線機"),
        ("高速双绞机", "高速双撚機"),
        ("高速绞线机", "高速撚線機"),
        ("行星式笼绞机", "プラネタリ型ケージ撚線機"),
        ("扁平排线及电梯扁平电线押出生产线", "フラットリボン・エレベータ用フラット電線押出ライン"),
        ("汽车线,建筑线,低烟无卤线押出生产线", "自動車・建築・低煙無ハロゲン電線押出ライン"),
        ("护套线及电力电缆押出生产线", "シース・電力ケーブル押出ライン"),
        ("绝缘芯线押出生产线", "絶縁芯線押出ライン"),
        ("化学发泡押出生产线", "化学発泡押出ライン"),
        ("物理发泡押出生产线", "物理発泡押出ライン"),
        ("摇盘机", "巻取機（コイルワインダ）"),
        ("甩桶放线架", "バレルペイオフスタンド"),
        ("卷取机", "テークアップ機"),
        ("成套设备系列", "成套設備シリーズ"),
        ("行星笼绞式复合光缆成缆机", "プラネタリケージ式複合光ケーブル撚線機"),
        ("光纤二次塑套押出生产线", "光ファイバ二次被覆押出ライン"),
        ("光缆护套押出生产线", "光ケーブルシース押出ライン"),
        ("50单双芯及皮线光缆生产线", "50 単芯・二芯・ドロップケーブル生産ライン"),
        ("30紧包光纤押出生产线", "30 タイトバッファ光ファイバ押出ライン"),
        ("USB3.1,Type-C 芯线成缆设备", "USB3.1/Type-C 芯線成ケーブル設備"),
        ("新能源充电桩电缆设备", "新エネ充電スタンドケーブル設備"),
        ("行业新闻", "業界ニュース"),
        ("企业新闻", "企業ニュース"),
        ("技术文章", "技術コラム"),
        # h1 variants that differ from category label
        ("轴转式绞线机", "軸回転式撚線機"),
        ("1000牵引轮外置式单绞机", "1000 キャプスタン外置型単撚機"),
        ("1250弓型高速双次绞线机", "1250 ボウ型高速二回撚線機"),
        ("扁平排线押出生产线", "フラットリボン押出ライン"),
        ("外披护套押出生产线", "シース被覆押出ライン"),
        ("QF-50单芯，双芯，皮线光缆生产线", "QF-50 単芯・二芯・ドロップケーブル生産ライン"),
        ("50单芯，双芯，皮线光缆生产线", "50 単芯・二芯・ドロップケーブル生産ライン"),
        ("USB3.1,Type-C 挤出生产线", "USB3.1/Type-C 押出ライン"),
        ("电动汽车（充电桩）线缆绞线设备", "電気自動車（充電スタンド）ケーブル撚線設備"),
        ("高频线缆包带机", "高周波ケーブルテープ巻機"),
        ("立式笼绞机", "縦型ケージ撚線機"),
        # breadcrumbs
        ("/ 首页", "/ ホーム"),
        ("/ 关于我们", "/ 会社概要"),
        ("/ 产品中心", "/ 製品"),
        ("/ 成功案例", "/ 導入事例"),
        ("/ 新闻动态", "/ ニュース"),
        ("/ 视频中心", "/ ビデオ"),
        ("/ 下载中心", "/ ダウンロード"),
        ("/ 招聘人才", "/ 採用情報"),
        ("/ 联系我们", "/ お問い合わせ"),
        ("/ 在线留言", "/ お問い合わせ"),
        # generic page headings
        ("产品中心", "製品センター"),
        ("成功案例", "導入事例"),
        ("视频中心", "ビデオセンター"),
        ("下载中心", "ダウンロード"),
        ("招聘人才", "採用情報"),
        ("在线留言", "メッセージを送る"),
        # contact info labels/values
        ("手机热线", "携帯ホットライン"),
        ("香港办公室电话", "香港オフィス電話"),
        ("传真", "FAX"),
        ("电子邮箱", "メール"),
        ("公司地址", "会社住所"),
        ("服务区域", "サービスエリア"),
        ("北部及其它大区 / 东部大区 / 西部及南部大区",
         "北部・その他地区 / 東部地区 / 西部・南部地区"),
        ("香港中环砵典乍街30号金明街502室",
         "香港中環ポッティンジャー・ストリート30号金明街502室"),
        # remaining category labels
        ("70多芯(软光缆及布线)光缆押出生产线", "70芯以上（ソフト光ケーブル・配線用）光ケーブル押出ライン"),
        ("300卧式缠绕双包一体屏蔽机 (USB3.1,Type-C)", "300 横型巻取・二重テープ一体型シールド機（USB3.1, Type-C）"),
        ("新能源(光伏,风能,充电桩等),智能化机器 (工业4.0)线缆押出生产线",
         "新エネ（太陽光・風力・充電スタンド等）・スマート（インダストリー4.0）ケーブル押出ライン"),
        ("铁氟龙(USB3.1,Type-C 同轴线及高温线) 押出生线",
         "PTFE（USB3.1, Type-C 同軸・高温電線）押出ライン"),
        ("辐照束下设备", "放射線アンダービーム設備"),
        ("300卧式缠绕双包一体屏蔽机", "300 横型巻取・二重テープ一体型シールド機"),
        ("行业信息", "業界情報"),
        ("行业资讯与专业技术分享", "業界ニュースと専門技術のご紹介"),
        ("1,500万+", "1,500万元+"),
        ("庆丰电工机械工厂", "慶豊電工機械 工場"),
        ("机械传动示意", "機械駆動の模式図"),
        ("宋体", "SimSun"),
        ("我们希望有更多的专业人才加入我们事业的行列", "より多くの専門人材が私たちの仲間に加わることを願っています"),
        ("更多的人关注庆丰的发展", "より多くの方々に慶豊の発展を注目していただきたい"),
        ("庆丰", "慶豊"),
        ("新闻动态", "ニュース"),
        ("成功案例", "導入事例"),
        ("行业技术", "技術"),
        ("展会活动", "展示会・イベント"),
        ("电线电缆设备制造商", "電線ケーブル設備メーカー"),
        ("全球客户的信赖之选", "世界のお客様に選ばれるパートナー"),
        ("USB3.1 Type-C 挤出生产线", "USB3.1 Type-C 押出ライン"),
        ("扫描频率", "走査周波数"),
        ("笼绞机", "ケージ撚線機"),
        ("的常见问题及生产流程", "のよくある問題と生産工程"),
        ("以上介绍的就是", "以上ご紹介したのは"),
    ],
}

# title/meta translation overrides per file (generated dynamically below)
PAGE_TITLES = {"en": {}, "ja": {}}

# body translations (per-file full replacement of body text)
# format: {"pro_show-249.html": {"div": "pro-detail-body", "html": "<div class='txt'><p>...</p></div>"}}
BODY_EN = load_json(ROOT + "_i18n_body_en.json", {})
BODY_JA = load_json(ROOT + "_i18n_body_ja.json", {})
TITLES = load_json(ROOT + "_i18n_titles.json", {"en": {}, "ja": {}})

def tr_title(lang, title):
    """Translate <title> and meta description best-effort."""
    return PAGE_TITLES[lang].get(title, title if lang == "zh" else title)

def rewrite_paths(html, lang):
    """Prefix ../ to assets/css/js/template refs for subdir pages.
    Also normalizes single-quoted src/href attributes to double quotes."""
    html = re.sub(r"""(src|href)\s*=\s*'([^']*)'""", r'\1="\2"', html, flags=re.I)

    def fix(m):
        p = m.group(2)
        if p.startswith(("http", "#", "mailto", "tel", "data:", "javascript:")):
            return m.group(0)
        if p.endswith(".css") or p.endswith(".js"):
            return m.group(0).replace(p, "../" + p)
        if p.startswith("assets/") or p.startswith("template/"):
            return m.group(0).replace(p, "../" + p)
        return m.group(0)
    html = re.sub(r'(src|href)="(css/[^"]+|js/[^"]+|template/[^"]+|assets/[^"]+)"', fix, html)

    def fixurl(m):
        q, pre, rest = m.group(1), m.group(2), m.group(3)
        return "url(%s../%s%s%s)" % (q, pre, rest, q)
    html = re.sub(r"url\(\s*(['\"]?)(assets/|css/|js/|template/)([^)'\"]*)\1\s*\)", fixurl, html)
    return html

def _replace_container(s, cls, new_inner):
    """Replace the inner HTML of the first <div class="cls"> ... </div> using
    a balanced <div> scanner so nested divs/scripts are handled correctly."""
    start_tag = '<div class="%s"' % cls
    i = s.find(start_tag)
    if i < 0:
        return s, False
    j = s.find(">", i)
    if j < 0:
        return s, False
    depth = 1
    k = j + 1
    n = len(s)
    while k < n and depth > 0:
        nd = s.find("<div", k)
        nc = s.find("</div>", k)
        if nc < 0:
            break
        if nd != -1 and nd < nc:
            depth += 1
            k = nd + 4
        else:
            depth -= 1
            if depth == 0:
                return s[: j + 1] + new_inner + s[nc:], True
            k = nc + 6
    return s, False


LANG_NAMES = {"zh": "中文", "en": "English", "ja": "日本語"}

_GLOBE = (
    '<svg class="lang-globe" viewBox="0 0 24 24" width="14" height="14" aria-hidden="true" '
    'fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/>'
    '<path d="M3 12h18M12 3c2.5 2.5 3.8 5.7 3.8 9s-1.3 6.5-3.8 9c-2.5-2.5-3.8-5.7-3.8-9S9.5 5.5 12 3z"/></svg>'
)

def lang_switch_html(cur_lang, self_page):
    if cur_lang == "zh":
        hrefs = {"zh": self_page, "en": "en/" + self_page, "ja": "ja/" + self_page}
    elif cur_lang == "en":
        hrefs = {"zh": "../" + self_page, "en": self_page, "ja": "../ja/" + self_page}
    else:
        hrefs = {"zh": "../" + self_page, "en": "../en/" + self_page, "ja": self_page}
    items = "".join(
        '<a href="%s" hreflang="%s"%s>%s</a>' % (
            hrefs[k], "zh-CN" if k == "zh" else k,
            ' class="on" aria-current="true"' if k == cur_lang else "",
            LANG_NAMES[k])
        for k in ("zh", "en", "ja"))
    return (
        '<div class="lang-switch">'
        '<button type="button" class="lang-btn" aria-haspopup="true" aria-expanded="false" aria-label="Language">'
        + _GLOBE +
        '<span class="lang-cur">%s</span><span class="lang-caret" aria-hidden="true"></span>'
        '</button>'
        '<div class="lang-menu">%s</div>'
        '</div>' % (LANG_NAMES[cur_lang], items)
    )

def _remove_balanced(html, start, pos, tag):
    depth = 1
    pat = re.compile(r"</?%s\b[^>]*>" % tag, re.I)
    while True:
        mm = pat.search(html, pos)
        if not mm:
            return html
        if mm.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return html[:start] + html[mm.end():]
        else:
            depth += 1
        pos = mm.end()

def strip_lang_switch(html):
    """Remove a previously-injected language switcher (span or div form)."""
    m = re.search(r"<(span|div)\s+class=\"lang-switch\"", html)
    if not m:
        return html
    return _remove_balanced(html, m.start(), m.end(), m.group(1))



def build(lang):
    files = sorted(glob.glob(ROOT + "*.html"))
    nav = NAV_TR[lang]
    btn = BTN[lang]
    done = 0
    for f in files:
        name = os.path.basename(f)
        s = io.open(f, encoding="utf-8", errors="ignore").read()
        s = strip_lang_switch(s)

        # ---- lang attr ----
        s = s.replace('lang="zh-CN"', 'lang="%s"' % ("en" if lang == "en" else "ja"))

        # ---- brand text ----
        # (footer brand block is handled first, see below, so the plain
        #  company-name replace does not pre-empt it)

        # ---- nav: translate the 9 link texts (order matters, do exact <li> replace) ----
        for cn, en_jp in zip(NAV, nav):
            s = s.replace(">%s</a>" % cn, ">%s</a>" % en_jp)
            s = s.replace(">%s</li>" % cn, ">%s</li>" % en_jp)

        # ---- header CTA button ----
        s = re.sub(r'<a class="btn btn-primary" href="contact.html">[^<]*</a>',
                   '<a class="btn btn-primary" href="contact.html">%s</a>' % btn, s)

        # ---- nav-toggle aria label ----
        s = s.replace('aria-label="打开菜单"', 'aria-label="Toggle menu"')
        s = s.replace('aria-label="主导航"',
                      'aria-label="Main navigation"' if lang == "en" else 'aria-label="メインナビゲーション"')

        # ---- footer brand block variants ----
        brand_sfx = FOOTER_COLS[lang]["brand_suffix"]
        s = s.replace('<span class="brand-mark">庆丰</span>东莞市庆丰电工机械有限公司',
                      '<span class="brand-mark">%s</span>%s'
                      % ("QF" if lang == "en" else "慶豊", brand_sfx))
        s = s.replace('<span class="brand-mark">庆丰</span>庆丰电工机械',
                      '<span class="brand-mark">%s</span>%s'
                      % ("QF" if lang == "en" else "慶豊", BRAND_EN if lang == "en" else BRAND_JA))

        # ---- brand text (header logo link + generic company name) ----
        s = s.replace(">庆丰电工机械<", ">%s<" % (BRAND_EN if lang == "en" else BRAND_JA))
        s = s.replace(">东莞市庆丰电工机械有限公司<", ">%s<" % (FULL_CN if lang == "ja" and name == "index.html" else ("Dongguan Qingfeng Electrical Machinery Co., Ltd." if lang == "en" else FULL_CN)))

        # footer intro
        s = s.replace("成立于 2000 年，面向全球长期致力于电线、电缆、光缆等设备技术研发、制造、服务为一体的高科技企业。",
                      FOOTER_COLS[lang]["intro"])
        s = s.replace("成立于 2000 年，面向全球长期致力于电线、电缆、光缆等设备技术研发、制造、服务为一体的企业。",
                      FOOTER_COLS[lang]["intro"])

        # footer column titles
        for cn, en_jp in [("快速导航", FOOTER_COLS[lang]["col1"]),
                          ("产品系列", FOOTER_COLS[lang]["col2"]),
                          ("联系方式", FOOTER_COLS[lang]["col3"])]:
            s = s.replace(">%s</h4>" % cn, ">%s</h4>" % en_jp)

        # footer series list
        for cn, en_jp in zip(["挤出机系列", "绞线及成缆系列", "屏蔽系列", "光缆设备系列", "辅助设备系列"],
                             FOOTER_COLS[lang]["series"]):
            s = s.replace(">%s</a>" % cn, ">%s</a>" % en_jp)

        # footer contact labels
        for cn, en_jp in zip(["手机：", "香港办公室：", "邮箱：", "地址："],
                             ["%s: " % FOOTER_COLS[lang]["labels"][0],
                              "%s: " % FOOTER_COLS[lang]["labels"][1],
                              "%s: " % FOOTER_COLS[lang]["labels"][2],
                              "%s: " % FOOTER_COLS[lang]["labels"][3]]):
            s = s.replace(cn, en_jp)

        # footer bottom
        s = s.replace("东莞市庆丰电工机械有限公司 版权所有", FTR_MISC[lang][0])
        s = s.replace("专业提供押出机、绞线机、辐照设备、高频线缆包带机", FTR_MISC[lang][1])

        # ---- common UI buttons ----
        s = s.replace(">联系我们</a>", ">%s</a>" % btn)  # also nav cta already done; header fallback
        s = s.replace("查看详情", UI[lang]["details"])
        s = s.replace("了解更多", UI[lang]["learn"])
        s = s.replace("返回产品中心", UI[lang]["back"])
        s = s.replace("查看全部产品 →", UI[lang]["viewall"])
        s = s.replace("查看全部产品", UI[lang]["viewall"])

        # ---- common phrases (back links / category labels) ----
        # NOTE: applied AFTER per-page body translation (see below) so that
        # exact-match page pairs are not broken by partial replacements.

        # ---- rewrite resource paths ---- (moved after body/COMMON below)

        # ---- insert language switcher into header-cta ----
        s = s.replace('<div class="header-cta">',
                      '<div class="header-cta">' + lang_switch_html(lang, name), 1)

        # ---- title / meta : handled after COMMON replacements (see below) ----

# ---- body translation ----
        map_key = name
        body = BODY_EN if lang == "en" else BODY_JA
        if map_key in body:
            spec = body[map_key]
            if spec.get("h1"):
                s = re.sub(r"(<h1[^>]*>).*?(</h1>)",
                           lambda m: m.group(1) + spec["h1"] + m.group(2), s, count=1, flags=re.S)
            if spec.get("sub") is not None:
                s = re.sub(r'(<p style="color:#999;margin-bottom:28px;border-bottom:1px solid #eee;padding-bottom:20px">).*?(</p>)',
                           lambda m: m.group(1) + spec["sub"] + m.group(2), s, count=1, flags=re.S)
            if spec.get("main"):
                s = re.sub(r"<main>.*?</main>", "<main>" + spec["main"] + "</main>", s, count=1, flags=re.S)
            dv = spec.get("div")
            html = spec.get("html")
            if dv and html:
                s, ok = _replace_container(s, dv, html)
                if not ok:
                    print("WARN: container %s not found/replaced in %s" % (dv, name))
            pairs = spec.get("pairs")
            if pairs:
                for old, new in sorted(pairs, key=lambda p: -len(p[0])):
                    s = s.replace(old, new)

        # ---- accessible labels on carousel prev/next arrows ----
        def _set_arrow_label(tag, label):
            t = re.sub(r'\s+aria-label="[^"]*"', '', tag.group(0))
            if re.search(r'aria-label', t):
                return t
            return t[:-1] + ' aria-label="%s">' % label

        _prev, _next = ("Previous", "Next") if lang == "en" else ("前へ", "次へ")
        s = re.sub(r"<a\s+class=['\"]sprev['\"][^>]*>",
                   lambda m: _set_arrow_label(m, _prev), s)
        s = re.sub(r"<a\s+class=['\"]snext['\"][^>]*>",
                   lambda m: _set_arrow_label(m, _next), s)

        # ---- titles / news headings / logo mark / meta ----
        # (BEFORE COMMON so full titles are matched before partial phrases)
        for zh, tr in TITLES.get(lang, {}).items():
            s = s.replace(zh, tr)
        s = s.replace('<span class="brand-mark">庆丰</span>',
                      '<span class="brand-mark">%s</span>' % ("QF" if lang == "en" else "慶豊"))
        brand_full = "Dongguan Qingfeng Electrical Machinery Co., Ltd." if lang == "en" else FULL_CN
        brand_short = BRAND_EN if lang == "en" else BRAND_JA
        tm = re.search(r"<title>(.*?)</title>", s, re.S)
        if tm:
            nt = tm.group(1)
            nt = nt.replace("东莞市庆丰电工机械有限公司", brand_full)
            nt = nt.replace("庆丰电工机械", brand_short)
            nt = nt.replace("东莞市", "")
            s = s.replace(tm.group(0), "<title>%s</title>" % nt)

        def _fix_meta(mm):
            content = mm.group(2)
            if re.search(r"[\u4e00-\u9fff]", content):
                base = ""
                t2 = re.search(r"<title>(.*?)</title>", s, re.S)
                if t2:
                    base = re.split(r"\s+[-–|]\s+", t2.group(1))[0].strip()
                    if re.search(r"[\u4e00-\u9fff]", base):
                        base = ""
                generic = ("High-frequency &amp; high-speed wire and cable machinery manufacturer: extrusion, stranding, shielding and fiber-optic cable equipment." if lang == "en"
                           else "高周波・高速電線ケーブル設備メーカー。押出・撚線・シールド・光ケーブル設備を提供。")
                return mm.group(1) + ((base + ". ") if base else "") + generic + mm.group(3)
            return mm.group(0)

        s = re.sub(r'(<meta name="description" content=")(.*?)(")', _fix_meta, s, count=1)

        # ---- common phrases (back links / category labels / h1 variants) ----
        for cn, tr in COMMON[lang]:
            s = s.replace(cn, tr)

        # ---- rewrite resource paths (after body injection so injected
        #      assets/... refs also get the ../ prefix) ----
        s = rewrite_paths(s, lang)
        s = upgrade_links(s)
        s = fill_alts(s)

        # ---- write out ----
        out = OUT[lang] + name
        io.open(out, "w", encoding="utf-8").write(s)
        done += 1
    print("[%s] wrote %d pages into %s" % (lang, done, OUT[lang]))

def fill_alts(html):
    """Give content images an alt derived from the page h1 (per-language)."""
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not m:
        return html
    alt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    if not alt:
        return html
    if len(alt) > 120:
        alt = alt[:120].rstrip() + "..."
    alt = _html.escape(_html.unescape(alt), quote=True)
    return re.sub(r'<img\b([^>]*?)\s*alt\s*=\s*(?:""|\'\')',
                  lambda mm: '<img%s alt="%s"' % (mm.group(1), alt), html)

def upgrade_links(html):
    """Upgrade known http-only external links to https (both hosts support it)."""
    return (html.replace("http://www.wirechina.net/", "https://www.wirechina.net/")
                .replace("http://www.wire-india.com/", "https://www.wire-india.com/"))

def _apply_body(html, mapping):
    for old, new in mapping:
        html = html.replace(old, new)
    return html

def build_zh():
    """Inject the language switcher into the Chinese root pages (idempotent)."""
    done = 0
    for f in sorted(glob.glob(ROOT + "*.html")):
        name = os.path.basename(f)
        s = io.open(f, encoding="utf-8", errors="ignore").read()
        s = strip_lang_switch(s)
        s = upgrade_links(s)
        s = fill_alts(s)
        if '<div class="header-cta">' in s:
            s = s.replace('<div class="header-cta">',
                          '<div class="header-cta">' + lang_switch_html("zh", name), 1)
            io.open(f, "w", encoding="utf-8").write(s)
            done += 1
    print("[zh] injected switcher into %d pages" % done)


if __name__ == "__main__":
    import sys as _s
    only = _s.argv[1] if len(_s.argv) > 1 else "both"
    if only in ("both", "en"):
        build("en")
    if only in ("both", "ja"):
        build("ja")
    build_zh()