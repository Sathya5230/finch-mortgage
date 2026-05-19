import os
import glob
import re
import shutil

# Copy the favicon to be the new nav logo
shutil.copy2('favicon.png', 'images/nav-logo.png')

html_files = glob.glob('**/*.html', recursive=True)
count = 0

for filepath in html_files:
    if filepath.startswith('node_modules/') or filepath.startswith('.git/'):
        continue
    with open(filepath, 'r') as f:
        content = f.read()

    # Find the nav-logo link and replace finch-logo.png with nav-logo.png
    # The regex targets only the img inside the nav-logo anchor
    # Example: <a class="nav-logo" href="index.html"><img alt="Finch Mortgages" loading="lazy" src="images/finch-logo.png" style="height: 60px; width: auto;"/></a>
    
    def repl(m):
        # m.group(0) is the entire <a class="nav-logo"...>...</a>
        # We want to replace finch-logo.png with nav-logo.png inside it
        return m.group(0).replace('finch-logo.png', 'nav-logo.png')

    new_content = re.sub(r'<a[^>]*class="[^"]*nav-logo[^"]*"[^>]*>.*?</a>', repl, content, flags=re.DOTALL)

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        count += 1

print(f"Updated {count} HTML files.")
