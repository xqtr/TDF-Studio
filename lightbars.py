

from bltcrt import *

def vmenu(items,x,y,at,at_sel,index):
  if len(items) == 0: return
  while True:
    for i in range(len(items)):
      writexy(x,y+i,at,items[i])
    writexy(x,y+index,at_sel,items[index])
    c = readkey()
    if c == KEY_LEFT:
      return c, index
    elif c == KEY_RIGHT:
      return c, index
    elif c == KEY_ESC:
      return c, index
    elif c == KEY_UP:
      index -= 1
      if index < 0: index = len(items)-1
    elif c == KEY_DOWN:
      index += 1
      if index > len(items)-1: index = 0
    elif c == KEY_END:
      index = len(items)-1
    elif c == KEY_HOME:
      index = 0
    elif c == KEY_RETURN or c == KEY_KPENTER:
      return KEY_RETURN, index
    

def hmenu(items,x,y,at,at_sel,index,ident=4):
  def getitemx(i):
    s = ''
    for z in range(i):
      s += ' '+items[z]+' '*(ident-1)
    return len(s)
      
  if len(items) == 0: return
  
  gotoxy(x,y)
  settextattr(at)
  
  #index = 0
  
  while True:
    gotoxy(x,y)
    settextattr(at)
    for i in items:
      write(' '+i+' '*(ident-1))
    writexy(x+getitemx(index),y,at_sel,' '+items[index]+' ')
    c = readkey()
    if c == KEY_LEFT:
      index -= 1
      if index < 0: index = len(items)-1
    elif c == KEY_RIGHT:
      index +=1
      if index >= len(items): index = 0
    elif c == KEY_ESC:
      return c, index, getitemx(index)
    elif c == KEY_UP:
      return c, index, getitemx(index)
    elif c == KEY_DOWN:
      return c, index, getitemx(index)
    elif c == KEY_END:
      index = len(items)-1
    elif c == KEY_HOME:
      index = 0
    elif c == KEY_RETURN or c == KEY_KPENTER:
      return KEY_RETURN, index, getitemx(index)
    
    
    
