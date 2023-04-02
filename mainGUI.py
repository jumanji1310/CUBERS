from tkinter import *
import random

# import detector.predict as predictor
import twophase.solver as sv


class Solver:

    def __init__(self, root):
        self.root = root
        self.valid_moves = ["R","R'","R2","F","F'","F2","D","D'","D2","L","L'","L2","B","B'","B2"]

        # make the window not resizable
        root.resizable(width=0, height=0)

        grid_width = 210
        grid_height = 210
        for i in range(3):
            root.rowconfigure(i, weight=1, minsize=grid_height)           
        for j in range(5):
            #extra width for first column
            if j == 0:
                root.columnconfigure(j, weight=1, minsize=grid_width + 200)
            else:
                root.columnconfigure(j, weight=1, minsize=grid_width)

        #frame0_0
        robot_name = Label(text="CUBERS",font=('Arial', 40))
        robot_name.grid(row=0, column=0,padx=30)

        #frame0_1 and frame0_2
        text = Label(text="Timer and Counter placeholder")
        text.grid(row=0, column=1,columnspan=2)

        #adding cube faces
        color = ['white' for _ in range(9)]
        # color = ['blue', 'yellow', 'yellow', 'orange', 'orange', 'white', 'red', 'red', 'white']
        self.cube_face_loc = [(0,3),(1,4),(1,3),(2,3),(1,2),(1,1)] # U R F D L B
        cube_face_label = ['U','R','F','D','L','B']
        for face_id, cell in enumerate(self.cube_face_loc):
            # creating inner grid
            i, j = cell[0], cell[1]
            frame = Frame(root,padx=5,pady=5)
            frame.grid(row=i, column=j)

            # set the size of the inner grid
            for i in range(3):
                frame.grid_rowconfigure(i, minsize=grid_height/3)
            for j in range(3):
                frame.grid_columnconfigure(j, minsize=grid_width/3)

            # add cube faces to the inner grid
            for i in range(3):
                for j in range(3):
                    face = ''
                    if i == 1 and j == 1:
                        face = cube_face_label[face_id]
                    label = Label(frame, text=face,font=('Arial', 20),bg=f'{color[i+j]}',borderwidth=2, relief=SOLID)
                    label.grid(row=i, column=j, sticky="nsew")

        #adding buttons frmae
        button_frame = Frame(root)
        button_frame.grid(row=2,column=0,columnspan=2)

        # set the size of the buttons in the frame
        for i in range(3):
            button_frame.grid_rowconfigure(i, minsize=grid_height/3)
        for j in range(3):
            button_frame.grid_columnconfigure(j, minsize=2*(grid_width + 100)/3)
        
        # add solve button
        button_solve = Button(button_frame, text="Solve",font=('Arial', 20))
        button_solve.grid(row=0, column=0, sticky="nsew")
        button_solve.bind("<Button-1>", self.solve)

        # add scramble button
        button_scramble = Button(button_frame, text="Scramble",font=('Arial', 20))
        button_scramble.grid(row=0, column=1, sticky="nsew")
        button_scramble.bind("<Button-1>", self.scramble)

        # add scan button
        button_scan = Button(button_frame, text="Scan",font=('Arial', 20))
        button_scan.grid(row=0, column=2, sticky="nsew")
        button_scan.bind("<Button-1>", self.update_cube)

        # add solution string
        solution_string = Label(button_frame, text="",font=('Arial', 12))
        solution_string.grid(row=1, column=0, columnspan=3, sticky ='w')

        # add input
        moves_field = Entry(button_frame,font=('Arial', 20))
        moves_field.grid(row=2, column=0, columnspan=2, sticky='nsew')

        # add send button
        button_send = Button(button_frame, text='Send',font=('Arial', 20))
        button_send.grid(row=2, column=2, sticky='nsew')
        button_send.bind("<Button-1>", lambda event: self.send(moves_field))

    def update_cube(self,event):
        # left to right top to bottom in order of U R F D L B
        self.cubestring = 'RBBUUFDDFLRDRRBRRFLFUUFULBDBLBFDBRRDULFDLFULULDBUBLRDF'
        # cubestring = predictor.predict_Colour('images/Set2')

        # converting cube state into colours
        colour = []
        for face in self.cubestring:
            if face == 'F':
                colour.append('white')
            elif face == 'U':
                colour.append('orange')
            elif face == 'R':
                colour.append('blue')
            elif face == 'L':
                colour.append('green')
            elif face == 'D':
                colour.append('red')
            elif face == 'B':
                colour.append('yellow')

        # updating cube state on GUI
        for face_id, (i, j) in enumerate(self.cube_face_loc):
            frames = self.root.grid_slaves(i, j)
            for row in range(3):
                for col in range(3):
                    square = frames[0].grid_slaves(row, col)
                    square_color = colour[face_id*9 + row*3 + col]
                    square[0].configure(background=square_color)
                    square[0].configure(highlightbackground='black')
            
    def scramble(self,event):
      
        # get 20 moves
        moves = []
        for i in range(20):
            idx =  random.randint(0,len(self.valid_moves)-1)
            moves.append(self.valid_moves[idx])
        moves = ' '.join(moves)
        
        # displaying scramble moves
        frame = self.root.grid_slaves(2,0)
        label = frame[0].grid_slaves(1,0)
        label[0].configure(text=f'Scramble: {moves}',foreground='black')

    def solve(self,event):
        # update cube before solving
        self.update_cube(event)
        solve_string = sv.solve(self.cubestring,max_length=20,timeout=0.1)

        # replacing moves with 3 turns with counter-clockwise ' notation
        solve_array = solve_string.split(' ')
        for i in range(len(solve_array) - 1):
            if solve_array[i][1] == '3':
                solve_array[i] = solve_array[i][0] + "'"

        moves = ' '.join(solve_array)

        # # replacing U moves
        # moves = []
        # for move in solve_array:
        #     if move in ["U","U'","U2"]:
        #         moves.append(self.replace_u(move))
        #     else:
        #         moves.append(move)
        # moves = ' '.join(moves)

        # displaying solution moves
        frame = self.root.grid_slaves(2,0)
        label = frame[0].grid_slaves(1,0)
        label[0].configure(text=f'Solution: {moves}',foreground='black')

    def send(self, input):
        # send moves from input
        input_string = input.get()

        # check if moves are valid and replace U turns
        try:
            moves = input_string.split(' ')
            new_moves = []

            # checking for valid moves
            for i in range(len(moves)):
                moves[i] = moves[i].upper()
                # swap U moves with alternative
                if moves[i] in ["U","U'","U2"]: 
                    new_moves.append(self.replace_u(moves[i]))
                elif moves[i] not in self.valid_moves:
                    raise
                else:
                    new_moves.append(moves[i])
            moves = ' '.join(new_moves)

            # displaying moves sent
            frame = self.root.grid_slaves(2,0)
            label = frame[0].grid_slaves(1,0)
            label[0].configure(text=f'Moves: {moves}',foreground='black')
            
        except Exception as e:
            # displaying error
            frame = self.root.grid_slaves(2,0)
            label = frame[0].grid_slaves(1,0)
            label[0].configure(text=f'Error: invalid moves',foreground='red')
    
    def replace_u(self, u_type):
        if u_type == "U":
            return "R L F2 B2 R' L' D R L F2 B2 R' L'"
        elif u_type == "U'":
            return "R L F2 B2 R' L' D' R L F2 B2 R' L'"
        elif u_type == "U2":
            return "R L F2 B2 R' L' D2 R L F2 B2 R' L'"
        
root = Tk()
Solver(root)
root.mainloop()