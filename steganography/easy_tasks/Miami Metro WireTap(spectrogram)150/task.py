import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
from scipy.signal import istft


def create_full_canvas_spectrogram(
    input_mp3,
    output_mp3,
    flag="Securinets{s3cur1n3t5_w1ll_n3v3r_g1v3_y0u_uppp}",
):
  print(
      "Analyzing input MP3 length to match full horizontal canvas duration..."
  )

  # Load audio to match its exact length
  sample_rate = 22050
  song = AudioSegment.from_mp3(input_mp3).set_channels(2).set_frame_rate(sample_rate)
  left_samples = np.array(song.get_array_of_samples())[0::2]
  total_audio_samples = len(left_samples)

  # Spectrogram parameters
  nperseg = 1024  # 513 frequency bins (vertical height)
  noverlap = 768
  hop_size = nperseg - noverlap

  # Calculate exact number of time frames needed to fill the entire song length horizontally
  target_width_frames = total_audio_samples // hop_size
  height = nperseg // 2 + 1  # 513 vertical bins

  print(
      f"Creating massive canvas: {target_width_frames}px wide x {height}px"
      " high..."
  )

  # Create blank grayscale image covering the entire duration
  img = Image.new("L", (target_width_frames, height), color=0)
  draw = ImageDraw.Draw(img)

  # Find a bold system font on Kali Linux
  font_paths = [
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
      "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
      "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
  ]
  font = None
  # Scale font size to take up most of the vertical height (e.g., ~350px tall)
  font_size = 350
  for path in font_paths:
    if os.path.exists(path):
      try:
        font = ImageFont.truetype(path, font_size)
        break
      except Exception:
        continue

  if font is None:
    font = ImageFont.load_default()

  # Draw the flag so it spans nicely across the canvas width and fills the vertical space
  # Padding it slightly from the left edge so it starts cleanly
  draw.text((100, 50), flag, fill=255, font=font)

  # Convert image to numpy array & flip vertically (low frequencies at bottom, high at top)
  img_array = np.array(img, dtype=np.float32) / 255.0
  img_array = np.flipud(img_array)

  print(
      "Applying Inverse Short-Time Fourier Transform (ISTFT) to map pixels to"
      " audio..."
  )
  np.random.seed(42)
  random_phases = np.exp(
      2j * np.pi * np.random.rand(img_array.shape[0], img_array.shape[1])
  )
  stft_matrix = img_array * random_phases * 25.0

  # Convert back to audio samples
  _, right_audio = istft(
      stft_matrix,
      fs=sample_rate,
      nperseg=nperseg,
      noverlap=noverlap,
      window="hann",
  )

  # Match exact sample lengths
  if len(right_audio) < total_audio_samples:
    right_audio = np.pad(
        right_audio, (0, total_audio_samples - len(right_audio)), "constant"
    )
  elif len(right_audio) > total_audio_samples:
    right_audio = right_audio[:total_audio_samples]

  # Normalize and scale right channel volume
  right_audio = right_audio / (np.max(np.abs(right_audio)) + 1e-5)
  right_samples = (right_audio * 15000).astype(np.int16)

  print("Merging clean left track with full-canvas spectrogram right track...")
  new_samples = np.empty(
      (len(left_samples) + len(right_samples),), dtype=np.int16
  )
  new_samples[0::2] = left_samples
  new_samples[1::2] = right_samples

  # Export final file at high bitrate
  output_segment = AudioSegment(
      data=new_samples.tobytes(),
      sample_width=2,
      frame_rate=sample_rate,
      channels=2,
  )
  output_segment.export(output_mp3, format="mp3", bitrate="320k")
  print(
      f"Success! Full-canvas spectrogram challenge file saved to: {output_mp3}"
  )


if __name__ == "__main__":
  create_full_canvas_spectrogram("audio.mp3", "challenge_output.mp3")
