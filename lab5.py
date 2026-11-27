import math
from enum import Enum


class Colour(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    BLACK = 5
    WHITE = 6


class Point:
    @staticmethod
    def _validate_coord(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Координата {name} має бути числом (int або float)")
        return float(value)

    def __init__(self, x=0.0, y=0.0):
        self._x = self._validate_coord(x, "x")
        self._y = self._validate_coord(y, "y")

    def __del__(self):
        print(f"[Деструктор] Точку {self} видалено")

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = self._validate_coord(value, "x")

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = self._validate_coord(value, "y")

    def distance_to(self, other):
        if not isinstance(other, Point):
            raise TypeError("Аргумент має бути об'єктом класу Point")
        return math.hypot(self._x - other._x, self._y - other._y)

    def __str__(self):
        return f"({self._x}; {self._y})"

    def show(self):
        print(f"Точка: {self}")


class Polynom:
    def __init__(self, points=None, colour=Colour.RED):
        self._points = list(points) if points else []
        self.colour = colour

    def __del__(self):
        print(f"[Деструктор] Багатокутник ({self._colour.name}) "
              f"з {len(self._points)} точок видалено")

    @property
    def points(self):
        return list(self._points)

    @property
    def colour(self):
        return self._colour

    @colour.setter
    def colour(self, value):
        if not isinstance(value, Colour):
            raise TypeError("colour має бути елементом enum Colour")
        self._colour = value

    def add_point(self, point):
        if not isinstance(point, Point):
            raise TypeError("point має бути об'єктом класу Point")
        self._points.append(point)

    def remove_point(self, index):
        if 0 <= index < len(self._points):
            return self._points.pop(index)
        raise IndexError("Немає точки з таким індексом")

    def perimeter(self):
        n = len(self._points)
        if n < 2:
            return 0.0
        total = 0.0
        for i in range(n):
            total += self._points[i].distance_to(self._points[(i + 1) % n])
        return total

    def longest_diagonal(self):
        n = len(self._points)
        if n < 4:
            return None
        best = None
        for i in range(n):
            for j in range(i + 1, n):
                adjacent = (j - i == 1) or (i == 0 and j == n - 1)
                if adjacent:
                    continue
                d = self._points[i].distance_to(self._points[j])
                if best is None or d > best[0]:
                    best = (d, self._points[i], self._points[j])
        return best

    def sort_by_x(self):
        self._points.sort(key=lambda p: (p.x, p.y))

    def sort_by_y(self):
        self._points.sort(key=lambda p: (p.y, p.x))

    def show(self):
        pts = ", ".join(str(p) for p in self._points)
        print(f"Багатокутник [{self._colour.name}], точок: "
              f"{len(self._points)}: {pts}")

    def show_perimeter(self):
        print(f"Периметр = {self.perimeter():.3f}")

    def show_longest_diagonal(self):
        res = self.longest_diagonal()
        if res is None:
            print("Діагоналей немає (потрібно щонайменше 4 вершини)")
        else:
            d, a, b = res
            print(f"Найдовша діагональ: {a} - {b}, довжина = {d:.3f}")


def main():
    print("=== 1. Створення точок (конструктор Point) ===")
    p1 = Point(0, 0)
    p2 = Point(4, 0)
    p3 = Point(5, 3)
    p4 = Point(2, 5)
    p5 = Point(-1, 3)
    p1.show()

    print("\n=== 2. Функції доступу: читання і зміна координат ===")
    print("x =", p5.x, "y =", p5.y)
    p5.x = -2
    print("Після p5.x = -2 ->", p5)
    p5.x = -1

    print("\n=== 3. Створення багатокутника (конструктор Polynom) ===")
    poly = Polynom([p1, p2, p3, p4], Colour.GREEN)
    poly.add_point(p5)
    poly.show()

    print("\n=== 4. Периметр і найдовша діагональ ===")
    poly.show_perimeter()
    poly.show_longest_diagonal()

    print("\n=== 5. Сортування за абсцисою (x) ===")
    poly.sort_by_x()
    poly.show()

    print("\n=== 6. Сортування за ординатою (y) ===")
    poly.sort_by_y()
    poly.show()

    print("\n=== 7. Зміна кольору (enum Colour) ===")
    poly.colour = Colour.BLUE
    poly.show()

    print("\n=== 8. Трикутник: діагоналей немає ===")
    tri = Polynom([Point(0, 0), Point(3, 0), Point(0, 4)], Colour.RED)
    tri.show()
    tri.show_perimeter()
    tri.show_longest_diagonal()

    print("\n=== 9. Видалення посилання на об'єкт (del) ===")
    del tri

    print("\n=== Кінець програми ===")


if __name__ == "__main__":
    main()