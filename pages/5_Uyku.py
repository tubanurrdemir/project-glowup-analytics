import streamlit as st
import pandas as pd
import os
from datetime import date


st.set_page_config(page_title="Uyku Takibi", page_icon="🌙")
st.header("🌙 Uyku Takibi")


UYKU_DOSYASI = "sleep_log.csv"


with st.form("uyku_formu"):
    st.write("Gelişim uykuda gerçekleşir. Dün gece nasıldı?")
    
    secilen_tarih = st.date_input("Tarih Seçiniz :", value=date.today())
    
    col1, col2 = st.columns(2)
    with col1:
        
        uyku_suresi = st.slider("Uyku Süresi (Saat)", min_value=0.0, max_value=24.0, value=7.5, step=0.5)
    with col2:
        
        uyku_kalitesi = st.selectbox("Uyku Kalitesi (1-5)", options=[1, 2, 3, 4, 5], index=2, 
                                     help="1: Çok kötü, sürekli uyandım. 5: Deliksiz ve dinç uyandım.")
        
    notlar = st.text_input("Gecenin Notu (Örn: Gece kahve içtim, stresliydim vb.)")
    
    submit_sleep = st.form_submit_button("Uyku Verisini Kaydet")


if submit_sleep:
    formatli_tarih = secilen_tarih.strftime("%d.%m.%Y")
    
    sleep_data = {
        "Date": [formatli_tarih],
        "Uyku_Suresi": [uyku_suresi],
        "Uyku_Kalitesi": [uyku_kalitesi],
        "Notlar": [notlar]
    }
    
    df_kayit = pd.DataFrame(sleep_data)
    
    
    if os.path.isfile(UYKU_DOSYASI):
        df_eski = pd.read_csv(UYKU_DOSYASI)
        df_yeni = pd.concat([df_eski, df_kayit], ignore_index=True)
        df_yeni.to_csv(UYKU_DOSYASI, index=False)
    else:
        df_kayit.to_csv(UYKU_DOSYASI, index=False)
        
    st.success(f"Kayıt Başarılı! Toplam {uyku_suresi} saat uyudun. 💤")


if os.path.isfile(UYKU_DOSYASI):
    st.divider()
    df_uyku = pd.read_csv(UYKU_DOSYASI)
    
    
    if not df_uyku.empty:
        st.subheader("📈 Uyku Analizin")
        
        
        df_recent = df_uyku.tail(7).copy()
        ortalama_uyku = df_recent["Uyku_Suresi"].mean()
        
        
        st.metric(label="Son 7 Günlük Ortalama Uykun", value=f"{ortalama_uyku:.1f} Saat")
        
        
        st.area_chart(df_recent.set_index("Date")["Uyku_Suresi"], color="#60b4ff")
        
        

        st.divider()
        with st.expander("🛠️ Geçmiş Verileri Düzenle / Sil"):
            st.write("Tablo üzerinde çift tıklayarak düzeltme yapabilir veya satır silebilirsin.")
            
            
            df_ters = df_uyku.iloc[::-1].reset_index(drop=True)
            
            guncel_tablo = st.data_editor(
                df_ters, 
                num_rows="dynamic", 
                use_container_width=True
            )
            
            if st.button("Değişiklikleri Kaydet", key="uyku_kaydet"):
                
                tablo_duz = guncel_tablo.iloc[::-1].reset_index(drop=True)
                tablo_duz.to_csv(UYKU_DOSYASI, index=False)
                st.success("Uyku verileri başarıyla güncellendi! 🚀")
                st.rerun()