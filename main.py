import streamlit as st
import tempfile
import os
from PIL import Image, ImageFilter
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

# Hata önleme ayarları
if not hasattr(Image, 'Resampling'):
    Image.Resampling = Image
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

st.set_page_config(page_title="Music Video Maker", layout="centered")
st.title("🎵 Music Video Maker")

# Label Yönetimi
if "labels" not in st.session_state:
    st.session_state.labels = ["EchoVerse Records", "Reborium Music Group"]

new_label_input = st.text_input("Create New Label", key="new_label_input")
if st.button("Add New Label"):
    if new_label_input.strip():
        st.session_state.labels.append(new_label_input.strip())
        st.success("Label eklendi!")

selected_label = st.selectbox("Select Label", st.session_state.labels)

# Dosya Yükleme
uploaded_image = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"])
uploaded_audio = st.file_uploader("Upload MP3 File", type=["mp3"])

if uploaded_image and uploaded_audio:
    if st.button("Generate Music Video"):
        with st.spinner("1080p Video oluşturuluyor..."):
            try:
                # Geçici dosyalar
                t_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                t_img.write(uploaded_image.read())
                t_aud = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                t_aud.write(uploaded_audio.read())

                # 1080p Hazırlık
                img = Image.open(t_img.name).convert("RGB")
                bg = img.resize((1920, 1080)).filter(ImageFilter.GaussianBlur(radius=30))
                img.thumbnail((1920, 1080), Image.ANTIALIAS)
                
                offset = ((1920 - img.width) // 2, (1080 - img.height) // 2)
                bg.paste(img, offset)
                
                final_bg_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
                bg.save(final_bg_path)

                # Video Oluşturma (TextClip iptal edildi)
                audio_clip = AudioFileClip(t_aud.name)
                video_clip = ImageClip(final_bg_path).set_duration(audio_clip.duration)
                final_video = video_clip.set_audio(audio_clip)
                
                output_file = "generated_video.mp4"
                final_video.write_videofile(output_file, fps=24, codec="libx264", bitrate="8000k")

                st.success(f"Video Başarıyla Oluşturuldu! (Label: {selected_label})")
                st.video(output_file)

                # Temizlik
                os.remove(t_img.name)
                os.remove(t_aud.name)
                os.remove(final_bg_path)

            except Exception as e:
                st.error(f"Hata oluştu: {e}")
