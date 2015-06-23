# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "Ivo"
__date__ = "$Jun 22, 2015 7:09:34 PM$"

import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
import sys
import urlparse

DUMMY_RESPONSE = """
<html>
    <head>
        <title>SabugoCam - WebServer</title>
    </head>
    <body>
        Execution commands success!
    </body>
</html>
"""

STEP_STEPPERMOTOR = 10
LIMIT_STEPPERMOTOR = 500

STEP_SERVOMOTOR = 10
LIMIT_SERVOMOTOR = 360

class HttpHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.execCommands()

    def do_POST(self):
        self.execCommands()

    def execCommands(self):
        # Parse query data & params to find out what was passed
        parsedParams = urlparse.urlparse(self.path)
        queryParsed = urlparse.parse_qs(parsedParams.query)

        if (queryParsed.get('joy')[0] != '0'):
            self.parserCommandJoystick(queryParsed)
        else:
            self.parserCommandTracker(queryParsed)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(DUMMY_RESPONSE))
        self.end_headers()
        self.wfile.write(DUMMY_RESPONSE)

    def parserCommandJoystick(self, query):
        if (query.get('joy')[0] == 'left'):
            #Move Left
            if(query.get('direction')[0] == '6') or (query.get('direction')[0] == '7') or (query.get('direction')[0] == '8'):
                self.stepperMotorMoveLeft()
            #Move Right
            elif(query.get('direction')[0] == '2') or (query.get('direction')[0] == '3') or (query.get('direction')[0] == '4'):
                self.stepperMotorMoveRight()
        elif (query.get('joy')[0] == 'right'):
            #Move Left
            if(query.get('direction')[0] == '6') or (query.get('direction')[0] == '7') or (query.get('direction')[0] == '8'):
                self.servoMotorMoveLeft()
            #Move Right
            elif(query.get('direction')[0] == '2') or (query.get('direction')[0] == '3') or (query.get('direction')[0] == '4'):
                self.servoMotorMoveRight()
            #Move up
            elif(query.get('direction')[0] == '1'):
                self.servoMotorMoveUP()
            #Move down
            elif(query.get('direction')[0] == '5'):
                self.servoMotorMoveDOWN()

    def parserCommandTracker(self, query):
        x = int(query.get('x')[0])
        self.servoMotorMoveX(x)
        y = int(query.get('y')[0])
        self.servoMotorMoveY(y)

    def stepperMotorMoveLeft(self):
        global stepperMotor;
        if(stepperMotor > STEP_STEPPERMOTOR):
            stepperMotor -= STEP_STEPPERMOTOR;
        print 'StepperMotor position = ' + `stepperMotor`
        print 'Mauro - Inserir controle de motor de passo'

    def stepperMotorMoveRight(self):
        global stepperMotor;
        if(stepperMotor < LIMIT_STEPPERMOTOR-STEP_STEPPERMOTOR):
            stepperMotor += STEP_STEPPERMOTOR;
        print 'StepperMotor position = ' + `stepperMotor`
        print 'Mauro - Inserir controle de motor de passo'

    def servoMotorMoveLeft(self):
        global servoMotorX;
        if(servoMotorX > STEP_SERVOMOTOR):
            servoMotorX -= STEP_SERVOMOTOR;
        self.servoMotorMoveX(servoMotorX)

    def servoMotorMoveRight(self):
        global servoMotorX;
        if(servoMotorX < LIMIT_SERVOMOTOR-STEP_SERVOMOTOR):
            servoMotorX += STEP_SERVOMOTOR;
        self.servoMotorMoveX(servoMotorX)

    def servoMotorMoveDOWN(self):
        global servoMotorY;
        if(servoMotorY > STEP_SERVOMOTOR):
            servoMotorY -= STEP_SERVOMOTOR;
        self.servoMotorMoveY(servoMotorY)

    def servoMotorMoveUP(self):
        global servoMotorY;
        if(servoMotorY < LIMIT_SERVOMOTOR-STEP_SERVOMOTOR):
            servoMotorY += STEP_SERVOMOTOR;
        self.servoMotorMoveY(servoMotorY)

    def servoMotorMoveX(self, value):
        global servoMotorX;
        servoMotorX = value;
        print 'ServorMotor X position = ' + `servoMotorX`
        print 'Mauro - Inserir controle do servomotor'

    def servoMotorMoveY(self, value):
        global servoMotorY;
        servoMotorY = value;
        print 'ServorMotor Y position = ' + `servoMotorY`
        print 'Mauro - Inserir controle do servomotor'

class ThreadingSimpleServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

if __name__ == "__main__":
    global servoMotorX;
    global servoMotorY;
    global stepperMotor;
    servoMotorX = 0;
    servoMotorY = 0;
    stepperMotor = 0;

    http_port = 8000
    SocketServer.TCPServer.allow_reuse_address = True
    httpd = ThreadingSimpleServer(("", http_port), HttpHandler)
    print "serving at port %d" % http_port
    sys.stdout.flush()
    httpd.serve_forever()
