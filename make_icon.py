import os
from PIL import Image, ImageDraw

# Ensure target directories exist
os.makedirs("frontend/static/icons", exist_ok=True)
os.makedirs("static/icons", exist_ok=True)

def generate_pulse_icon(size):
    # Create high-res dark rounded background
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Background circle/rounded rect in deep navy
    padding = int(size * 0.04)
    draw.rounded_rectangle(
        [(padding, padding), (size - padding, size - padding)],
        radius=int(size * 0.28),
        fill="#0a0f1d",
        outline="#1e293b",
        width=max(2, int(size * 0.03))
    )
    
    # Pulse path coordinates normalized (0 to 1) matching SVG: M22 12h-4l-3 9L9 3l-3 9H2
    # Transformed to standard viewBox points:
    points_norm = [
        (0.12, 0.50), # Start left
        (0.28, 0.50), # Line to first bump
        (0.38, 0.85), # Low spike
        (0.60, 0.15), # High spike
        (0.72, 0.50), # Return to baseline
        (0.88, 0.50)  # Exit right
    ]
    
    points = [(int(x * size), int(y * size)) for x, y in points_norm]
    line_width = max(3, int(size * 0.075))
    
    # Draw glow line then bright core pulse line
    glow_color = (37, 99, 235, 120)
    core_color = "#3b82f6"
    
    draw.line(points, fill=glow_color, width=line_width + 4, joint="round")
    draw.line(points, fill=core_color, width=line_width, joint="round")
    
    return img

for sz in [192, 512]:
    icon = generate_pulse_icon(sz)
    # Save to both frontend static and root static to guarantee coverage
    icon.save(f"frontend/static/icons/icon-{sz}.png")
    icon.save(f"static/icons/icon-{sz}.png")
    print(f"Generated icon-{sz}.png with pulse symbol")

print("PWA Icons updated successfully!")