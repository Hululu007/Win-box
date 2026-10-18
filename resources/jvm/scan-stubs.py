import sys, zipfile, re, collections, os

JAR = sys.argv[1]
STUBS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stubs', 'stubs.jar')

existing = set()
zz = zipfile.ZipFile(STUBS)
for n in zz.namelist():
    if n.endswith('.class'):
        existing.add(n[:-6].replace('/', '.'))

z = zipfile.ZipFile(JAR)
refs = collections.Counter()
for n in z.namelist():
    if not n.endswith('.class'):
        continue
    for m in re.finditer(rb'(androidx|android)/[A-Za-z0-9_$/]{2,80}', z.read(n)):
        refs[m.group().decode('latin1').split('$')[0]] += 1

scope = sys.argv[2] if len(sys.argv) > 2 else 'androidx'
print(f"=== {scope} 引用 vs stubs ===")
for k, v in sorted(refs.items()):
    if not k.startswith(scope + '/'):
        continue
    mark = 'MISSING' if k.replace('/', '.') not in existing else 'ok'
    print(f"  [{mark}] {k}  ({v})")
