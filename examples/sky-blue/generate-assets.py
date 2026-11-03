"""Generate original stage-0 design assets. Requires Pillow; no app dependencies.

Usage: python generate-assets.py --font /path/to/a/CJK-font.ttc
Outputs are reproducible fixtures and design diagrams, not a rendered video.
"""
from __future__ import annotations

import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import sys
import wave

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
PROJECT = BASE.parent.parent
BG = '#0B1020'
PANEL = '#192238'
TEXT = '#EFF5FF'
MUTED = '#A9BAD5'
ACCENT = '#67D8FF'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--font', type=Path)
    args = parser.parse_args()
    candidates = [args.font, Path('C:/Windows/Fonts/msyh.ttc'),
                  Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')]
    font_path = next((p for p in candidates if p and p.is_file()), None)
    if font_path is None:
        parser.error('Provide a CJK font using --font.')
    media = BASE / 'assets'
    media.mkdir(parents=True, exist_ok=True)

    def font(size):
        return ImageFont.truetype(str(font_path), size)

    def label(draw, xy, text, size=28, fill=TEXT):
        draw.text(xy, text, font=font(size), fill=fill)

    def canvas(title, subtitle):
        im = Image.new('RGB', (1080, 720), BG)
        draw = ImageDraw.Draw(im)
        label(draw, (60, 38), title, 44)
        label(draw, (60, 105), subtitle, 24, MUTED)
        label(draw, (60, 665), '原创教学示意图 · 非真实比例', 22, MUTED)
        return im, draw

    im, d = canvas('阳光包含不同颜色的光', '太阳光看起来接近白色，其中包含多种可见光。')
    d.ellipse((70, 250, 230, 410), fill='#FFD66B')
    d.line((230, 330, 480, 330), fill=TEXT, width=16)
    d.polygon([(480, 225), (480, 440), (650, 380)], fill='#53677D', outline=ACCENT)
    colors = ['#FF707A', '#FFA354', '#FFD66B', '#75DBA1', '#67D8FF', '#7E9CFF', '#B194F5']
    for i, color in enumerate(colors):
        y = 210 + i * 45
        d.line((620, 350, 950, y), fill=color, width=12)
    label(d, (68, 480), '白光', 32)
    label(d, (460, 490), '用分光示意理解颜色组成', 28, MUTED)
    im.save(media / 'sunlight.png')

    im, d = canvas('空气会让光发生散射', '较短波长的蓝光，比红光更容易被空气分子散射。')
    d.line((60, 340, 1000, 340), fill='#FF8580', width=10)
    for x, y in [(270, 340), (530, 340), (780, 340)]:
        d.ellipse((x-25, y-25, x+25, y+25), fill='#DCEBFF')
        for dx, dy in [(90, -110), (100, 120), (-80, 100)]:
            d.line((x, y, x+dx, y+dy), fill=ACCENT, width=8)
            d.ellipse((x+dx-7, y+dy-7, x+dx+7, y+dy+7), fill=ACCENT)
    label(d, (60, 540), '蓝色线：散射方向示意', 28, ACCENT)
    label(d, (60, 590), '红色线：部分光继续传播的示意', 28, '#FF8580')
    im.save(media / 'scattering.png')

    im, d = canvas('日落时，光走过更长的大气路径', '更多蓝光被散射离开直射路径，直射光更偏红橙。')
    d.rounded_rectangle((70, 220, 1010, 550), radius=36, fill='#1D3551')
    d.ellipse((80, 300, 190, 410), fill='#FFAA6B')
    d.line((190, 355, 925, 470), fill='#FF9278', width=14)
    for x in range(300, 901, 140):
        y = 355 + int((x-190) * 115 / 735)
        d.line((x, y, x+30, y-120), fill=ACCENT, width=6)
    d.ellipse((910, 455, 950, 495), fill=TEXT)
    label(d, (100, 500), '较长的大气传播路径', 28, MUTED)
    label(d, (90, 580), '观察者接收到的直射光颜色发生变化', 30)
    im.save(media / 'sunset.png')

    # Wireframe is a static design deliverable, never a fake running editor.
    im = Image.new('RGB', (1600, 1000), '#0E1421')
    d = ImageDraw.Draw(im)
    label(d, (32, 16), '知帧 KnowFrame / 编辑器线框', 32)
    label(d, (32, 62), '阶段 0 设计稿 · 非运行界面 · 首版功能布局', 22, MUTED)

    def box(rect, fill=PANEL, outline='#31425F', radius=12):
        d.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=2)

    box((24, 108, 1576, 180))
    label(d, (45, 128), '‹ 项目列表     为什么天空是蓝色？', 25)
    label(d, (930, 130), '已保存  14:30', 22, MUTED)
    box((1190, 121, 1300, 166), '#263A54')
    label(d, (1216, 128), '保存', 23)
    box((1325, 121, 1545, 166), '#145B76')
    label(d, (1360, 128), '导出 MP4', 23)
    box((24, 196, 314, 750))
    label(d, (44, 214), '分镜    |    素材', 26)
    box((44, 266, 294, 312), '#263A54')
    label(d, (94, 273), '+ 新增分镜', 23)
    scenes = [('01  标题', '6 秒'), ('02  阳光的颜色', '12 秒'),
              ('03  空气散射', '18 秒'), ('04  日落', '16 秒'), ('05  总结', '8 秒')]
    for i, (name, sec) in enumerate(scenes):
        y = 334 + i * 68
        box((44, y, 294, y+54), '#243D54' if i == 2 else '#111B2A',
            ACCENT if i == 2 else '#31425F')
        label(d, (56, y+13), name, 21)
        label(d, (239, y+16), sec, 16, MUTED)
    label(d, (44, 704), '↑ 上移    ↓ 下移    删除', 18, MUTED)

    box((330, 196, 1160, 750), '#101827')
    d.rounded_rectangle((625, 216, 878, 666), radius=14, fill='#153B59', outline=ACCENT, width=2)
    label(d, (648, 290), '空气散射', 34)
    for x, y in [(685, 425), (750, 425), (815, 425)]:
        d.ellipse((x-9, y-9, x+9, y+9), fill=TEXT)
        d.line((x, y, x+20, y-65), fill=ACCENT, width=4)
        d.line((x, y, x-15, y+60), fill=ACCENT, width=4)
    label(d, (649, 545), '蓝光更容易被散射', 20)
    label(d, (367, 690), '播放 / 暂停       00:18 / 01:00       9:16 · 30fps', 24, MUTED)

    box((1176, 196, 1576, 750))
    label(d, (1200, 215), '分镜属性 · 03', 26)
    for y, title, value in [(272, '模板', '知识点'), (354, '标题', '空气会让光发生散射'),
                            (436, '画面正文', '蓝光更容易被散射'), (518, '分镜时长', '18.0 秒 / 540 帧'),
                            (600, '配音', '上传 / 选择配音')]:
        label(d, (1200, y), title, 19, MUTED)
        box((1200, y+29, 1552, y+68), '#111B2A')
        label(d, (1212, y+35), value, 21)
    label(d, (1200, 701), '音乐与配音音量可分别调整', 19, MUTED)

    box((24, 766, 1576, 974))
    label(d, (44, 784), '分镜时间条 · 点击定位，使用上移 / 下移排序', 22)
    durations = [6, 12, 18, 16, 8]
    x = 150
    for i, seconds in enumerate(durations):
        width = int(seconds / 60 * 1380)
        box((x, 834, x+width-5, 888), '#24526D' if i == 2 else '#263A54')
        label(d, (x+10, 850), f'{i+1:02} / {seconds}s', 19)
        x += width
    label(d, (44, 918), '音乐', 20, MUTED)
    box((150, 910, 1525, 950), '#214E46')
    label(d, (170, 916), '全片音乐 · 首版显示音频片段摘要；波形与自动卡点后续实现', 20)
    design = PROJECT / 'docs/design'
    design.mkdir(parents=True, exist_ok=True)
    im.save(design / 'editor-wireframe.png')

    sample_rate = 24000

    def write_wav(name, duration, sample):
        frames = array('h', (int(max(-1, min(1, sample(i / sample_rate))) * 32767)
                             for i in range(round(duration * sample_rate))))
        if sys.byteorder != 'little':
            frames.byteswap()
        with wave.open(str(media / name), 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(frames.tobytes())

    def music(t):
        beat_pos = t % 0.5
        pulse = 0.12 * math.exp(-beat_pos * 45) * math.sin(2 * math.pi * 110 * t)
        notes = [261.6256, 329.6276, 391.9954, 329.6276]
        note = notes[int(t / 2) % len(notes)]
        bed = 0.045 * math.sin(2 * math.pi * note * t)
        envelope = min(1, t / 0.5, (60-t) / 0.5)
        return (pulse + bed) * max(0, envelope)

    write_wav('test-music-120bpm-60s.wav', 60, music)
    write_wav('test-cue-0.25s.wav', .25,
              lambda t: .18 * math.sin(2 * math.pi * 880 * t) * math.exp(-t * 24)
              * min(1, t / .005))
    write_wav('voice-calibration-tone-6s.wav', 6,
              lambda t: .08 * math.sin(2 * math.pi * 440 * t)
              * min(1, t / .02, (6-t) / .02))

    scenes = [
        ('intro', 'title', '为什么天空是蓝色？', '从阳光和空气说起',
         '抬头看天空，你有没有想过，它为什么常常是蓝色的？我们从阳光说起。', 180, 'sunlight'),
        ('sunlight', 'knowledge', '阳光包含不同颜色', '看似白色的阳光，包含多种可见光。',
         '太阳光看起来接近白色，其中却包含不同颜色的光。蓝光和红光，波长并不一样；蓝光的波长更短。', 360, 'sunlight'),
        ('scattering', 'knowledge', '空气会让光发生散射', '空气分子更容易散射较短波长的蓝光。',
         '阳光进入大气后，会被空气分子散射到不同方向。相比红光，蓝光更容易被散射。于是，我们望向远离太阳的天空时，接收到许多散射来的蓝光。', 540, 'scattering'),
        ('sunset', 'knowledge', '日落为什么偏红？', '阳光穿过更长的大气路径，直射光的颜色发生变化。',
         '日落时，太阳光穿过大气的路径更长，更多蓝光被散射离开直射方向。抵达眼睛的直射光，就更偏红色和橙色。', 480, 'sunset'),
        ('summary', 'summary', '记住这条线索', '阳光的颜色组成 + 空气散射 = 常见天空颜色的线索',
         '理解天空的颜色，要同时看阳光包含什么颜色，以及大气怎样散射这些光。', 240, None),
    ]
    document = {
        'schemaVersion': 1,
        'settings': {'width': 1080, 'height': 1920, 'fps': 30},
        'theme': {'background': BG, 'accent': ACCENT, 'fontId': 'bundled-cjk'},
        'scenes': [dict(id='scene_'+sid, templateId=template, title=title, body=body,
                        narrationText=narration, durationFrames=frames,
                        imageAssetId='asset_'+image if image else None, voiceover=None)
                   for sid, template, title, body, narration, frames, image in scenes],
        'music': {'assetId': 'asset_test_music', 'sourceStartSample': 0,
                  'durationSamples': 60*sample_rate, 'gainDb': -18},
    }

    entries = []
    for asset_id, filename, role in [
        ('asset_sunlight', 'sunlight.png', 'illustration'),
        ('asset_scattering', 'scattering.png', 'illustration'),
        ('asset_sunset', 'sunset.png', 'illustration'),
        ('asset_test_music', 'test-music-120bpm-60s.wav', 'synthetic-test-music'),
        ('asset_test_cue', 'test-cue-0.25s.wav', 'synthetic-test-cue'),
        ('asset_voice_calibration', 'voice-calibration-tone-6s.wav', 'non-speech-calibration'),
    ]:
        path = media / filename
        kind = 'image' if path.suffix == '.png' else 'audio'
        if kind == 'image':
            with Image.open(path) as image:
                metadata = {'width': image.width, 'height': image.height}
        else:
            with wave.open(str(path), 'rb') as wav:
                metadata = {'sampleRate': wav.getframerate(), 'channels': wav.getnchannels(),
                            'durationSamples': wav.getnframes()}
        entries.append(dict(id=asset_id, kind=kind, role=role, status='ready',
                            sourceFile='assets/'+filename, metadata=metadata,
                            byteSize=path.stat().st_size,
                            sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                            provenance='Original procedural fixture; no third-party media.'))
    fixture = {'fixtureVersion': 1, 'project': {'name': '为什么天空是蓝色？', 'document': document},
               'assetManifest': entries}
    (BASE / 'project.fixture.json').write_text(json.dumps(fixture, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    beat_reference = {'fixtureVersion': 1, 'assetId': 'asset_test_music', 'bpm': 120,
                      'meaning': 'Generator event times, not results of an audio-analysis algorithm; onset envelope fades at intro/outro.',
                      'beats': [{'seconds': i*.5, 'barStart': i % 4 == 0} for i in range(120)]}
    (BASE / 'beat-reference.json').write_text(json.dumps(beat_reference, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    start = 0
    lines = ['# 样例讲解文稿与分镜', '', '设计时长 60 秒；配音尚未录制，实际录音后需核对每镜时长。', '']
    for sid, template, title, body, narration, frames, image in scenes:
        lines += [f'## {start/30:g}—{(start+frames)/30:g} 秒：{title}', '',
                  f'- 模板：`{template}`', f'- 画面文字：{body}',
                  f'- 图解：{image or "无"}', f'- 讲解：{narration}', '']
        start += frames
    lines += ['科学依据见 [sources.md](sources.md)。此稿是原创建议讲法，并非来源的逐字翻译。', '']
    (BASE / 'script.md').write_text('\n'.join(lines), encoding='utf-8')
    print('Generated: 3 illustrations, 3 WAV fixtures, project/beat JSON, script, wireframe.')


if __name__ == '__main__':
    main()
