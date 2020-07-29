#!/usr/bin/python3

#from bltcrt import *
import bltcrt as crt
import os
import xbox
import xtdf
import xstrings
import lightbars
import pyperclip

chigh = '▓'
clow =  "░"
scrollbar = {"enable":True,"hichar":chigh,"lochar":clow,"hiatt":7,"loatt":8}
avail_at = 7
tdfdir = '.'+crt.pathchar+'tdfs'+crt.pathchar
tdffont = tdfdir + 'ENERGYX.TDF'
availchars = ''
tdfstring = 'test123'
tdfx = 2
tdfy = 5

def copy2clipboard_ascii():
  s = ''
  for y in range(4,23):
    for x in range(80):
      s += crt.gettextat(x,y)
    s += chr(13)
  pyperclip.copy(s)
  
def copy2clipboard_ansi():
  s = ''
  oldat = crt.getattrat(1,4)
  curat = 0
  for y in range(4,23):
    for x in range(80):
      curat = crt.getattrat(x,y)
      if oldat != curat:
        s += ansi_color(curat,oldat)
        oldat = curat
      s += crt.gettextat(x,y)
    s += chr(13)
  pyperclip.copy(s)
 
def setsystemfont(screen):
  global font_hintings
  global font_hinting
  global font_size
  global cell_width
  global cell_height
  global font_index
  global font_name
  global font_files
  crt.blt.set("input.filter={keyboard}")
  while True:
    
    crt.restorescreen(screen)
    crt.refresh()
    key = crt.blt.read()
  
    if key == crt.blt.TK_LEFT and crt.blt.state(crt.blt.TK_CONTROL) and crt.cell_width  > 4:
      crt.cell_width -= 1
      crt.setup_cellsize()
    elif key == crt.blt.TK_RIGHT and crt.blt.state(crt.blt.TK_CONTROL) and crt.cell_width  < 24:
      crt.cell_width += 1
      crt.setup_cellsize()
    elif key == crt.blt.TK_DOWN and crt.blt.state(crt.blt.TK_CONTROL) and crt.cell_height  < 24:
      crt.cell_height += 1
      crt.setup_cellsize()
    elif key == crt.blt.TK_UP and crt.blt.state(crt.blt.TK_CONTROL) and crt.cell_height  > 4:
      crt.cell_height -= 1
      crt.setup_cellsize()
    elif key == crt.blt.TK_EQUALS and crt.blt.state(crt.blt.TK_CONTROL) and crt.font_size  < 64:
      crt.font_size += 1
      crt.font_name = './fonts/'+crt.font_files[crt.font_index]
      crt.setup_font()
    elif key == crt.blt.TK_MINUS and crt.blt.state(crt.blt.TK_CONTROL) and crt.font_size > 4:
      crt.font_size -= 1
      crt.font_name = './fonts/'+crt.font_files[crt.font_index]
      crt.setup_font()
    elif key == crt.blt.TK_TAB:
      crt.font_hinting = (crt.font_hinting + 1) % len(crt.font_hintings)
      crt.font_name = './fonts/'+crt.font_files[crt.font_index]
      crt.setup_font()
    elif (key == crt.blt.TK_F) and (crt.blt.state(crt.blt.TK_CONTROL)): 
      crt.font_index += 1
      if crt.font_index > len(crt.font_files)-1:
        crt.font_index = 0
      crt.font_name = './fonts/'+crt.font_files[crt.font_index]
      crt.setup_font()
    elif key == crt.KEY_CLOSE or key == crt.KEY_ESC:
      break
  crt.savesettings()
  

def ansi_color(Attr,compare=None):
  fg = ['30','34','32','36','31','35','33','37','90','94','92','96','91','95','93','97']
  bg = ['40','44','42','46','41','45','43','47']
  
  f = Attr % 16
  b = Attr // 16
  
  if compare:
    fc = compare % 16
    bc = compare // 16
    if fc != f and bc != b:
      s = chr(27) + '[%s;%sm' % (fg[f],bg[b])
    elif fc != f:
      s = chr(27) + '[%sm' % (fg[f])
    elif bc != b:
      s = chr(27) + '[%sm' % (bg[b])
  else:
    s = chr(27) + '[%s;%sm' % (fg[f],bg[b])
  
  return s
  
