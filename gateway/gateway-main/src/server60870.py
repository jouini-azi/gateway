from http import server
from lib60870 import *
import time

class IEC60870_5_104_server:

    def printCP56Time2a(self, time):
        print("%02i:%02i:%02i %02i/%02i/%04i" % ( CP56Time2a_getHour(time),
                        CP56Time2a_getMinute(time),
                        CP56Time2a_getSecond(time),
                        CP56Time2a_getDayOfMonth(time),
                        CP56Time2a_getMonth(time),
                        CP56Time2a_getYear(time) + 2000) )
    
    def clock(self, param, con, asdu, newTime):
        """
        set the time

        :param param : parameter	user provided parameter

        :param con : represents the TCP connection that received the time sync command

        :param asdu : the received ASDU
        
        :newTime : time received with the time sync message. The user can update this time for the ACT-CON message
        """
        print("Process time sync command with time ")
        self.printCP56Time2a(newTime)
        newSystemTimeInMs = CP56Time2a_toMsTimestamp(newTime)
        """
        :param CP56Time2a_toMsTimestamp : Convert a 7 byte time to a ms timestamp
        """
        #/*  */
        CP56Time2a_setFromMsTimestamp(newTime, Hal_getTimeInMs())
        """
        Set time for ACT_CON message

        :param CP56Time2a_setFromMsTimestamp : Set the time value of a 7 byte time from a UTC ms timestamp
        """
        #/* update system time here */
        return True

    def GI_h(self, param, connection, asdu, qoi):
        """
        Handle the interrogration command from the client

        :param param : parameter user provided parameter

        :param connection : represents the TCP connection that received the time sync command

        :param asdu : the received ASDU

        :param qoi : //

        """
        print(f"Received interrogation for group {qoi}")

        #only handle station interrogation

        if (qoi == 20): 
            
            #Get the application layer parameters used by this connection

            alParams = IMasterConnection_getApplicationLayerParameters(connection)

            IMasterConnection_sendACT_CON(connection, asdu, negative =False)
            """
            Send an ACT_CON ASDU to the client/master
            
            :param asdu : the ASDU to send to the client/master
            :param negative : value of the negative flag
            """

            #The CS101 specification only allows information objects without timestamp in GI responses
            
            # measuredvalue
            type = MeasuredValueScaled
            #Create a new ASDU.
            newAsdu = CS101_ASDU_create(alParams, isSequence = False, cot = CS101_COT_INTERROGATED_BY_STATION, oa = 0,ca = 1, isTest =  False, isNegative =  False)
            """
            Create a new ASDU

            :param alparams : the application layer parameters used to encode the ASDU
            
            
            :param isSequence : if the information objects will be encoded as a compact sequence of information objects with subsequent IOA values

            :param cot : Cause of transmission

            :param oa : originator address (OA) to be used

            :param ca : the common address (CA) of the ASDU

            :param isTest : if the test flag will be set or not

            :param isNegative : if the negative flag will be set or not
            """
            io = None
            for ioa in self.IOA_list:
                if self.IOA_list[ioa]['type'] == type:
                    if io == None:
                        #Create a new instance of MeasuredValueScaled information object
                        io = cast( MeasuredValueScaled_create(None,ioa,value = self.IOA_list[ioa]['data'], quality =IEC60870_QUALITY_GOOD), InformationObject) #
                        """
                        Create a new instance of MeasuredValueScaled information object
                        
                        :param self : Reference to an existing instance to reuse, if NULL a new instance will we dynamically allocated

                        :param ioa : information object address

                        :param value : scaled value ( range -32768 - 32767)

                        :param quality : quality descriptor
                        """
                        #add an information object to the ASDU
                        CS101_ASDU_addInformationObject(newAsdu, io)
                    else:
                        CS101_ASDU_addInformationObject(newAsdu, cast( MeasuredValueScaled_create(cast(io,MeasuredValueScaled),ioa,self.IOA_list[ioa]['data'],IEC60870_QUALITY_GOOD), InformationObject) )
            if io != None:
                #Destroy object - free all related resources
                InformationObject_destroy(io)
                #Send an ASDU to the client/master.
                IMasterConnection_sendASDU(connection, newAsdu)
            #Destroy the ASDU object (release all resources) 
            CS101_ASDU_destroy(newAsdu)

            #singlepoint
            type = SinglePointInformation
            #Create a new ASDU.
            newAsdu = CS101_ASDU_create(alParams, False, CS101_COT_INTERROGATED_BY_STATION, 0, 1, False, False)
            io = None
            for ioa in self.IOA_list:
                if self.IOA_list[ioa]['type'] == type:
                    if io == None:
                        io = cast( SinglePointInformation_create(None, ioa, self.IOA_list[ioa]['data'], IEC60870_QUALITY_GOOD), InformationObject)
                        #add an information object to the ASDU
                        CS101_ASDU_addInformationObject(newAsdu, io)
                    else:
                        CS101_ASDU_addInformationObject(newAsdu, cast( SinglePointInformation_create(cast(io,SinglePointInformation), ioa,self.IOA_list[ioa]['data'],IEC60870_QUALITY_GOOD), InformationObject) )
            if io != None:
                #Destroy object - free all related resources
                InformationObject_destroy(io)
                #Send an ASDU to the client/master.
                IMasterConnection_sendASDU(connection, newAsdu)
            #Destroy the ASDU object (release all resources) 
            CS101_ASDU_destroy(newAsdu)

            #doublepoint
            type = DoublePointInformation
            #Create a new ASDU.
            newAsdu = CS101_ASDU_create(alParams, False, CS101_COT_INTERROGATED_BY_STATION, 0, 1, False, False)
            io = None
            for ioa in self.IOA_list:
                if self.IOA_list[ioa]['type'] == type:
                    if io == None:
                        io = cast( DoublePointInformation_create(None, ioa, self.IOA_list[ioa]['data'], IEC60870_QUALITY_GOOD), InformationObject)
                        #add an information object to the ASDU
                        CS101_ASDU_addInformationObject(newAsdu, io)
                    else:
                        CS101_ASDU_addInformationObject(newAsdu, cast( DoublePointInformation_create(cast(io,DoublePointInformation), ioa,self.IOA_list[ioa]['data'],IEC60870_QUALITY_GOOD), InformationObject) )
            if io != None:
                #Destroy object - free all related resources
                InformationObject_destroy(io)
                #Send an ASDU to the client/master.
                IMasterConnection_sendASDU(connection, newAsdu)
            #CS101_ASDU_destroy = Destroy the ASDU object (release all resources) 
            CS101_ASDU_destroy(newAsdu)

            #Send an ASDU to the client/master.
            IMasterConnection_sendACT_TERM(connection, asdu)
        else:
            #Send an ASDU to the client/master.
            IMasterConnection_sendACT_CON(connection, asdu, True)



    def ASDU_h(self, param, connection, asdu):
        print("ASDU received")

        #Get the cause of transmission (COT) of the ASDU.
        cot = CS101_ASDU_getCOT(asdu)

        #CS104_COT_ACTIVATION = 6
        if cot == CS101_COT_ACTIVATION:
            #Get the information object with the given index
            io = CS101_ASDU_getElement(asdu, 0)
            #Get object Adress , type of Object Adress is int
            ioa = InformationObject_getObjectAddress(io)
            if not ioa in self.IOA_list:
                print("could not find IOA")
                #Set the cause of transmission (COT) of the ASDU
                #CS101_COT_UNKNOWN_IOA = 47
                CS101_ASDU_setCOT(asdu, CS101_COT_UNKNOWN_IOA)
            else:
                ioa_object = self.IOA_list[ioa]

                #Get the type ID of the ASDU.
                if (CS101_ASDU_getTypeID(asdu) == C_SC_NA_1): # C_SC_NA_1 = 1
                    print("received single command")
                    if ioa_object['type'] == SingleCommand:
                        sc = cast( io, SingleCommand)
                        #Get object Adress , type of Object Adress is int
                        print(f"IOA: {InformationObject_getObjectAddress(io)} switch to {SingleCommand_getState(sc)}, select:{SingleCommand_isSelect(sc)}")
                        #Get the state (command) value.
                        ioa_object['data'] = SingleCommand_getState(sc)
                        if self.IOA_list[ioa]['callback'] != None:
                            self.IOA_list[ioa]['callback'](ioa,ioa_object, self, SingleCommand_isSelect(sc))
                        #Set the cause of transmission (COT) of the ASDU
                        CS101_ASDU_setCOT(asdu, CS101_COT_ACTIVATION_CON)  #CS101_COT_ACTIVATION_CON = 7
                    else:
                        print("mismatching asdu type:")
                        #Set the cause of transmission (COT) of the ASDU
                        CS101_ASDU_setCOT(asdu, CS101_COT_UNKNOWN_TYPE_ID)

                #Get the type ID of the ASDU
                if (CS101_ASDU_getTypeID(asdu) == C_DC_NA_1):
                    print("received double command")
                    if ioa_object['type'] == DoubleCommand:
                        sc = cast( io, DoubleCommand)
                        #Get object Adress , type of Object Adress is int
                        print(f"IOA: {InformationObject_getObjectAddress(io)} switch to {DoubleCommand_getState(sc)}, select:{DoubleCommand_isSelect(sc)}")
                        ioa_object['data'] = DoubleCommand_getState(sc)
                        if self.IOA_list[ioa]['callback'] != None:
                            self.IOA_list[ioa]['callback'](ioa,ioa_object, self, DoubleCommand_isSelect(sc))
                        #Set the cause of transmission (COT) of the ASDU
                        CS101_ASDU_setCOT(asdu, CS101_COT_ACTIVATION_CON)
                    else:
                        print("mismatching asdu type:")
                        #CS101_ASDU_setCOT = Set the cause of transmission (COT) of the ASDU
                        CS101_ASDU_setCOT(asdu, CS101_COT_UNKNOWN_TYPE_ID)
            #Destroy object - free all related resources
            InformationObject_destroy(io)
        elif cot == CS101_COT_ACTIVATION_TERMINATION:  #CS101_COT_ACTIVATION_TERMINATION = 10
            print("GI done")
        else:
            #Get the cause of transmission (COT) of the ASDU
            print("ASDU unknown: " + str(CS101_ASDU_getCOT(asdu)))
            CS101_ASDU_setCOT(asdu, CS101_COT_UNKNOWN_COT)  #CS101_COT_UNKNOWN_COT = 45
        
        #Send an ACT_TERM ASDU to the client/master ;
        #ACT_TERM is used to indicate that the command execution is complete;
        IMasterConnection_sendASDU(connection, asdu)
        """
        Send an ASDU to the client/master

        :param connection : the connection object

        :param asdu : the ASDU to send to the client/master
        """
        return True


    def Conn_req(self, param, address):
        print("New connection request")
        return True
    #Show the Connection event
    def Conn_event(self, param, con, event):
        #CS104_CON_EVENT_CONNECTION_OPENED = 0
        if (event == CS104_CON_EVENT_CONNECTION_OPENED):
            print(f"Connection opened {con}")
        #CS104_CON_EVENT_CONNECTION_CLOSED = 1
        elif (event == CS104_CON_EVENT_CONNECTION_CLOSED):
            print(f"Connection closed {con}")
        #CS104_CON_EVENT_ACTIVATED = 2
        elif (event == CS104_CON_EVENT_ACTIVATED):
            print(f"Connection activated {con}")
        #CS104_CON_EVENT_DEACTIVATED = 3
        elif (event == CS104_CON_EVENT_DEACTIVATED):
            print(f"Connection deactivated {con}")

    def read(self, param, connection, asdu, ioa):
        if ioa in self.IOA_list:
            # update data
            if self.IOA_list[ioa]['callback'] != None:
                self.IOA_list[ioa]['callback'](ioa,self.IOA_list[ioa], self)
            #Create a new ASDU. The type ID will be derived from the first InformationObject that will be added
            newAsdu = CS101_ASDU_create(self.alParams, False, CS101_COT_SPONTANEOUS, 0, 1, False, False) #CS101_COT_SPONTANEOUS = 3
            if self.IOA_list[ioa]['type'] == MeasuredValueScaled:
                #Create a new instance of MeasuredValueScaled information object
                io = cast(MeasuredValueScaled_create(None, ioa, self.IOA_list[ioa]['data'], IEC60870_QUALITY_GOOD),InformationObject)
            elif self.IOA_list[ioa]['type'] == SinglePointInformation:
                #Create a new instance of Single point information object
                io = cast(SinglePointInformation_create(None, ioa, self.IOA_list[ioa]['data'], IEC60870_QUALITY_GOOD),InformationObject)
            elif self.IOA_list[ioa]['type'] == DoublePointInformation:
                #Create a new instance of Double point information object
                io = cast(DoublePointInformation_create(None, ioa, self.IOA_list[ioa]['data'], IEC60870_QUALITY_GOOD),InformationObject)
            else:
                return False
            #add an information object to the ASDU
            CS101_ASDU_addInformationObject(newAsdu, io)
            #Destroy object - free all related resources
            InformationObject_destroy(io)
            #Add ASDU to slave event queue - don't release the ASDU afterwards!
            CS104_Slave_enqueueASDU(self.slave, newAsdu)
            #Destroy the ASDU object (release all resources)
            CS101_ASDU_destroy(newAsdu)
            return True
        return False


    def __init__(self, ip = "0.0.0.0"):
        self.clockSyncHandler = CS101_ClockSynchronizationHandler(self.clock)
        """
        ..py:function CS101_ClockSynchronizationHandler(self.clock) :: Handler for clock synchronization command
        
        :type self.clock : function
        """

        self.interrogationHandler = CS101_InterrogationHandler(self.GI_h)
        """
        ..py:function CS101_InterrogationHandler(self.GI_h) :: 	Handler for interrogation command (C_IC_NA_1 - 100)
        
        :type self.GI_h : function
        """

        self.asduHandler = CS101_ASDUHandler(self.ASDU_h)
        """
        ..py:function CS101_InterrogationHandler(self.ASDU_h) :: 	Handler for interrogation command (C_IC_NA_1 - 100)

        :type self.ASDU_h : function
        """

        self.connectionRequestHandler = CS104_ConnectionRequestHandler(self.Conn_req)
        """
        ..py:function CS104_ConnectionRequestHandler(self.conn_req) ::Connection request handler is called when a client tries to connect to the server
        
        :type self.conn_req : function
        """

        self.connectionEventHandler = CS104_ConnectionEventHandler(self.Conn_event)
        """"
        ..py:function CS104_ConnectionEventHandler(self.conn_event) ::Handler that is called when a peer connection is established or closed, or START_DT/STOP_DT is issued
        
        :type self.conn_event : function
        """

        self.readEventHandler = CS101_ReadHandler(self.read)
        """
        ..py:function CS101_ReadHandler(self.read):: Handler for read command (C_RD_NA_1 - 102)

        :type self.read : function
        
        """

        self.slave = CS104_Slave_create(100, 100)
        """
        ..py:function CS104_Slave_create(maxLowPrioQueueSize , maxHighPrioQueueSize) :: Create a new instance of a CS104 slave (server) 
        
        :type maxLowPrioQueueSize : int
        :param maxLowPrioQueueSize : the maximum size of the event queue


        type maxHighPrioQueueSize : int
        :param maxHighPrioQueueSize : the maximum size of the high-priority queue
        """
        
        CS104_Slave_setLocalAddress(self.slave, ip)
        """
        ..py function CS104_Slave_setLocalAddress(self.slave , ip)::Set the local IP address to bind the server use "0.0.0.0" to bind to all interfaces. 
        
        :param self.slave : the slave instance

        :param ip : the IP address string or hostname
        """

        CS104_Slave_setServerMode(self.slave, serverMode = CS104_MODE_SINGLE_REDUNDANCY_GROUP)
        """
        ..py function CS104_Slave_setServerMode(self.slave , serverMode) :: Set one of the server modes.
        
        :param self.slave : the slave instance

        :param serverMode : the server mode
        """
        self.alParams = CS104_Slave_getAppLayerParameters(self.slave)
        """
        ..py function CS104_Slave_getAppLayerParameters(self.slave) :: Get the application layer parameters instance
        
        :param self.slave : the slave instance
        """
        #/* set the callback handler for the clock synchronization command */
        CS104_Slave_setClockSyncHandler(self.slave, self.clockSyncHandler,parameter =  None)
        #/* set the callback handler for the interrogation command */
        CS104_Slave_setInterrogationHandler(self.slave, self.interrogationHandler, None)
        #/* set handler for other message types */
        CS104_Slave_setASDUHandler(self.slave, self.asduHandler, None)

        # Set the connection request handler
        CS104_Slave_setConnectionRequestHandler(self.slave, self.connectionRequestHandler, None)

        #/* set handler to track connection events (optional) */
        CS104_Slave_setConnectionEventHandler(self.slave, self.connectionEventHandler, None)

        #/* set handler for read request (C_RD_NA_1 - 102) */ 
        CS104_Slave_setReadHandler(self.slave, self.readEventHandler, None)

        self.IOA_list = {}
    #/* Add a new IOA to the list/*
    def addioa(self, number, type = MeasuredValueScaled, data = 0, callback = None, event = False):
        if not number in self.IOA_list:
            self.IOA_list[int(number)] = { 'type': type, 'data': data, 'callback': callback, 'event': event }
            return 0
        else:
            return -1

    # Update the data of the ioa
    def update_data(self):
        for ioa in self.IOA_list:
            if self.IOA_list[ioa]['callback'] != None:
                self.IOA_list[ioa]['callback'](ioa,self.IOA_list[ioa], self)

    # Add a new ASDU to IOA
    def updateioa(self, ioa, data):
        value = int(float(data))
        if value != self.IOA_list[ioa]['data']:
            self.IOA_list[ioa]['data'] = value
            if self.IOA_list[ioa]['event'] == True:
                #Create a new ASDU. The type ID will be derived from the first InformationObject that will be added. 
                newAsdu = CS101_ASDU_create(self.alParams, False, CS101_COT_SPONTANEOUS, 0, 1, False, False)
                if self.IOA_list[ioa]['type'] == MeasuredValueScaled:
                    #Create a new instance of MeasuredValueScaled information object.
                    io = cast(MeasuredValueScaled_create(None, ioa, self.IOA_list[ioa]['data'], IEC60870_QUALITY_GOOD),InformationObject)
                elif self.IOA_list[ioa]['type'] == SinglePointInformation:
                    #Create a new instance of Single point information object.
                    io = cast(SinglePointInformation_create(None, ioa, self.IOA_list[ioa]['data'], IEC60870_QUALITY_GOOD),InformationObject)
                elif self.IOA_list[ioa]['type'] == DoublePointInformation:
                    #Create a new instance of Double point information object.
                    io = cast(DoublePointInformation_create(None, ioa, self.IOA_list[ioa]['data'], IEC60870_QUALITY_GOOD),InformationObject)
                else:
                    return -1
                #add an information object to the ASDU
                CS101_ASDU_addInformationObject(newAsdu, io)
                InformationObject_destroy(io)
                #/* Add ASDU to slave event queue - don't release the ASDU afterwards!
                #Add an ASDU to the low-priority queue of the slave (use for periodic and spontaneous messages)
                CS104_Slave_enqueueASDU(self.slave, newAsdu)
                #Destroy the ASDU object (release all resources)
                CS101_ASDU_destroy(newAsdu)

        return 0
    #Start the server
    def start(self):
        #Start the CS 104 slave. The slave (server) will listen on the configured TCP/IP port.
        CS104_Slave_start(self.slave)

        #Check if slave is running
        if CS104_Slave_isRunning(self.slave) == False:
            print("server failed!\n")
            return -1
        else:
            print('worked')
        return 0

    #Stop the server
    def stop(self):
        #Stop the server
        CS104_Slave_stop(self.slave)
        #Delete the slave instance. Release all resources
        CS104_Slave_destroy(self.slave)
