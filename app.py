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

h1, h2, h3 { font-family: 'Noto Sans JP', sans-serif !important; font-weight: 700 !important; }

.title-bar {
    background: linear-gradient(135deg, #FFD700 0%, #FFA000 100%);
    color: #1A1A1A; padding: 20px 32px; border-radius: 12px;
    margin-bottom: 24px; display: flex; align-items: center; gap: 16px;
}
.title-bar h1 { color: #1A1A1A !important; font-size: 1.6rem !important; margin: 0 !important; }
.title-bar span { font-size: 0.85rem; opacity: 0.75; }

.section-header {
    background: var(--komatsu-gray); border-left: 4px solid var(--komatsu-yellow);
    padding: 10px 16px; border-radius: 0 8px 8px 0; margin: 20px 0 12px 0;
    font-weight: 700; font-size: 1.05rem; letter-spacing: 0.03em;
}

.progress-outer { background: var(--komatsu-mid); border-radius: 999px; height: 10px; margin: 8px 0; }
.progress-inner { background: linear-gradient(90deg, #FFD700, #FFA000); height: 10px; border-radius: 999px; transition: width 0.5s ease; }

.badge { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 0.78rem; font-weight: 600; }
.badge-ok  { background: rgba(0,200,83,0.2);   color: #00C853; border: 1px solid #00C853; }
.badge-ng  { background: rgba(255,61,61,0.2);  color: #FF3D3D; border: 1px solid #FF3D3D; }
.badge-na  { background: rgba(160,160,160,0.15); color: #A0A0A0; border: 1px solid #444; }

.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: var(--komatsu-mid) !important; border: 1px solid var(--border) !important;
    color: var(--text-primary) !important; border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stCheckbox"] label { color: var(--text-primary) !important; font-size: 0.9rem !important; }

.stButton > button {
    background: var(--komatsu-yellow) !important; color: #1A1A1A !important;
    font-weight: 700 !important; border: none !important; border-radius: 8px !important;
    padding: 10px 24px !important; font-family: 'Noto Sans JP', sans-serif !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stSelectbox > div > div {
    background: var(--komatsu-mid) !important; border: 1px solid var(--border) !important;
    color: var(--text-primary) !important; border-radius: 6px !important;
}

.alert-box {
    background: rgba(255,61,61,0.1); border: 1px solid #FF3D3D; border-radius: 8px;
    padding: 12px 16px; margin: 12px 0; color: #FF3D3D; font-size: 0.9rem;
}
.info-box {
    background: rgba(33,150,243,0.1); border: 1px solid #2196F3; border-radius: 8px;
    padding: 12px 16px; margin: 12px 0; color: #90CAF9; font-size: 0.9rem;
}
.success-box {
    background: rgba(0,200,83,0.1); border: 1px solid #00C853; border-radius: 8px;
    padding: 16px; margin: 12px 0; color: #00C853; font-size: 0.95rem; font-weight: 600;
}

table { border-collapse: collapse; width: 100%; }
th { background: var(--komatsu-yellow); color: #1A1A1A; padding: 8px 12px; font-weight: 700; }
td { border: 1px solid var(--border); padding: 8px 12px; }
tr:nth-child(even) td { background: var(--komatsu-gray); }
hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ─── セッション初期化 ──────────────────────────────────────────
def init_session():
    defaults = {
        "info_date": datetime.now().strftime("%Y-%m-%d"),
        "info_time": datetime.now().strftime("%H:%M"),
        "info_checker": "", "info_user": "", "info_model": "",
        "info_machine_no": "", "info_sm": "", "info_bucket": "",
        "info_tooth_len": "", "info_correction": "NTTドコモRRS",
        "info_fw_ver": "", "info_app_ver": "",
        "gnss_main_v_rms": "", "gnss_main_h_rms": "", "gnss_pdop": "",
        "gnss_delay": "", "gnss_baseline": "", "gnss_sub_v_rms": "", "gnss_sub_h_rms": "",
        "ref_name": "", "ref_n": "", "ref_e": "", "ref_z": "", "ref_dir": "",
        "blade_results": [{"姿勢": str(i+1), "N": "", "E": "", "Z": ""} for i in range(4)],
        "checks": {},
        "net_antenna": "", "net_delay": "", "net_baseline": "",
        "env_hv_dist": "", "env_main_sat": "", "env_sub_sat": "", "env_sat_diff": "",
        # フローチャート用
        "flow_step": 0,
        "flow_answers": {},
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

# ─── 診断フローチャートデータ ──────────────────────────────────
# ノード構造: {id, text, yes→, no→, leaf(原因+対策)}
FLOW_NODES = {
    "start": {
        "text": "刃先精度が±5cm以内に収まらない",
        "question": "GNSSステータスは緑色（FIX）になっていますか？",
        "yes": "fix_ok", "no": "fix_ng"
    },
    "fix_ng": {
        "question": "補正情報（ドコモ/固定局）は受信できていますか？",
        "yes": "corr_ok_fixng", "no": "corr_ng"
    },
    "corr_ng": {
        "leaf": True,
        "cause": "補正情報が届いていない",
        "actions": [
            "ドコモ回線：電波状態・SIM確認、Ntrip設定（ID/PW/マウント）確認",
            "固定局：電源ON、チャンネル一致、無線機のPマーク点滅確認",
            "ベースライン距離が10km以内か確認",
            "GNSSアンテナケーブルのコネクタ緩み・断線確認",
        ]
    },
    "corr_ok_fixng": {
        "leaf": True,
        "cause": "補正情報は受信しているがFIXしない",
        "actions": [
            "上空視界の確認（衛星数が十分か）",
            "マルチパス環境（建物・崖）からの移動",
            "高圧電線・変電所の付近でないか確認",
            "衛星種類を一部無効化して再試行（Galileo/Beidou/QZSS）",
            "アンテナの向き・取付位置の再確認",
        ]
    },
    "fix_ok": {
        "question": "全姿勢で誤差の方向・大きさがほぼ一定（系統誤差）ですか？",
        "yes": "systematic", "no": "random"
    },
    "random": {
        "question": "姿勢によって誤差の方向がバラバラ（ランダム）ですか？",
        "yes": "imu_check", "no": "intermit"
    },
    "intermit": {
        "leaf": True,
        "cause": "間欠的・不定期な誤差",
        "actions": [
            "GNSSの補正情報遅延時間を確認（1s以内が目標）",
            "IMUハーネスの断線・コネクタ緩みを確認",
            "バイブレーション・衝撃によるIMUセンサのガタつき確認",
            "タブレット～コントローラ間のBluetooth/Wi-Fi接続安定性確認",
        ]
    },
    "imu_check": {
        "question": "作業機の画面追従（動き）は正確に同期していますか？",
        "yes": "gnss_multipath", "no": "imu_ng"
    },
    "imu_ng": {
        "leaf": True,
        "cause": "IMUセンサの取付不良・故障の疑い",
        "actions": [
            "各IMUセンサの取付箇所・方向・ガタつきを再確認",
            "IMUセンサハーネスのコネクタ嵌合・断線・腐食を確認",
            "センサ交換して改善するか確認",
            "ファームウェアを最新版に更新",
        ]
    },
    "gnss_multipath": {
        "leaf": True,
        "cause": "GNSSのマルチパス・環境ノイズの疑い",
        "actions": [
            "測定場所を開けた場所へ移動",
            "建物・クレーン等の反射物から離れる",
            "PDOP値を確認（3.0以下が望ましい）",
            "時間帯を変えて衛星配置が改善するか確認",
        ]
    },
    "systematic": {
        "question": "Z方向（高さ）に系統的なズレがありますか？",
        "yes": "z_error", "no": "xy_error"
    },
    "z_error": {
        "question": "ツース長・バケットファイルは正確に設定されていますか？",
        "yes": "z_gnss", "no": "z_bucket"
    },
    "z_bucket": {
        "leaf": True,
        "cause": "バケット設定値の誤り（Z方向）",
        "actions": [
            "ツース長さを実測して正確な値を入力",
            "バケットファイルの各部寸法（刃先位置）を再確認・修正",
            "ATTカプラー・ツース盤・平刃の設定が正しいか確認",
            "ツース摩耗量の入力値を確認",
            "マッチングオフセットをリセット",
        ]
    },
    "z_gnss": {
        "leaf": True,
        "cause": "GNSS高さ精度の問題（Z方向）",
        "actions": [
            "GNSS垂直RMS値を確認（0.03m以内が目標）",
            "ベースライン距離を短縮（固定局を近づける）",
            "プロジェクトファイルの基準点Z座標を再確認",
            "ローカライゼーション作業を再実施",
            "観測時間を延長してGNSS安定化を待つ",
        ]
    },
    "xy_error": {
        "question": "N方向（前後）またはE方向（左右）のどちらかに偏っていますか？",
        "yes": "ne_error", "no": "project_error"
    },
    "ne_error": {
        "question": "GNSSアンテナの取付位置・向き・間隔は仕様通りですか？",
        "yes": "project_error", "no": "antenna_ng"
    },
    "antenna_ng": {
        "leaf": True,
        "cause": "GNSSアンテナの取付不良",
        "actions": [
            "メイン・サブアンテナの前後方向（向き）を取付説明書で再確認",
            "アンテナ間隔・取付高さの寸法を再測定・入力",
            "アンテナケーブルのコネクタ芯の曲がり・緩みを確認",
            "アンテナのガタつきを確認・締め直し",
        ]
    },
    "project_error": {
        "leaf": True,
        "cause": "プロジェクトファイル・ローカライゼーションの誤り",
        "actions": [
            "プロジェクトファイルの基準点座標（N/E/Z）を再確認",
            "ローカライゼーションを再実施（補正情報と一致した状態で）",
            "他車両・他機種で同PJファイルを試し、精度を比較",
            "設計データの描画位置・向きが現場と一致しているか確認",
            "補正情報の種類（RRS/VRS/固定局）とPJファイルが一致しているか確認",
        ]
    },
}

# ─── サイドバー ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏗️ SC 3Dマシンガイダンス")
    st.markdown("**刃先精度確認システム**")
    st.markdown("---")

    pages = ["事前確認チェック", "刃先座標チェック", "診断フローチャート", "サマリー・レポート"]
    page = st.radio("ページ選択", pages, index=0)
    st.markdown("---")

    all_items = [i[0] for s in SECTIONS.values() for i in s["items"]]
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

    st.markdown('<div class="section-header">📋 基本情報</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.session_state.info_date    = st.text_input("確認日", st.session_state.info_date)
    with c2: st.session_state.info_time    = st.text_input("時刻",   st.session_state.info_time)
    with c3: st.session_state.info_checker = st.text_input("確認者氏名", st.session_state.info_checker)
    with c4: st.session_state.info_user    = st.text_input("ユーザー名", st.session_state.info_user)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.session_state.info_model      = st.text_input("機種・型式", st.session_state.info_model)
    with c2: st.session_state.info_machine_no = st.text_input("機番 #",     st.session_state.info_machine_no)
    with c3: st.session_state.info_sm         = st.text_input("サービスメータ (h)", st.session_state.info_sm)
    with c4: st.session_state.info_bucket     = st.text_input("装着バケット", st.session_state.info_bucket)

    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.info_tooth_len = st.text_input("ツース長さ (mm)", st.session_state.info_tooth_len)
    with c2: st.session_state.info_fw_ver    = st.text_input("FWバージョン",    st.session_state.info_fw_ver)
    with c3: st.session_state.info_app_ver   = st.text_input("アプリバージョン", st.session_state.info_app_ver)

    correction_opts = ["NTTドコモRRS", "ネットワーク型（その他）", "固定局（無線）", "固定局（有線）"]
    idx = correction_opts.index(st.session_state.info_correction) if st.session_state.info_correction in correction_opts else 0
    st.session_state.info_correction = st.selectbox("補正情報", correction_opts, index=idx)

    st.markdown("---")

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
                    st.session_state.checks[key] = "OK"; st.rerun()
            with cols[2]:
                if st.button("❌ NG", key=f"ng_{key}", use_container_width=True):
                    st.session_state.checks[key] = "NG"; st.rerun()
            with cols[3]:
                badge = {"OK": '<span class="badge badge-ok">OK</span>',
                         "NG": '<span class="badge badge-ng">NG</span>',
                         "未確認": '<span class="badge badge-na">未</span>'}.get(current, "")
                st.markdown(badge, unsafe_allow_html=True)

            if key == "kit_12": st.session_state.info_fw_ver  = st.text_input("　FWバージョン記入",   st.session_state.info_fw_ver,  key="fw_v2",  label_visibility="collapsed")
            if key == "kit_13": st.session_state.info_app_ver = st.text_input("　アプリバージョン記入", st.session_state.info_app_ver, key="app_v2", label_visibility="collapsed")
            if key == "env_02": st.session_state.env_hv_dist  = st.text_input("　離隔距離 (m)", st.session_state.env_hv_dist, key=f"hv_{key}")
            if key == "env_05": st.session_state.env_main_sat = st.text_input("　メインアンテナ利用衛星数 (個)", st.session_state.env_main_sat, key=f"ms_{key}")
            if key == "env_06": st.session_state.env_sub_sat  = st.text_input("　サブアンテナ利用衛星数 (個)", st.session_state.env_sub_sat, key=f"ss_{key}")
            if key == "env_07": st.session_state.env_sat_diff = st.text_input("　衛星数差異 (個)", st.session_state.env_sat_diff, key=f"sd_{key}")
            if key == "net_01": st.session_state.net_antenna  = st.text_input("　アンテナ本数", st.session_state.net_antenna, key=f"na_{key}")
            if key == "net_02" and sec_key == "net": st.session_state.net_delay = st.text_input("　補正情報遅延時間 (s)", st.session_state.net_delay, key=f"nd_{key}")
            if key == "net_04": st.session_state.net_baseline = st.text_input("　ベースライン間距離 (m)", st.session_state.net_baseline, key=f"nb_{key}")

    is_fixed = "固定局" in st.session_state.info_correction
    is_net   = not is_fixed

    render_section("kit",      SECTIONS["kit"])
    render_section("gnss_env", SECTIONS["gnss_env"])
    render_section("net",      SECTIONS["net"],   skip_net=is_fixed)
    render_section("fixed",    SECTIONS["fixed"], skip_fixed=is_net)
    render_section("project",  SECTIONS["project"])
    render_section("settings", SECTIONS["settings"])

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

    all_answered = sum(1 for k in all_items if st.session_state.checks.get(k) in ["OK", "NG"])
    if all_answered > 0 and not ng_keys:
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
        st.session_state.gnss_pdop  = st.text_input("PDOP", st.session_state.gnss_pdop)
        st.session_state.gnss_delay = st.text_input("遅延時間 [s]", st.session_state.gnss_delay)
    with c3:
        st.session_state.gnss_baseline  = st.text_input("ベースライン間距離 [m]", st.session_state.gnss_baseline)
        st.session_state.gnss_sub_v_rms = st.text_input("サブGNSS垂直精度RMS [m]", st.session_state.gnss_sub_v_rms)
        st.session_state.gnss_sub_h_rms = st.text_input("サブGNSS水平精度RMS [m]", st.session_state.gnss_sub_h_rms)

    st.markdown('<div class="section-header">📍 基準点情報</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.ref_name = st.text_input("基準点名", st.session_state.ref_name)
        cn, ce, cz = st.columns(3)
        with cn: st.session_state.ref_n = st.text_input("N", st.session_state.ref_n)
        with ce: st.session_state.ref_e = st.text_input("E", st.session_state.ref_e)
        with cz: st.session_state.ref_z = st.text_input("Z", st.session_state.ref_z)
    with c2:
        st.session_state.ref_dir = st.text_input("基準点への向き・方位", st.session_state.ref_dir)
        st.markdown('<div class="info-box">💡 方位は pilotアプリ 3D表示で確認してください</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📊 刃先座標計測結果（差分入力）　※ 座標ではなく「差分」の値を入力</div>', unsafe_allow_html=True)

    # 作業機姿勢 参考図（埋め込み画像）
    st.markdown("**🦾 作業機姿勢 参考図（姿勢1〜4）**")
    _IMG_B64 = "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"
    st.markdown(
        f'<div style="background:#fff;border-radius:8px;padding:12px;'
        f'margin-bottom:12px;text-align:center;">'  
        f'<img src="data:image/png;base64,{_IMG_B64}" '
        f'style="max-width:100%;height:auto;" alt="作業機姿勢参考図"/></div>'
        f'<div style="font-size:0.78rem;color:#A0A0A0;margin-bottom:16px;">'
        f'● 各姿勢で刃先を基準点に合わせて座標差分を計測してください</div>',
        unsafe_allow_html=True
    )

    THRESHOLD = 0.05
    st.markdown("各姿勢における計測値（N/E/Z 差分）を入力してください。許容値 **±0.05m（±5cm）**")

    for i, row in enumerate(st.session_state.blade_results):
        with st.container():
            st.markdown(
                f"<div style='background:var(--komatsu-gray);border:1px solid var(--border);"
                f"border-left:4px solid var(--komatsu-yellow);border-radius:8px;"
                f"padding:10px 16px;margin-bottom:8px;font-weight:700;'>📐 姿勢 {i+1}</div>",
                unsafe_allow_html=True
            )
            c1, c2, c3, c4 = st.columns([3, 3, 3, 2])
            with c1: n_val = st.text_input("N差分 (m)", row["N"], key=f"n_{i}", placeholder="例: 0.012")
            with c2: e_val = st.text_input("E差分 (m)", row["E"], key=f"e_{i}", placeholder="例: -0.023")
            with c3: z_val = st.text_input("Z差分 (m)", row["Z"], key=f"z_{i}", placeholder="例: 0.008")
            st.session_state.blade_results[i]["N"] = n_val
            st.session_state.blade_results[i]["E"] = e_val
            st.session_state.blade_results[i]["Z"] = z_val
            with c4:
                st.markdown("<br>", unsafe_allow_html=True)
                try:
                    n_f, e_f, z_f = float(n_val), float(e_val), float(z_val)
                    all_ok = all(abs(v) <= THRESHOLD for v in [n_f, e_f, z_f])
                    if all_ok:
                        st.markdown('<span class="badge badge-ok">✅ OK</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="badge badge-ng">❌ NG</span>', unsafe_allow_html=True)
                except:
                    st.markdown('<span class="badge badge-na">未入力</span>', unsafe_allow_html=True)

            try:
                n_f, e_f, z_f = float(n_val), float(e_val), float(z_val)
                cols_d = st.columns(3)
                for col_d, lbl, val in zip(cols_d, ["N", "E", "Z"], [n_f, e_f, z_f]):
                    color = "#00C853" if abs(val) <= THRESHOLD else "#FF3D3D"
                    with col_d:
                        st.markdown(
                            f"<div style='text-align:center;background:var(--komatsu-mid);"
                            f"border-radius:6px;padding:6px 4px;margin-top:6px;'>"
                            f"<div style='font-size:0.7rem;color:var(--text-secondary);'>{lbl}差分</div>"
                            f"<div style='font-size:1.1rem;font-weight:700;color:{color};"
                            f"font-family:monospace;'>{val:+.4f}m</div></div>",
                            unsafe_allow_html=True
                        )
            except:
                pass

    # 傾向分析
    st.markdown("---")
    st.markdown("### 📈 傾向分析")
    ns, es, zs = [], [], []
    for row in st.session_state.blade_results:
        try:
            ns.append(float(row["N"])); es.append(float(row["E"])); zs.append(float(row["Z"]))
        except: pass

    if ns and es and zs:
        import statistics
        def metric_card(label, vals, col):
            avg = statistics.mean(vals)
            rng = max(vals) - min(vals)
            ok = all(abs(v) <= THRESHOLD for v in vals)
            with col:
                color = "#00C853" if ok else "#FF3D3D"
                st.markdown(f"""
                <div style="background:var(--komatsu-gray);border:1px solid {color};border-radius:8px;
                            padding:12px;text-align:center;">
                    <div style="font-size:0.8rem;color:var(--text-secondary);">{label}</div>
                    <div style="font-size:1.5rem;font-weight:700;color:{color};font-family:'JetBrains Mono',monospace;">{avg:+.4f}m</div>
                    <div style="font-size:0.75rem;color:var(--text-secondary);">平均 ｜ 範囲: {rng:.4f}m</div>
                </div>
                """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        metric_card("N（前後方向）", ns, col1)
        metric_card("E（左右方向）", es, col2)
        metric_card("Z（高さ方向）", zs, col3)

        tips = []
        avg_n, avg_e, avg_z = statistics.mean(ns), statistics.mean(es), statistics.mean(zs)
        rng_n = max(ns) - min(ns)
        if abs(avg_n) > THRESHOLD: tips.append(f"N方向（前後）に {avg_n:+.3f}m の系統誤差 → 車体前後キャリブ・PJファイル確認")
        if abs(avg_e) > THRESHOLD: tips.append(f"E方向（左右）に {avg_e:+.3f}m の系統誤差 → GNSSアンテナ左右位置・向き確認")
        if abs(avg_z) > THRESHOLD: tips.append(f"Z方向（高さ）に {avg_z:+.3f}m のズレ → ツース長さ・バケットファイル設定確認")
        if rng_n > 0.03: tips.append(f"N方向のばらつき {rng_n:.3f}m が大きい → IMUセンサ振れ・ドリフト疑い")

        if tips:
            for t in tips:
                st.markdown(f'<div class="alert-box">⚠️ {t}</div>', unsafe_allow_html=True)
            st.markdown('<div class="info-box">💡「診断フローチャート」ページで原因の絞り込みができます</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-box">✅ 全姿勢 ±5cm以内。刃先精度は正常範囲です。</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">計測値を入力すると傾向分析が表示されます</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
elif page == "診断フローチャート":
# ═══════════════════════════════════════════════════════════════

    st.markdown('<div class="section-header">🔍 刃先精度不良 診断フローチャート</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    💡 症状に応じてYes/Noで回答し、原因と対策を絞り込みます。<br>
    全体のフロー図（SVG）も下部に掲載しています。
    </div>
    """, unsafe_allow_html=True)

    # ── インタラクティブ診断（全幅） ──────────────────────────────
    st.markdown("### ▶ インタラクティブ診断")

    if "flow_current" not in st.session_state:
        st.session_state.flow_current = "start"
        st.session_state.flow_history = []

    current_id = st.session_state.flow_current
    node = FLOW_NODES.get(current_id, {})

    # パンくず
    if st.session_state.flow_history:
        trail = " → ".join([f"**{h}**" for h in st.session_state.flow_history[-4:]])
        st.markdown(f"<small style='color:var(--text-secondary);'>経路: {trail}</small>", unsafe_allow_html=True)

    if node.get("leaf"):
        st.markdown(f"""
        <div style="background:rgba(255,61,61,0.1);border:2px solid #FF3D3D;border-radius:12px;padding:20px;margin:12px 0;">
            <div style="font-size:1.1rem;font-weight:700;color:#FF3D3D;margin-bottom:12px;">
                ⚠️ 推定原因: {node['cause']}
            </div>
            <div style="font-weight:600;color:#F0F0F0;margin-bottom:8px;">📋 対処手順:</div>
        """ + "".join([
            f'<div style="background:var(--komatsu-gray);border-radius:6px;padding:8px 12px;margin:4px 0;color:#F0F0F0;">'
            f'<span style="color:var(--komatsu-yellow);font-weight:700;">{j+1}.</span> {act}</div>'
            for j, act in enumerate(node["actions"])
        ]) + "</div>", unsafe_allow_html=True)

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("🔄 最初からやり直す"):
                st.session_state.flow_current = "start"
                st.session_state.flow_history = []
                st.rerun()
        with col_r2:
            if st.session_state.flow_history and st.button("⬅ 一つ前に戻る"):
                st.session_state.flow_current = st.session_state.flow_history.pop()
                st.rerun()

    else:
        q = node.get("question", "")
        st.markdown(f"""
        <div style="background:var(--komatsu-gray);border:2px solid var(--komatsu-yellow);
                    border-radius:12px;padding:20px;margin:12px 0;">
            <div style="font-size:1.05rem;font-weight:700;color:#F0F0F0;line-height:1.6;">
                ❓ {q}
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_y, col_n, col_b = st.columns([2, 2, 1])
        with col_y:
            if st.button("✅ はい (Yes)", use_container_width=True):
                st.session_state.flow_history.append(current_id)
                st.session_state.flow_current = node.get("yes", "start")
                st.rerun()
        with col_n:
            if st.button("❌ いいえ (No)", use_container_width=True):
                st.session_state.flow_history.append(current_id)
                st.session_state.flow_current = node.get("no", "start")
                st.rerun()
        with col_b:
            if st.session_state.flow_history:
                if st.button("⬅ 戻る"):
                    st.session_state.flow_current = st.session_state.flow_history.pop()
                    st.rerun()

    # ── フロー全体図（全幅・下部） ─────────────────────────────
    st.markdown("---")
    st.markdown("### 📊 診断フロー全体図")
    import streamlit.components.v1 as _components
    _FLOW_HTML = '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n<style>\n  body { margin: 0; background: #1e1e1e; display: flex; justify-content: center; }\n  svg { display: block; }\n</style>\n</head>\n<body>\n<svg viewBox="0 0 860 1480" width="860" xmlns="http://www.w3.org/2000/svg"\n     style="font-family:sans-serif;">\n  <defs>\n    <marker id="a0" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#888"/></marker>\n    <marker id="ay" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#00C853"/></marker>\n    <marker id="an" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#FF3D3D"/></marker>\n  </defs>\n  <rect width="860" height="1480" fill="#1e1e1e"/>\n\n  <!-- START -->\n  <rect x="230" y="14" width="400" height="44" rx="22" fill="#CC2222"/>\n  <text x="430" y="41" text-anchor="middle" font-size="14" font-weight="bold" fill="#fff">&#x5203;&#x5148;&#x7CBE;&#x5EA6;&#x304C;&#xB1;5cm&#x4EE5;&#x5185;&#x306B;&#x53CE;&#x307E;&#x3089;&#x306A;&#x3044;</text>\n  <line x1="430" y1="58" x2="430" y2="80" stroke="#888" stroke-width="2" marker-end="url(#a0)"/>\n\n  <!-- Q1 GNSS FIX cy=118 hw=155 hh=38 -->\n  <polygon points="430,80 585,118 430,156 275,118" fill="#252525" stroke="#FFD700" stroke-width="2"/>\n  <text x="430" y="112" text-anchor="middle" font-size="12" fill="#FFD700">GNSS&#x30B9;&#x30C6;&#x30FC;&#x30BF;&#x30B9;&#x306F;</text>\n  <text x="430" y="130" text-anchor="middle" font-size="12" fill="#FFD700">&#x7DD1;&#x8272;&#xFF08;FIX&#xFF09;&#x3067;&#x3059;&#x304B;&#xFF1F;</text>\n  <!-- YES right bypass x=770 to Q3 cy=400 -->\n  <line x1="585" y1="118" x2="770" y2="118" stroke="#00C853" stroke-width="1.5"/>\n  <line x1="770" y1="118" x2="770" y2="400" stroke="#00C853" stroke-width="1.5"/>\n  <line x1="770" y1="400" x2="585" y2="400" stroke="#00C853" stroke-width="1.5" marker-end="url(#ay)"/>\n  <text x="677" y="110" text-anchor="middle" font-size="11" fill="#00C853">YES</text>\n  <!-- NO down -->\n  <line x1="430" y1="156" x2="430" y2="180" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#an)"/>\n  <text x="446" y="173" font-size="11" fill="#FF3D3D">NO</text>\n\n  <!-- Q2 補正 cy=228 hw=145 hh=48 -->\n  <polygon points="430,180 575,228 430,276 285,228" fill="#252525" stroke="#FFD700" stroke-width="2"/>\n  <text x="430" y="222" text-anchor="middle" font-size="12" fill="#FFD700">&#x88DC;&#x6B63;&#x60C5;&#x5831;&#x306F;</text>\n  <text x="430" y="240" text-anchor="middle" font-size="12" fill="#FFD700">&#x53D7;&#x4FE1;&#x3067;&#x304D;&#x3066;&#x3044;&#x307E;&#x3059;&#x304B;&#xFF1F;</text>\n  <!-- YES leaf FIX不可 -->\n  <line x1="575" y1="228" x2="606" y2="228" stroke="#00C853" stroke-width="1.5" marker-end="url(#ay)"/>\n  <text x="590" y="220" text-anchor="middle" font-size="11" fill="#00C853">YES</text>\n  <rect x="608" y="206" width="170" height="48" rx="6" fill="#550000" stroke="#FF3D3D" stroke-width="1.5"/>\n  <text x="693" y="226" text-anchor="middle" font-size="11" fill="#FF3D3D" font-weight="bold">&#x1F4CC; FIX&#x4E0D;&#x53EF;</text>\n  <text x="693" y="244" text-anchor="middle" font-size="11" fill="#FF3D3D">&#x4E0A;&#x7A7A;&#x30FB;&#x74B0;&#x5883;&#x78BA;&#x8A8D;</text>\n  <!-- NO down leaf 補正なし -->\n  <line x1="430" y1="276" x2="430" y2="294" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#an)"/>\n  <text x="446" y="288" font-size="11" fill="#FF3D3D">NO</text>\n  <rect x="220" y="296" width="420" height="52" rx="6" fill="#550000" stroke="#FF3D3D" stroke-width="1.5"/>\n  <text x="430" y="319" text-anchor="middle" font-size="12" fill="#FF3D3D" font-weight="bold">&#x1F4CC; &#x88DC;&#x6B63;&#x60C5;&#x5831;&#x304C;&#x5C4A;&#x3044;&#x3066;&#x3044;&#x306A;&#x3044;</text>\n  <text x="430" y="337" text-anchor="middle" font-size="11" fill="#FF3D3D">SIM / Ntrip / &#x56FA;&#x5B9A;&#x5C40; / &#x7121;&#x7DDA;&#x6A5F;&#x3092;&#x78BA;&#x8A8D;</text>\n  <!-- gap 348->362 -->\n\n  <!-- Q3 一定? cy=400 hw=155 hh=38 -->\n  <polygon points="430,362 585,400 430,438 275,400" fill="#252525" stroke="#FFD700" stroke-width="2"/>\n  <text x="430" y="394" text-anchor="middle" font-size="12" fill="#FFD700">&#x8AA4;&#x5DEE;&#x306E;&#x65B9;&#x5411;&#x30FB;&#x5927;&#x304D;&#x3055;&#x304C;</text>\n  <text x="430" y="412" text-anchor="middle" font-size="12" fill="#FFD700">&#x59FF;&#x52E2;&#x306B;&#x3088;&#x3089;&#x305A;&#x4E00;&#x5B9A;&#x3067;&#x3059;&#x304B;&#xFF1F;</text>\n  <!-- YES dashed down to Q4 -->\n  <line x1="430" y1="438" x2="430" y2="920" stroke="#00C853" stroke-width="1.5" stroke-dasharray="7,5"/>\n  <text x="448" y="458" font-size="11" fill="#00C853">YES&#x2193;</text>\n  <!-- NO left to branch cx=155 -->\n  <line x1="275" y1="400" x2="155" y2="400" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#an)"/>\n  <text x="210" y="392" text-anchor="middle" font-size="11" fill="#FF3D3D">NO</text>\n\n  <!-- ===== 左ブランチ cx=155 ===== -->\n  <text x="155" y="462" text-anchor="middle" font-size="10" fill="#666">&#x25BC; &#x59FF;&#x52E2;&#x4F9D;&#x5B58;&#x30EB;&#x30FC;&#x30C8;</text>\n\n  <!-- Q_RAND cy=500 hw=105 hh=32 -->\n  <polygon points="155,468 260,500 155,532 50,500" fill="#252525" stroke="#FFD700" stroke-width="1.5"/>\n  <text x="155" y="494" text-anchor="middle" font-size="11" fill="#FFD700">&#x8AA4;&#x5DEE;&#x306E;&#x65B9;&#x5411;&#x304C;</text>\n  <text x="155" y="510" text-anchor="middle" font-size="11" fill="#FFD700">&#x30D0;&#x30E9;&#x30D0;&#x30E9;&#x3067;&#x3059;&#x304B;&#xFF1F;</text>\n  <!-- RAND NO left bypass x=12 to PJ leaf y=800 -->\n  <line x1="50"  y1="500" x2="12"  y2="500" stroke="#FF3D3D" stroke-width="1.5"/>\n  <line x1="12"  y1="500" x2="12"  y2="814" stroke="#FF3D3D" stroke-width="1.5"/>\n  <line x1="12"  y1="814" x2="46"  y2="814" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#an)"/>\n  <text x="30"   y="492" font-size="11" fill="#FF3D3D">NO</text>\n  <!-- RAND YES down -->\n  <line x1="155" y1="532" x2="155" y2="562" stroke="#00C853" stroke-width="1.5" marker-end="url(#ay)"/>\n  <text x="171" y="552" font-size="11" fill="#00C853">YES</text>\n\n  <!-- Q_IMU cy=596 hw=105 hh=32 -->\n  <polygon points="155,562 260,596 155,630 50,596" fill="#252525" stroke="#FFD700" stroke-width="1.5"/>\n  <text x="155" y="590" text-anchor="middle" font-size="11" fill="#FFD700">&#x4F5C;&#x696D;&#x6A5F;&#x306E;&#x8FFD;&#x5F93;&#x306F;</text>\n  <text x="155" y="606" text-anchor="middle" font-size="11" fill="#FFD700">&#x6B63;&#x78BA;&#x3067;&#x3059;&#x304B;&#xFF1F;</text>\n  <!-- IMU NO down leaf -->\n  <line x1="155" y1="630" x2="155" y2="658" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#an)"/>\n  <text x="171" y="650" font-size="11" fill="#FF3D3D">NO</text>\n  <rect x="52"  y="660" width="206" height="50" rx="6" fill="#550000" stroke="#FF3D3D" stroke-width="1.5"/>\n  <text x="155" y="681" text-anchor="middle" font-size="12" fill="#FF3D3D" font-weight="bold">&#x1F4CC; IMU&#x30BB;&#x30F3;&#x30B5;&#x4E0D;&#x826F;</text>\n  <text x="155" y="699" text-anchor="middle" font-size="11" fill="#FF3D3D">&#x53D6;&#x4ED8;&#x30FB;&#x30CF;&#x30FC;&#x30CD;&#x30B9;&#x78BA;&#x8A8D;</text>\n  <!-- IMU YES right leaf マルチパス (点線右側 x=460-680) -->\n  <line x1="260" y1="596" x2="460" y2="596" stroke="#00C853" stroke-width="1.5" marker-end="url(#ay)"/>\n  <text x="360" y="588" text-anchor="middle" font-size="11" fill="#00C853">YES</text>\n  <rect x="462" y="572" width="210" height="52" rx="6" fill="#443300" stroke="#FF9800" stroke-width="1.5"/>\n  <text x="567" y="592" text-anchor="middle" font-size="12" fill="#FF9800" font-weight="bold">&#x1F4CC; &#x30DE;&#x30EB;&#x30C1;&#x30D1;&#x30B9;&#x30FB;&#x74B0;&#x5883;&#x30CE;&#x30A4;&#x30BA;</text>\n  <text x="567" y="610" text-anchor="middle" font-size="11" fill="#FF9800">&#x5834;&#x6240;&#x79FB;&#x52D5;&#x30BFPDOP&#x78BA;&#x8A8D;</text>\n\n  <!-- PJ leaf (RAND NO) y=796-848 x=46-286 -->\n  <rect x="46"  y="796" width="240" height="52" rx="6" fill="#443300" stroke="#FF9800" stroke-width="1.5"/>\n  <text x="166" y="819" text-anchor="middle" font-size="12" fill="#FF9800" font-weight="bold">&#x1F4CC; PJ&#x30D5;&#x30A1;&#x30A4;&#x30EB;&#x30FB;&#x8A2D;&#x5B9A;&#x78BA;&#x8A8D;</text>\n  <text x="166" y="837" text-anchor="middle" font-size="11" fill="#FF9800">&#x30ED;&#x30FC;&#x30AB;&#x30E9;&#x30A4;&#x30BC;&#x30FC;&#x30B7;&#x30E7;&#x30F3;&#x518D;&#x5B9F;&#x65BD;</text>\n\n  <!-- === 区切り === -->\n  <line x1="20" y1="892" x2="840" y2="892" stroke="#333" stroke-width="1" stroke-dasharray="5,5"/>\n  <text x="430" y="910" text-anchor="middle" font-size="10" fill="#555">&#x2500; &#x7CFB;&#x7D71;&#x8AA4;&#x5DEE;&#x30EB;&#x30FC;&#x30C8;&#xFF08;&#x59FF;&#x52E2;&#x306B;&#x3088;&#x3089;&#x305A;&#x4E00;&#x5B9A;&#xFF09; &#x2500;</text>\n\n  <!-- Q4 Z方向 cy=958 hw=155 hh=38 -->\n  <polygon points="430,920 585,958 430,996 275,958" fill="#252525" stroke="#FFD700" stroke-width="2"/>\n  <text x="430" y="952" text-anchor="middle" font-size="12" fill="#FFD700">Z&#x65B9;&#x5411;&#xFF08;&#x9AD8;&#x3055;&#xFF09;&#x306B;</text>\n  <text x="430" y="970" text-anchor="middle" font-size="12" fill="#FFD700">&#x7CFB;&#x7D71;&#x8AA4;&#x5DEE;&#x304C;&#x3042;&#x308A;&#x307E;&#x3059;&#x304B;&#xFF1F;</text>\n  <!-- YES down -->\n  <line x1="430" y1="996" x2="430" y2="1022" stroke="#00C853" stroke-width="1.5" marker-end="url(#ay)"/>\n  <text x="446" y="1014" font-size="11" fill="#00C853">YES</text>\n  <!-- NO right bypass x=770 to Q6 cy=1220 -->\n  <line x1="585" y1="958"  x2="770" y2="958"  stroke="#FF3D3D" stroke-width="1.5"/>\n  <line x1="770" y1="958"  x2="770" y2="1220" stroke="#FF3D3D" stroke-width="1.5"/>\n  <line x1="770" y1="1220" x2="585" y2="1220" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#an)"/>\n  <text x="677" y="950" text-anchor="middle" font-size="11" fill="#FF3D3D">NO</text>\n\n  <!-- Q5 バケット cy=1064 hw=148 hh=42 -->\n  <polygon points="430,1022 578,1064 430,1106 282,1064" fill="#252525" stroke="#FFD700" stroke-width="1.5"/>\n  <text x="430" y="1058" text-anchor="middle" font-size="12" fill="#FFD700">&#x30D0;&#x30B1;&#x30C3;&#x30C8;&#x30D5;&#x30A1;&#x30A4;&#x30EB;&#x30FB;</text>\n  <text x="430" y="1076" text-anchor="middle" font-size="12" fill="#FFD700">&#x30C4;&#x30FC;&#x30B9;&#x9577;&#x306F;&#x6B63;&#x78BA;&#x3067;&#x3059;&#x304B;&#xFF1F;</text>\n  <!-- YES right leaf GNSS高さ -->\n  <line x1="578" y1="1064" x2="606" y2="1064" stroke="#00C853" stroke-width="1.5" marker-end="url(#ay)"/>\n  <text x="592" y="1056" text-anchor="middle" font-size="11" fill="#00C853">YES</text>\n  <rect x="608" y="1042" width="170" height="48" rx="6" fill="#443300" stroke="#FF9800" stroke-width="1.5"/>\n  <text x="693" y="1062" text-anchor="middle" font-size="11" fill="#FF9800" font-weight="bold">&#x1F4CC; GNSS&#x9AD8;&#x3055;&#x7CBE;&#x5EA6;</text>\n  <text x="693" y="1080" text-anchor="middle" font-size="11" fill="#FF9800">&#x5782;&#x76F4;RMS&#x30BFPJ&#x78BA;&#x8A8D;</text>\n  <!-- NO down leaf バケット -->\n  <line x1="430" y1="1106" x2="430" y2="1124" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#an)"/>\n  <text x="446" y="1118" font-size="11" fill="#FF3D3D">NO</text>\n  <rect x="220" y="1126" width="420" height="52" rx="6" fill="#550000" stroke="#FF3D3D" stroke-width="1.5"/>\n  <text x="430" y="1149" text-anchor="middle" font-size="12" fill="#FF3D3D" font-weight="bold">&#x1F4CC; &#x30D0;&#x30B1;&#x30C3;&#x30C8;&#x8A2D;&#x5B9A;&#x8AA4;&#x308A;</text>\n  <text x="430" y="1167" text-anchor="middle" font-size="11" fill="#FF3D3D">&#x30C4;&#x30FC;&#x30B9;&#x9577;&#x30FB;&#x5BF8;&#x6CD5;&#x3092;&#x4FEE;&#x6B63;</text>\n  <!-- gap 1178->1196 -->\n\n  <!-- Q6 N/E cy=1234 hw=155 hh=38 -->\n  <polygon points="430,1196 585,1234 430,1272 275,1234" fill="#252525" stroke="#FFD700" stroke-width="2"/>\n  <text x="430" y="1228" text-anchor="middle" font-size="12" fill="#FFD700">N/E&#x65B9;&#x5411;&#xFF08;&#x524D;&#x5F8C;&#x5DE6;&#x53F3;&#xFF09;&#x306B;</text>\n  <text x="430" y="1246" text-anchor="middle" font-size="12" fill="#FFD700">&#x7CFB;&#x7D71;&#x8AA4;&#x5DEE;&#x304C;&#x3042;&#x308A;&#x307E;&#x3059;&#x304B;&#xFF1F;</text>\n  <!-- YES down -->\n  <line x1="430" y1="1272" x2="430" y2="1298" stroke="#00C853" stroke-width="1.5" marker-end="url(#ay)"/>\n  <text x="446" y="1290" font-size="11" fill="#00C853">YES</text>\n  <!-- NO right leaf PJ誤り -->\n  <line x1="585" y1="1234" x2="606" y2="1234" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#an)"/>\n  <text x="595" y="1226" text-anchor="middle" font-size="11" fill="#FF3D3D">NO</text>\n  <rect x="608" y="1212" width="170" height="48" rx="6" fill="#443300" stroke="#FF9800" stroke-width="1.5"/>\n  <text x="693" y="1232" text-anchor="middle" font-size="11" fill="#FF9800" font-weight="bold">&#x1F4CC; PJ&#x30D5;&#x30A1;&#x30A4;&#x30EB;&#x8AA4;&#x308A;</text>\n  <text x="693" y="1250" text-anchor="middle" font-size="11" fill="#FF9800">&#x57FA;&#x6E96;&#x70B9;&#x30BFLOC</text>\n\n  <!-- Q7 アンテナ cy=1336 hw=148 hh=38 -->\n  <polygon points="430,1298 578,1336 430,1374 282,1336" fill="#252525" stroke="#FFD700" stroke-width="1.5"/>\n  <text x="430" y="1330" text-anchor="middle" font-size="12" fill="#FFD700">&#x30A2;&#x30F3;&#x30C6;&#x30CA;&#x53D6;&#x4ED8;&#x4F4D;&#x7F6E;&#x30FB;&#x5411;&#x304D;&#x306F;</text>\n  <text x="430" y="1348" text-anchor="middle" font-size="12" fill="#FFD700">&#x4ED5;&#x69D8;&#x901A;&#x308A;&#x3067;&#x3059;&#x304B;&#xFF1F;</text>\n  <!-- YES right leaf PJ誤り -->\n  <line x1="578" y1="1336" x2="606" y2="1336" stroke="#00C853" stroke-width="1.5" marker-end="url(#ay)"/>\n  <text x="592" y="1328" text-anchor="middle" font-size="11" fill="#00C853">YES</text>\n  <rect x="608" y="1314" width="170" height="48" rx="6" fill="#443300" stroke="#FF9800" stroke-width="1.5"/>\n  <text x="693" y="1334" text-anchor="middle" font-size="11" fill="#FF9800" font-weight="bold">&#x1F4CC; PJ&#x30D5;&#x30A1;&#x30A4;&#x30EB;&#x8AA4;&#x308A;</text>\n  <text x="693" y="1352" text-anchor="middle" font-size="11" fill="#FF9800">&#x57FA;&#x6E96;&#x70B9;&#x30BFLOC</text>\n  <!-- NO down leaf アンテナ不良 -->\n  <line x1="430" y1="1374" x2="430" y2="1392" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#an)"/>\n  <text x="446" y="1386" font-size="11" fill="#FF3D3D">NO</text>\n  <rect x="220" y="1394" width="420" height="52" rx="6" fill="#550000" stroke="#FF3D3D" stroke-width="1.5"/>\n  <text x="430" y="1417" text-anchor="middle" font-size="12" fill="#FF3D3D" font-weight="bold">&#x1F4CC; &#x30A2;&#x30F3;&#x30C6;&#x30CA;&#x53D6;&#x4ED8;&#x4E0D;&#x826F;</text>\n  <text x="430" y="1435" text-anchor="middle" font-size="11" fill="#FF3D3D">&#x4F4D;&#x7F6E;&#x30FB;&#x5411;&#x304D;&#x30FB;&#x30AC;&#x30BF;&#x78BA;&#x8A8D;</text>\n\n  <!-- 凡例 -->\n  <rect x="248" y="1456" width="12" height="12" fill="#FFD700"/>\n  <text x="266" y="1467" font-size="11" fill="#aaa">&#x5224;&#x65AD;&#x5206;&#x5C90;</text>\n  <rect x="358" y="1456" width="12" height="12" fill="#FF3D3D" opacity="0.8"/>\n  <text x="376" y="1467" font-size="11" fill="#aaa">&#x539F;&#x56E0;&#xFF08;&#x8D64;&#xFF09;</text>\n  <rect x="468" y="1456" width="12" height="12" fill="#FF9800" opacity="0.8"/>\n  <text x="486" y="1467" font-size="11" fill="#aaa">&#x539F;&#x56E0;&#xFF08;&#x6A59;&#xFF09;</text>\n</svg>\n</body>\n</html>'
    _components.html(_FLOW_HTML, height=1500, scrolling=True)

# ═══════════════════════════════════════════════════════════════
elif page == "サマリー・レポート":
# ═══════════════════════════════════════════════════════════════

    st.markdown('<div class="section-header">📋 確認サマリー</div>', unsafe_allow_html=True)

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
                {'<span class="badge badge-ng">' + str(ng_c) + ' NG</span>&nbsp;' if ng_c else ''}
                <span class="badge badge-na">{tot - ok_c - ng_c} 未</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 刃先座標計測結果")
    THRESHOLD = 0.05
    rows_html = "<table><tr><th>姿勢</th><th>N差分 (m)</th><th>E差分 (m)</th><th>Z差分 (m)</th><th>判定</th></tr>"
    for row in st.session_state.blade_results:
        try:
            n_f, e_f, z_f = float(row["N"]), float(row["E"]), float(row["Z"])
            ok = all(abs(v) <= THRESHOLD for v in [n_f, e_f, z_f])
            judge = '<span class="badge badge-ok">OK</span>' if ok else '<span class="badge badge-ng">NG</span>'
            rows_html += f"<tr><td>{row['姿勢']}</td><td>{n_f:+.4f}</td><td>{e_f:+.4f}</td><td>{z_f:+.4f}</td><td>{judge}</td></tr>"
        except:
            rows_html += f"<tr><td>{row['姿勢']}</td><td>-</td><td>-</td><td>-</td><td><span class='badge badge-na'>未入力</span></td></tr>"
    st.markdown(rows_html + "</table>", unsafe_allow_html=True)

    # JSON出力
    st.markdown("---")
    st.markdown("### 💾 データ出力")
    report_data = {
        "生成日時": datetime.now().isoformat(),
        "基本情報": {
            "確認日": st.session_state.info_date, "時刻": st.session_state.info_time,
            "確認者": st.session_state.info_checker, "ユーザー": st.session_state.info_user,
            "機種型式": st.session_state.info_model, "機番": st.session_state.info_machine_no,
            "SM(h)": st.session_state.info_sm, "バケット": st.session_state.info_bucket,
            "ツース長(mm)": st.session_state.info_tooth_len,
            "補正情報": st.session_state.info_correction,
            "FWバージョン": st.session_state.info_fw_ver, "アプリバージョン": st.session_state.info_app_ver,
        },
        "チェック結果": st.session_state.checks,
        "GNSS精度": {
            "メイン垂直RMS": st.session_state.gnss_main_v_rms,
            "メイン水平RMS": st.session_state.gnss_main_h_rms,
            "PDOP": st.session_state.gnss_pdop, "遅延時間": st.session_state.gnss_delay,
            "ベースライン距離": st.session_state.gnss_baseline,
            "サブ垂直RMS": st.session_state.gnss_sub_v_rms, "サブ水平RMS": st.session_state.gnss_sub_h_rms,
        },
        "基準点": {"名称": st.session_state.ref_name, "N": st.session_state.ref_n,
                   "E": st.session_state.ref_e, "Z": st.session_state.ref_z, "方位": st.session_state.ref_dir},
        "刃先座標計測": st.session_state.blade_results,
    }
    json_str = json.dumps(report_data, ensure_ascii=False, indent=2)
    fname = f"刃先精度確認_{st.session_state.info_date}_{st.session_state.info_model}_{st.session_state.info_machine_no}.json"
    st.download_button("📥 JSONレポートをダウンロード", data=json_str.encode("utf-8"),
                       file_name=fname, mime="application/json")
    st.markdown('<div class="info-box">💡 ダウンロードしたJSONは次回読み込みや解析ツールへの入力に利用できます</div>', unsafe_allow_html=True)