def listpallete():
  s = ''
  pal = {1:False,2:False,3:False,4:False,5:False,6:False,7:False,8:False,9:False,
  10:False,11:False,12:False,13:False,14:False,15:False,0:False}
  
  for y in range(4,23):
    for x in range(80):
      fg = crt.getattrat(x,y) % 16
      pal[fg]=True;
      
  for x in range(16):
    if pal[x]:
      s +=' |16|'+str(x).rjust(2,'0')+'ÛÛ|15'+str(x)
  return s
  
def subcolor(orig,dest):
  for y in range(4,23):
    for x in range(80):
      at = crt.getattrat(x,y)
      if at == orig:
        crt.setattrat(x,y,dest)

def savetoansi(filename):
  if filename == '':
    return False
  f=open(filename,'w+', encoding="cp437")
  oldat = 0
  for y in range(4,23):
    for x in range(80):
      attr = crt.getattrat(x,y)
      if oldat != attr:
        f.write(ansi_color(attr,oldat))
      oldat = attr
      f.write(crt.gettextat(x,y))
    f.write(chr(13))
  f.close()


def isinteger(i):
  try:
    i += 1
    return True
  except:
    return False

def cleararea(x1,y1,x2,y2,bg):
  for i in range(y2-y1):
    crt.gotoxy(x1,y1+i)
    crt.write(bg*(x2-x1))
    
def getintbox(x1,y1,x2,y2,title,prompt):
  lightbox(x1,y1,x2,y2,xbox.box2,True)
  crt.writexy(x1+2,y1,15,title)
  crt.writexy(x1+2,y1+2,11,prompt)
  txt = 'a'
  crt.settextattr(14)
  while True:
    res, txt = crt.blt.read_str(x1+8,y1+1, '', 2)
    try:
      a = int(txt)
      if a < 70:
        return a
    except:
      pass
      
def getyesnobox(title,prompt):
  lightbox(30,10,50,15,xbox.box2,True)
  crt.writexy(32,10,15,title)
  crt.writexy(32,12,11,prompt)
  mmenu = ['Yes','No']
  index = 1
  key, index, dx = lightbars.hmenu(mmenu,36,13,7,15+16,index)
  if key == crt.KEY_RETURN:
    if index == 0:
      return True
    else:
      return False

def getstrbox(x1,y1,x2,y2,title,prompt):
  lightbox(x1,y1,x2,y2,xbox.box2,True)
  crt.writexy(x1+2,y1,15,title)
  crt.writexy(x1+2,y1+2,11,prompt)
  txt = ''
  crt.settextattr(14)
  res, txt = crt.blt.read_str(x1+8,y1+1, '', 20)
  return txt
      
def menulist(items,x1,y1,x2,y2,hc=15,nc=7,sel=0,sb=scrollbar):
    def updatebar():
        if sb["enable"] == False: return
        for i in range(0,y2-y1+1):
            crt.writexy(x2,y1+i,sb["loatt"],sb["lochar"])
        if len(items) < 2:
            y = 0
        else:
            y = (selbar * (y2-y1)) // (len(items)-1)
        crt.writexy(x2,y1+y,sb["hiatt"],sb["hichar"])
    
    if len(items)<1:
      return -1
    exit_code = ""
    key = ""
    value = -1
    done = False
    if sel <= len(items):
        top = sel-(y2-y1)
        if top < 1: top = 0
    else:
        top = 0
    if sel <= len(items):
        selbar = sel
    else:
        selbar = 0
    
    while done == False:
        crt.gotoxy(x1,y1)
        y = top
        while y1+y-top<=y2:
            if y<len(items):
                crt.writexy(x1,y1+y-top,nc,items[y].ljust(x2-x1, " ")[:x2-x1])
            else:
                crt.writexy(x1,y1+y-top,nc," ".ljust(x2-x1, " ")[:x2-x1])
            y += 1
        crt.writexy(x1,y1+selbar-top,hc,items[selbar].ljust(x2-x1, " ")[:x2-x1])
        #crt.writexy(3,23,7,items[selbar].ljust(75," "))
        updatebar()
        crt.gotoxy(1,25)
        
        key = crt.readkey()
        if key == crt.KEY_UP:
            selbar=selbar-1
            if selbar < 1:
                selbar = 0
            if selbar < top:
                top = selbar
        elif key == crt.KEY_PGUP:
            selbar = selbar - (y2-y1)
            if selbar < 0:
                selbar = 0
                top = 0
            else:
                top = top - (y2-y1)
                if top < 0:
                    top = 0
        elif key == crt.KEY_PGDN:
            selbar = selbar+(y2-y1)
            if selbar > len(items)-1:
                selbar = len(items)-1
            top = top+(y2-y1)
            if top > len(items)-1-(y2-y1):
                top = len(items)-1-(y2-y1)
                if top < 0:
                    top = 0
        elif key == crt.KEY_END:
            selbar=len(items)-1
            if len(items)-(y2-y1)-1 > 0:
                top = len(items)-(y2-y1)-1
            else:
                top = 0
        elif key == crt.KEY_HOME:
            selbar=0
            top = 0
        elif key == crt.KEY_DOWN: 
            selbar=selbar+1
            if selbar > len(items)-1:
                selbar = len(items)-1
            if selbar > top+y2-y1:
                top += 1
        elif key == crt.KEY_ENTER:
            value = selbar
            exit_code = crt.KEY_ENTER
            done = True
        elif key in exit_keys:
            exit_code = key
            value = selbar
            done = True
    return value, exit_code
    
