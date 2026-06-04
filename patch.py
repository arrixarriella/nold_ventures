path = r'C:\Users\user\OneDrive\Desktop\Nold Ventures\venv\Lib\site-packages\africastalking\Service.py'

with open(path, 'r') as f:
    content = f.read()

# Patch GET request
content = content.replace(
    'res = requests.get(\n            url=url,\n            headers=headers,\n            params=params,\n            data=data,\n            timeout=timeout,\n        )',
    'res = requests.get(\n            url=url,\n            headers=headers,\n            params=params,\n            data=data,\n            timeout=timeout,\n            verify=False,\n        )'
)

# Patch POST request
content = content.replace(
    'res = requests.post(\n            url=url,\n            headers=headers,\n            params=params,\n            data=data,\n            timeout=timeout,\n        )',
    'res = requests.post(\n            url=url,\n            headers=headers,\n            params=params,\n            data=data,\n            timeout=timeout,\n            verify=False,\n        )'
)

with open(path, 'w') as f:
    f.write(content)

print('Patched!')

# Verify
with open(path, 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'verify' in line:
        print(f"Line {i+1}: {line.strip()}")