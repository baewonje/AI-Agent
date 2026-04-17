from pathlib import Path
p = Path('h:/AI Agent/agent/evaluator.py')
text = p.read_text(encoding='utf-8')
for i, line in enumerate(text.splitlines(), 1):
    if i >= 40 and i <= 48:
        print(i, repr(line))
