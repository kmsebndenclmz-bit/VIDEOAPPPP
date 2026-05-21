import streamlit as st
import os
import sys
import subprocess

# Kütüphaneleri kod çalışırken yükle
try:
    import moviepy
    import PIL
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy==1.0.3", "Pillow==9.5.0"])

# Şimdi import et
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
from PIL import Image, ImageFilter
import tempfile

# Sayfa yapılandırması
st.set_page_config(page_title="Music Video Maker", layout="centered")
    
# Geri kalan kodların
st.set_page_config(page_title="Music Video Maker", layout="centered")
st.title("🎵 Music Video Maker")

# Label yönetimi
if "labels" not in st.session_state:
    st.session_state.labels = ["EchoVerse Records", "Reborium Music Group"]

st.subheader("Label Settings")
new_label = st.text_input("Create New Label")
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
    # ... kendi kodların ...

st.title("🎵 Music Video Maker")

# Label yönetimi
if "labels" not in st.session_state:
    st.session_state.labels = ["© EchoVerse Records", "© Reborium Music Group"]

st.subheader("Label Settings")
new_label = st.text_input("Create New Label")
if st.button("Add New Label"):
    if new_label.strip() != "":
        st.session_state.labels.append(new_label.strip())
        st.success(f"Added: {new_label}")

selected_label = st.selectbox("Select Label", st.session_state.labels)

# Dosya yükleme
uploaded_image = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"])
uploaded_audio = st.file_uploader("Upload MP3 File", type=["mp3"])

if uploaded_image and uploaded_audio:
    if st.button("Generate Music Video"):
        with st.spinner("Rendering video..."):
            temp_dir = tempfile.mkdtemp()
            image_path = os.path.join(temp_dir, "cover.png")
            audio_path = os.path.join(temp_dir, "audio.mp3")
            output_path = os.path.join(temp_dir, "final_video.mp4")

            with open(image_path, "wb") as f: f.write(uploaded_image.read())
            with open(audio_path, "wb") as f: f.write(uploaded_audio.read())

            audio = AudioFileClip(audio_path)
            
            # Arka plan oluştur
            bg_image = Image.open(image_path).convert("RGB").resize((1920, 1080)).filter(ImageFilter.GaussianBlur(radius=35))
            blurred_bg_path = os.path.join(temp_dir, "blurred_bg.jpg")
            bg_image.save(blurred_bg_path)

            background_clip = ImageClip(blurred_bg_path).set_duration(audio.duration).resize((1920, 1080))
            main_clip = ImageClip(image_path).set_duration(audio.duration).resize(height=850).set_position("center")
            
            # Metin oluşturma (MoviePy'nin yerleşik fontunu kullanıyoruz)
            label_clip = TextClip(selected_label, fontsize=70, color='white', font='DejaVu-Sans', method='caption', size=(1920, 100))
            label_clip = label_clip.set_duration(audio.duration).set_position(('left', 'bottom'))

            final_video = CompositeVideoClip([background_clip, main_clip, label_clip], size=(1920, 1080)).set_audio(audio)
            final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")

            st.success("Video generated successfully!")
            with open(output_path, "rb") as file:
                st.download_button("Download Video", data=file, file_name="music_video.mp4", mime="video/mp4")
