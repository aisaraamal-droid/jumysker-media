# -*- coding: utf-8 -*-
"""Подгонка клипа ведущего под чистый голос ElevenLabs.

Seedance сам переозвучивает реплику по образцу (и по-русски/по-казахски неразборчиво), но ритм речи
у него близок к образцу. Поэтому: выравниваем огибающие громкости (его дорожка ↔ наш TTS) через DTW,
сглаживаем отображение времени и берём кадры клипа по этому отображению. Звук — только наш TTS.
"""
import subprocess
import numpy as np

HOP = 0.04


def envelope(path, hop=HOP):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    n = int(16000 * hop)
    m = len(x) // n
    e = np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1)) + 1e-4
    e = np.log(e)
    return (e - e.mean()) / (e.std() + 1e-6)


def dtw_path(a, b, band=0.35):
    """Путь DTW с запретом длинных горизонталей/вертикалей (шаги (1,1),(1,2),(2,1))."""
    n, m = len(a), len(b)
    INF = 1e18
    D = np.full((n + 1, m + 1), INF)
    D[0, 0] = 0
    w = int(max(n, m) * band) + abs(n - m)
    for i in range(1, n + 1):
        jc = i * m / n
        for j in range(max(1, int(jc - w)), min(m, int(jc + w)) + 1):
            c = (a[i - 1] - b[j - 1]) ** 2
            best = D[i - 1, j - 1]
            if i >= 2 and j >= 1:
                best = min(best, D[i - 2, j - 1] + c * 0.5)
            if i >= 1 and j >= 2:
                best = min(best, D[i - 1, j - 2] + c * 0.5)
            D[i, j] = best + c
    i, j, path = n, m, [(n - 1, m - 1)]
    while i > 1 or j > 1:
        cands = [(D[i - 1, j - 1], i - 1, j - 1)]
        if i >= 2:
            cands.append((D[i - 2, j - 1], i - 2, j - 1))
        if j >= 2:
            cands.append((D[i - 1, j - 2], i - 1, j - 2))
        _, i, j = min(cands)
        i, j = max(i, 1), max(j, 1)
        path.append((i - 1, j - 1))
    return path[::-1]


def time_map(tts_audio, clip_audio, out_dur, smooth=0.36, lo=0.55, hi=1.8):
    """Возвращает функцию: время в итоговом ролике (по TTS) -> время в клипе Seedance."""
    a, b = envelope(tts_audio), envelope(clip_audio)
    path = dtw_path(a, b)
    ta = np.arange(len(a)) * HOP
    tb = np.zeros(len(a))
    cnt = np.zeros(len(a))
    for i, j in path:
        tb[i] += j * HOP
        cnt[i] += 1
    tb = tb / np.maximum(cnt, 1)
    k = max(1, int(smooth / HOP))
    pad = np.pad(tb, (k, k), mode="edge")
    tb = np.convolve(pad, np.ones(2 * k + 1) / (2 * k + 1), mode="valid")
    # монотонность и ограничение скорости
    for i in range(1, len(tb)):
        tb[i] = min(max(tb[i], tb[i - 1] + lo * HOP), tb[i - 1] + hi * HOP)
    clip_len = len(b) * HOP

    def f(t):
        if t <= ta[-1]:
            return float(np.interp(t, ta, tb))
        return float(min(clip_len - 0.05, tb[-1] + (t - ta[-1])))
    return f


def mouth_signal(frames, box):
    """Средняя межкадровая разница в области рта — грубая мера «рот двигается»."""
    from PIL import Image
    prev, sig = None, []
    for p in frames:
        im = np.asarray(Image.open(p).convert("L").crop(box), dtype=np.float32)
        sig.append(0.0 if prev is None else float(np.abs(im - prev).mean()))
        prev = im
    return np.array(sig)
