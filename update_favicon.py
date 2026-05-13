import os
import glob

html_files = glob.glob('**/*.html', recursive=True)

for filepath in html_files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace the svg link with png link
    new_content = content.replace(
        '<link href="/favicon.svg" rel="icon" type="image/svg+xml"/>',
        '<link href="/favicon.png" rel="icon" type="image/png"/>'
    )
    
    # Sometimes there might be variations in spacing
    if new_content == content:
        import re
        new_content = re.sub(
            r'<link[^>]*href="[^"]*favicon\.svg"[^>]*>',
            '<link href="/favicon.png" rel="icon" type="image/png"/>',
            content
        )
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
