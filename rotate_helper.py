def rotate_cw(word):
    new_string = ""
    for col in range(3):
        for row in range(2,-1,-1):
            new_string += word[row*3 + col]
    return new_string

def rotate_ccw(word):
    new_string = ""
    for col in range(2,-1,-1):
        for row in range(3):
            new_string += word[row*3 + col]
    return new_string

def flip_2(word):
    new_string = ""
    for row in range(2,-1,-1):
        for col in range(2,-1,-1):
            new_string += word[row*3 + col]
    return new_string

def rotate_other_cw(cube_state, move):
    state_list = list(cube_state)
    copy_list = list(cube_state)
    if move == "U":
        state_list[9],state_list[10],state_list[11] = copy_list[45],copy_list[46],copy_list[47]
        state_list[18],state_list[19],state_list[20] = copy_list[9],copy_list[10],copy_list[11]
        state_list[36],state_list[37],state_list[38] = copy_list[18],copy_list[19],copy_list[20]
        state_list[45],state_list[46],state_list[47] = copy_list[36],copy_list[37],copy_list[38]
        return  rotate_cw(''.join(state_list[:9])) + ''.join(state_list[9:])
    elif move == "R":
        state_list[2],state_list[5],state_list[8] = copy_list[20],copy_list[23],copy_list[26]
        state_list[20],state_list[23],state_list[26] = copy_list[29],copy_list[32],copy_list[35]
        state_list[29],state_list[32],state_list[35] = copy_list[51],copy_list[48],copy_list[45]
        state_list[45],state_list[48],state_list[51] = copy_list[8],copy_list[5],copy_list[2]
        return  ''.join(state_list[:9]) + rotate_cw(''.join(state_list[9:18])) + ''.join(state_list[18:])
    elif move == "F":
        state_list[6],state_list[7],state_list[8] = copy_list[44],copy_list[41],copy_list[38]
        state_list[9],state_list[12],state_list[15] = copy_list[6],copy_list[7],copy_list[8]
        state_list[27],state_list[28],state_list[29] = copy_list[15], copy_list[12],copy_list[9]
        state_list[38],state_list[41],state_list[44] = copy_list[27],copy_list[28],copy_list[29]
        return  ''.join(state_list[:18]) + rotate_cw(''.join(state_list[18:27])) + ''.join(state_list[27:])
    elif move == "D":
        state_list[15],state_list[16],state_list[17] = copy_list[24],copy_list[25],copy_list[26]
        state_list[24],state_list[25],state_list[26] = copy_list[42],copy_list[43],copy_list[44]
        state_list[42],state_list[43],state_list[44] = copy_list[51],copy_list[52],copy_list[53]
        state_list[51],state_list[52],state_list[53] = copy_list[15],copy_list[16],copy_list[17]
        return  ''.join(state_list[:27]) + rotate_cw(''.join(state_list[27:36])) + ''.join(state_list[36:])
    elif move == "L":
        state_list[0],state_list[3],state_list[6] = copy_list[53],copy_list[50],copy_list[47]
        state_list[18],state_list[21],state_list[24] = copy_list[0],copy_list[3],copy_list[6]
        state_list[27],state_list[30],state_list[33] = copy_list[18],copy_list[21],copy_list[24]
        state_list[47],state_list[50],state_list[53] = copy_list[33],copy_list[30],copy_list[27]
        return  ''.join(state_list[:36]) + rotate_cw(''.join(state_list[36:45])) + ''.join(state_list[45:])
    elif move == "B":
        state_list[0],state_list[1],state_list[2] = copy_list[11],copy_list[14],copy_list[17]
        state_list[11],state_list[14],state_list[17] = copy_list[35],copy_list[34],copy_list[33]
        state_list[33],state_list[34],state_list[35] = copy_list[36],copy_list[39],copy_list[42]
        state_list[36],state_list[39],state_list[42] = copy_list[2],copy_list[1],copy_list[0]
        return  ''.join(state_list[:45]) + rotate_cw(''.join(state_list[45:54])) + ''.join(state_list[54:])
    return ''.join(state_list)

def update_cubestring(cubestring, moves):
    for move in moves:
        if move == "U":
            cubestring = rotate_other_cw(cubestring, 'U')
        elif move == "U'":
            for _ in range(3):
                cubestring = rotate_other_cw(cubestring, 'U')
        elif move == "U2":
            for _ in range(2):
                cubestring = rotate_other_cw(cubestring, 'U')      
        elif move == "R":
            cubestring = rotate_other_cw(cubestring, 'R')
        elif move == "R'":
            for _ in range(3):
                cubestring = rotate_other_cw(cubestring, 'R')
        elif move == "R2":
            for _ in range(2):
                cubestring = rotate_other_cw(cubestring, 'R')     
        elif move == "F":
            cubestring = rotate_other_cw(cubestring, 'F')
        elif move == "F'":
            for _ in range(3):
                cubestring = rotate_other_cw(cubestring, 'F')
        elif move == "F2":
            for _ in range(2):
                cubestring = rotate_other_cw(cubestring, 'F')     
        elif move == "D":
            cubestring = rotate_other_cw(cubestring, 'D')
        elif move == "D'":
            for _ in range(3):
                cubestring = rotate_other_cw(cubestring, 'D')
        elif move == "D2":
            for _ in range(2):
                cubestring = rotate_other_cw(cubestring, 'D')
        elif move == "L":
            cubestring = rotate_other_cw(cubestring, 'L')
        elif move == "L'":
            for _ in range(3):
                cubestring = rotate_other_cw(cubestring, 'L')
        elif move == "L2":
            for _ in range(2):
                cubestring = rotate_other_cw(cubestring, 'L')
        elif move == "B":
            cubestring = rotate_other_cw(cubestring, 'B')
        elif move == "B'":
            for _ in range(3):
                cubestring = rotate_other_cw(cubestring, 'B')
        elif move == "B2":
            for _ in range(2):
                cubestring = rotate_other_cw(cubestring, 'B')     
    return cubestring        

# Example usage
# input_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
# new_state = update_cubestring(input_state,"R' F D2 R2 D' R2 D B L2 D F' R' D' L' B2 L B2 L' F2 D2 L".split(' '))
# print(new_state)
# "LRUDULFLFRDBBRDRRDUUDFFUDBBLLURDFRULUBRRLLDUFLDFFBBBFB"