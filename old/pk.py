import random

r_min,r_max = 450,2550
c_min,c_max = 600,3400

r_divs = 5
c_divs = 6
r_space = (r_max-r_min)/r_divs
c_space = (c_max-c_min)/c_divs
points =[]
for r in range(r_divs):
    for c in range(c_divs):
        rl = round(r_min + r *r_space)
        rr = round(r_min + (r+1) * r_space)
        cl = round(c_min + c *c_space)
        cr = round(c_min + (c+1) * c_space)
        print(f"row({rl},{rr}")
        print(f"col({cl},{cr}")
        print(f"**************")
        point = {
            "row":random.randint(rl,rr),
            "column":random.randint(cl,cr)
        }
        points.append(point)