from html.parser import HTMLParser
import sys

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        
    def handle_starttag(self, tag, attrs):
        if tag not in ['meta', 'link', 'img', 'br', 'hr', 'input', 'source', 'circle', 'path', 'rect', 'polyline', 'line', 'polygon']:
            self.tags.append(tag)
            
    def handle_endtag(self, tag):
        if tag not in ['meta', 'link', 'img', 'br', 'hr', 'input', 'source', 'circle', 'path', 'rect', 'polyline', 'line', 'polygon']:
            if len(self.tags) == 0:
                print(f"Error: Found end tag </{tag}> but no start tags exist!")
            else:
                last_tag = self.tags.pop()
                if last_tag != tag:
                    print(f"Error: Mismatched tag. Expected </{last_tag}> but found </{tag}>.")
                    # push it back and stop to avoid cascade
                    self.tags.append(last_tag)

parser = MyHTMLParser()
with open("weekly-reports.html", "r", encoding="utf-8") as f:
    try:
        parser.feed(f.read())
        if len(parser.tags) > 0:
            print(f"Unclosed tags remaining: {parser.tags}")
        else:
            print("HTML parsing passed (tags match).")
    except Exception as e:
        print(f"Parse error: {e}")
