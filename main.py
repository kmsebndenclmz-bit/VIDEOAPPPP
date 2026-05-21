import streamlit as st
import tempfile
import os
from PIL import Image

# 1. Hata giderme satırı (PIL hatası için)
if not hasattr(Image, 'Resampling'):
    Image.Resampling = Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

# 2. Sayfa ayarları (SADECE 1 KEZ)
st.set_page_config(page_title="Music Video Maker", layout="centered")

st.title("🎵 Music Video Maker")

# Label yönetimi
if "labels" not in st.session_state:
    st.session_state.labels = ["EchoVerse Records", "Reborium Music Group"]

st.subheader("Label Settings")
new_label = st.text_input("Create New Label", key="label_giris_kutusu")

if st.button("Add New Label"):
    if new_label.strip() != "":
        st.session_state.labels.append(new_label.strip())
        st.success(f"Added: {new_label}")

selected_label = st.selectbox("Select Label", st.session_state.labels)

# Dosya yükleme
uploaded_image = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"])
uploaded_audio = st.file_uploader("Upload MP3 File", type=["mp3"])

if uploaded_image and uploaded_audio:
    st.write("Video oluşturulmaya hazır!")
    
    if st.button("Generate Music Video"):
        with st.spinner("Video oluşturuluyor..."):
            try:
                tfile_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                tfile_img.write(uploaded_image.read())
                
                tfile_aud = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tfile_aud.write(uploaded_audio.read())
                
                audio_clip = AudioFileClip(tfile_aud.name)
                image_clip = ImageClip(tfile_img.name).set_duration(audio_clip.duration)
                video = CompositeVideoClip([image_clip.set_audio(audio_clip)])
                
                output_filename = "final_video.mp4"
                video.write_videofile(output_filename, fps=24)
                
                st.success("Video başarıyla oluşturuldu!")
                st.video(output_filename)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
