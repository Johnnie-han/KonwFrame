"""Check stage-0 document links and sample integrity, not application behavior."""
from array import array
import hashlib
import json
from pathlib import Path
import re
import sys
import wave

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / 'examples/sky-blue'


def main():
    checks = []

    def check(condition, description):
        if not condition:
            raise AssertionError(description)
        checks.append(description)

    required = [
        'docs/00-project-overview.md', 'docs/01-product-requirements.md',
        'docs/02-user-flows-and-ui.md', 'docs/03-architecture.md',
        'docs/04-data-model.md', 'docs/05-api-contracts.md',
        'docs/06-video-and-audio-rules.md', 'docs/07-test-and-acceptance.md',
        'docs/08-roadmap.md', 'docs/09-development-log.md', 'docs/10-deployment.md',
        'docs/features/mvp-editor.md', 'docs/decisions/0001-single-server.md',
        'docs/acceptance/stage-0.md', 'examples/sky-blue/script.md',
        'examples/sky-blue/sources.md', 'examples/sky-blue/README.md',
    ]
    for relative in required:
        check((ROOT / relative).is_file(), 'exists: '+relative)
    for path in [ROOT / 'README.md', *sorted((ROOT / 'docs').rglob('*.md')),
                 *sorted(BASE.glob('*.md'))]:
        text = path.read_text(encoding='utf-8')
        check('<!-- 在此补充正式内容' not in text, 'not placeholder: '+str(path.relative_to(ROOT)))
        for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)', text):
            target = match.group(1)
            if '://' in target or target.startswith('#'):
                continue
            target = target.split('#', 1)[0]
            check((path.parent / target).exists(), 'local link: '+target)

    fixture = json.loads((BASE / 'project.fixture.json').read_text(encoding='utf-8'))
    document = fixture['project']['document']
    check(document['schemaVersion'] == 1, 'schemaVersion=1')
    check(document['settings'] == {'width': 1080, 'height': 1920, 'fps': 30}, 'fixed video settings')
    scenes = document['scenes']
    check(len(scenes) == 5, 'five sample scenes')
    check(len({s['id'] for s in scenes}) == len(scenes), 'unique scene IDs')
    check(sum(s['durationFrames'] for s in scenes) == 1800, 'sample total=1800 frames / 60s')
    check({s['templateId'] for s in scenes} == {'title', 'knowledge', 'summary'}, 'three template types covered')
    assets = fixture['assetManifest']
    check(len({a['id'] for a in assets}) == len(assets), 'unique sample asset IDs')
    by_id = {a['id']: a for a in assets}
    for scene in scenes:
        check(isinstance(scene['durationFrames'], int) and scene['durationFrames'] >= 30,
              'scene duration valid: '+scene['id'])
        check(scene['voiceover'] is None, 'no fabricated speech binding: '+scene['id'])
        if scene['imageAssetId']:
            check(by_id[scene['imageAssetId']]['kind'] == 'image', 'image reference: '+scene['id'])
    check(by_id[document['music']['assetId']]['kind'] == 'audio', 'music reference resolves')
    check(document['music']['durationSamples'] == 60*24000, 'music sample length binding')

    audio = []
    for asset in assets:
        path = (BASE / asset['sourceFile']).resolve()
        check(path.is_relative_to(BASE), 'fixture path inside sample: '+asset['id'])
        check(path.stat().st_size == asset['byteSize'], 'byte size: '+asset['id'])
        check(hashlib.sha256(path.read_bytes()).hexdigest() == asset['sha256'], 'SHA-256: '+asset['id'])
        if asset['kind'] == 'image':
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                check(image.size == (1080, 720), 'PNG dimensions: '+asset['id'])
        else:
            with wave.open(str(path), 'rb') as wav:
                check(wav.getnchannels() == 1 and wav.getsampwidth() == 2, 'mono PCM16: '+asset['id'])
                check(wav.getframerate() == asset['metadata']['sampleRate'] and
                      wav.getnframes() == asset['metadata']['durationSamples'], 'WAV metadata: '+asset['id'])
                samples = array('h', wav.readframes(wav.getnframes()))
                if sys.byteorder != 'little':
                    samples.byteswap()
                peak = max(abs(s) for s in samples)
                check(0 < peak < 32767, 'non-silent, no full-scale samples: '+asset['id'])
                audio.append({'id': asset['id'], 'durationSeconds': len(samples)/wav.getframerate(),
                              'peakPcm16': peak})
    beats = json.loads((BASE / 'beat-reference.json').read_text(encoding='utf-8'))
    check(beats['assetId'] == document['music']['assetId'], 'beat reference asset')
    check(len(beats['beats']) == 120 and all(b['seconds'] == i*.5 for i, b in enumerate(beats['beats'])),
          '120 generator beat times spaced 0.5s')
    with Image.open(ROOT / 'docs/design/editor-wireframe.png') as image:
        check(image.size == (1600, 1000), 'wireframe readable design canvas')
    requirements = (ROOT / 'docs/01-product-requirements.md').read_text(encoding='utf-8')
    testplan = (ROOT / 'docs/07-test-and-acceptance.md').read_text(encoding='utf-8')
    for i in range(1, 11):
        code = f'F{i:02}'
        check(code in requirements and code in testplan, 'requirement trace: '+code)
    roadmap = (ROOT / 'docs/08-roadmap.md').read_text(encoding='utf-8')
    check('| [x] | 阶段 0：需求与设计 | 已完成 |' in roadmap, 'stage 0 completion recorded')
    for i in range(1, 7):
        check(bool(re.search(r'\| \[ \] \| 阶段 ' + str(i) + r'：[^|]+\| 未开始 \|', roadmap)),
              f'stage {i} remains unstarted')

    report = {
        'scope': 'Stage-0 documentation and fixture integrity only; no application, audio listening, video render or server deployment verified.',
        'date': '2026-11-03', 'passed': True, 'checkCount': len(checks),
        'audio': audio, 'checks': checks,
    }
    output = ROOT / 'docs/acceptance/stage-0-verification.json'
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': True, 'checkCount': len(checks), 'audio': audio}, ensure_ascii=False))


if __name__ == '__main__':
    main()
