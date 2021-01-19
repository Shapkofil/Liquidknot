def bounds_to_json(scene, resolution=None, bounds=None, context=None):
    scale = scene.render.resolution_percentage / 100.0
    size_x = int(scene.render.resolution_x * scale)
    size_y = int(scene.render.resolution_y * scale)

    if resolution is None:
        if context is not None:
            region = context.region
            resolution = [region.width, region.height]
            bounds = [0, 0, region.width, region.height]
        else:
            resolution = [size_x, size_y]
            bounds = [scene.render.border_min_x * size_x,
                      scene.render.border_min_y * size_y,
                      scene.render.border_max_x * size_x,
                      scene.render.border_max_y * size_y]
    elif bounds is None:
        bounds = [0, 0, resolution[0], resolution[1]]

    return [int(x) for x in resolution], [int(x) for x in bounds]
