import streamlit as st
import json
from datetime import datetime

st.set_page_config(
    page_title="SC 3Dマシンガイダンス 刃先精度確認",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── カスタムCSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --komatsu-yellow: #FFD700;
    --komatsu-dark:   #1A1A1A;
    --komatsu-gray:   #2D2D2D;
    --komatsu-mid:    #3D3D3D;
    --accent-green:   #00C853;
    --accent-red:     #FF3D3D;
    --accent-blue:    #2196F3;
    --text-primary:   #F0F0F0;
    --text-secondary: #A0A0A0;
    --border:         #444;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--komatsu-dark) !important;
    color: var(--text-primary) !important;
    font-family: 'Noto Sans JP', sans-serif !important;
}

[data-testid="stSidebar"] {
    background-color: var(--komatsu-gray) !important;
    border-right: 2px solid var(--komatsu-yellow);
}

[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

h1, h2, h3 {
    font-family: 'Noto Sans JP', sans-serif !important;
    font-weight: 700 !important;
}

/* タイトルバー */
.title-bar {
    background: linear-gradient(135deg, #FFD700 0%, #FFA000 100%);
    color: #1A1A1A;
    padding: 20px 32px;
    border-radius: 12px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.title-bar h1 { color: #1A1A1A !important; font-size: 1.6rem !important; margin: 0 !important; }
.title-bar span { font-size: 0.85rem; opacity: 0.75; }

/* セクションヘッダー */
.section-header {
    background: var(--komatsu-gray);
    border-left: 4px solid var(--komatsu-yellow);
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
    margin: 20px 0 12px 0;
    font-weight: 700;
    font-size: 1.05rem;
    letter-spacing: 0.03em;
}

/* チェックカード */
.check-card {
    background: var(--komatsu-gray);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
}
.check-card:hover { border-color: var(--komatsu-yellow); }

/* 進捗バー */
.progress-outer {
    background: var(--komatsu-mid);
    border-radius: 999px;
    height: 10px;
    margin: 8px 0;
}
.progress-inner {
    background: linear-gradient(90deg, #FFD700, #FFA000);
    height: 10px;
    border-radius: 999px;
    transition: width 0.5s ease;
}

/* ステータスバッジ */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
}
.badge-ok  { background: rgba(0,200,83,0.2); color: #00C853; border: 1px solid #00C853; }
.badge-ng  { background: rgba(255,61,61,0.2); color: #FF3D3D; border: 1px solid #FF3D3D; }
.badge-na  { background: rgba(160,160,160,0.15); color: #A0A0A0; border: 1px solid #444; }

/* 数値入力フィールド */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: var(--komatsu-mid) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* チェックボックス */
[data-testid="stCheckbox"] label {
    color: var(--text-primary) !important;
    font-size: 0.9rem !important;
}

/* ボタン */
.stButton > button {
    background: var(--komatsu-yellow) !important;
    color: #1A1A1A !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-family: 'Noto Sans JP', sans-serif !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stSelectbox > div > div {
    background: var(--komatsu-mid) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 6px !important;
}

.alert-box {
    background: rgba(255,61,61,0.1);
    border: 1px solid #FF3D3D;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 12px 0;
    color: #FF3D3D;
    font-size: 0.9rem;
}
.info-box {
    background: rgba(33,150,243,0.1);
    border: 1px solid #2196F3;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 12px 0;
    color: #90CAF9;
    font-size: 0.9rem;
}
.success-box {
    background: rgba(0,200,83,0.1);
    border: 1px solid #00C853;
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
    color: #00C853;
    font-size: 0.95rem;
    font-weight: 600;
}

/* テーブル */
table { border-collapse: collapse; width: 100%; }
th { background: var(--komatsu-yellow); color: #1A1A1A; padding: 8px 12px; font-weight: 700; }
td { border: 1px solid var(--border); padding: 8px 12px; }
tr:nth-child(even) td { background: var(--komatsu-gray); }

/* divider */
hr { border-color: var(--border) !important; }

/* tooltip */
[data-testid="stTooltipHoverTarget"] { color: var(--komatsu-yellow) !important; }
</style>
""", unsafe_allow_html=True)

# ─── セッション初期化 ──────────────────────────────────────────
def init_session():
    defaults = {
        # 基本情報
        "info_date": datetime.now().strftime("%Y-%m-%d"),
        "info_time": datetime.now().strftime("%H:%M"),
        "info_checker": "",
        "info_user": "",
        "info_model": "",
        "info_machine_no": "",
        "info_sm": "",
        "info_bucket": "",
        "info_tooth_len": "",
        "info_correction": "NTTドコモRRS",
        "info_fw_ver": "",
        "info_app_ver": "",
        # GNSS精度
        "gnss_main_v_rms": "",
        "gnss_main_h_rms": "",
        "gnss_pdop": "",
        "gnss_delay": "",
        "gnss_baseline": "",
        "gnss_sub_v_rms": "",
        "gnss_sub_h_rms": "",
        # 基準点
        "ref_name": "",
        "ref_n": "", "ref_e": "", "ref_z": "",
        "ref_dir": "",
        # 刃先座標計測
        "blade_results": [{"姿勢": str(i+1), "N": "", "E": "", "Z": ""} for i in range(4)],
        # チェック結果
        "checks": {},
        # ネットワーク型 数値
        "net_antenna": "",
        "net_delay": "",
        "net_baseline": "",
        # 固定局 数値
        "fix_gnss_status": False,
        # 環境
        "env_hv_dist": "",
        "env_main_sat": "",
        "env_sub_sat": "",
        "env_sat_diff": "",
        # ページ
        "page": "事前確認",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─── チェックリスト定義 ────────────────────────────────────────
SECTIONS = {
    "kit": {
        "label": "■ レトロフィットキット装着関連",
        "items": [
            ("kit_01", "バケットIMUセンサは、取付説明書記載の通りに正しく装着できている（装着箇所、ガタつき、向き）"),
            ("kit_02", "アームIMUセンサは、取付説明書記載の通りに正しく装着できている（装着箇所、ガタつき、向き）"),
            ("kit_03", "ブームIMUセンサは、取付説明書記載の通りに正しく装着できている（装着箇所、ガタつき、向き）"),
            ("kit_04", "ボディIMUセンサは、取付説明書記載の通りに正しく装着できている（装着箇所、ガタつき、向き）"),
            ("kit_05", "IMUセンサ各部に損傷、変形、脱落は無い"),
            ("kit_06", "各部IMUセンサハーネスは、取付説明書記載の通りに正しく装着できている（コネクタ嵌合、水進入、内部腐食）"),
            ("kit_07", "ハーネス各部に、損傷、変形、脱落は無い"),
            ("kit_08", "GNSSアンテナは、取付説明書記載の通りに正しく装着できている（装着箇所、ガタつき、向き）"),
            ("kit_09", "GNSSアンテナケーブルは、取付説明書記載の通りに正しく装着できている（コネクタ芯形状、緩み）"),
            ("kit_10", "コントローラは、取付説明書記載の通りに正しく装着できている"),
            ("kit_11", "GNSSアンテナやコントローラに損傷、変形、脱落は無い"),
            ("kit_12", "コントローラのファームウェアは最新である"),
            ("kit_13", "タブレットアプリは最新バージョンである"),
            ("kit_14", "使用時コントローラのLEDランプは「5G」を除き全て点灯している（2.4G、POWER、POS、LINK、MODE）"),
        ]
    },
    "gnss_env": {
        "label": "■ GNSS取得環境関連",
        "items": [
            ("env_01", "上空視界が開けた屋外に居る"),
            ("env_02", "高圧電線の直下もしくは付近ではない"),
            ("env_03", "付近に空港や変電所などの電波環境に影響を与える施設は無い"),
            ("env_04", "ビルや崖・壁面の付近などマルチパスの影響を受けるような場所ではない"),
            ("env_05", "メインアンテナのGNSS衛星補足数は「０」ではない"),
            ("env_06", "サブアンテナのGNSS衛星補足数は「０」ではない"),
            ("env_07", "メインアンテナとサブアンテナの衛星補足数に大きな差異は無い"),
        ]
    },
    "net": {
        "label": "■ GNSS補正情報関連（ネットワーク型：ドコモ等）",
        "items": [
            ("net_01", "携帯電波圏内で電波強度も良好に安定して4G・LTE通信が出来ている"),
            ("net_02", "補正情報は遅延無く正しく受信できている"),
            ("net_03", "メインアンテナ・サブアンテナともにFIX出来てGNSSステータスも緑色である"),
            ("net_04", "ベースライン間距離は10km以内である（10kmを超えない）"),
        ]
    },
    "fixed": {
        "label": "■ GNSS補正情報関連（固定局使用時）",
        "items": [
            ("fix_01", "固定局の電源はONになっている"),
            ("fix_02", "固定局は正しく設置できている（三脚、傾き、基準点中心、設置場所の上空視界、電波遮蔽物）"),
            ("fix_03", "固定局設定は正しくできている（設置高さ、設置基準点座標、送信チャンネル、RTCM）"),
            ("fix_04", "車載無線機の電源はONになっている"),
            ("fix_05", "無線機のチャンネル設定は合っている"),
            ("fix_06", "無線機コントローラ画面中にPマークが一定間隔で点滅している（アルインコ製デジタル無線機の場合）"),
            ("fix_07", "メインアンテナ・サブアンテナともにFIX出来てGNSSステータスも緑色である"),
            ("fix_08", "その他に無線機を搭載した車両の往来は無い"),
        ]
    },
    "project": {
        "label": "■ プロジェクトファイル関連",
        "items": [
            ("prj_01", "建機側で設定している補正情報と同じ内容でローカライゼーションを実施したプロジェクトファイルである"),
            ("prj_02", "使用しているプロジェクトファイルの基準点情報に間違いは無い"),
            ("prj_03", "選択しているプロジェクトファイルは間違いなく合っている"),
            ("prj_04", "同じプロジェクトファイルを使用して他の車両で刃先精度確認しても精度に問題は無い"),
            ("prj_05", "ｉ建機・他レトロなど含む刃先精度確認実績のあるプロジェクトファイルだ"),
            ("prj_06", "設計データの描画表示もイメージと合っている（形状、高さ、向き）"),
            ("prj_07", "画面に描画されている作業機姿勢は、実際の作業機姿勢と合っている（静止、動作、追従）"),
            ("prj_08", "車体の傾きも正しく画面上に表示されている（ピッチ、ロール）"),
        ]
    },
    "settings": {
        "label": "■ 各種設定関連",
        "items": [
            ("set_01", "補正情報の設定内容に間違いは無い（RRS/VRS、固定局、Ntrip）"),
            ("set_02", "補正情報は遅延無く正しく受信できている（0～1s）"),
            ("set_03", "使用する衛星種類を減らしても変わらない（Galileo、Beidou、QZSS）"),
            ("set_04", "バケットファイル選択は実際に装着しているものと同一で間違っていない"),
            ("set_05", "選択しているバケットファイル内各部寸法数値に間違いは無い"),
            ("set_06", "バケットファイルは正しく作成できている（ATTカプラー、ツース盤、平刃、底板補強）"),
            ("set_07", "ツース摩耗量入力に異常値は入っていない"),
            ("set_08", "刃先精度確認画面でのマッチング項にオフセット数値は入っていない（念のためリセットも実施）"),
        ]
    },
}

# ─── サイドバー ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏗️ SC 3Dマシンガイダンス")
    st.markdown("**刃先精度確認システム**")
    st.markdown("---")

    pages = ["事前確認チェック", "刃先座標チェック", "サマリー・レポート"]
    page = st.radio("ページ選択", pages, index=0)
    st.markdown("---")

    # 進捗表示
    all_items = []
    for sec in SECTIONS.values():
        for key, _ in sec["items"]:
            all_items.append(key)

    checked = sum(1 for k in all_items if st.session_state.checks.get(k) == "OK")
    total = len(all_items)
    pct = int(checked / total * 100) if total else 0

    st.markdown(f"**確認進捗: {checked}/{total} ({pct}%)**")
    st.markdown(f"""
    <div class="progress-outer">
        <div class="progress-inner" style="width:{pct}%"></div>
    </div>
    """, unsafe_allow_html=True)

    ng_items = [k for k in all_items if st.session_state.checks.get(k) == "NG"]
    if ng_items:
        st.markdown(f'<div class="alert-box">⚠️ NG項目: {len(ng_items)}件</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 全リセット"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ─── タイトルバー ──────────────────────────────────────────────
st.markdown(f"""
<div class="title-bar">
    <div>
        <h1>SC 3Dマシンガイダンス　刃先精度不良確認</h1>
        <span>3D Machine Guidance Blade Tip Accuracy Check System　｜　{datetime.now().strftime('%Y年%m月%d日')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
if page == "事前確認チェック":
# ═══════════════════════════════════════════════════════════════

    # 基本情報
    st.markdown('<div class="section-header">📋 基本情報</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.session_state.info_date = st.text_input("確認日", st.session_state.info_date)
    with c2:
        st.session_state.info_time = st.text_input("時刻", st.session_state.info_time)
    with c3:
        st.session_state.info_checker = st.text_input("確認者氏名", st.session_state.info_checker)
    with c4:
        st.session_state.info_user = st.text_input("ユーザー名", st.session_state.info_user)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.session_state.info_model = st.text_input("機種・型式", st.session_state.info_model)
    with c2:
        st.session_state.info_machine_no = st.text_input("機番 #", st.session_state.info_machine_no)
    with c3:
        st.session_state.info_sm = st.text_input("サービスメータ (h)", st.session_state.info_sm)
    with c4:
        st.session_state.info_bucket = st.text_input("装着バケット", st.session_state.info_bucket)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.info_tooth_len = st.text_input("ツース長さ (mm)", st.session_state.info_tooth_len)
    with c2:
        st.session_state.info_fw_ver = st.text_input("FWバージョン", st.session_state.info_fw_ver)
    with c3:
        st.session_state.info_app_ver = st.text_input("アプリバージョン", st.session_state.info_app_ver)

    c1, c2 = st.columns(2)
    with c1:
        st.session_state.info_correction = st.selectbox(
            "補正情報",
            ["NTTドコモRRS", "ネットワーク型（その他）", "固定局（無線）", "固定局（有線）"],
            index=["NTTドコモRRS", "ネットワーク型（その他）", "固定局（無線）", "固定局（有線）"].index(st.session_state.info_correction)
        )

    st.markdown("---")

    # ─── チェックリスト描画 ─────────────────────────────────────
    def render_section(sec_key, sec_data, skip_fixed=False, skip_net=False):
        st.markdown(f'<div class="section-header">{sec_data["label"]}</div>', unsafe_allow_html=True)

        if sec_key == "net" and skip_net:
            st.markdown('<div class="info-box">ℹ️ ネットワーク型は使用していません（固定局使用）</div>', unsafe_allow_html=True)
            return
        if sec_key == "fixed" and skip_fixed:
            st.markdown('<div class="info-box">ℹ️ 固定局は使用していません（ネットワーク型使用）</div>', unsafe_allow_html=True)
            return

        for key, label in sec_data["items"]:
            current = st.session_state.checks.get(key, "未確認")
            cols = st.columns([6, 1, 1, 1])
            with cols[0]:
                st.markdown(f"<small>{'▶ ' if current == 'NG' else '　'}{label}</small>", unsafe_allow_html=True)
            with cols[1]:
                if st.button("✅ OK", key=f"ok_{key}", use_container_width=True):
                    st.session_state.checks[key] = "OK"
                    st.rerun()
            with cols[2]:
                if st.button("❌ NG", key=f"ng_{key}", use_container_width=True):
                    st.session_state.checks[key] = "NG"
                    st.rerun()
            with cols[3]:
                badge = {"OK": '<span class="badge badge-ok">OK</span>',
                         "NG": '<span class="badge badge-ng">NG</span>',
                         "未確認": '<span class="badge badge-na">未</span>'}.get(current, "")
                st.markdown(badge, unsafe_allow_html=True)

            # 数値入力が必要な項目
            if key == "kit_12":
                v = st.text_input("　FWバージョン記入", st.session_state.info_fw_ver, key="fw_v2", label_visibility="collapsed")
                st.session_state.info_fw_ver = v
            if key == "kit_13":
                v = st.text_input("　アプリバージョン記入", st.session_state.info_app_ver, key="app_v2", label_visibility="collapsed")
                st.session_state.info_app_ver = v
            if key == "env_02":
                st.session_state.env_hv_dist = st.text_input("　離隔距離 (m)", st.session_state.env_hv_dist, key=f"hv_{key}")
            if key == "env_05":
                st.session_state.env_main_sat = st.text_input("　メインアンテナ利用衛星数 (個)", st.session_state.env_main_sat, key=f"ms_{key}")
            if key == "env_06":
                st.session_state.env_sub_sat = st.text_input("　サブアンテナ利用衛星数 (個)", st.session_state.env_sub_sat, key=f"ss_{key}")
            if key == "env_07":
                st.session_state.env_sat_diff = st.text_input("　衛星数差異 (個)", st.session_state.env_sat_diff, key=f"sd_{key}")
            if key == "net_01":
                st.session_state.net_antenna = st.text_input("　アンテナ本数", st.session_state.net_antenna, key=f"na_{key}")
            if key == "net_02" and sec_key == "net":
                st.session_state.net_delay = st.text_input("　補正情報遅延時間 (s)", st.session_state.net_delay, key=f"nd_{key}")
            if key == "net_04":
                st.session_state.net_baseline = st.text_input("　ベースライン間距離 (m)", st.session_state.net_baseline, key=f"nb_{key}")

    is_fixed = "固定局" in st.session_state.info_correction
    is_net   = not is_fixed

    render_section("kit",      SECTIONS["kit"])
    render_section("gnss_env", SECTIONS["gnss_env"])
    render_section("net",      SECTIONS["net"],   skip_net=is_fixed)
    render_section("fixed",    SECTIONS["fixed"], skip_fixed=is_net)
    render_section("project",  SECTIONS["project"])
    render_section("settings", SECTIONS["settings"])

    # ─── NG警告まとめ ───────────────────────────────────────────
    ng_keys = [k for k in st.session_state.checks if st.session_state.checks[k] == "NG"]
    if ng_keys:
        st.markdown("---")
        st.markdown("### ⚠️ NG項目 一覧")
        for sec_key, sec_data in SECTIONS.items():
            ng_in_sec = [(k, l) for k, l in sec_data["items"] if k in ng_keys]
            if ng_in_sec:
                st.markdown(f"**{sec_data['label']}**")
                for k, l in ng_in_sec:
                    st.markdown(f'<div class="alert-box">❌ {l}</div>', unsafe_allow_html=True)

    all_checked = sum(1 for k in [i[0] for s in SECTIONS.values() for i in s["items"]] if st.session_state.checks.get(k) in ["OK", "NG"])
    if all_checked > 0 and not ng_keys:
        st.markdown('<div class="success-box">✅ 全チェック項目：問題なし。次のシートへ進んでください。</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
elif page == "刃先座標チェック":
# ═══════════════════════════════════════════════════════════════

    st.markdown('<div class="section-header">📐 GNSS精度情報</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.session_state.gnss_main_v_rms = st.text_input("メインGNSS垂直精度RMS [m]", st.session_state.gnss_main_v_rms)
        st.session_state.gnss_main_h_rms = st.text_input("メインGNSS水平精度RMS [m]", st.session_state.gnss_main_h_rms)
    with c2:
        st.session_state.gnss_pdop       = st.text_input("PDOP", st.session_state.gnss_pdop)
        st.session_state.gnss_delay      = st.text_input("遅延時間 [s]", st.session_state.gnss_delay)
    with c3:
        st.session_state.gnss_baseline   = st.text_input("ベースライン間距離 [m]", st.session_state.gnss_baseline)
        st.session_state.gnss_sub_v_rms  = st.text_input("サブGNSS垂直精度RMS [m]", st.session_state.gnss_sub_v_rms)
        st.session_state.gnss_sub_h_rms  = st.text_input("サブGNSS水平精度RMS [m]", st.session_state.gnss_sub_h_rms)

    st.markdown('<div class="section-header">📍 基準点情報</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.ref_name = st.text_input("基準点名", st.session_state.ref_name)
        c_n, c_e, c_z = st.columns(3)
        with c_n: st.session_state.ref_n = st.text_input("N", st.session_state.ref_n)
        with c_e: st.session_state.ref_e = st.text_input("E", st.session_state.ref_e)
        with c_z: st.session_state.ref_z = st.text_input("Z", st.session_state.ref_z)
    with c2:
        st.session_state.ref_dir = st.text_input("基準点への向き・方位 (N方位等)", st.session_state.ref_dir)
        st.markdown('<div class="info-box">💡 方位は pilotアプリ 3D表示で確認してください</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📊 刃先座標計測結果（差分入力）　※ 座標ではなく「差分」の値を入力</div>', unsafe_allow_html=True)
    st.markdown("各姿勢における計測値（N/E/Z 差分）と作業機姿勢画像を入力してください。許容値 **±0.05m（±5cm）**")

    THRESHOLD = 0.05

    if "posture_images" not in st.session_state:
        st.session_state.posture_images = [None, None, None, None]

    for i, row in enumerate(st.session_state.blade_results):
        with st.container():
            st.markdown(
                f"<div style='background:var(--komatsu-gray);border:1px solid var(--border);"
                f"border-left:4px solid var(--komatsu-yellow);border-radius:8px;"
                f"padding:10px 16px;margin-bottom:8px;font-weight:700;'>📐 姿勢 {i+1}</div>",
                unsafe_allow_html=True
            )
            col_vals, col_img = st.columns([3, 2])

            with col_vals:
                c1, c2, c3, c4 = st.columns([3, 3, 3, 2])
                with c1:
                    n_val = st.text_input("N差分 (m)", row["N"], key=f"n_{i}", placeholder="例: 0.012")
                    st.session_state.blade_results[i]["N"] = n_val
                with c2:
                    e_val = st.text_input("E差分 (m)", row["E"], key=f"e_{i}", placeholder="例: -0.023")
                    st.session_state.blade_results[i]["E"] = e_val
                with c3:
                    z_val = st.text_input("Z差分 (m)", row["Z"], key=f"z_{i}", placeholder="例: 0.008")
                    st.session_state.blade_results[i]["Z"] = z_val
                with c4:
                    st.markdown("<br>", unsafe_allow_html=True)
                    try:
                        n_f, e_f, z_f = float(n_val), float(e_val), float(z_val)
                        all_ok = all(abs(v) <= THRESHOLD for v in [n_f, e_f, z_f])
                        if all_ok:
                            st.markdown('<span class="badge badge-ok">✅ OK<br>±5cm以内</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="badge badge-ng">❌ NG<br>超過</span>', unsafe_allow_html=True)
                    except Exception:
                        st.markdown('<span class="badge badge-na">未入力</span>', unsafe_allow_html=True)

                try:
                    n_f, e_f, z_f = float(n_val), float(e_val), float(z_val)
                    cols_d = st.columns(3)
                    for col_d, label_d, val_d in zip(cols_d, ["N", "E", "Z"], [n_f, e_f, z_f]):
                        color_d = "#00C853" if abs(val_d) <= THRESHOLD else "#FF3D3D"
                        with col_d:
                            st.markdown(
                                f"<div style='text-align:center;background:var(--komatsu-mid);"
                                f"border-radius:6px;padding:6px 4px;margin-top:6px;'>"
                                f"<div style='font-size:0.7rem;color:var(--text-secondary);'>{label_d}差分</div>"
                                f"<div style='font-size:1.1rem;font-weight:700;color:{color_d};"
                                f"font-family:monospace;'>{val_d:+.4f}m</div></div>",
                                unsafe_allow_html=True
                            )
                except Exception:
                    pass

            with col_img:
                st.markdown(f"**📷 姿勢{i+1} 作業機写真**")
                st.markdown(
                    "<div style='font-size:0.78rem;color:var(--text-secondary);margin-bottom:6px;'>"
                    "全体および作業機接地部が分かる写真をアップロード</div>",
                    unsafe_allow_html=True
                )
                uploaded = st.file_uploader(
                    f"姿勢{i+1}の写真",
                    type=["jpg", "jpeg", "png"],
                    key=f"img_{i}",
                    label_visibility="collapsed"
                )
                if uploaded is not None:
                    st.session_state.posture_images[i] = uploaded.read()

                if st.session_state.posture_images[i] is not None:
                    st.image(
                        st.session_state.posture_images[i],
                        caption=f"姿勢{i+1} 作業機姿勢",
                        use_container_width=True
                    )
                    st.markdown('<span class="badge badge-ok">📷 画像登録済み</span>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        "<div style='border:2px dashed #444;border-radius:8px;"
                        "padding:32px;text-align:center;color:#A0A0A0;'>"
                        "📷<br><span style='font-size:0.85rem;'>写真をアップロード</span><br>"
                        "<span style='font-size:0.75rem;'>JPG / PNG</span></div>",
                        unsafe_allow_html=True
                    )

    # 傾向分析
    st.markdown("---")
    st.markdown("### 📈 傾向分析")
    ns, es, zs = [], [], []
    for row in st.session_state.blade_results:
        try:
            ns.append(float(row["N"])); es.append(float(row["E"])); zs.append(float(row["Z"]))
        except:
            pass

    if ns and es and zs:
        import statistics
        col1, col2, col3 = st.columns(3)
        def metric_card(label, vals, col):
            avg = statistics.mean(vals)
            rng = max(vals) - min(vals)
            ok = all(abs(v) <= THRESHOLD for v in vals)
            with col:
                color = "#00C853" if ok else "#FF3D3D"
                st.markdown(f"""
                <div style="background:var(--komatsu-gray);border:1px solid {color};border-radius:8px;padding:12px;text-align:center;">
                    <div style="font-size:0.8rem;color:var(--text-secondary);">{label}</div>
                    <div style="font-size:1.5rem;font-weight:700;color:{color};font-family:'JetBrains Mono',monospace;">{avg:+.4f}m</div>
                    <div style="font-size:0.75rem;color:var(--text-secondary);">平均 | 範囲: {rng:.4f}m</div>
                </div>
                """, unsafe_allow_html=True)

        metric_card("N（前後方向）", ns, col1)
        metric_card("E（左右方向）", es, col2)
        metric_card("Z（高さ方向）", zs, col3)

        # 傾向コメント
        tips = []
        avg_n, avg_e, avg_z = statistics.mean(ns), statistics.mean(es), statistics.mean(zs)
        if abs(avg_n) > THRESHOLD:
            tips.append(f"N方向（前後）に {avg_n:+.3f}m の系統的なズレ → 車体前後キャリブレーション要確認")
        if abs(avg_e) > THRESHOLD:
            tips.append(f"E方向（左右）に {avg_e:+.3f}m の系統的なズレ → GNSSアンテナ左右取付位置・向き要確認")
        if abs(avg_z) > THRESHOLD:
            tips.append(f"Z方向（高さ）に {avg_z:+.3f}m のズレ → ツース長さ・バケットファイル設定要確認")
        rng_n = max(ns) - min(ns)
        if rng_n > 0.03:
            tips.append(f"N方向のばらつき {rng_n:.3f}m が大きい → IMUセンサ振れ・ドリフト疑い")

        if tips:
            for t in tips:
                st.markdown(f'<div class="alert-box">⚠️ {t}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">✅ 全姿勢 ±5cm以内。刃先精度は正常範囲です。</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">計測値を入力すると傾向分析が表示されます</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
elif page == "サマリー・レポート":
# ═══════════════════════════════════════════════════════════════

    st.markdown('<div class="section-header">📋 確認サマリー</div>', unsafe_allow_html=True)

    # 基本情報カード
    st.markdown(f"""
    <table>
    <tr><th>確認日時</th><td>{st.session_state.info_date} {st.session_state.info_time}</td>
        <th>確認者</th><td>{st.session_state.info_checker}</td></tr>
    <tr><th>ユーザー</th><td>{st.session_state.info_user}</td>
        <th>機種・機番</th><td>{st.session_state.info_model} #{st.session_state.info_machine_no}</td></tr>
    <tr><th>バケット</th><td>{st.session_state.info_bucket}</td>
        <th>ツース長</th><td>{st.session_state.info_tooth_len} mm</td></tr>
    <tr><th>補正情報</th><td>{st.session_state.info_correction}</td>
        <th>FW Ver.</th><td>{st.session_state.info_fw_ver}</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # チェック結果サマリー
    total_all = sum(len(v["items"]) for v in SECTIONS.values())
    ok_all    = sum(1 for k in st.session_state.checks if st.session_state.checks[k] == "OK")
    ng_all    = sum(1 for k in st.session_state.checks if st.session_state.checks[k] == "NG")
    skip_all  = total_all - ok_all - ng_all

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, color in [
        (c1, "総項目数", total_all, "#A0A0A0"),
        (c2, "OK", ok_all, "#00C853"),
        (c3, "NG", ng_all, "#FF3D3D"),
        (c4, "未確認", skip_all, "#FFA000"),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:var(--komatsu-gray);border:1px solid {color};border-radius:8px;
                        padding:16px;text-align:center;margin-bottom:12px;">
                <div style="font-size:0.8rem;color:var(--text-secondary);">{label}</div>
                <div style="font-size:2.2rem;font-weight:700;color:{color};">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    # セクション別
    st.markdown("### セクション別 結果")
    for sec_key, sec_data in SECTIONS.items():
        items = sec_data["items"]
        ok_c  = sum(1 for k, _ in items if st.session_state.checks.get(k) == "OK")
        ng_c  = sum(1 for k, _ in items if st.session_state.checks.get(k) == "NG")
        tot   = len(items)
        color = "#FF3D3D" if ng_c > 0 else "#00C853" if ok_c == tot else "#FFA000"
        st.markdown(f"""
        <div style="background:var(--komatsu-gray);border-left:4px solid {color};
                    border-radius:0 8px 8px 0;padding:10px 16px;margin-bottom:8px;
                    display:flex;justify-content:space-between;align-items:center;">
            <span>{sec_data['label']}</span>
            <span>
                <span class="badge badge-ok">{ok_c} OK</span>&nbsp;
                {'<span class="badge badge-ng">' + str(ng_c) + ' NG</span>' if ng_c else ''}
                &nbsp;<span class="badge badge-na">{tot - ok_c - ng_c} 未</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    # 刃先座標結果
    st.markdown("### 刃先座標計測結果")
    st.markdown("""
    <table>
    <tr><th>姿勢</th><th>N差分 (m)</th><th>E差分 (m)</th><th>Z差分 (m)</th><th>判定</th></tr>
    """, unsafe_allow_html=True)

    THRESHOLD = 0.05
    rows_html = ""
    for row in st.session_state.blade_results:
        try:
            n_f, e_f, z_f = float(row["N"]), float(row["E"]), float(row["Z"])
            ok = all(abs(v) <= THRESHOLD for v in [n_f, e_f, z_f])
            judge = '<span class="badge badge-ok">OK</span>' if ok else '<span class="badge badge-ng">NG</span>'
            rows_html += f"<tr><td>{row['姿勢']}</td><td>{n_f:+.4f}</td><td>{e_f:+.4f}</td><td>{z_f:+.4f}</td><td>{judge}</td></tr>"
        except:
            rows_html += f"<tr><td>{row['姿勢']}</td><td>-</td><td>-</td><td>-</td><td><span class='badge badge-na'>未入力</span></td></tr>"

    st.markdown(rows_html + "</table>", unsafe_allow_html=True)

    # 作業機姿勢画像サマリー
    st.markdown("### 📷 作業機姿勢画像")
    imgs = st.session_state.get("posture_images", [None, None, None, None])
    if any(img is not None for img in imgs):
        img_cols = st.columns(4)
        for i, (col, img) in enumerate(zip(img_cols, imgs)):
            with col:
                if img is not None:
                    st.image(img, caption=f"姿勢 {i+1}", use_container_width=True)
                    st.markdown('<span class="badge badge-ok">📷 登録済み</span>', unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"<div style='border:2px dashed #444;border-radius:8px;padding:24px;"
                        f"text-align:center;color:#A0A0A0;'>📷<br><small>姿勢{i+1} 未登録</small></div>",
                        unsafe_allow_html=True
                    )
    else:
        st.markdown('<div class="info-box">💡 刃先座標チェックページで各姿勢の写真をアップロードすると、ここに表示されます</div>', unsafe_allow_html=True)


    # JSONダウンロード
    st.markdown("---")
    st.markdown("### 💾 データ出力")

    report_data = {
        "生成日時": datetime.now().isoformat(),
        "基本情報": {
            "確認日": st.session_state.info_date,
            "時刻":   st.session_state.info_time,
            "確認者": st.session_state.info_checker,
            "ユーザー": st.session_state.info_user,
            "機種型式": st.session_state.info_model,
            "機番": st.session_state.info_machine_no,
            "サービスメータ(h)": st.session_state.info_sm,
            "バケット": st.session_state.info_bucket,
            "ツース長(mm)": st.session_state.info_tooth_len,
            "補正情報": st.session_state.info_correction,
            "FWバージョン": st.session_state.info_fw_ver,
            "アプリバージョン": st.session_state.info_app_ver,
        },
        "チェック結果": st.session_state.checks,
        "GNSS精度": {
            "メイン垂直RMS": st.session_state.gnss_main_v_rms,
            "メイン水平RMS": st.session_state.gnss_main_h_rms,
            "PDOP": st.session_state.gnss_pdop,
            "遅延時間": st.session_state.gnss_delay,
            "ベースライン距離": st.session_state.gnss_baseline,
            "サブ垂直RMS": st.session_state.gnss_sub_v_rms,
            "サブ水平RMS": st.session_state.gnss_sub_h_rms,
        },
        "基準点": {
            "名称": st.session_state.ref_name,
            "N": st.session_state.ref_n,
            "E": st.session_state.ref_e,
            "Z": st.session_state.ref_z,
            "方位": st.session_state.ref_dir,
        },
        "刃先座標計測": st.session_state.blade_results,
    }

    json_str = json.dumps(report_data, ensure_ascii=False, indent=2)
    fname = f"刃先精度確認_{st.session_state.info_date}_{st.session_state.info_model}_{st.session_state.info_machine_no}.json"

    st.download_button(
        label="📥 JSONレポートをダウンロード",
        data=json_str.encode("utf-8"),
        file_name=fname,
        mime="application/json",
    )
    st.markdown('<div class="info-box">💡 ダウンロードしたJSONは次回読み込みや解析ツールへの入力に利用できます</div>', unsafe_allow_html=True)
