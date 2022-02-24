cuboids = []
with open("22_input.txt", "r") as f:
    for row in f:
        row = row.strip().replace("x=", "").replace(",y=", " ").replace(",z=", " ")
        row = row.replace("..", " ")
        row = row.replace("on", "1").replace("off", "0")
        cuboids.append([int(x) for x in row.split()])


def intersection(s, t):
    mm = [lambda a, b: -b, max, min, max, min, max, min]
    n = [mm[i](s[i], t[i]) for i in range(7)]
    return None if n[1] > n[2] or n[3] > n[4] or n[5] > n[6] else n


cores = []
for cuboid in cuboids:
    toadd = [cuboid] if cuboid[0] == 1 else []
    for core in cores:
        inter = intersection(cuboid, core)
        if inter:
            toadd.append(inter)
    cores.extend(toadd)


def countoncubes(cores):
    oncount = 0
    for c in cores:
        oncount += c[0] * (c[2] - c[1] + 1) * (c[4] - c[3] + 1) * (c[6] - c[5] + 1)
    return oncount


print(countoncubes(cores))
