import os
import re

def main():
    repo_dir = "/Users/sathyamoorthy/Desktop/finch mortgage"
    
    for root, dirs, files in os.walk(repo_dir):
        if '.git' in root or 'node_modules' in root:
            continue
        for file in files:
            if not file.endswith('.html'):
                continue
            
            filepath = os.path.join(root, file)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if it has a mobile menu
            if 'class="mobile-dropdown-menu"' not in content:
                continue
                
            # Determine prefix
            rel_path = os.path.relpath(filepath, repo_dir)
            depth = len(rel_path.split(os.sep)) - 1
            prefix = '../' * max(0, depth)
            
            # Find the Pre-Approval line using regex to ignore slight variations in spacing
            pattern = re.compile(r'(<a href="[^"]*services/pre-approval\.html"[^>]*>Pre-Approval</a>)')
            
            match = pattern.search(content)
            if match:
                target_line = match.group(1)
                
                # Check if already added to MOBILE menu specifically
                check_string = f'<a href="{prefix}services/construction-loan.html" style="font-size:1rem;font-weight:600'
                if check_string in content:
                    continue
                
                new_links = f"""{target_line}
<a href="{prefix}services/next-home-buyer.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Next Home Buyer</a>
<a href="{prefix}services/self-employed.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Self Employed</a>
<a href="{prefix}services/asset-finance.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Asset Finance</a>
<a href="{prefix}services/commercial-property.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Commercial Property</a>
<a href="{prefix}services/construction-loan.html" style="font-size:1rem;font-weight:600;color:var(--neutral-black);text-decoration:none;">Construction Loan</a>"""
                
                new_content = content.replace(target_line, new_links)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {rel_path}")

if __name__ == "__main__":
    main()