def listfonts(fd):
  global availchars
  oldavailchars = availchars
  
  def updatebar():
    if sb["enable"] == False: return
    for i in range(0,y2-y1+1):
      crt.writexy(x2,y1+i,sb["loatt"],sb["lochar"])
    if len(items) < 2:
      y = 0
    else:
      y = (selbar * (y2-y1)) // (len(items)-1)
    crt.writexy(x2,y1+y,sb["hiatt"],sb["hichar"])
    
  
  
  #get files
  items = []
  for currentpath, folders, files in os.walk(fd):
    for fl in files:
      afile = {}
      afile['name']=fl
      afile['path']=currentpath
      items.append(afile)
      
      
  top = 0
  selbar = 0
  x1 = 3
  y1 = 5
  x2 = 20
  y2 = 20
  nc = 7
  hc = 30
  sb = scrollbar
  ss = ''
  
  def searchnext(index):
    if index >= len(items)-1:
      st = 0
    else:
      st = index+1
    
    while st < len(items)-1:
      if ss in items[st]['name'].lower():
        return True,st
        break
      st += 1
    return False,-1
  
  
  oldfont = xtdf.fontfile
  oldsel  = xtdf.selected
  
  done = False
  
  while done == False:
    lightbox(1,4,80,21,xbox.box2)
    crt.gotoxy(x1,y1)
    y = top
    while y1+y-top<=y2:
      if y<len(items):
        crt.writexy(x1,y1+y-top,nc,items[y]['name'].ljust(x2-x1, " ")[:x2-x1])
      else:
        crt.writexy(x1,y1+y-top,nc," ".ljust(x2-x1, " ")[:x2-x1])
      y += 1
    crt.writexy(x1,y1+selbar-top,hc,items[selbar]['name'].ljust(x2-x1, " ")[:x2-x1])
    crt.writexypipe(3,4,7,40,'Dir.: |15'+items[selbar]['path'])
    
    crt.writexy(3,21,15,ss.ljust(11,' '))
    crt.writexy(3+len(ss),21,1,'.'*(10-len(ss)+1))
    
    if xtdf.istdf(items[selbar]['path']+crt.pathchar+items[selbar]['name']):
      xtdf.init(items[selbar]['path']+crt.pathchar+items[selbar]['name'])
      crt.writexypipe(30,4,7,30,'Name: |15'+xtdf.fonts[0]['name'].rstrip('\x00'))
      crt.writexypipe(60,4,7,20,'Has: |15'+str(xtdf.total)+' |07fonts')
      crt.settextattr(7)
      cleararea(22,5,80,20,' ')
      xtdf.writestr(22,5,'abc123')
      
      availchars=xtdf.availablechars()
      crt.writexy(15+1,23,avail_at,'chars: '+availchars[:44])
      crt.writexy(15+2,24,avail_at,availchars[45:])
      
      
    #crt.writexy(3,23,7,items[selbar].ljust(75," "))
    updatebar()
    crt.gotoxy(1,25)
    
    key = crt.readkey()
    if key == crt.KEY_UP:
      selbar=selbar-1
      if selbar < 1:
        selbar = 0
      if selbar < top:
        top = selbar
    elif key == crt.KEY_PGUP:
      selbar = selbar - (y2-y1)
      if selbar < 0:
        selbar = 0
        top = 0
      else:
        top = top - (y2-y1)
        if top < 0:
          top = 0
    elif key == crt.KEY_PGDN:
      selbar = selbar+(y2-y1)
      if selbar > len(items)-1:
        selbar = len(items)-1
      top = top+(y2-y1)
      if top > len(items)-1-(y2-y1):
        top = len(items)-1-(y2-y1)
        if top < 0:
          top = 0
    elif key == crt.KEY_END:
      selbar=len(items)-1
      if len(items)-(y2-y1)-1 > 0:
        top = len(items)-(y2-y1)-1
      else:
        top = 0
    elif key == crt.KEY_HOME:
      selbar=0
      top = 0
    elif key == crt.KEY_DOWN: 
      selbar=selbar+1
      if selbar > len(items)-1:
        selbar = len(items)-1
      if selbar > top+y2-y1:
        top += 1
    elif key == crt.KEY_RETURN:
      value = selbar
      exit_code = crt.KEY_RETURN
      if xtdf.istdf(items[selbar]['path']+crt.pathchar+items[selbar]['name']):
        xtdf.init(items[selbar]['path']+crt.pathchar+items[selbar]['name'])
        availchars = xtdf.availablechars()
      done = True
    elif key == crt.KEY_ESC:
      if xtdf.istdf(oldfont):
        xtdf.init(oldfont)
        xtdf.selected = oldsel
      availchars = oldavailchars
      done = True
    elif key == crt.KEY_D and crt.state(crt.KEY_CONTROL):
      if getyesnobox('Delete file','Are you sure?'):
        os.remove(items[selbar]['path']+crt.pathchar+items[selbar]['name'])
        items.clear()
        for currentpath, folders, files in os.walk(fd):
          for fl in files:
            afile = {}
            afile['name']=fl
            afile['path']=currentpath
            items.append(afile)
        selbar = 0
        topbar = 0        
    elif key == crt.KEY_A and crt.state(crt.KEY_CONTROL):
      r,s = searchnext(selbar)
      if r:
        selbar = s
        top = s
    elif key == crt.KEY_Y and crt.state(crt.KEY_CONTROL):
      ss = ''
    elif crt.KEY_A <= key <= crt.KEY_Z:
      if len(ss) <=10:
        ss += chr(key+61)
        ss = ss.lower()
        r,s = searchnext(selbar)
        if r:
          selbar = s
          top = s
    elif crt.KEY_1 <= key <= crt.KEY_0:
      if len(ss) <=10:
        ss += chr(key+19)
        ss = ss.lower()
        r,s = searchnext(selbar)
        if r:
          selbar = s
          top = s
    elif key == crt.KEY_BACKSPACE:
      ss = ss[:-1]
      
    
  
      

