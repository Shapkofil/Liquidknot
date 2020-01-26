def bounds_to_json(scene):
    scale = scene.render.resolution_percentage / 100.0
    size_x = int(scene.render.resolution_x * scale)
    size_y = int(scene.render.resolution_y * scale)

    resolution = [size_x, size_y]
    bounds = [scene.render.border_min_x * size_x,
              scene.render.border_min_y * size_y,
              scene.render.border_max_x * size_x,
              scene.render.border_max_y * size_y]

    return [int(x) for x in resolution], [int(x) for x in bounds]
