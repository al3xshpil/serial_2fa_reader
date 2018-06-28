import serial, time, re
#initialization and open the port
#possible timeout values:

def GetGcode():
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    #ser.port = "/dev/ttyS2"
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_NONE #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    ser.timeout = None          #block read
    #ser.timeout = 0             #non-block read
    #ser.timeout = 5              #timeout block read
    #ser.xonxoff = False     #disable software flow control
    #ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    #ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    #ser.writeTimeout = 2     #timeout for write
    try:
        ser.open()

    except Exception:

        print("error open serial port: ")
        exit()


    if ser.isOpen():
        try:


            ser.flushInput() #flush input buffer, discarding all its contents


            ser.flushOutput()#flush output buffer, aborting current output

                         #and discard all that is in buffer

            #ser.write(b"ATI\r\n")


            #print("write data: ATI")


            time.sleep(1)  #give the serial port sometime to receive the data

            ser.write( b"AT+CMGF=1\r\n" )

            time.sleep(1)

            ser.write(b"AT+CPMS=\"MT\"\r\n")

            time.sleep(1)


            #ser.write(b"AT+CMGL=\"REC UNREAD\"\r\n") #For new messages
            ser.write( b"AT+CMGL=\"REC UNREAD\"\r\n" )
            #print("Reading messages...")

            #For test

            time.sleep(1)

            numOfLines = 0

            buffer = []

            while True:


                response = ser.readline()
                buffer.append(response)
                #print("read data: " + response)

                numOfLines = numOfLines + 1
                if (numOfLines >= 9):
                    break


            ser.close()


            #print("buffer: ")
            #print(buffer)

        except Exception:


            print("error communicating...: ")

    else:
        print("cannot open serial port ")


    try:
        gcode_regular = re.compile("G-[0-9][0-9][0-9][0-9][0-9][0-9]")
        Message = filter(gcode_regular.match, buffer)
        gcode = re.search("G-[0-9][0-9][0-9][0-9][0-9][0-9]", Message[0])
        gcode = gcode.group(0)

        #print("Nash poluchenniy G-Code: "+ gcode)
    except Exception:
        print("No new messages")

    return(gcode)