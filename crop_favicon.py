from PIL import Image

img = Image.open('images/finch-logo.png').convert("RGBA")
width, height = img.size
pixels = img.load()

# Find bounding box of all non-transparent pixels
min_x = width
max_x = 0
min_y = height
max_y = 0

for x in range(width):
    for y in range(height):
        if pixels[x, y][3] > 10:
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

# Now, scan from min_x to the right to find the first significant gap (e.g. 5 pixels wide)
icon_right = min_x
gap_count = 0
for x in range(min_x, max_x):
    col_empty = True
    for y in range(min_y, max_y + 1):
        if pixels[x, y][3] > 10:
            col_empty = False
            break
            
    if col_empty:
        gap_count += 1
        if gap_count > 8: # If we see an 8px wide transparent vertical line, we've found the gap between icon and text
            icon_right = x - gap_count
            break
    else:
        gap_count = 0
        icon_right = x

if icon_right == min_x:
    # Fallback if no gap found
    icon_right = min_x + (max_y - min_y)

# The icon is from min_x to icon_right, and min_y to max_y
icon_w = icon_right - min_x
icon_h = max_y - min_y

# We want a square box containing the icon
size = max(icon_w, icon_h)
center_x = min_x + icon_w // 2
center_y = min_y + icon_h // 2

# Pad the size slightly (e.g., 5% of size)
pad = int(size * 0.05)
size += pad * 2

box = (
    center_x - size // 2,
    center_y - size // 2,
    center_x + size // 2,
    center_y + size // 2
)

cropped = img.crop(box)
cropped.save('favicon.png')
print(f"Cropped precisely to box {box}")
