import streamlit as st

# Sayfa ayarlarını yapıyoruz
st.set_page_config(
    page_title="Glow-Up Analytics",
    page_icon="🚀",
    layout="centered"
)

# Başlık
st.title("Glow-Up Analytics'e Hoş Geldin! 🚀")

# Markdown Alanı (Başındaki ve sonundaki tırnaklara dikkat!)
st.markdown("""
### Kendi Potansiyelini Keşfet
Bu uygulama, hayatının kontrolünü eline alman için tasarlandı. 

👈 **Sol taraftaki menüyü (Sidebar) kullanarak:**
* 👤 **Profil:** Vücut ölçülerini ve hedeflerini güncelle.
* 🍽️ **Beslenme:** Makrolarını takip et.
* 🏋️‍♀️ **Antrenman:** İdman hacmini ve gelişimini kaydet.
* 💊 **Supplement:** Günlük takviyelerini ve vitaminlerini yönet.
* 🌙 **Uyku:** Dinlenme kaliteni analiz et.

**Hadi başlayalım! Sol menüden bir sayfa seç.**
""")