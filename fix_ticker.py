import re

file_path = 'index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The core logo set with only approved lenders (12 items)
set_html = """<div style="display:flex; gap:1.5rem; padding-right:1.5rem; align-items:center;">
<div class="flex items-center justify-center px-4"><img alt="ANZ" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/anz-com-au-logo.png" width="256" height="256" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="Avanti Finance" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/avantifinance-co-nz-logo.png" width="256" height="256" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="Basecorp Finance" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="images/lenders/basecorp-finance.svg" width="160" height="48" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="BNZ" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/bnz-co-nz-logo.png" width="256" height="256" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="Cressida Capital" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/cressida-co-nz-logo.png" width="256" height="256" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="First Mortgage Trust" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/fmt-co-nz-logo.png" width="256" height="256" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="General Finance" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/general-finance-cz-logo.png" width="256" height="256" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="Heartland Bank" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/heartland-co-nz-logo.png" width="256" height="256" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="Liberty Financial" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="images/lenders/liberty-financial.svg" width="160" height="48" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="Pepper Money" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/peppermoney-com-au-logo.png" width="256" height="256" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="SBS Bank" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="images/lenders/sbs-bank.svg" width="160" height="48" loading="lazy" decoding="async"/></div>
<div class="flex items-center justify-center px-4"><img alt="Southern Cross Partners" class="h-10 md:h-12 w-auto object-contain transition-all duration-300" src="logos/southerncrosspartners-co-nz-logo.png" width="256" height="256" loading="lazy" decoding="async"/></div>
</div>"""

# 6 sets for infinite scroll
new_sets = "\n".join([f"<!-- ── SET {i+1} ── -->\n{set_html}" for i in range(6)])

# Replace the content of ticker-wrap
pattern = r'(<div class="ticker-wrap" style="display:flex; width:max-content; align-items:center; animation: tickerScroll [^"]+">).*?(</div>\s*<!-- Fade edges -->)'
replacement = r'<div class="ticker-wrap" style="display:flex; width:max-content; align-items:center; animation: tickerScroll 120s linear infinite;">\n' + new_sets + r'\n\2'

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated index.html ticker with 12 approved lenders")