def loadtdf(filename):
  global availchars
  global tdfx, tdfy, tdfstring
  if not xtdf.istdf(filename): return False
  xtdf.init(filename)
  availchars = xtdf.availablechars()
  crt.settextattr(7)
  xtdf.writestr(tdfx,tdfy,tdfstring)
  return True

def statusbar():
  crt.writexy(1,25,3*16,' '*80)
  crt.writexy(1,25,3*16,'file:'+xtdf.fontfile[-15:])
  crt.writexy(23,25,3*16,u'│'+' name:'+xtdf.fonts[xtdf.selected]['name'])
  crt.writexy(45,25,3*16,u'│'+' no:'+str(xtdf.selected+1)+'/'+str(xtdf.total))
  crt.writexy(56,25,3*16,u'│'+' spacing:'+str(xtdf.fonts[xtdf.selected]['spacing']))
  crt.writexy(68,25,3*16,u'│'+' type:'+xtdf.fonts[xtdf.selected]['type'])

def shadowbox(x1,y1,x2,y2,at):
  for i in range(x1+1,x2+1):
    crt.setattrat(i,y2+1,at)
  for i in range(y1+1,y2+2):
    crt.setattrat(x2+1,i,at)
    
      
def lightbox(x1,y1,x2,y2,box,shadow=False):
  crt.settextattr(1)
  xbox.ansibox(x1,y1,x2,y2,box)
  crt.setattrat(x1,y1,15)
  crt.setattrat(x2,y2,11)
  if shadow:
    shadowbox(x1,y1,x2,y2,8)
    
