#include "project.h"

int step_delay = 1000; //uS
int delay = 10; //ms
int turn_delay = 6; //ms
int fullsteps = 200; //200 steps in full revolution
int speed = 1;

void turn(int face, int clockwise, int steps){  

    // set face to LOW state to enable the motor
    if (face == 0){
        Enable_1_Write(0); 
    }else if (face == 1){
        Enable_2_Write(0); 
    }else if (face == 2){
        Enable_3_Write(0);         
    }else if (face == 3){
        Enable_4_Write(0);         
    }else if (face == 4){
        Enable_5_Write(0);         
    }
    CyDelay(delay);
    
    // setting direction
    if (clockwise){
        Direction_Write(1); // HIGH for clockwise
    }else{
        Direction_Write(0); // LOW for counter clockwise
    }
    
    // Step pulse depending on number of steps and current speed
    for (int i=0; i < steps; i++){
        Step_Write(1);
        CyDelayUs(step_delay);
        Step_Write(0);
        CyDelayUs(step_delay);
    }
    
    // set face to HIGH state to disable the motor
    CyDelay(delay);
    int sleep = 1;
    if (sleep == 1){
        if (face == 0){
            Enable_1_Write(1); 
        }else if (face == 1){
            Enable_2_Write(1); 
        }else if (face == 2){
            Enable_3_Write(1);         
        }else if (face == 3){
            Enable_4_Write(1);         
        }else if (face == 4){
            Enable_5_Write(1);         
        }
    }
    CyDelay(speed*turn_delay);
}

int main(void)
{
    CyGlobalIntEnable; /* Enable global interrupts. */    
    // Initialise enable to be high (off) and direction to be 0
    Direction_Write(0);
    Enable_1_Write(1);
    Enable_2_Write(1);
    Enable_3_Write(1);
    Enable_4_Write(1);
    Enable_5_Write(1);
    
    char buffer[500];
    uint16_t index = 0;
    char ch; //current character
    char move[3] = ""; //max move length of 2 and null terminator
    int moveIndex = 0;
    UART_Start(); // Start UART component

    UART_PutString("Robot Initialised \r\n");
    
    for(;;)
    {
        if(UART_GetRxBufferSize() > 0) // Check if there are incoming characters
        {
            ch = UART_GetChar(); // Read incoming character

            //process string if return character is found
            if (ch == '\r')
            {
                for (int i = 0; i < index; i++){  
                    if (buffer[i] == ' '){ //there is a space
                        if(moveIndex > 0){
                            move[moveIndex] = '\0'; // Add null terminator to move string
                            moveIndex = 0; // Reset move index
                            
                            // Do something with the move string
                            if(strcmp(move, "R") == 0){
                                UART_PutString("R\r\n");
                                turn(0, 0, fullsteps/4);
                            }else if(strcmp(move, "R'") == 0){
                                UART_PutString("R'\r\n");
                                turn(0, 1, fullsteps/4);
                            }else if(strcmp(move, "R2") == 0){
                                UART_PutString("R2\r\n");
                                turn(0, 0, fullsteps/2);
                            }else if(strcmp(move, "F") == 0){
                                UART_PutString("F\r\n");
                                turn(1, 0, fullsteps/4);
                            }else if(strcmp(move, "F'") == 0){
                                UART_PutString("F'\r\n");
                                turn(1, 1, fullsteps/4);
                            }else if(strcmp(move, "F2") == 0){
                                UART_PutString("F2\r\n");
                                turn(1, 0, fullsteps/2);
                            }else if(strcmp(move, "D") == 0){
                                UART_PutString("D\r\n");
                                turn(2, 0, fullsteps/4);
                            }else if(strcmp(move, "D'") == 0){
                                UART_PutString("D'\r\n");
                                turn(2, 1, fullsteps/4);
                            }else if(strcmp(move, "D2") == 0){
                                UART_PutString("D2\r\n");
                                turn(2, 0, fullsteps/2);
                            }else if(strcmp(move, "L") == 0){
                                UART_PutString("L\r\n");
                                turn(3, 0, fullsteps/4);
                            }else if(strcmp(move, "L'") == 0){
                                UART_PutString("L'\r\n");
                                turn(3, 1, fullsteps/4);
                            }else if(strcmp(move, "L2") == 0){
                                UART_PutString("L2\r\n");
                                turn(3, 0, fullsteps/2);
                            }else if(strcmp(move, "B") == 0){
                                UART_PutString("B\r\n");
                                turn(4, 0, fullsteps/4);
                            }else if(strcmp(move, "B'") == 0){
                                UART_PutString("B'\r\n");
                                turn(4, 1, fullsteps/4);
                            }else if(strcmp(move, "B2") == 0){
                                UART_PutString("B2\r\n");
                                turn(4, 0, fullsteps/2);
                            }else if (strcmp(move, "slow") == 0){
                                UART_PutString("slow\r\n");
                                speed = 10;
                            }else if (strcmp(move, "fast") == 0){
                                UART_PutString("fast\r\n");
                                speed = 1;
                            }
                        }
                    }
                    else{
                        // Add current character to move string
                        move[moveIndex] = buffer[i];
                        moveIndex++;
                    }
                }
                index = 0;
                UART_PutString("Finished\r\n");
            }
            else
            {
                buffer[index] = ch; // Store incoming character in buffer
                index++;

                if(index >= 500) // Check if buffer is full
                {
                    index = 0; // Reset buffer index
                }
            }
        }
    }
}

/* [] END OF FILE */
