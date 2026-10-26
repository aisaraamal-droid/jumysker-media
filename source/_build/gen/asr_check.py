"""Локальная проверка речи (Whisper small через sherpa-onnx): python3 asr_check.py MODEL_DIR AUDIO LANG(ru|kk)"""
import sys, subprocess, numpy as np, sherpa_onnx
model, audio, lang = sys.argv[1], sys.argv[2], sys.argv[3]
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
samples = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=f"{model}/small-encoder.int8.onnx", decoder=f"{model}/small-decoder.int8.onnx",
                                                 tokens=f"{model}/small-tokens.txt", language=lang, task="transcribe", num_threads=4)
s = rec.create_stream(); s.accept_waveform(16000, samples); rec.decode_stream(s)
print(s.result.text.strip())
