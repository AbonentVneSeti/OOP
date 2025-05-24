import random
from Point2d import Point2d, HEIGHT, WIDTH
from Vector2d import Vector2d

def main():
    print("Класс Point2d:")
    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)

    a = Point2d(x,y)
    print(f"Point2d по x={x}, y={y}: {a}")
    print()

    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)

    b = Point2d(x,y)

    print(f"{a} == {a}: {a == a}")
    print(f"{a} == {b}: {a == b}")
    print()

    print("Класс Vector2d:")
    vec1 = Vector2d(x,y)
    print(f"Vector2d по x={x}, y={y}: vec1={vec1}")
    vec2 = Vector2d.from_points(a,b)
    print(f"Vector2d по start={a}, end={b}: vec2={vec2}")
    print()

    print("Доступ по индексу:")
    for i in range(len(vec1)): print(f"vec1[{i}] = {vec1[i]}")
    print()

    print(f"Итерирование {vec1}:")
    for i in vec1: print(i)
    print()

    print(f"{vec1} == {vec2}: {vec1 == vec2}")
    print(f"{vec1} == {vec1}: {vec1 == vec1}")
    print()

    print(f"abs({vec1}) = {abs(vec1)}")
    print(f"{vec1} + {vec2} = {vec1 + vec2}")
    print(f"{vec1} - {vec2} = {vec1 - vec2}")
    randval = random.randint(0,15)
    print(f"{vec1}*{randval} = {vec1 * randval}")
    print(f"{randval}*{vec1} = {randval * vec1}")
    randval = random.randint(1, 15)
    print(f"{vec1}//{randval} = {vec1 // randval}")
    print()

    print(f"Скалярное произведение {vec1}.dot_product({vec2}) = {vec1.dot_product(vec2)}")
    print(f"Статическое скалярное произведение Vector2d.dot_product_static({vec1},{vec2}) = {Vector2d.dot_product_static(vec1,vec2)}")
    print()

    print(f"Векторное произведение {vec1}.cross_product({vec2}) = {vec1.cross_product(vec2)}")
    print(f"Статическое векторное произведение Vector2d.cross_product_static({vec1},{vec2}) = {Vector2d.cross_product_static(vec1, vec2)}")
    print()

    vec3 = vec1+vec2
    print(f"Смешанное произведение {vec1}.triple_product({vec2},{vec3}) = {vec1.triple_product(vec2,vec3)}")
    print(f"Статическое смешанное произведение Vector2d.triple_product_static({vec1},{vec2},{vec3}) = {Vector2d.triple_product_static(vec1, vec2, vec3)}")
    
if __name__ == "__main__":
    main()