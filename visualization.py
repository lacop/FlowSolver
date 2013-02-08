from level import Level
from PIL import Image, ImageDraw

GRID_SIZE = 50
DOT_RADIUS = 20
GRID_WIDTH = 1
BACKGROUND_COLOR = "black"
GRID_COLOR = "white"
LINE_RADIUS = 5

COLORS = ["red", "green", "blue", "white", "yellow", "orange", "pink", "purple", "gray", "cyan"]

def get_solution(level, valuation, showdist = False, colormap = None):
    size = (GRID_SIZE * level.cols, GRID_SIZE * level.rows)
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
            c,t = valuation[y][x][0]
            d = valuation[y][x][1]

            cx, cy = [i * GRID_SIZE + GRID_SIZE / 2 for i in [x, y]]

            color = COLORS[c % len(COLORS)]
            if colormap is not None:
                color = colormap[c]

            if t == 0:
                draw.ellipse((cx - DOT_RADIUS, cy - DOT_RADIUS, cx + DOT_RADIUS, cy + DOT_RADIUS), fill = color)
            else:
                if t in [2, 3, 6]: # top
                    draw.rectangle((cx-LINE_RADIUS, cy - GRID_SIZE/2, cx+LINE_RADIUS, cy), fill = color)
                if t in [1, 3, 4]: # right
                    draw.rectangle((cx, cy-LINE_RADIUS, cx + GRID_SIZE/2, cy+LINE_RADIUS), fill = color)
                if t in [2, 4, 5]: # bottom
                    draw.rectangle((cx-LINE_RADIUS, cy, cx+LINE_RADIUS, cy + GRID_SIZE/2), fill = color)
                if t in [1, 5, 6]: # left
                    draw.rectangle((cx - GRID_SIZE/2, cy-LINE_RADIUS, cx, cy+LINE_RADIUS), fill = color)

            if showdist:
                draw.text((cx-1, cy), str(d), fill = 'black')
                draw.text((cx+1, cy), str(d), fill = 'black')
                draw.text((cx, cy-1), str(d), fill = 'black')
                draw.text((cx, cy+1), str(d), fill = 'black')
                draw.text((cx, cy), str(d), fill = 'white')

    return img