import math


# Phase 5
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def replace_at_index(s: str, r: str, idx: int) -> str:
    return s[:idx] + r + s[idx + len(r):]


# Phase 1
class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.canvas = [" " * width for _ in range(height)]

    # Phase 2 and 3
    def print(self):
        header = " " + "".join([str(i % 10) for i in range(self.width)])
        print(header)
        for idx, row in enumerate(self.canvas):
            print(idx % 10, row, idx % 10, sep="")
        print(header)

    # Phase 4
    def draw_polygon(self, *points: Point, closed: bool = True, line_char: str = "*"):

        def draw_line_segment(canvas, start: Point, end: Point, line_char: str = "*"):
            x1, y1 = start.x, start.y
            x2, y2 = end.x, end.y

            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            sx = 1 if x1 < x2 else -1
            sy = 1 if y1 < y2 else -1
            error = dx - dy

            while x1 != x2 or y1 != y2:
                canvas[y1] = replace_at_index(canvas[y1], line_char, x1)

                double_error = error * 2
                if double_error > -dy:
                    error -= dy
                    x1 += sx

                if double_error < dx:
                    error += dx
                    y1 += sy

            canvas[y2] = replace_at_index(canvas[y2], line_char, x2)

        start_points = points[:-1]
        end_points = points[1:]
        if closed:
            start_points += (points[-1],)
            end_points += (points[0],)

        for start_point, end_point in zip(start_points, end_points):
            draw_line_segment(self.canvas, start_point, end_point, line_char)

    def draw_line(self, start: Point, end: Point, line_char: str = "*"):
        self.draw_polygon(start, end, closed=False, line_char=line_char)

    def draw_rectangle(self, upper_left: Point, lower_right: Point, line_char: str = "*"):
        x1, y1 = upper_left.x, upper_left.y
        x2, y2 = lower_right.x, lower_right.y

        self.draw_polygon(upper_left, Point(x2, y1), lower_right, Point(x1, y2), line_char=line_char)

    def draw_n_gon(self, center: Point, radius: int, number_of_points: int, rotation: int = 0,
                   line_char: str = "*"):
        angles = range(rotation, 360 + rotation, 360 // number_of_points)

        points = []
        for angle in angles:
            angle_in_radians = math.radians(angle)
            x = center.x + radius * math.cos(angle_in_radians)
            y = center.y + radius * math.sin(angle_in_radians)
            points.append(Point(round(x), round(y)))

        self.draw_polygon(*points, line_char=line_char)


canvas_width = 100
canvas_height = 40
canvas = Canvas(canvas_width, canvas_height)

canvas.draw_line(Point(10, 4), Point(92, 19), "+")
canvas.draw_polygon(Point(7, 12), Point(24, 29), Point(42, 15), Point(37, 32), Point(15, 35))
canvas.draw_rectangle(Point(45, 2), Point(80, 27), line_char='#')
canvas.draw_n_gon(Point(72, 25), 12, 20, 80, "-")

canvas.print()


# Assignment 2: Class customization
# Phase 1
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    # Phase 4
    def distance_from_origin(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)


# __str__ methode is used to print a single object,
# and __repr__ one is used to print a collection of objects?

# Phase 2

class Shape:
    def __init__(self, *points):
        self.points = list(points)

    def __str__(self):
        return f"Shape [{', '.join(map(str, self.points))}]"

    def __repr__(self):
        return f"Shape({', '.join(map(repr, self.points))})"

    # Phase 3
    def centroid(self) -> Point:
        n = len(self.points)

        sum_x = sum(point.x for point in self.points)
        sum_y = sum(point.y for point in self.points)

        centroid_x = sum_x / n
        centroid_y = sum_y / n

        return Point(centroid_x, centroid_y)

    # Phase 5
    def distance_from_origin(self) -> float:
        centroid = self.centroid()
        return centroid.distance_from_origin()

    def __eq__(self, other):
        return self.distance_from_origin() == other.distance_from_origin()

    def __lt__(self, other):
        return self.distance_from_origin() < other.distance_from_origin()


# Testcode
p1 = Point(2.3, 43.14)
p2 = Point(5.53, 2.5)
p3 = Point(12.2, 28.7)

s1 = Shape(p1, p2, p3)
s2 = Shape(p2)
s3 = Shape()
print(p1)
print([p1, p2, p3])

print(s1)
print(s2)
print(s3)

s1 = Shape(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
s2 = Shape(Point(0, 0.5), Point(0.5, 1), Point(1, 0.5), Point(0.5, 0))
s3 = Shape(Point(0.25, 0.25), Point(0.25, 0.75), Point(0.75, 0.75), Point(0.75, 0.25))
print(s1.centroid())
print(s2.centroid())
print(s3.centroid())

p1 = Point(1, 1)
p2 = Point(5, 5)
p3 = Point(10, 10)
print(p1.distance_from_origin())
print(p2.distance_from_origin())
print(p3.distance_from_origin())

s1 = Shape(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
s2 = Shape(Point(0, 0.5), Point(0.5, 1), Point(1, 0.5), Point(0.5, 0))
print(s1 == s2)
s2 = Shape(Point(5, 5), Point(5, 6), Point(6, 6), Point(6, 5))
print(s1 < s2)
s3 = Shape(Point(10, 10), Point(10, 11), Point(11, 11), Point(11, 10))
shapes = [s3, s1, s2]
print(shapes)
print(sorted(shapes))
