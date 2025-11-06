from math import sqrt
from PIL import Image
import math

#рисуем линию алгоритмом Брезенхема
def draw_line(img, x0, y0, x1, y1, color):
    dx = x1 - x0
    dy = y1 - y0

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    if dx < 0: dx = -dx
    if dy < 0: dy = -dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x0, y0
    e = 0
    img.putpixel((x, y), color)

    for i in range(el):
        e += 2 * es
        if e > el:
            e -= 2 * el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        img.putpixel((x, y), color)

#рисуем пунктирную линию
def draw_line_dashed(img, x0, y0, x1, y1, color):
    dx = x1 - x0
    dy = y1 - y0

    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x0, y0
    e = 0

    total_length = el
    segment_length = total_length / 11

    for i in range(el + 1):
        segment_index = int(i / segment_length)
        if segment_index % 2 == 0 and segment_index < 11:
            img.putpixel((x, y), color)
        e += 2 * es
        if e > el:
            e -= 2 * el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy

#вычисляет точку на отрезке между p0 и p1 в параметрическом виде
def pod(p0, p1, t):
    return (p0[0] * (1 - t) + p1[0] * t,
            p0[1] * (1 - t) + p1[1] * t)

#вычисляет расстояние от точки до прямой
def distance_point_to_line(px, py, x0, y0, x1, y1):
    ux = x1 - x0
    uy = y1 - y0
    vx = px - x0
    vy = py - y0

    u_len = sqrt(ux * ux + uy * uy)
    v_len = sqrt(vx * vx + vy * vy)
    if u_len == 0 or v_len == 0:
        return v_len

    dot = ux * vx + uy * vy
    cos_theta = dot / (u_len * v_len)
    if cos_theta > 1: cos_theta = 1
    if cos_theta < -1: cos_theta = -1

    sin_theta = sqrt(1 - cos_theta * cos_theta)
    return v_len * sin_theta

#рекурсивно рисует кривую Безье
def bezier_recursive(img, p0, p1, p2, p3, d=2.0, color=(255, 0, 0), t=0.5):
    d1 = distance_point_to_line(p1[0], p1[1], p0[0], p0[1], p3[0], p3[1])
    d2 = distance_point_to_line(p2[0], p2[1], p0[0], p0[1], p3[0], p3[1])

    if d1 < d and d2 < d:
        draw_line(img, int(p0[0]), int(p0[1]), int(p3[0]), int(p3[1]), color)
        return

    p01 = pod(p0, p1, t)
    p11 = pod(p1, p2, t)
    p21 = pod(p2, p3, t)
    p02 = pod(p01, p11, t)
    p12 = pod(p11, p21, t)
    p03 = pod(p02, p12, t)

    bezier_recursive(img, p0, p01, p02, p03, d, color, t)
    bezier_recursive(img, p03, p12, p21, p3, d, color, t)

#рисует окружность используя алгоритм Брезенхэма
def draw_me(img, x0, y0, r, color):
    d = 3 - 2 * r
    x, y = 0, r
    while y >= x:
        img.putpixel((x0 + x, y0 + y), color)
        img.putpixel((x0 + x, y0 - y), color)
        img.putpixel((x0 - x, y0 + y), color)
        img.putpixel((x0 - x, y0 - y), color)
        img.putpixel((x0 + y, y0 + x), color)
        img.putpixel((x0 + y, y0 - x), color)
        img.putpixel((x0 - y, y0 + x), color)
        img.putpixel((x0 - y, y0 - x), color)

        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * x - 4 * y + 10
            y -= 1

        x += 1

#Рисует пунктирную окружность
def draw_me_dashed(img, x0, y0, r, color):
    d = 2 - 2 * r
    x, y = 0, r
    while y >= 0:
        for dx, dy in [(x, y), (x, -y), (-x, y), (-x, -y)]:
            angle = math.degrees(math.atan2(dy, dx))
            if angle < 0:
                angle += 360
            if int(angle // 30) % 2 == 0:
                img.putpixel((x0 + dx, y0 + dy), color)

        if d < 0:
            error = 2 * d + 2 * y - 1
            if error <= 0:
                x += 1
                d = d + 2 * x + 1
                continue
            else:
                x += 1
                y -= 1
                d = d + 2 * x - 2 * y + 2
                continue
        elif d > 0:
            error = 2 * d - 2 * x - 1
            if error <= 0:
                x += 1
                y -= 1
                d = d + 2 * x - 2 * y + 2
                continue
            else:
                y -= 1
                d = d - 2 * y + 1
                continue
        else:
            x += 1
            y -= 1
            d = d + 2 * x - 2 * y + 2

#Проверяет, находится ли точка внутри многоугольника
def point_in_polygon(x, y, points):
    inside = False
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        if ((y1 > y) != (y2 > y)) and \
                (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-10) + x1):
            inside = not inside
    return inside


