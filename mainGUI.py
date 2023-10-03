from tkinter import *
import random
import cv2
import detector.predict as predictor
from twophase import start_twophase, run_twophase
from rotate_helper import *
import time
from capture import predict_image, normalise
"""
Starting comms to PsoC
"""
start_serial = True
if start_serial:
    import serial

    # Define the serial port and baud rate.
    serial_port = 'COM6'
    baud_rate = 9600

    # Open the serial port.
    ser = serial.Serial(serial_port, baud_rate)

class Solver:

    def __init__(self, root):
        """
        Start two phase
        """
        self.process = start_twophase()
        self.root = root
        self.valid_moves = ["R","R'","R2","F","F'","F2","D","D'","D2","L","L'","L2","B","B'","B2"]
        self.moveLength = 0
        self.cubestring = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        self.vid = cv2.VideoCapture(0)
        ret, self.frame = self.vid.read()
        self.scanTime = 0
        self.searchTime = 0

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
        statFrame = Frame(root)
        statFrame.grid_rowconfigure(0, minsize=grid_height/2)
        statFrame.grid_rowconfigure(1, minsize=grid_height/2)
        statFrame.grid(row=1, column=0,columnspan=1,sticky='w')
        self.sec = StringVar(value ='Timer: 0.0 seconds')
        timerText = Label(statFrame, textvariable=self.sec,font=('Arial', 24))
        timerText.grid(row=0,column=0)
        self.counter = StringVar(value = 'Counter: 0 moves left')
        counterText = Label(statFrame, textvariable=self.counter,font=('Arial',24))
        counterText.grid(row=1,column=0)

        #adding cube faces
        color = ['white' for _ in range(9)]
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
        button_scan.bind("<Button-1>", self.scan)

        # add solution string
        self.solutionStr = StringVar(value="")
        solution_string = Label(button_frame, textvariable=self.solutionStr,font=('Arial', 12))
        solution_string.grid(row=1, column=0, columnspan=3, sticky ='w')

        # add input
        moves_field = Entry(button_frame,font=('Arial', 20))
        moves_field.grid(row=2, column=0, columnspan=2, sticky='nsew')

        """ add hint to input field """

        # call function when we click on entry box
        def click(*args):
            moves_field.delete(0, 'end')
            moves_field.config(font=('Arial', 20))

        # call function when we leave entry box
        def leave(*args):
            if not moves_field.get(): # check if input box is empty
                moves_field.delete(0, 'end')
                moves_field.insert(0, "Enter moves like R, R' or R2 separated by space")
                moves_field.config(font=('Arial', 12))
                root.focus()

        # Add text in Entry box
        moves_field.insert(0, "Enter moves like R, R' or R2 separated by space")
        moves_field.config(font=('Arial', 12))

        # Use bind method
        moves_field.bind("<Button-1>", click)
        moves_field.bind("<Leave>", leave)
        """"""""""""""""""""""""""""""""""""""""""""""""""""""

        # add send button
        button_send = Button(button_frame, text='Send',font=('Arial', 20))
        button_send.grid(row=2, column=2, sticky='nsew')
        button_send.bind("<Button-1>", lambda event: self.send(moves_field))

        # adding slow fast speed
        def choose_speed():
            selection = "Changed speed to " + str('Slow' if speed.get() == 1 else 'Fast')
            print(selection)
            if str(speed.get()) == "1":
                self.sendToPsoC('slow ')
            else:
                self.sendToPsoC('fast ')


        """ Adding toggle between Slow and Fast"""
        toggle_frame = Frame(root)
        toggle_frame.grid_rowconfigure(0, minsize=grid_height/2)
        toggle_frame.grid_rowconfigure(1, minsize=grid_height/2)
        toggle_frame.grid(row=2,column=2)
        speed = IntVar(value=2)
        slow = Radiobutton(toggle_frame, text='Slow',font=('Arial', 20), variable=speed,value=1, command=choose_speed)
        slow.grid(row=0,column=0)
        fast = Radiobutton(toggle_frame, text='Fast',font=('Arial', 20), variable=speed,value=2, command=choose_speed)
        fast.grid(row=1,column=0)

    def update_cube(self):
        """
        Display cubestring on the GUI
        """
        # converting cube state into colours
        colour = []
        for face in self.cubestring:
            if face == 'F':
                colour.append('white')
            elif face == 'U':
                colour.append('blue')
            elif face == 'R':
                colour.append('red')
            elif face == 'L':
                colour.append('orange')
            elif face == 'D':
                colour.append('green')
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

    def scan(self,event):
        """
        Scan image to determine each square colour of each face and update the cubestring
        """
        # left to right top to bottom in order of U R F D L B
        self.cubestring = 'LRUDULFLFRDBBRDRRDUUDFFUDBBLLURDFRULUBRRLLDUFLDFFBBBFB' # opposite of L' D2 F2 L B2 L' B2 L D R F D' L2 B' D' R2 D R2 D2 F' R
        # R' F D2 R2 D' R2 D B L2 D F' R' D' L' B2 L B2 L' F2 D2 L

        start_time = time.time()
        # Capture a single frame from the camera
        ret, self.frame = self.vid.read()
        # cv2.imshow('Scan',frame)
        # cv2.waitKey(0)
        self.cubestring = predict_image(normalise(self.frame))

        # self.cubestring = predictor.predict_Colour('images/Capture')
        self.update_cube()
        end_time = time.time()
        self.scanTime = end_time - start_time
        print(f"Scan time: {self.scanTime} seconds")
        self.sec.set(f'Timer: {self.scanTime:.4f} seconds')

        cv2.imshow("Scan Frame",self.frame)
    def scramble(self,event):
        """
        Generate 25 random valid moves for robot to scramble
        """
        # get 25 moves
        moves = []
        for i in range(25):
            idx =  random.randint(0,len(self.valid_moves)-1)
            moves.append(self.valid_moves[idx])
        moves = ' '.join(moves) + ' ' # join moves and add extra space at the end
        self.moveLength = len(moves.split(" ")) - 1
        self.solutionStr.set(f'Scramble: {moves} ({self.moveLength} moves)')

        print(f'Scramble: {moves}')

        # send to PsoC
        self.sendToPsoC(moves)

    def solve(self,event):
        """
        Scan the cube, update the GUI and solve it
        """

        # scan cube before solving
        self.scan(event)
        start_time = time.time()
        # Convert cube state where up face becomes back face
        """
        U to B
        F to U
        D to F
        B to D
        """
        up_string = self.cubestring[:9]
        right_string = self.cubestring[9:18]
        front_string = self.cubestring[18:27]
        down_string = self.cubestring[27:36]
        left_string = self.cubestring[36:45]
        back_string = self.cubestring[45:54]
        new_cubestring = front_string + rotate_cw(right_string) + down_string + flip_2(back_string) + rotate_ccw(left_string) + flip_2(up_string)

        stateswap_dict = {'U':'B','F':'U','D':'F','B':'D'}
        new_cubestring2 = ""
        for letter in new_cubestring:
            if letter in stateswap_dict:
                new_cubestring2 += stateswap_dict[letter]
            else:
                new_cubestring2 += letter

        solve_string = run_twophase(self.process,new_cubestring2)
        solve_array = solve_string.split(' ')[:-1]

        # Converting to moves and rotating so B moves become U moves
        """
        U to F
        F to D
        D to B
        """
        moveswap_dict = {'U':'F','F':'D','D':'B'}
        for i in range(len(solve_array)):
            if solve_array[i][0] in moveswap_dict:
                solve_array[i] = moveswap_dict[solve_array[i][0]] + solve_array[i][1:]

        moves = ' '.join(solve_array) + ' '
        self.moveLength = len(moves.split(" ")) - 1
        self.solutionStr.set(f'Solution: {moves} ({self.moveLength} moves)')

        end_time = time.time()
        self.searchTime = end_time - start_time
        print(f"Search time: {self.searchTime} seconds")
        self.sec.set(f'Timer: {self.scanTime + self.searchTime:.4f} seconds')

        # print moves
        print(f'Solution: {moves}')

        # send to PsoC
        self.sendToPsoC(moves)

    def send(self, input):
        """
        send moves from input to motors
        """

        input_string = input.get()
        # check if moves are valid and replace U turns
        try:
            moves = input_string.split(' ')
            new_moves = []

            # checking for valid moves
            for i in range(len(moves)):
                moves[i] = moves[i].upper()
                if moves[i] not in self.valid_moves:
                    raise
                else:
                    new_moves.append(moves[i])
            moves = ' '.join(new_moves) + ' ' # join moves and add extra space at the end
            self.moveLength = len(moves.split(" ")) - 1
            self.solutionStr.set(f'Moves: {moves}  ({self.moveLength} moves)')

            print(f'Send: {moves}')
            # send to PsoC
            self.sendToPsoC(moves)

        except Exception as e:
            # displaying error
            self.solutionStr.set('Error: invalid moves')

    def sendToPsoC(self, message):
        if start_serial:
            ser.write(f'{message}\r'.encode())

            self.counter.set(f'Counter: {self.moveLength} moves left')
            start_time = time.time()  # Record start time
            print('Received message: ',end="")
            while True:
                # calculating elapsed time
                end_time = time.time()  # Record end time
                solve_time = end_time - start_time  # Calculate elapsed time

                # updating timer
                self.sec.set(f'Timer: {self.scanTime + self.searchTime + solve_time:.4f} seconds')
                root.update()

                # checking message from PsoC
                received_message = ser.readline().decode().strip()  # Read a line from serial
                print(f' {received_message}',end="")

                if received_message == 'Finished':
                    print(f'\nSolve time: {solve_time:.4f} seconds')
                    print(f'Total time: {self.scanTime + self.searchTime + solve_time:.4f} seconds')
                    break  # Exit the loop if 'stop' is received
                elif received_message in self.valid_moves:
                    # updating counter
                    self.moveLength -= 1
                    self.counter.set(f'Counter: {self.moveLength} moves left')

                    # updating cube state on GUI
                    self.cubestring = update_cubestring(self.cubestring, [received_message])
                    self.update_cube()
        else:
            print(f'Emulating message {message}')

root = Tk()
Solver(root)
root.mainloop()