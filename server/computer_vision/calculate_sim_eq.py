import sympy as sym

lower_bound_x = 0
upper_bound_x = 250
lower_bound_y = 0
upper_bound_y = 250


def triangulate_position(p1, p2, d1, d2):
    x,y = sym.symbols('x,y')
    eq1 = sym.Eq((x - p1[0])**2 + (y - p1[1])**2, d1**2)
    eq2 = sym.Eq((x - p2[0])**2 + (y - p2[1])**2, d2**2)
    results = sym.solve([eq1,eq2],(x,y))
    

    valid_results = []

    for x,y in results:
        if x < lower_bound_x or x > upper_bound_x:
            continue
        if y < lower_bound_y or y > upper_bound_y:
            continue
        valid_results.append((int(x), int(y)))

    assert(len(valid_results) == 1)

    result = valid_results[0]
    print(f"\n\n\nRESULT: {result}")
    return result

triangulate_position((0,235),(15,250),59,67)