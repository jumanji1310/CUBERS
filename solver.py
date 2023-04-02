
# cubestring = 'FLDFUBRLDRUFRRRBRRUFBDFBDDLBRUBDFUUFUDBDLLLLLLURUBBDFF'

# for scramble of B1 R2 L1 F3 B3 R3 B1 (7f)
cubestring = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'


import twophase.solver as sv
cubestring = 'RBBUUFDDFLRDRRBRRFLFUUFULBDBLBFDBRRDULFDLFULULDBUBLRDF' # blue on top R2 F2 U3 F2 U3 R2 D3 F2 L1 D1 F2 L1 R2 B1 L2 R1 B3 U3 L2 (19f)
print(sv.solve(cubestring,max_length=20,timeout=0.1))

goalstring = 'RBBUUFDDFLRDRRBRRFLFUUFULBDBLBFDBRRDULFDLFULULDBUBLRDF'
sv.solveto(cubestring,goalstring,max_length=20,timeout=0.1)