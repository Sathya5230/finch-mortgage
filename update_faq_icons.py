import os

target_svg_index = '<svg fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" style="display:inline-block;vertical-align:middle;flex-shrink:0;" viewbox="0 0 24 24" width="20"><polyline points="6 9 12 15 18 9"></polyline></svg>'
target_svg_faq = '<svg fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" style="display:inline-block;vertical-align:middle;flex-shrink:0;" viewbox="0 0 24 24" width="20"><polyline points="6 9 12 15 18 9"></polyline></svg>'

replacement_svg = '<svg class="faq-icon" fill="none" height="20" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" style="display:inline-block;vertical-align:middle;flex-shrink:0;transition: transform 0.3s;" viewBox="0 0 24 24" width="20"><line x1="12" y1="5" x2="12" y2="19" class="vertical-line" style="transition: opacity 0.3s;"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>'

files = ['index.html', 'faq.html']

for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    # We only want to replace the SVGs inside the FAQ sections.
    # index.html FAQ section starts with <!-- ═══ 9. FAQ EMBED ═══ -->
    # faq.html has them inside <div class="faq-item">
    
    # A simple targeted replace for faq-item's svg
    # The chevron svg in the nav bar shouldn't have class faq-icon, but it's okay if we just replace it where it matters.
    # Actually, the nav bar uses height="13" width="13", the FAQ uses height="20" width="20".
    # So replacing the 20x20 one is safe and targeted perfectly to FAQs!
    
    new_content = content.replace(target_svg_index, replacement_svg)
    if content != new_content:
        with open(file, 'w') as f:
            f.write(new_content)
        print(f"Updated {file}")
