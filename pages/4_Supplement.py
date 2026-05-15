import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Supplement Takibi", page_icon="💊")
st.header("💊 Supplement ve Vitamin Takibi")

LISTE_DOSYASI = "supplement_list.csv"
GUNLUK_DOSYASI = "supplement_log.csv"


with st.expander("⚙️ Supplement Listeni Yönet (Yeni Ekle)"):
    st.write("Kullandığın takviyeleri buraya ekle. ")
    
    yeni_supp = st.text_input("Yeni Supplement Adı (Örn: C Vitamini):")
    if st.button("Listeye Ekle"):
        if yeni_supp:
            
            if os.path.isfile(LISTE_DOSYASI):
                df_list = pd.read_csv(LISTE_DOSYASI)
            else:
                df_list = pd.DataFrame(columns=["Supplement_Adi"])
            
            
            if yeni_supp not in df_list["Supplement_Adi"].values:
                
                yeni_satir = pd.DataFrame({"Supplement_Adi": [yeni_supp]})
                df_list = pd.concat([df_list, yeni_satir], ignore_index=True)
                df_list.to_csv(LISTE_DOSYASI, index=False)
                st.success(f"**{yeni_supp}** başarıyla listene eklendi!")
                st.rerun() 
            else:
                st.warning("Bu supplement zaten listende mevcut.")

   
    if os.path.isfile(LISTE_DOSYASI):
        df_list = pd.read_csv(LISTE_DOSYASI)
        if not df_list.empty:
            st.info("📝 **Mevcut Listen:** " + ", ".join(df_list["Supplement_Adi"].tolist()))


st.divider()


if os.path.isfile(LISTE_DOSYASI) and not pd.read_csv(LISTE_DOSYASI).empty:
    
    mevcut_supplementler = pd.read_csv(LISTE_DOSYASI)["Supplement_Adi"].tolist()
    
    with st.form("gunluk_supp_formu"):
        secilen_tarih = st.date_input("Tarih Seçiniz:", value=date.today())
        st.write("Bugün hangilerini aldın?")
        
        
        sonuclar = {}
        for supp in mevcut_supplementler:
            sonuclar[supp] = st.checkbox(supp)
            
        submit_supp = st.form_submit_button("Günlüğü Kaydet")
        
    if submit_supp:
        formatli_tarih = secilen_tarih.strftime("%d.%m.%Y")
        
        
        kayit_verisi = {"Date": [formatli_tarih]}
        
        
        for supp, durum in sonuclar.items():
            kayit_verisi[supp] = [durum]
            
        df_kayit = pd.DataFrame(kayit_verisi)
        
        
        if os.path.isfile(GUNLUK_DOSYASI):
            df_eski = pd.read_csv(GUNLUK_DOSYASI)
            df_yeni = pd.concat([df_eski, df_kayit], ignore_index=True)
            df_yeni.to_csv(GUNLUK_DOSYASI, index=False)
        else:
           
            df_kayit.to_csv(GUNLUK_DOSYASI, index=False)
            
        st.success("Günlük başarıyla kaydedildi! 💊")

else:
    
    st.info("Önce yukarıdaki menüden kullandığın supplementleri eklemelisin.")


if os.path.isfile(GUNLUK_DOSYASI):
    st.divider()
    st.subheader("📅 Son Takviye Kayıtların")
    
    df_show = pd.read_csv(GUNLUK_DOSYASI)
    
    
    df_visual = df_show.tail(10).copy()
    
    st.dataframe(df_visual, use_container_width=True)
    
    
    st.info(f"Toplam **{len(df_show)}** günlük supplement kaydın bulunuyor. İstikrarını bozma! ")


st.divider()

with st.expander("🛠️ Geçmiş Verileri Düzenle / Sil"):
    if os.path.isfile(GUNLUK_DOSYASI):
        df_edit = pd.read_csv(GUNLUK_DOSYASI)
        
        st.write("Tablodaki kutucukları işaretleyerek/kaldırarak veya sol taraftan satır silerek geçmiş günleri düzenleyebilirsin.")
        
        
        guncel_tablo = st.data_editor(
            df_edit, 
            num_rows="dynamic", 
            use_container_width=True
        )
        
        
        if st.button("Değişiklikleri Veritabanına Kaydet", key="supp_kaydet"):
            guncel_tablo.to_csv(GUNLUK_DOSYASI, index=False)
            st.success("Veriler başarıyla güncellendi! 🚀")
            st.rerun() 