#Рисует только те части линии, которые находятся вне многоугольника
def draw_line_outside_polygon(img, x0, y0, x1, y1, color, polygon):
    intersections = []
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        inter = segment_intersection((x0, y0), (x1, y1), p1, p2)
        if inter:
            intersections.append(inter)

    intersections.append((x0, y0))
    intersections.append((x1, y1))

    intersections.sort(key=lambda p: (p[0] - x0) ** 2 + (p[1] - y0) ** 2)

    for i in range(len(intersections) - 1):
        xA, yA = intersections[i]
        xB, yB = intersections[i + 1]
        mid_x = (xA + xB) / 2
        mid_y = (yA + yB) / 2
        if not point_in_polygon(mid_x, mid_y, polygon):
            draw_line(img, int(xA), int(yA), int(xB), int(yB), color)

#Рисует внешнюю дугу
def draw_me_outer_arc(img, x0, y0, r, color):
    d = 3 - 2 * r
    x, y = 0, r
    while y >= x:
        img.putpixel((x0 + x, y0 + y), color)
        img.putpixel((x0 - x, y0 + y), color)
        img.putpixel((x0 + y, y0 + x), color)
        img.putpixel((x0 - y, y0 + x), color)
        img.putpixel((x0 - y, y0 - x), color)

        if d < 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * x - 4 * y + 10
            y -= 1

        x += 1

#Заполняет область текстурой вне круга
def fill_texture_outside_circle(img, inters, texture, circle_center, circle_radius):
    tex_w, tex_h = texture.size
    cx, cy = circle_center
    r2 = circle_radius ** 2

    for i in range(0, len(inters) - 1, 2):
        x_start, y = inters[i]
        x_end, _ = inters[i + 1]

        if 0 <= y < img.height:
            for x in range(x_start, x_end):
                if 0 <= x < img.width:
                    if (x - cx) ** 2 + (y - cy) ** 2 >= r2:
                        tx = x % tex_w
                        ty = y % tex_h
                        color = texture.getpixel((tx, ty))
                        img.putpixel((x, y), color)

#Возвращает массив сторон многоугольника
def get_side_array(points):
    answ = []
    for i in range(len(points)):
        current = points[i]
        next = points[(i + 1) % len(points)]
        if current[1] != next[1]:
            answ.append((current, next))
    return tuple(answ)


def find_t(side, y):
    return (y - side[0][1]) / (side[1][1] - side[0][1])

#Находит точку пересечения стороны с горизонтальной линией y
def get_intersection(side, y):
    t = find_t(side, y)
    x_0 = int(t * side[1][0] + (1 - t) * side[0][0])
    return (x_0, y)

#Находит точку пересечения двух отрезков
def segment_intersection(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None

    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denom

    if 0 <= t <= 1 and 0 <= u <= 1:
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)
        return (x, y)
    return None


#Возвращает массив точек пересечения всех сторон с горизонтальной линией y
def get_intersection_array(sides, y):
    answ = []
    for i in range(len(sides)):
        if y < min(sides[i][0][1], sides[i][1][1]) or y > max(sides[i][0][1], sides[i][1][1]):
            continue
        temp = get_intersection(sides[i], y)
        if temp not in answ:
            answ.append(temp)
    answ.sort(key=lambda point: point[0])
    return answ


img = Image.new('RGB', (200, 200))

draw_line(img, 60, 130, 100, 50, (255, 255, 255))
draw_line(img, 60, 130, 140, 130, (255, 255, 255))
draw_line(img, 100, 50, 140, 130, (255, 255, 255))

triangle = [(60, 130), (100, 50), (140, 130)]
draw_line_outside_polygon(img, 0, 6, 199, 110, (255, 255, 255), triangle)

draw_line_dashed(img, 56, 133, 100, 45, (255, 255, 255))
draw_line_dashed(img, 56, 133, 144, 133, (255, 255, 255))
draw_line_dashed(img, 100, 45, 144, 133, (255, 255, 255))

draw_me(img, 100, 100, 20, (255, 255, 255))
draw_me_dashed(img, 100, 100, 17, (255, 255, 255))
draw_me_outer_arc(img, 100, 100, 90, (255, 255, 255))

draw_me(img, 100, 100, 20, (255, 255, 255))
draw_line(img, 60, 130, 100, 50, (255, 255, 255))

triangle = [(60, 130), (100, 50), (140, 130)]
sides = get_side_array(triangle)

circle_center = (100, 100)
circle_radius = 20

texture = Image.open(r"task_picture.jpg").convert("RGB")

mini = min(p[1] for p in triangle)
maxi = max(p[1] for p in triangle)

for y in range(mini, maxi):
    inters = get_intersection_array(sides, y)
    if len(inters) >= 2:
        fill_texture_outside_circle(img, inters, texture, circle_center, circle_radius)

img.show()
