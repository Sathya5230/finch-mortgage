import re

file_path = 'index.html'

with open(file_path, 'r') as f:
    content = f.read()

# The core logo set
set_html = """<div style="display:flex; gap:1.5rem; padding-right:1.5rem; align-items:center;">
<div class="flex items-center justify-center px-4"><img alt="ANZ" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/anz-com-au-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="Avanti Finance" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/avantifinance-co-nz-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="BNZ" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/bnz-co-nz-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="Cape and Coast Bank" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/capeandcoastbank-com-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="Cressida" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/cressida-co-nz-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="FMT" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/fmt-co-nz-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="General Finance" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/general-finance-cz-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="Heartland" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/heartland-co-nz-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="Kiwibank" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/kiwibank-co-nz-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="Pepper Money" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/peppermoney-com-au-logo.png"/></div>
<div class="flex items-center justify-center px-4"><img alt="Southern Cross Partners" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/southerncrosspartners-co-nz-logo.png"/></div>
</div>"""

# 6 sets
new_sets = "\n".join([f"<!-- ── SET {i+1} ── -->\n{set_html}" for i in range(6)])

# Replace the content of ticker-wrap
pattern = r'(<div class="ticker-wrap" style="display:flex; width:max-content; align-items:center; animation: tickerScroll 40s linear infinite;">).*?(</div>\s*<!-- Fade edges -->)'
replacement = r'<div class="ticker-wrap" style="display:flex; width:max-content; align-items:center; animation: tickerScroll 120s linear infinite;">\n' + new_sets + r'\n\2'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(file_path, 'w') as f:
    f.write(new_content)

print("Updated index.html ticker")
