import streamlit as st
import pandas as pd
import os
from datetime import date


st.set_page_config(page_title="Beslenme Takibi", page_icon="🍽️")
st.header("🍽️ Beslenme ve Makro Takibi")


with st.form("beslenme_formu"):
    secilen_tarih = st.date_input("Tarih Seçiniz:", value=date.today())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        protein = st.number_input("Protein (g):", min_value=0.0, value=0.0, step=1.0)
    with col2:
        carbs = st.number_input("Karbonhidrat (g):", min_value=0.0, value=0.0, step=1.0)
    with col3:
        fats = st.number_input("Yağ (g):", min_value=0.0, value=0.0, step=1.0)
    
    submit_nutrition = st.form_submit_button("Makroları Kaydet")


if submit_nutrition:
  
    toplam_kalori = (protein * 4) + (carbs * 4) + (fats * 9)
    formatli_tarih = secilen_tarih.strftime("%d.%m.%Y")
    
    
    nutrition_data = {
        "Date": [formatli_tarih],
        "Protein": [protein],
        "Carbs": [carbs],
        "Fats": [fats],
        "Total_Calories": [toplam_kalori]
    }
    
    
    pd.DataFrame(nutrition_data).to_csv(
        "nutrition_log.csv", 
        mode='a', 
        index=False, 
        header=not os.path.isfile("nutrition_log.csv")
    )
    st.success(f"Kayıt Başarılı! Toplam Kalori: **{toplam_kalori:.0f} kcal** 🔥")


if os.path.isfile("nutrition_log.csv"):
    st.divider()
    st.subheader("📈 Beslenmeni  İncele")
    
    
    df_nut = pd.read_csv("nutrition_log.csv")
    df_recent = df_nut.tail(7).copy()
    
  
    grafik_secimi = st.segmented_control(
        "Hangi grafiği incelemek istersin?", 
        options=["Kalori", "Makrolar"], 
        default="Kalori",
        selection_mode="single"
    )
    
    
    if grafik_secimi == "Kalori":
        st.write("🔥 **Kalori Takibi**")
        st.line_chart(
            df_recent.set_index("Date")["Total_Calories"],
            color="#FF4B4B" 
        )
        
    elif grafik_secimi == "Makrolar":
        st.write("🥗 **Makro Takibi**")
        st.line_chart(
            df_recent.set_index("Date")[["Protein", "Carbs", "Fats"]]
        )


# --- GEÇMİŞ VERİ YÖNETİMİ (CRUD: UPDATE & DELETE) ---
st.divider()

with st.expander("🛠️ Geçmiş Verileri Düzenle / Sil"):
    dosya_adi = "nutrition_log.csv"
    
    if os.path.isfile(dosya_adi):
        df_edit = pd.read_csv(dosya_adi)
        
        st.write("Tablodaki hücrelere çift tıklayarak değiştirebilir veya sol taraftan satır silebilirsin.")
        
        guncel_tablo = st.data_editor(
            df_edit, 
            num_rows="dynamic", 
            use_container_width=True
        )
        
        
        if st.button("Değişiklikleri Veritabanına Kaydet"):
            guncel_tablo.to_csv(dosya_adi, index=False)
            st.success("Veriler başarıyla güncellendi! 🚀")
            st.rerun() 