def msgbox(title,text):
  l = len(text) // 2
  lightbox(40-l-2,10,40+l+2,14,xbox.box2,True)
  crt.writexy(40-l,10,15,title)
  crt.writexy(40-l,12,11,text)
  crt.writexy(40-11,14,1,' press a key to continue ')
  crt.readkey()

def mainscreen():
  global tdfx, tdfy, tdfstring
  global colorpallete
  global color_pal
  
  
  def refreshtext():
    crt.settextattr(7)
    cleararea(1,4,80,25,' ')
    xtdf.writestr(tdfx,tdfy,tdfstring)
    statusbar()
    crt.refresh()
    
  crt.textcolor(1)
  lightbox(1,1,80,3,xbox.box2)
  crt.writexypipe(3,2,7,70,'|15F|07ile    |15S|07creen    |15H|07elp    |15Q|07uit')
  
  mmenu = ['Next','Previous','Font','Screen','Help','Quit']
  index = 0
  if not loadtdf(tdffont):
    crt.writexy(2,5,1,'Font is not valid! Use another one.')
  statusbar()
  while True:
    crt.writexy(15+1,23,avail_at,'chars: '+availchars[:44])
    crt.writexy(15+2,24,avail_at,availchars[45:])
    
    key, index, dx = lightbars.hmenu(mmenu,3,2,11,15+16,index)
    
    if key == crt.KEY_RETURN or key == crt.KEY_DOWN:
      crt.settextattr(1)
      if index == 0:
        xtdf.selected += 1
        if xtdf.selected > xtdf.total-1:
          xtdf.selected = 0
        refreshtext()
      elif index == 1:
        xtdf.selected -= 1
        if xtdf.selected < 0:
          xtdf.selected = xtdf.total - 1
        refreshtext()
      elif index == 2:
        screen1 = crt.savescreen()
        lightbox(3+dx,4,3+dx+10,10,xbox.box4,True)
        file_menu = [' Open    ',' Export  ',' Text    ',' Spacing ',' Pallete ']
        k,i = lightbars.vmenu(file_menu,3+dx+1,5,11,31,0)
        if k == crt.KEY_RETURN:
          if i == 0:
            listfonts(tdfdir)
          elif i == 1:
            name = getstrbox(30,10,50,15,'Export to:','File:')
            if name !='':
              name.replace(' ','_')
              name.replace('.','_')
              xtdf.extractfont(tdfdir+name+'.tdf')
          elif i == 2: #text
            tdfstring = getstrbox(30,10,50,14,'Change Text','String:')
            if tdfstring == '': tdfstring = 'abc123'
          elif i == 3: #spacing
            v = getintbox(30,10,50,14,'Font Spacing','Value:')
            if v<10:
              xtdf.fonts[xtdf.selected]['spacing']=v
          elif i ==4:
            crt.restorescreen(screen1)
            s=listpallete()
            lightbox(5,10,75,14,xbox.box2,True)
            crt.writexy(7,10,15,' Used colors ')
            crt.writexypipe(7,12,7,60,s)
            crt.writexy(28,14,1,' press a key to continue ')
            crt.readkey()
        crt.restorescreen(screen1)
        refreshtext()
      elif index == 3:
        screen1 = crt.savescreen()
        lightbox(3+dx,4,3+dx+23,11,xbox.box4,True)
        screen_menu = [' X Position'.ljust(22,' '),' Y Position'.ljust(22,' '),' Save Image as ANSI'.ljust(22,' '),' Copy Clipboard ASCII ',' Copy Clipboard ANSI  ',' System Font'.ljust(22,' ')]
        k,i = lightbars.vmenu(screen_menu,3+dx+1,5,11,31,0)
        from bltcrt import colorpallete, color_pal
        if k == crt.KEY_RETURN:
          if i == 0:
            v = getintbox(30,10,50,14,'Change X Pos.','Value:')
            if v:
              tdfx = int(v)
          elif i == 1:
            v = getintbox(30,10,50,14,'Change Y Pos.','Value:')
            if v>3:
              tdfy = int(v)
          elif i == 2:
            fn = getstrbox(30,10,50,14,'Save Image','Name:')
            if fn != '':
              fn.replace(' ','_')
              fn.replace('.','_')
              crt.restorescreen(screen1)
              savetoansi(fn+'.ans')
          elif i == 3:
            crt.restorescreen(screen1)
            copy2clipboard_ascii()
            msgbox('Info','Text copied to clipboard.')
          elif i == 4:
            crt.restorescreen(screen1)
            copy2clipboard_ansi()
            msgbox('Info','Text copied to clipboard.')
          elif i == 5:
            crt.settextattr(7)
            cleararea(1,4,80,25,' ')
            crt.writexy(3,5,15,'Use these key combinations to change font and window settings.')
            crt.writexypipe(5,7,11,60,'CTRL + Up   |07: Decrease cell height')
            crt.writexypipe(5,8,11,60,'CTRL + Down |07: Increase cell height')
            crt.writexypipe(5,9,11,60,'CTRL + Left |07: Decrease cell width ')
            crt.writexypipe(5,10,11,60,'CTRL + -    |07: Decrease font size ')
            crt.writexypipe(5,11,11,60,'CTRL + =    |07: Increase font size ')
            crt.writexypipe(5,12,11,60,'CTRL + F    |07: Cycle font files')
            crt.writexypipe(5,13,11,60,'            |07  from the ./fonts dir.')
            crt.writexypipe(5,14,11,60,'TAB         |07: Font hinting')
            crt.writexy(15,20,7,'Press ESC when ready to apply settings...')
            xd=crt.savescreen()
            setsystemfont(xd)
            
        crt.restorescreen(screen1)
        refreshtext()
      elif index == 4:
        screen1 = crt.savescreen()
        lightbox(3+dx,4,3+dx+12,7,xbox.box4,True)
        help_menu = [' Shortcuts ',' About     ']
        k, i = lightbars.vmenu(help_menu,3+dx+1,5,11,31,0)
        if k == crt.KEY_RETURN:
          if i == 0:
            crt.settextattr(7)
            cleararea(1,4,80,25,' ')
            crt.writexy(3,5,15,'Keyboard Shortcuts')
            crt.writexy(5,10,7,'None for the time being. I had to find a way to fill those menus :)')
            crt.writexy(26,20,7,'press any key to continue...')
            crt.readkey()
          if i == 1:
            crt.settextattr(7)
            cleararea(1,4,80,25,' ')
            crt.writexy(3,5,15,'TDF Studio v2.0')
            crt.writexy(5,7,7,'This is a program to use TDF font files. You can export a font file')
            crt.writexy(5,8,7,'from a set file, save text to an ANSI image or copy it to the      ')
            crt.writexy(5,9,7,'clipboard.                                                         ')
            
            crt.writexy(5,17,7,'made by XQTR of Another Droid BBS // telnet: andr01d.zapto.org:9999')
            crt.writexy(26,20,7,'press any key to continue...')
            crt.readkey()
            
        crt.restorescreen(screen1)
      elif index == 5:
        screen1 = crt.savescreen()
        lightbox(3+dx,4,3+dx+6,7,xbox.box4,True)
        quit_menu = [' No  ',' Yes ']
        k,i = lightbars.vmenu(quit_menu,3+dx+1,5,11,31,0)
        if k == crt.KEY_RETURN:
          if i == 1:
            break
        crt.restorescreen(screen1)
    elif key == crt.KEY_ESC:
      dx = 46
      screen1 = crt.savescreen()
      lightbox(3+dx,4,3+dx+6,7,xbox.box4,True)
      quit_menu = [' No  ',' Yes ']
      k,i = lightbars.vmenu(quit_menu,3+dx+1,5,11,31,0)
      if k == crt.KEY_RETURN:
        if i == 1:
          break
        
      crt.restorescreen(screen1)
      
# Main Block
crt.loadsettings()
crt.init()
crt.windowtitle('TDF Studio v2.0')
mainscreen()
crt.shutdown()
#crt.savesettings()

