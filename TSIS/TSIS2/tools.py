from collections import deque


def flood_fill(surface, x, y, new_color):
    old_color = surface.get_at((x, y))

    if old_color == new_color:
        return

    width, height = surface.get_size()
    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or py < 0 or px >= width or py >= height:
            continue

        if surface.get_at((px, py)) != old_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))