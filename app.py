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

    # 作業機姿勢 SVG図
    st.markdown("**🦾 作業機姿勢 参考図（姿勢1〜4）**")
    st.markdown("""
    <div style="background:#f8f8f8;border-radius:8px;padding:16px;margin-bottom:12px;overflow-x:auto;">
    <svg viewBox="0 0 900 200" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:900px;">
      <defs>
        <marker id="ah" markerWidth="6" markerHeight="4" refX="6" refY="2" orient="auto">
          <polygon points="0 0, 6 2, 0 4" fill="#555"/>
        </marker>
      </defs>
      <!-- 地面ライン -->
      <line x1="0" y1="175" x2="900" y2="175" stroke="#888" stroke-width="1" stroke-dasharray="4,3"/>

      <!-- ===== 姿勢1 ===== -->
      <text x="112" y="14" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">姿勢１（標準）</text>
      <!-- 機体 -->
      <rect x="60" y="130" width="100" height="40" rx="4" fill="#BDBDBD" stroke="#555" stroke-width="1.5"/>
      <!-- キャビン -->
      <rect x="120" y="110" width="36" height="22" rx="3" fill="#90A4AE" stroke="#555" stroke-width="1"/>
      <!-- ブーム -->
      <line x1="152" y1="130" x2="185" y2="85" stroke="#795548" stroke-width="5" stroke-linecap="round"/>
      <!-- アーム -->
      <line x1="185" y1="85" x2="200" y2="145" stroke="#5D4037" stroke-width="4" stroke-linecap="round"/>
      <!-- バケット -->
      <polyline points="200,145 215,155 210,175" fill="none" stroke="#333" stroke-width="3" stroke-linecap="round"/>
      <!-- 刃先 -->
      <circle cx="210" cy="175" r="3" fill="#FF3D3D"/>
      <!-- ラベル -->
      <text x="112" y="194" text-anchor="middle" font-size="9" fill="#555">バケット・アームともダンプ</text>

      <!-- ===== 姿勢2 ===== -->
      <text x="337" y="14" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">姿勢２（ブーム上げ）</text>
      <rect x="280" y="130" width="100" height="40" rx="4" fill="#BDBDBD" stroke="#555" stroke-width="1.5"/>
      <rect x="340" y="110" width="36" height="22" rx="3" fill="#90A4AE" stroke="#555" stroke-width="1"/>
      <!-- ブーム高め -->
      <line x1="372" y1="128" x2="395" y2="65" stroke="#795548" stroke-width="5" stroke-linecap="round"/>
      <!-- アーム ダンプ気味 -->
      <line x1="395" y1="65" x2="418" y2="135" stroke="#5D4037" stroke-width="4" stroke-linecap="round"/>
      <!-- バケット -->
      <polyline points="418,135 432,148 428,175" fill="none" stroke="#333" stroke-width="3" stroke-linecap="round"/>
      <circle cx="428" cy="175" r="3" fill="#FF3D3D"/>
      <text x="337" y="194" text-anchor="middle" font-size="9" fill="#555">ブーム上げ・スペース確保</text>

      <!-- ===== 姿勢3 ===== -->
      <text x="562" y="14" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">姿勢３（アーム垂直）</text>
      <rect x="505" y="130" width="100" height="40" rx="4" fill="#BDBDBD" stroke="#555" stroke-width="1.5"/>
      <rect x="565" y="110" width="36" height="22" rx="3" fill="#90A4AE" stroke="#555" stroke-width="1"/>
      <!-- ブーム普通 -->
      <line x1="597" y1="128" x2="620" y2="80" stroke="#795548" stroke-width="5" stroke-linecap="round"/>
      <!-- アーム ほぼ垂直 -->
      <line x1="620" y1="80" x2="622" y2="148" stroke="#5D4037" stroke-width="4" stroke-linecap="round"/>
      <!-- バケット -->
      <polyline points="622,148 635,158 630,175" fill="none" stroke="#333" stroke-width="3" stroke-linecap="round"/>
      <circle cx="630" cy="175" r="3" fill="#FF3D3D"/>
      <text x="562" y="194" text-anchor="middle" font-size="9" fill="#555">アーム垂直・スペース不足時</text>

      <!-- ===== 姿勢4 ===== -->
      <text x="787" y="14" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">姿勢４（引き寄せ）</text>
      <rect x="730" y="130" width="100" height="40" rx="4" fill="#BDBDBD" stroke="#555" stroke-width="1.5"/>
      <rect x="790" y="110" width="36" height="22" rx="3" fill="#90A4AE" stroke="#555" stroke-width="1"/>
      <!-- ブーム高め -->
      <line x1="822" y1="125" x2="840" y2="60" stroke="#795548" stroke-width="5" stroke-linecap="round"/>
      <!-- アーム 引き込み -->
      <line x1="840" y1="60" x2="825" y2="130" stroke="#5D4037" stroke-width="4" stroke-linecap="round"/>
      <!-- バケット -->
      <polyline points="825,130 815,145 812,175" fill="none" stroke="#333" stroke-width="3" stroke-linecap="round"/>
      <circle cx="812" cy="175" r="3" fill="#FF3D3D"/>
      <text x="787" y="194" text-anchor="middle" font-size="9" fill="#555">ブーム高め・アーム引き込み</text>
    </svg>
    </div>
    <div style="font-size:0.78rem;color:var(--text-secondary);margin-bottom:16px;">
    ● 赤点 = 刃先位置　　各姿勢で刃先を基準点に合わせて座標差分を計測してください
    </div>
    """, unsafe_allow_html=True)

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

    col_flow, col_visual = st.columns([1, 1])

    with col_flow:
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
            # 原因特定
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
            # 質問表示
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

    with col_visual:
        st.markdown("### 📊 診断フロー全体図")
        # SVGフローチャート
        st.markdown("""
        <div style="background:#1e1e1e;border-radius:8px;padding:12px;overflow-x:auto;">
        <svg viewBox="0 0 560 780" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:560px;font-family:'Noto Sans JP',sans-serif;">
          <defs>
            <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0,8 3,0 6" fill="#888"/>
            </marker>
            <marker id="arr_y" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0,8 3,0 6" fill="#00C853"/>
            </marker>
            <marker id="arr_n" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0,8 3,0 6" fill="#FF3D3D"/>
            </marker>
          </defs>

          <!-- ======= START ======= -->
          <rect x="160" y="10" width="240" height="38" rx="19" fill="#FF3D3D" opacity="0.9"/>
          <text x="280" y="33" text-anchor="middle" font-size="12" font-weight="bold" fill="#fff">刃先精度が±5cm以内に収まらない</text>

          <!-- START → Q1 -->
          <line x1="280" y1="48" x2="280" y2="70" stroke="#888" stroke-width="1.5" marker-end="url(#arr)"/>

          <!-- Q1: GNSSステータス -->
          <polygon points="280,70 420,100 280,130 140,100" fill="#2D2D2D" stroke="#FFD700" stroke-width="2"/>
          <text x="280" y="96" text-anchor="middle" font-size="10" fill="#FFD700">GNSSステータスは</text>
          <text x="280" y="112" text-anchor="middle" font-size="10" fill="#FFD700">緑色（FIX）ですか？</text>

          <!-- Q1 YES → Q2 -->
          <line x1="420" y1="100" x2="480" y2="100" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>
          <text x="450" y="94" text-anchor="middle" font-size="9" fill="#00C853">YES</text>

          <!-- Q1 NO → 補正確認 -->
          <line x1="280" y1="130" x2="280" y2="155" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="295" y="148" font-size="9" fill="#FF3D3D">NO</text>

          <!-- Q_CORR: 補正情報は受信できていますか -->
          <polygon points="280,155 400,180 280,205 160,180" fill="#2D2D2D" stroke="#FFD700" stroke-width="1.5"/>
          <text x="280" y="176" text-anchor="middle" font-size="10" fill="#FFD700">補正情報は</text>
          <text x="280" y="192" text-anchor="middle" font-size="10" fill="#FFD700">受信できていますか？</text>

          <!-- CORR YES → LEAF_FIX_NG -->
          <line x1="400" y1="180" x2="480" y2="180" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>
          <text x="440" y="174" text-anchor="middle" font-size="9" fill="#00C853">YES</text>

          <!-- CORR NO → LEAF_CORR_NG -->
          <line x1="280" y1="205" x2="280" y2="225" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="295" y="220" font-size="9" fill="#FF3D3D">NO</text>

          <!-- LEAF: 補正情報なし -->
          <rect x="170" y="225" width="220" height="38" rx="6" fill="#FF3D3D" opacity="0.2" stroke="#FF3D3D" stroke-width="1.5"/>
          <text x="280" y="242" text-anchor="middle" font-size="10" fill="#FF3D3D" font-weight="bold">📌 補正情報が届いていない</text>
          <text x="280" y="256" text-anchor="middle" font-size="9" fill="#FF3D3D">SIM/Ntrip/固定局/無線機を確認</text>

          <!-- LEAF: FIX NG （補正あるがFIXしない） -->
          <rect x="485" y="163" width="65" height="38" rx="6" fill="#FF3D3D" opacity="0.2" stroke="#FF3D3D" stroke-width="1.5"/>
          <text x="517" y="179" text-anchor="middle" font-size="9" fill="#FF3D3D" font-weight="bold">📌 FIX不可</text>
          <text x="517" y="193" text-anchor="middle" font-size="9" fill="#FF3D3D">上空・環境確認</text>

          <!-- ======= Q2: 系統誤差? (YES from Q1, x=480) ======= -->
          <line x1="480" y1="100" x2="490" y2="100" stroke="#00C853" stroke-width="1.5"/>
          <line x1="490" y1="100" x2="490" y2="285" stroke="#00C853" stroke-width="1.5"/>
          <line x1="490" y1="285" x2="420" y2="285" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>

          <polygon points="280,285 420,315 280,345 140,315" fill="#2D2D2D" stroke="#FFD700" stroke-width="2"/>
          <text x="280" y="311" text-anchor="middle" font-size="10" fill="#FFD700">誤差の方向・大きさが</text>
          <text x="280" y="327" text-anchor="middle" font-size="10" fill="#FFD700">姿勢によらず一定ですか？</text>

          <!-- Q2 YES → Z確認 -->
          <line x1="280" y1="345" x2="280" y2="370" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>
          <text x="295" y="362" font-size="9" fill="#00C853">YES</text>

          <!-- Q2 NO → ランダム確認 -->
          <line x1="140" y1="315" x2="60" y2="315" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="92" y="309" text-anchor="middle" font-size="9" fill="#FF3D3D">NO</text>

          <!-- Q_RANDOM: ランダムバラつき -->
          <polygon points="60,315 140,340 60,365 -20,340" fill="#2D2D2D" stroke="#FFD700" stroke-width="1.5"/>
          <text x="60" y="336" text-anchor="middle" font-size="9" fill="#FFD700">誤差の方向が</text>
          <text x="60" y="350" text-anchor="middle" font-size="9" fill="#FFD700">バラバラですか？</text>

          <!-- RANDOM YES → IMU確認 -->
          <line x1="60" y1="365" x2="60" y2="390" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>
          <text x="72" y="382" font-size="9" fill="#00C853">YES</text>

          <!-- IMU追従確認 -->
          <polygon points="60,390 160,415 60,440 -40,415" fill="#2D2D2D" stroke="#FFD700" stroke-width="1.5"/>
          <text x="60" y="411" text-anchor="middle" font-size="9" fill="#FFD700">作業機の追従は</text>
          <text x="60" y="425" text-anchor="middle" font-size="9" fill="#FFD700">正確ですか？</text>

          <!-- IMU追従 NO → LEAF IMU不良 -->
          <line x1="60" y1="440" x2="60" y2="465" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="72" y="457" font-size="9" fill="#FF3D3D">NO</text>
          <rect x="-10" y="465" width="140" height="36" rx="6" fill="#FF3D3D" opacity="0.2" stroke="#FF3D3D" stroke-width="1.5"/>
          <text x="60" y="481" text-anchor="middle" font-size="9" fill="#FF3D3D" font-weight="bold">📌 IMUセンサ不良</text>
          <text x="60" y="495" text-anchor="middle" font-size="9" fill="#FF3D3D">取付・ハーネス確認</text>

          <!-- IMU追従 YES → LEAF マルチパス -->
          <line x1="160" y1="415" x2="240" y2="415" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>
          <text x="200" y="409" text-anchor="middle" font-size="9" fill="#00C853">YES</text>
          <rect x="240" y="398" width="140" height="36" rx="6" fill="#FF9800" opacity="0.2" stroke="#FF9800" stroke-width="1.5"/>
          <text x="310" y="414" text-anchor="middle" font-size="9" fill="#FF9800" font-weight="bold">📌 マルチパス・環境ノイズ</text>
          <text x="310" y="428" text-anchor="middle" font-size="9" fill="#FF9800">場所移動・PDOP確認</text>

          <!-- RANDOM NO → LEAF 間欠的 -->
          <line x1="-20" y1="340" x2="-60" y2="340" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <!-- (描画領域外なので省略・テキストのみ) -->

          <!-- ======= Q_Z: Z方向誤差? ======= -->
          <polygon points="280,370 400,400 280,430 160,400" fill="#2D2D2D" stroke="#FFD700" stroke-width="2"/>
          <text x="280" y="396" text-anchor="middle" font-size="10" fill="#FFD700">Z方向（高さ）に</text>
          <text x="280" y="412" text-anchor="middle" font-size="10" fill="#FFD700">系統誤差がありますか？</text>

          <!-- Q_Z YES → バケット設定 -->
          <line x1="280" y1="430" x2="280" y2="455" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>
          <text x="295" y="447" font-size="9" fill="#00C853">YES</text>

          <!-- バケット正確? -->
          <polygon points="280,455 410,482 280,509 150,482" fill="#2D2D2D" stroke="#FFD700" stroke-width="1.5"/>
          <text x="280" y="478" text-anchor="middle" font-size="10" fill="#FFD700">バケットファイル・</text>
          <text x="280" y="494" text-anchor="middle" font-size="10" fill="#FFD700">ツース長は正確ですか？</text>

          <!-- バケット NO → LEAF バケット設定誤り -->
          <line x1="150" y1="482" x2="80" y2="482" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="108" y="476" text-anchor="middle" font-size="9" fill="#FF3D3D">NO</text>
          <rect x="-10" y="568" width="150" height="36" rx="6" fill="#FF3D3D" opacity="0.2" stroke="#FF3D3D" stroke-width="1.5"/>
          <!-- 矢印下へ -->
          <line x1="80" y1="482" x2="65" y2="482" stroke="#FF3D3D" stroke-width="1.5"/>
          <line x1="65" y1="482" x2="65" y2="568" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="65" y="584" text-anchor="middle" font-size="9" fill="#FF3D3D" font-weight="bold">📌 バケット設定誤り</text>
          <text x="65" y="598" text-anchor="middle" font-size="9" fill="#FF3D3D">ツース長・寸法を修正</text>

          <!-- バケット YES → LEAF GNSS高さ精度 -->
          <line x1="410" y1="482" x2="470" y2="482" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>
          <text x="440" y="476" text-anchor="middle" font-size="9" fill="#00C853">YES</text>
          <rect x="470" y="465" width="80" height="36" rx="6" fill="#FF9800" opacity="0.2" stroke="#FF9800" stroke-width="1.5"/>
          <text x="510" y="481" text-anchor="middle" font-size="9" fill="#FF9800" font-weight="bold">📌 GNSS高さ精度</text>
          <text x="510" y="495" text-anchor="middle" font-size="9" fill="#FF9800">垂直RMS・PJ確認</text>

          <!-- Q_Z NO → XY誤差 -->
          <line x1="400" y1="400" x2="475" y2="400" stroke="#FF3D3D" stroke-width="1.5"/>
          <line x1="475" y1="400" x2="475" y2="545" stroke="#FF3D3D" stroke-width="1.5"/>
          <line x1="475" y1="545" x2="410" y2="545" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="480" y="394" font-size="9" fill="#FF3D3D">NO</text>

          <!-- Q_NE: N/E方向に偏り -->
          <polygon points="280,545 410,572 280,599 150,572" fill="#2D2D2D" stroke="#FFD700" stroke-width="1.5"/>
          <text x="280" y="568" text-anchor="middle" font-size="10" fill="#FFD700">N/E方向（前後左右）に</text>
          <text x="280" y="584" text-anchor="middle" font-size="10" fill="#FFD700">系統誤差がありますか？</text>

          <!-- Q_NE YES → アンテナ確認 -->
          <line x1="280" y1="599" x2="280" y2="622" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>
          <text x="295" y="615" font-size="9" fill="#00C853">YES</text>

          <!-- アンテナ仕様通り? -->
          <polygon points="280,622 395,648 280,674 165,648" fill="#2D2D2D" stroke="#FFD700" stroke-width="1.5"/>
          <text x="280" y="644" text-anchor="middle" font-size="10" fill="#FFD700">アンテナ取付位置・向きは</text>
          <text x="280" y="660" text-anchor="middle" font-size="10" fill="#FFD700">仕様通りですか？</text>

          <!-- アンテナ NO → LEAF アンテナ不良 -->
          <line x1="165" y1="648" x2="95" y2="648" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="122" y="642" text-anchor="middle" font-size="9" fill="#FF3D3D">NO</text>
          <rect x="-10" y="668" width="150" height="36" rx="6" fill="#FF3D3D" opacity="0.2" stroke="#FF3D3D" stroke-width="1.5"/>
          <!-- 矢印 -->
          <line x1="95" y1="648" x2="65" y2="648" stroke="#FF3D3D" stroke-width="1.5"/>
          <line x1="65" y1="648" x2="65" y2="668" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="65" y="684" text-anchor="middle" font-size="9" fill="#FF3D3D" font-weight="bold">📌 アンテナ取付不良</text>
          <text x="65" y="698" text-anchor="middle" font-size="9" fill="#FF3D3D">位置・向き・ガタ確認</text>

          <!-- アンテナ YES → LEAF PJファイル -->
          <line x1="395" y1="648" x2="460" y2="648" stroke="#00C853" stroke-width="1.5" marker-end="url(#arr_y)"/>
          <text x="427" y="642" text-anchor="middle" font-size="9" fill="#00C853">YES</text>
          <rect x="460" y="630" width="90" height="36" rx="6" fill="#FF9800" opacity="0.2" stroke="#FF9800" stroke-width="1.5"/>
          <text x="505" y="646" text-anchor="middle" font-size="9" fill="#FF9800" font-weight="bold">📌 PJファイル誤り</text>
          <text x="505" y="660" text-anchor="middle" font-size="9" fill="#FF9800">基準点・ローカライゼーション</text>

          <!-- Q_NE NO → LEAF PJファイル（同じ） -->
          <line x1="150" y1="572" x2="80" y2="572" stroke="#FF3D3D" stroke-width="1.5"/>
          <rect x="-10" y="715" width="150" height="36" rx="6" fill="#FF9800" opacity="0.2" stroke="#FF9800" stroke-width="1.5"/>
          <line x1="80" y1="572" x2="40" y2="572" stroke="#FF3D3D" stroke-width="1.5"/>
          <line x1="40" y1="572" x2="40" y2="715" stroke="#FF3D3D" stroke-width="1.5" marker-end="url(#arr_n)"/>
          <text x="65" y="731" text-anchor="middle" font-size="9" fill="#FF9800" font-weight="bold">📌 PJファイル・設定確認</text>
          <text x="65" y="745" text-anchor="middle" font-size="9" fill="#FF9800">ローカライゼーション再実施</text>

          <!-- 凡例 -->
          <rect x="380" y="740" width="10" height="10" fill="#FFD700"/>
          <text x="396" y="750" font-size="9" fill="#aaa">判断分岐</text>
          <rect x="440" y="740" width="10" height="10" fill="#FF3D3D" opacity="0.4"/>
          <text x="456" y="750" font-size="9" fill="#aaa">原因（赤）</text>
          <rect x="510" y="740" width="10" height="10" fill="#FF9800" opacity="0.4"/>
          <text x="526" y="750" font-size="9" fill="#aaa">原因（橙）</text>
        </svg>
        </div>
        """, unsafe_allow_html=True)

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
