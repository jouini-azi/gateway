from lib60870 import *
import time

class IEC60870_5_104_client:
  """
  This Class will represent the client side of the protocol IEC60870
  """
  def connectionHandler (self, parameter, connection, event):
    """
    connectionHandler(self , parameter , connection , event)
    Show the Connection event
    
    :param event: event type between  client and  server

    :type parameter:void

    :param parameter: user provided parameter
    
    :param connection: the connection object
    """
    if event == CS104_CONNECTION_OPENED:
          print("Connection established")
    elif event == CS104_CONNECTION_CLOSED:
          print("Connection closed")
    elif event == CS104_CONNECTION_STARTDT_CON_RECEIVED:
          print("Received STARTDT_CON")
    elif event == CS104_CONNECTION_STOPDT_CON_RECEIVED:
          print("Received STOPDT_CON")


  # CS101_ASDUReceivedHandler implementation
  # For CS104 the address parameter has to be ignored
  def asduReceivedHandler (self, parameter, address, asdu):
    """
    asduReceivedHandler(self , parameter , address ,asdu)
    Display the type of ASDU and IOA and the value related to it.
    
    :type parameter : void

    :param parameter : user provided parameter

    :type address : int

    :param address : adress of the sender station , it is undefined for CS104 , the adresse will always be -1


    :param asdu : Apllication Service Data unit
    """
    print("RECVD ASDU type: %s(%i) elements: %i" % (
            TypeID_toString(CS101_ASDU_getTypeID(asdu)),
            CS101_ASDU_getTypeID(asdu),
            CS101_ASDU_getNumberOfElements(asdu)))
    # Get the type ID of the ASDU
    if (CS101_ASDU_getTypeID(asdu) == M_ME_TE_1):

        print("  measured scaled values with CP56Time2a timestamp:")
        # Get the number of information objects (elements) in the ASDU
        for i in range(CS101_ASDU_getNumberOfElements(asdu)):
            # CS101_ASDU_getElement = Get the information object with the given index
            io = cast(CS101_ASDU_getElement(asdu, i), MeasuredValueScaledWithCP56Time2a) 
            print("    IOA: %i value: %i" % (
                    InformationObject_getObjectAddress(cast(io, InformationObject) ),
                    MeasuredValueScaled_getValue(cast(io, MeasuredValueScaled) )
            ))
            MeasuredValueScaledWithCP56Time2a_destroy(io)
    # Get the type ID of the ASDU
    elif (CS101_ASDU_getTypeID(asdu) == M_SP_NA_1):
        print("  single point information:")
        # Get the number of information objects (elements) in the ASDU
        for i in range(CS101_ASDU_getNumberOfElements(asdu)):
            # Get the information object with the given index
            io = cast(CS101_ASDU_getElement(asdu, i), SinglePointInformation) 
            print("    IOA: %i value: %i" % (
                    InformationObject_getObjectAddress(cast(io,InformationObject) ),
                    SinglePointInformation_getValue(cast(io,SinglePointInformation) )
            ))
            SinglePointInformation_destroy(io)
    # Get the type ID of the ASDU
    elif (CS101_ASDU_getTypeID(asdu) == M_DP_NA_1):
        print("  double point information:")
        # Get the number of information objects (elements) in the ASDU
        for i in range(CS101_ASDU_getNumberOfElements(asdu)):
            # Get the information object with the given index
            io = cast(CS101_ASDU_getElement(asdu, i), DoublePointInformation) 
            print("    IOA: %i value: %i" % (
                    InformationObject_getObjectAddress(cast(io,InformationObject) ),
                    DoublePointInformation_getValue(cast(io,DoublePointInformation) )
            ))
            DoublePointInformation_destroy(io)
    # Get the type ID of the ASDU       
    elif (CS101_ASDU_getTypeID(asdu) == M_ME_NB_1):
        print("  measured value scaled:")
        # Get the number of information objects (elements) in the ASDU
        for i in range(CS101_ASDU_getNumberOfElements(asdu)):
            # CS101_ASDU_getElement = Get the information object with the given index
            io = cast(CS101_ASDU_getElement(asdu, i), MeasuredValueScaled) 
            print("    IOA: %i value: %i" % (
                    InformationObject_getObjectAddress(cast(io,InformationObject) ),
                    MeasuredValueScaled_getValue(cast(io,MeasuredValueScaled) )
            ))
            MeasuredValueScaled_destroy(io)
    # Get the type ID of the ASDU   
    elif (CS101_ASDU_getTypeID(asdu) == C_SC_NA_1):
        print("received single command response")
        # Get the number of information objects (elements) in the ASDU
        for i in range(CS101_ASDU_getNumberOfElements(asdu)):
            # Get the information object with the given index
            io = cast(CS101_ASDU_getElement(asdu, i), SinglePointInformation) 
            print("    IOA: %i value: %i" % (
                    InformationObject_getObjectAddress(cast(io,InformationObject) ),
                    SinglePointInformation_getValue(cast(io,SinglePointInformation) )
            ))
            SinglePointInformation_destroy(io)
    # Get the type ID of the ASDU   
    elif (CS101_ASDU_getTypeID(asdu) == C_DC_NA_1):
        print("received double command response")
        # Get the number of information objects (elements) in the ASDU
        for i in range(CS101_ASDU_getNumberOfElements(asdu)):
            # Get the information object with the given index  
            io = cast(CS101_ASDU_getElement(asdu, i), DoublePointInformation) 
            print("    IOA: %i value: %i" % (
                    InformationObject_getObjectAddress(cast(io,InformationObject) ),
                    DoublePointInformation_getValue(cast(io,DoublePointInformation) )
            ))
            DoublePointInformation_destroy(io)

    return True


  def __init__(self, ip = 'localhost', port = IEC_60870_5_104_DEFAULT_PORT):
    print("Connecting to: %s:%i" % ( ip, port))

    self.con = CS104_Connection_create(ip, port)
    """
    CS104_Connection_create(ip, port)
    
    Create a new connection object

    :type ip : char

    :param ip : host name of IP address of the server to connect

    :type port : int

    :param port : tcp port of the server to connect
    """

    self.p_connectionHandler =  CS104_ConnectionHandler(self.connectionHandler)
    """
    CS104_ConnectionHandler(parameter, connection , event)
    Handler that is called when the connection is established or closed
    
    :type parameter : void

    :param parameter : user provided parameter
    
    :type connection : CS104_Connection

    :param connection : adress of the sender station , it is undefined for CS104 , the adresse will always be -1
    
    :type event : CS104_ConnectionEvent

    :param event : Apllication Service Data unit
    """
    self.p_asduReceivedHandler = CS101_ASDUReceivedHandler(self.asduReceivedHandler)
    """
    CS101_ASDUReceivedHandler(parameter, address , asdu)
    
    Callback handler for received ASDUs

    :type parameter : void

    :param parameter : user provided parameter

    :type address : int

    :param address : adress of the sender station , it is undefined for CS104 so the adresse will always be -1

    :type asdu : CS101_ASDU

    :param asdu : Apllication Service Data unit

    """

    CS104_Connection_setConnectionHandler(self.con, self.p_connectionHandler, None)
    """
    CS104_Connection_setConnectionHandler(self,CS104_ConnectionHandler , parameter)

    Set the connection event handler

    :type CS104_ConnectionHandler: CS104_ConnectionHandler

    :param CS104_ConnectionHandler : user provided callback handler function

    :type parameter : void

    :param parameter : user provided parameter that is passed to the callback handler
    """

    CS104_Connection_setASDUReceivedHandler(self.con, self.p_asduReceivedHandler, None)
    """
    CS104_Connection_setASDUReceivedHandler(self , p_asduReceivedHandler , parameter)

    Register a callback handler for received ASDUs

    :type self : CS104_Connection

    :param self : connexion

    :type p_asduReceivedHandler : CS101_ASDUReceivedHandler

    :param p_asduReceivedHandler : 'mezlt nchouf
    
    :type parameter : void

    :param parameter : user provided parameter that is passed to the callback handler
    """
  def start(self):
    """
    CS104_Connection_connect(self.con)

    Establishes a connection to a server

    :param self.con : bool

    :return : true when connected, false otherwise
    """
    if (CS104_Connection_connect(self.con)):
        print("Connected!")

        
        CS104_Connection_sendStartDT(self.con)
        """"
        CS104_Connection_sendStartDT(self.con)
        start data transmission on this connection

        *After issuing this command the client (master)
        will receive spontaneous (unsolicited) messages from the server (slave).

        :type self.con : CS104_Connection

        """
        time.sleep( 2 )
        newTime = sCP56Time2a()

        CP56Time2a_createFromMsTimestamp(CP56Time2a(newTime), Hal_getTimeInMs())
        """
        CP56Time2a_createFromMsTimestamp(CP56Time2a(newTime) , Hal_getTimeInMs)
        Create a 7 byte time from a UTC ms timestamp

        :param CP56Time2a :DateTime time

        """
        print("Send time sync command")

        CS104_Connection_sendClockSyncCommand(self.con, 1, CP56Time2a(newTime))
        """"
        CS104_Connection_sendClockSyncCommand(self.con, ca , CP56Time2a(newTime))
        Sends a clock synchronization command (C_CS_NA_1 typeID: 103) 
        
        :type con :CS104_Connection

        :param con :

        :type ca : int

        :param ca : Common address of the slave/server

        :type CP56Time2a : sCP56Time2a

        :param CP56Time2a : new system time for the slave/server
        """

        CS104_Connection_sendInterrogationCommand(self.con, CS101_COT_ACTIVATION, 1, IEC60870_QOI_STATION)
        """
        CS104_Connection_sendInterrogationCommand(self.con , CS101_COT_ACTIVATION , ca , IEC60870_QOI_STATION)
        send an interrogation command
        
        :type con :CS104_Connection

        :param con : connexion

        :type CS101_COT_ACTIVATION : enum

        :param CS101_COT_ACTIVATION :  =6

        :type ca : int

        :param ca : Common address of the slave/server

        :type IEC60870_QOI_STATION : Macros

        :param  IEC60870_QOI_STATION : =20


        :return : true if message was sent, false otherwise

        """
        time.sleep( 2 )

        sc = cast(SingleCommand_create(None, 100, 1, True, 7), InformationObject)
        """"
        SingleCommand_create(self , ioa , command , selectcommand , qu)
        Create a single point command information object. 

        :type self : SingleCommand

        :param self : existing instance to reuse or NULL to create a new instance

        :type ioa :int

        :param ioa : information object address 

        :type command : bool

        :param command : the command value

        :type selectcommand : bool

        :param selectcommand :	(S/E bit) if true send "select", otherwise "execute" 

        :type qu : int

        :param qu : qualifier of command QU parameter
        (0 = no additional definition, 1 = short pulse, 2 = long pulse, 3 = persistent output)
        """
        print("Send single control command")

        CS104_Connection_sendProcessCommandEx(self.con, CS101_COT_ACTIVATION, 7, sc)
        """"
        CS104_Connection_sendProcessCommandEx(self.con , cot , ca ,sc)
        Send a process command to the controlled (or other) station

        :type con : CS104_Connection

        :param con : connexion

        :type cot : CS101_CauseOfTransmission

        :param cot : the cause of transmission
        (should be ACTIVATION to select/execute or ACT_TERM to cancel the command)

        :type ca : int

        :param ca : the common address of the information object

        :type sc : InformationObject

        :param sc : the command information object (e.g. SingleCommand or DoubleCommand)
        """

        InformationObject_destroy(sc)
        """
        InformationObject_destroy(sc)
        Destroy object - free all related resources

        :type sc : InformationObject

        :param sc : the command information object (e.g. SingleCommand or DoubleCommand)
        """
        time.sleep( 1 )

        CS104_Connection_sendStopDT(self.con)
        """
        CS104_Connection_sendStopDT(self.con)
        stop data transmission on this connection
        
        :type con : CS104_Connection

        :param con : connexion

        """
    else:
        print("Connect failed!")

    print("exit")
#test the class
if __name__== "__main__":
  client = IEC60870_5_104_client()
  client.start()
