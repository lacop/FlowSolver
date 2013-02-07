from level import Level
from PIL import Image, ImageDraw

GRID_SIZE = 50
DOT_RADIUS = 20
GRID_WIDTH = 1
BACKGROUND_COLOR = "black"
GRID_COLOR = "white"

COLORS = ["red", "green", "blue", "white", "yellow", "orange", "pink", "purple", "gray", "cyan"]

def get_solution(level, valuation):
    size = (GRID_SIZE * level.rows, GRID_SIZE * level.cols)
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, size[0], size[1]), fill = BACKGROUND_COLOR)

    # Prepare grid
    for i in range(level.rows):
        draw.line([(0, i * GRID_SIZE), (size[0], GRID_SIZE* i)], width = GRID_WIDTH, fill = GRID_COLOR)
    for i in range(level.cols):
        draw.line([(i * GRID_SIZE, 0), (GRID_SIZE* i, size[1])], width = GRID_WIDTH, fill = GRID_COLOR)

    # Draw valuation
    for x in range(level.cols):
        for y in range(level.rows):
            c,t = valuation[y][x]

            color = COLORS[c % len(COLORS)]
            cx, cy = [i * GRID_SIZE + GRID_SIZE / 2 for i in [x, y]]

            if t == 0:
                draw.ellipse((cx - DOT_RADIUS, cy - DOT_RADIUS, cx + DOT_RADIUS, cy + DOT_RADIUS), fill = color)
            else:
                if t in [2, 3, 6]: # top
                    draw.line((cx, cy, cx, cy - GRID_SIZE/2), fill = color)
                if t in [1, 3, 4]: # right
                    draw.line((cx, cy, cx + GRID_SIZE/2, cy), fill = color)
                if t in [2, 4, 5]: # bottom
                    draw.line((cx, cy, cx, cy + GRID_SIZE/2), fill = color)
                if t in [1, 5, 6]: # left
                    draw.line((cx, cy, cx - GRID_SIZE/2, cy), fill = color)
    return img