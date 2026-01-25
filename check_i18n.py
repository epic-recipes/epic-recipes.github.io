from bs4 import BeautifulSoup

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

buttons = soup.find_all('button')
missing_i18n = []

for btn in buttons:
    # Check if it has data-i18n
    if not btn.has_attr('data-i18n'):
        # Check if it has text content that is not just whitespace
        text = btn.get_text(strip=True)
        # Also check if it has only an icon (e.g. <i> inside) and no text
        # If text is empty or just symbols, maybe it is fine.
        # But if it has words, it needs i18n.
        if text:
             # Heuristic: if text length > 1 (to avoid single symbols like 'x' or '+')
             # actually some buttons might be 'X' or '+' and might not need i18n if they are universal,
             # but let's list them to be sure.
             missing_i18n.append({
                 'line': getattr(btn, 'sourceline', 'unknown'), 
                 'text': text,
                 'html': str(btn)[:100]
             })

inputs = soup.find_all('input', type=['button', 'submit', 'reset'])
for inp in inputs:
    if not inp.has_attr('data-i18n'):
        val = inp.get('value', '')
        if val:
             missing_i18n.append({
                 'line': getattr(inp, 'sourceline', 'unknown'),
                 'text': val,
                 'html': str(inp)[:100]
             })

print(f"Found {len(missing_i18n)} buttons potentially missing i18n:")
for item in missing_i18n:
    print(f"Line {item['line']}: Text='{item['text']}' HTML={item['html']}")
