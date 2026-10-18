import math
import struct
import wave

# Define the Morse code dictionary
MORSE_CODE_DICT = {
    'A': '.-',
    'B': '-...',
    'C': '-.-.',
    'D': '-..',
    'E': '.',
    'F': '..-.',
    'G': '--.',
    'H': '....',
    'I': '..',
    'J': '.---',
    'K': '-.-',
    'L': '.-..',
    'M': '--',
    'N': '-.',
    'O': '---',
    'P': '.--.',
    'Q': '--.-',
    'R': '.-.',
    'S': '...',
    'T': '-',
    'U': '..-',
    'V': '...-',
    'W': '.--',
    'X': '-..-',
    'Y': '-.--',
    'Z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    '{': '-.--.-',  # Using close approximation or handle gracefully
    '}': '-.--.-',
    '_': '..--.-',
    ' ': ' '
}


def text_to_morse(text):
  morse_sequence = []
  for char in text.upper():
    if char in MORSE_CODE_DICT:
      morse_sequence.append(MORSE_CODE_DICT[char])
    elif char == '{':
      morse_sequence.append('-.--.-')
    elif char == '}':
      morse_sequence.append('-.--.-')
    elif char == '_':
      morse_sequence.append('..--.-')
    else:
      morse_sequence.append(' ')
  return ' '.join(morse_sequence)


def generate_tone(frequency, duration, sample_rate=44100, volume=0.5):
  num_samples = int(sample_rate * duration)
  samples = []
  for i in range(num_samples):
    t = i / sample_rate
    # Sine wave formula with a slight fade-in/out envelope to prevent clicking
    envelope = 1.0
    if i < 400:
      envelope = i / 400
    elif i > num_samples - 400:
      envelope = (num_samples - i) / 400

    sample = int(
        32767
        * volume
        * envelope
        * math.sin(2 * math.pi * frequency * t)
    )
    samples.append(struct.pack('<h', sample))
  return b''.join(samples)


def generate_silence(duration, sample_rate=44100):
  num_samples = int(sample_rate * duration)
  return b'\x00\x00' * num_samples


def create_morse_wav(filename, flag_text):
  sample_rate = 44100
  frequency = 700  # 700 Hz tone
  dot_duration = 0.08  # Duration of a dot in seconds
  dash_duration = dot_duration * 3
  intra_symbol_gap = dot_duration
  letter_gap = dot_duration * 3
  word_gap = dot_duration * 7

  morse_str = text_to_morse(flag_text)
  audio_data = bytearray()

  dot_audio = generate_tone(frequency, dot_duration, sample_rate)
  dash_audio = generate_tone(frequency, dash_duration, sample_rate)
  intra_gap_audio = generate_silence(intra_symbol_gap, sample_rate)
  letter_gap_audio = generate_silence(letter_gap, sample_rate)
  word_gap_audio = generate_silence(word_gap, sample_rate)

  words = morse_str.split('   ')
  for w_idx, word in enumerate(words):
    letters = word.split(' ')
    for l_idx, letter in enumerate(letters):
      for s_idx, symbol in enumerate(letter):
        if symbol == '.':
          audio_data.extend(dot_audio)
        elif symbol == '-':
          audio_data.extend(dash_audio)

        if s_idx < len(letter) - 1:
          audio_data.extend(intra_gap_audio)

      if l_idx < len(letters) - 1:
        audio_data.extend(letter_gap_audio)

    if w_idx < len(words) - 1:
      audio_data.extend(word_gap_audio)

  with wave.open(filename, 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(audio_data)

  print(f'Successfully generated {filename} for flag: {flag_text}')


if __name__ == '__main__':
  flag = 'Securinets{d1d_y0u_4ctu4lly_l1st3n_0r_just_us3_cyberchef}'
  create_morse_wav('flag.wav', flag)
