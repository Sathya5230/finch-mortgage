import os
import glob

directory = "weekly-reports"
html_files = glob.glob(os.path.join(directory, "*.html"))

target_content = "<script>if (typeof lucide !== 'undefined')\n</script>"
replacement_content = ""

target_content_2 = "<script>if (typeof lucide !== 'undefined')</script>"

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if target_content in content:
        content = content.replace(target_content, replacement_content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed {filepath}")
    elif target_content_2 in content:
        content = content.replace(target_content_2, replacement_content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed {filepath}")

# Also check weekly-reports.html itself just in case
with open("weekly-reports.html", "r", encoding="utf-8") as f:
    content = f.read()
if target_content in content or target_content_2 in content:
    content = content.replace(target_content, replacement_content).replace(target_content_2, replacement_content)
    with open("weekly-reports.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed weekly-reports.html")
