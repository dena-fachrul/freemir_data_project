import streamlit as st
import pandas as pd
import re
import io
from collections import Counter

# ================= KONFIGURASI HALAMAN =================
st.set_page_config(
    page_title="TikTok Comment Cleaner",
    page_icon="🧹",
    layout="centered"
)

# ================= CSS CUSTOM (AGAR TAMPILAN LEBIH CANTIK) =================
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
    }
    .stDownloadButton>button {
        width: 100%;
        background-color: #00cc66;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ================= 1. KAMUS & DATA (DARI KODINGAN KAMU) =================
# Saya masukkan semua kamus kamu di sini agar aplikasi mandiri
KAMUS_ALAY = {
    'yg':'yang','yng':'yang','ygk':'yang','ygj':'yang','gmn':'bagaimana',
    'gmna':'bagaimana','gimna':'bagaimana','gmnk':'bagaimana','gmn?':'bagaimana',
    'knp':'kenapa','kenp':'kenapa','knapa':'kenapa','knaoa':'kenapa','gk':'tidak',
    'ga':'tidak','g':'tidak','nggak':'tidak','ngak':'tidak','ndak':'tidak',
    'engga':'tidak','enggak':'tidak','dri':'dari','dr':'dari','drh':'darah',
    'darii':'dari','dri?':'dari','sbnr':'sebenarnya','sbner':'sebenarnya',
    'sebnernya':'sebenarnya','sbnrny':'sebenarnya','sbnarnya':'sebenarnya',
    'skrg':'sekarang','skrang':'sekarang',
    'skrng':'sekarang','skrn':'sekarang','skarng':'sekarang','skg':'sekarang',
    'tdk':'tidak','tkn':'tekan','tknya':'tekanannya','jd':'jadi','jdi':'jadi',
    'jdii':'jadi','jd?':'jadi','jdnya':'jadinya','jdny':'jadinya','sis':'sisa',
    'sisah':'sisa','sisanya':'sisanya',
    'sisa2':'sisa-sisa','bgt':'banget','bget':'banget','bgtt':'banget',
    'bangt':'banget','bnget':'banget','bnyak':'banyak','bnyk':'banyak',
    'banyk':'banyak','byk':'banyak','bmyk':'banyak','dl':'dulu','dlu':'dulu',
    'dlh':'dulu','duluu':'dulu',
    'dluu':'dulu','kl':'kalau','klo':'kalau','klw':'kalau','klau':'kalau',
    'klao':'kalau','sm':'sama','sma':'sama','smua':'semua','smw':'semua',
    'smuanya':'semuanya','smunya':'semuanya','sm2':'semua','aja':'saja',
    'aj':'saja','ajaa':'saja',
    'sja':'saja','sprti':'seperti','spti':'seperti','sprti?':'seperti',
    'sprtii':'seperti','speti':'seperti','trs':'terus','trus':'terus',
    'tros':'terus','trss':'terus','trs2':'terus-terusan','trusny':'terusnya',
    'udh':'sudah','ud':'sudah','uda':'sudah',
    'udahh':'sudah','udh2':'sudah-sudah','udh?':'sudah','dh':'sudah',
    'dah':'sudah','sdh':'sudah','ak':'aku','aq':'aku','q':'aku','gw':'aku',
    'gue':'aku','gua':'aku','km':'kamu','kmu':'kamu','kam':'kamu',
    'lu':'kamu','loe':'kamu','loe2':'kamu','plis':'please','plizz':'please',
    'pliiz':'please','pliss':'please','pls':'please','btw':'by the way',
    'btul':'betul','btl':'betul','bener':'benar','benr':'benar','bnr':'benar',
    'y':'ya','iy':'iya',
    'yo':'ya','ok':'oke','okk':'oke','oky':'oke','okeh':'oke','cm':'cuma',
    'cma':'cuma','cman':'cuma','cuman':'cuma','mw':'mau','mauu':'mau',
    'mauuu':'mau','ngap':'kenapa','ngapa':'kenapa','ngapain':'kenapa',
    'gausah':'tidak usah','gusah':'tidak usah',
    'gabisa':'tidak bisa','gabisaa':'tidak bisa','gbs':'tidak bisa',
    'gabise':'tidak bisa','gabis':'tidak bisa','tau':'tahu','gtau':'tidak tahu',
    'gatau':'tidak tahu','gtw':'tidak tahu','taun':'tahu','tauu':'tahu',
    'ksh':'kasih','kasihh':'kasih','msh':'masih','masi':'masih',
    'msih':'masih','msi':'masih','td':'tadi','tdi':'tadi','drtd':'dari tadi',
    'tdnya':'tadinya','kmrn':'kemarin','kmren':'kemarin','kemaren':'kemarin',
    'kmarin':'kemarin','mkn':'makan','mkan':'makan','mknya':'makannya',
    'makan2':'makan-makan','minum2':'minum-minum',
    'mnum':'minum','minumh':'minum','msk':'masuk','msuke':'masuk ke',
    'bkn':'bukan','bkan':'bukan','bknya':'bukannya','lbh':'lebih','lbih':'lebih',
    'krg':'kurang','tll':'terlalu','trllu':'terlalu','jdwl':'jadwal',
    'tmpt':'tempat','tmpat':'tempat',
    'tmptny':'tempatnya','tmpt2':'tempat-tempat','tmn':'teman','tmnn':'teman',
    'temen':'teman','temenn':'teman','bt':'bantu','bntu':'bantu',
    'bntuin':'bantuin','blm':'belum','blum':'belum','lgi':'lagi',
    'lg':'lagi','lgii':'lagi','lg2':'lagi-lagi',
    'ny':'nya','nyaa':'nya','nyy':'nya','nyg':'yang','da':'sudah',
    'udhah':'sudah','skrngny':'sekarangnya','skt':'sakit','skit':'sakit',
    'sktny':'sakitnya','pke':'pakai','pkai':'pakai','pake':'pakai',
    'pakenya':'pakainya','pkonya':'pokoknya',
    'ngk':'tidak','gnk':'tidak','kgn':'kangen','kgnn':'kangen','gitukan':'begitukan',
    'gtkan':'begitukan','bekuin':'dibekukan','beq':'beku','microwve':'microwave',
    'microwa':'microwave','ush':'usah','prasaan':'perasaan','perasn':'perasaan',
    'lmbek':'lembek','lemek':'lembek',
    'ank':'anak','anakk':'anak','anak2':'anak-anak','pngukus':'pengukus',
    'pnh':'penuh','pnuh':'penuh','iner':'inner','inerpot':'inner pot',
    'paksu':'suami','ushh':'usah','tgk':'tengok','tngok':'tengok',
    'bole':'boleh','blh':'boleh','sne':'sana',
    'sni':'sini','airny':'airnya','mndidih':'mendidih','duk':'duduk','duuk':'duduk',
    'dug':'dukung','nasiny':'nasinya','nsi':'nasi','bsi':'basi','best':'bagus',
    'baguss':'bagus','try':'coba','cloudkitchen':'cloud kitchen',
    'ratarata':'rata-rata','rata2':'rata-rata',
    'huhu':'sedih','duuh':'aduh','bolehh':'boleh','yaa':'ya','kk':'kakak',
    'thn':'tahun','rekomen':'rekomendasi','sbb':'sebab','ikut2':'ikut-ikut',
    'ltran':'literan','enteng':'ringan','diluar':'di luar','simpen':'simpan',
    'same':'sampai','lngsung':'langsung',
    'ditaro':'ditaruh','soalnya':'karena','dimasukin':'dimasukkan',
    'diangetin':'dihangatkan','pda':'pada','kbuang':'kebuang','yh':'ya',
    'mnding':'mending','drmh':'di rumah','kels':'kelas','krj':'kerja',
    'plg':'pulang','dpemanas':'di pemanas',
    'pdhl':'padahal','mssi':'masih','dbuang':'dibuang','nene':'nenek',
    'ampe':'sampai','tar':'nanti','seminggu':'satu minggu','majikan':'majikan',
    'nasgor':'nasi goreng','racikan':'racikan','aqu':'aku','siihh':'sih',
    'gag':'tidak','blg':'bilang','jgk':'juga',
    'krn':'karena','bs':'bisa','angi':'angin','pntg':'penting','ka':'kak',
    'angetin':'hangatkan','endoll':'enak','jg':'juga','w':'aku','taro':'simpan',
    'betuul':'betul','kdg':'kadang','bund':'bunda','gj':'juga',
    'hr':'hari','hri':'hari',
    # Tambahan baru
    'sy':'saya','pk':'pakai','pki':'pakai','pk youngma':'pakai','mateng':'matang',
    'matiin':'mematikan','mubadzir':'mubazir','mubazir':'mubazir','jga':'juga',
    'namnya':'namanya','max':'maksimal','2jam':'2 jam','di cabut':'dicabut',
    'dicabut':'dicabut','br':'baru','bngt':'banget','bun':'bunda','basik':'basi',
    'uap nya':'uapnya','nasih':'nasi','menyembab':'menyebabkan',
    'menyembabkan':'menyebabkan','colokan nya':'colokannya','renggangkan':'renggangkan',
    'mejikom':'magic com','emg':'memang','dll':'dan lain-lain','brg':'barang',
    'smpe':'sampai','tonggolannya':'tombolnya','besokin':'besoknya',
    'wlpn':'walaupun','prodak':'produk','poll':'sekali','jeglek':'jatuh',
    'diemin':'diamkan','mnt':'menit','mntn':'menit',
    'amin':'ada yang','nyisa':'tersisa','frizer':'freezer',
    'pn':'pun','nang':'ke','riview':'review','nih':'ini','pya':'punya',
    'th':'tahun','colokin':'colokkan','sya':'saya','trgantung':'tergantung',
    'sampe':'sampai',
    'besttt':'terbaik','usahain':'usahakan','2kali':'dua kali','zonk':'kecewa',
    'aman2':'aman-aman','telor':'telur','15menit':'15 menit','hbis':'habis',
    'bngeet':'banget','tur':'terus',
    'kepake':'kepakai','sayng':'sayang','apapaun':'apapun',
    'digituin':'diperlakukan begitu','pawon':'dapur','apik':'bagus',
    'nasix':'nasi','malem':'malam','maka nya':'makanya','tergos':'tergores',
    'gadi':'ganti','awettt':'awet','stelah':'setelah','matan':'matang',
    'trgntg':'tergantung','berasny':'berasnya','dirumah':'di rumah',
    'ttp':'tetap','tinggak':'tinggal','minyaj':'minyak',
    'stsinlis':'stainless','gak':'tidak','emang':'memang','tpi':'tapi',
    'bgus':'bagus','kyk':'kayak','pnya':'punya','akuuu':'aku',
    'lngsng':'langsung','busukkk':'busuk',
    'cabutt':'cabut','pencer':'pencet','tu':'itu','philip':'Philips',
    'youngma':'YongMa','yongma':'YongMa','yong ma':'YongMa',
    'kosmos':'Cosmos','cosmos':'Cosmos',
    'cpt':'cepat','bgs':'bagus','nyolok':'colok','tak':'tidak',
    'dlm':'dalam','krna':'karena','mf':'maaf','nginep':'menginap',
    'ktnya':'katanya','matng':'matang',
    'clokanya':'colokannya','type':'tipe','24jam':'24 jam','tnpa':'tanpa',
    'semporna':'sempurna','didlm':'di dalam','kuwalitas':'kualitas',
    'magicoom':'magic com','gpp':'tidak apa-apa','pd':'pada',
    'megicom':'magic com','utk':'untuk','bner':'benar','bukn':'bukan',
    'merendhkn':'merendahkan','bermerk':'bermerek','akn':'akan',
    'cepet':'cepat','kucek':'mengucek','mamahku':'ibuku',
    'airn':'air','gmpang':'gampang','stlah':'setelah','mnikah':'menikah',
    'mam':'mama','mf':'maaf','klo':'kalau','didlm':'di dalam','pd':'pada',
    'bukn':'bukan','kwalitas':'kualitas','magicoom':'magic com','tp':'tapi'
}

KATA_TANYA = {
    'gimana', 'bagaimana', 'apa', 'apakah', 'kah', 'berapa', 'brp',
    'kapan', 'mana', 'dimana', 'boleh', 'bisa', 'aman', 'kenapa', 'kok'
}

KATA_SETUJU = {
    'betul', 'bener', 'benar', 'setuju', 'sepakat', 'valid', 'memang',
    'yoi', 'tepat', 'real', 'iya', 'emang', 'terima kasih', 'makasih', 'sama-sama'
}

KATA_POSITIF = {
    'enak', 'sedap', 'bagus', 'mantap', 'suka', 'sehat', 'awet', 'praktis', 'cepat',
    'berguna', 'pulen', 'ok', 'oke', 'solusi', 'bantu', 'info', 'jelas', 'satset',
    'hemat', 'murah', 'sering', 'selalu', 'biasa', 'aman', 'cocok', 'efisien',
    'coba', 'masuk', 'stok', 'tahan', 'alhamdulillah', 'keren', 'cantik'
}

KATA_NEGATIF = {
    'tidak', 'jangan', 'bukan', 'gak', 'ga', 'basi', 'bau', 'keras', 'hambar',
    'sakit', 'racun', 'bahaya', 'takut', 'mahal', 'ribet', 'susah', 'lembek',
    'benyek', 'dingin', 'aneh', 'rugi', 'boncos', 'kurang', 'salah', 'jelek',
    'bakteri', 'kanker', 'mager', 'malas', 'pelit', 'plastik', 'gula', 'pemicu',
    'diare', 'ngapain'
}

STOPWORDS = {
    'yang', 'dan', 'di', 'ke', 'dari', 'ini', 'itu', 'aku', 'kamu', 'saya', 'dia',
    'kita', 'kakak', 'kak', 'ka', 'bang', 'dok', 'dokter', 'mas', 'mba', 'sudah',
    'belum', 'bisa', 'ada', 'mau', 'lagi', 'aja', 'saja', 'kok', 'sih', 'ya',
    'yuk', 'dong', 'kan', 'pun', 'tapi', 'kalau', 'karena', 'untuk', 'buat',
    'sama', 'dengan', 'atau', 'jadi', 'pas', 'cuma', 'banget', 'loh', 'deh', 'nah',
    'tuh', 'memang'
}

MINIMAL_KARAKTER = 5

# ================= 2. FUNGSI LOGIKA (BACKEND) =================

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text_clean = re.sub(r'[^a-zA-Z0-9\s.,?!-]', '', text)
    text_clean = re.sub(r'\s+', ' ', text_clean).strip()

    words = text_clean.split()
    cleaned_words = []

    for word in words:
        m = re.match(r'^([A-Za-z0-9-]+)([?.!,]*)$', word)
        if m:
            base = m.group(1).lower()
            punct = m.group(2) or ''
        else:
            base = word.lower()
            punct = ''

        if base in KAMUS_ALAY:
            cleaned_words.append(KAMUS_ALAY[base] + punct)
        else:
            cleaned_words.append(base + punct if base != word else word)

    sentence = " ".join(cleaned_words)
    sentence = re.sub(r'([.,?!])(\w)', r'\1 \2', sentence)
    return sentence.capitalize()


def get_keywords_list(text: str):
    if not isinstance(text, str):
        return []
    clean_for_key = re.sub(r'[^\w\s]', '', text.lower())
    words = clean_for_key.split()
    meaningful_words = [
        w.capitalize()
        for w in words
        if w not in STOPWORDS and len(w) > 2
    ]
    return meaningful_words


def categorize_comment(text: str) -> str:
    if not isinstance(text, str):
        return "Neutral"

    if "?" in text:
        return "Question"

    text_lower = text.lower()
    words = re.sub(r'[^\w\s]', '', text_lower).split()

    for word in words:
        if word in KATA_TANYA:
            return "Question"

    if any(w in words for w in KATA_SETUJU):
        return "Statement"

    score = 0
    skip_next = False
    for i, word in enumerate(words):
        if skip_next:
            skip_next = False
            continue

        is_negation = word in ['tidak', 'jangan', 'bukan', 'gak', 'ga', 'kurang']
        if is_negation and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word in KATA_POSITIF:
                score -= 2
                skip_next = True
            elif next_word in KATA_NEGATIF:
                score += 1
                skip_next = True
        else:
            if word in KATA_POSITIF:
                score += 1
            elif word in KATA_NEGATIF:
                score -= 1

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"


def process_uploaded_file(uploaded_file):
    """Fungsi utama untuk memproses file yang diupload user"""
    xls = pd.read_excel(uploaded_file, sheet_name=None, header=None)
    
    output_sheets = {}
    summary_rows = []
    global_keywords = []
    
    # Progress bar
    progress_bar = st.progress(0)
    total_sheets = len(xls)
    current_sheet_idx = 0

    for sheet_name, df in xls.items():
        raw_data = df.iloc[:, 0].astype(str).tolist()

        data_main = []
        all_keywords_in_sheet = []
        nomor = 1

        for i in range(len(raw_data)):
            current_cell = raw_data[i].strip()

            if current_cell.endswith("Reply"):
                if i >= 2:
                    comment_ori = raw_data[i - 1].strip()
                    username = raw_data[i - 2].strip()

                    comment_clean = clean_text(comment_ori)

                    if comment_clean and len(comment_clean) >= MINIMAL_KARAKTER:
                        kw_list = get_keywords_list(comment_clean)
                        all_keywords_in_sheet.extend(kw_list)
                        global_keywords.extend(kw_list)

                        kw_sorted_len = sorted(list(set(kw_list)), key=len, reverse=True)
                        kw_string = ", ".join(kw_sorted_len[:3])
                        sentiment_label = categorize_comment(comment_clean)

                        row_dict = {
                            'No': nomor,
                            'Username': username,
                            'Comment': comment_clean,
                            'Keywords': kw_string,
                            'Sentiment': sentiment_label
                        }
                        data_main.append(row_dict)

                        summary_rows.append({
                            'Sheet': sheet_name,
                            'No': nomor,
                            'Username': username,
                            'Comment': comment_clean,
                            'Keywords': kw_string,
                            'Sentiment': sentiment_label
                        })

                        nomor += 1

        if data_main:
            df_main = pd.DataFrame(data_main)
            keyword_counts = Counter(all_keywords_in_sheet)
            keyword_counts_filtered = {k: v for k, v in keyword_counts.items() if v >= 5}

            if keyword_counts_filtered:
                df_kw_stats = pd.DataFrame(keyword_counts_filtered.items(), columns=['Unique Keyword', 'Freq'])
                df_kw_stats = df_kw_stats.sort_values(by='Freq', ascending=False).reset_index(drop=True)
            else:
                df_kw_stats = pd.DataFrame(columns=['Unique Keyword', 'Freq'])

            cat_counts = df_main['Sentiment'].value_counts().reset_index()
            cat_counts.columns = ['Sentiment Label', 'Count']

            df_main['   '] = ''
            df_kw_stats['    '] = ''

            df_final_sheet = pd.concat([df_main, df_kw_stats, cat_counts], axis=1)
            output_sheets[sheet_name] = df_final_sheet
        
        # Update progress bar
        current_sheet_idx += 1
        progress_bar.progress(current_sheet_idx / total_sheets)

    # --- SUMMARY SHEET ---
    df_summary_final = None
    if summary_rows:
        df_summary_main = pd.DataFrame(summary_rows, columns=['Sheet', 'No', 'Username', 'Comment', 'Keywords', 'Sentiment'])
        
        keyword_counts_global = Counter(global_keywords)
        keyword_counts_global_filtered = {k: v for k, v in keyword_counts_global.items() if v >= 5}

        if keyword_counts_global_filtered:
            df_sum_kw_stats = pd.DataFrame(keyword_counts_global_filtered.items(), columns=['Unique Keyword', 'Freq'])
            df_sum_kw_stats = df_sum_kw_stats.sort_values(by='Freq', ascending=False).reset_index(drop=True)
        else:
            df_sum_kw_stats = pd.DataFrame(columns=['Unique Keyword', 'Freq'])

        sentiment_counts_global = df_summary_main['Sentiment'].value_counts().reset_index()
        sentiment_counts_global.columns = ['Sentiment Label', 'Count']

        df_summary_main['   '] = ''
        df_sum_kw_stats['    '] = ''

        df_summary_final = pd.concat([df_summary_main, df_sum_kw_stats, sentiment_counts_global], axis=1)

    # --- WRITE TO BUFFER (Bukan File Disk) ---
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        for sheet, df_out in output_sheets.items():
            df_out.to_excel(writer, sheet_name=sheet, index=False)
        if df_summary_final is not None:
            df_summary_final.to_excel(writer, sheet_name='Summaries', index=False)
    
    return buffer

# ================= 3. TAMPILAN WEB (FRONTEND) =================

st.title("🧹 TikTok Comment Cleaner")
st.write("""
Aplikasi ini membersihkan komentar TikTok dari bahasa alay, 
mengambil keyword penting, dan menganalisis sentimen secara otomatis.
""")

with st.expander("ℹ️ Cara Penggunaan"):
    st.write("""
    1. Siapkan file Excel (`.xlsx`) hasil copy-paste dari TikTok (format sesuai template).
    2. Upload file pada kotak di bawah.
    3. Tunggu proses cleaning selesai.
    4. Klik tombol **Download** untuk mengunduh hasil yang sudah bersih.
    """)

# Kotak Upload File
uploaded_file = st.file_uploader("Upload File Excel Kamu", type=['xlsx'])

if uploaded_file is not None:
    st.info("File berhasil diupload. Sedang memproses...")
    
    try:
        # Jalankan proses
        result_buffer = process_uploaded_file(uploaded_file)
        
        # Reset pointer buffer ke awal agar bisa didownload
        result_buffer.seek(0)
        
        st.success("✅ Proses selesai! Silakan download hasilnya.")
        
        # Tombol Download
        st.download_button(
            label="📥 Download Hasil Cleaning (.xlsx)",
            data=result_buffer,
            file_name="output_comment_clean.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses file: {e}")
        st.write("Pastikan format Excel sesuai dengan standar.")

st.write("---")
st.caption("Dibuat dengan Python & Streamlit")