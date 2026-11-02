from pathlib import Path
import re, json

root = Path(__file__).parent/'staged'
count = 0
for base in root.rglob('DOC.md'):
    if 'dist' in base.parts:
        continue
    for path in base.parent.rglob('*.md'):
        for ref in re.findall(r'`((?:references|release-deltas)/[^`]+\.md)`', path.read_text(encoding='utf-8')):
            assert (base.parent/ref).is_file(), (path, ref)
    count += 1
for registry in root.glob('*/dist/registry.json'):
    for entry in json.loads(registry.read_text(encoding='utf-8'))['docs']:
        for lang in entry['languages']:
            for version in lang['versions']:
                for file in version['files']:
                    generated = registry.parent/version['path']/file
                    source = registry.parent.parent/version['path']/file
                    assert generated.read_bytes() == source.read_bytes(), generated
print(f'Checked references and generated content for {count} documentation entries.')
