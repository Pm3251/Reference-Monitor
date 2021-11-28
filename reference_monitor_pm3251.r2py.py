
TYPE="type"
ARGS="args"
RETURN="return"
EXCP="exceptions"
TARGET="target"
FUNC="func"
OBJC="objc"
class ABFile():
  def __init__(self,filename,create):
    # globals
    mycontext['debug'] = False
    # local (per object) reference to the underlying file
    self.Afn = filename+'.a'
    self.Bfn = filename+'.b'
    self.temp_file = filename
    # make the files and add 'SE' to the readat file...
    if create:
      self.Afile = openfile(self.Afn,create)
      self.Bfile = openfile(self.Bfn,create)
      self.Afile.writeat('SE',0)
      self.temp_file = openfile(self.temp_file,create)
    else:
      self.Afile = openfile(self.Afn,True)
      self.Bfile = openfile(self.Bfn,True)
      self.temp_file = openfile(self.temp_file,False)
      read_text = self.temp_file.readat(None,0)
      self.Afile.writeat(read_text,0)
      self.Bfile.writeat(read_text,0)
  def writeat(self,data,offset):
    # Write the requested data to the B file using the sandbox's writeat call
    self.Bfile.writeat(data,offset)
  def readat(self,bytes,offset):
    # Read from the A file using the sandbox's readat...
    return self.Afile.readat(bytes,offset)
  def close(self):
    test_data = self.Bfile.readat(None,0)
    size = len(test_data)
    if(test_data[0] == 'S' and test_data[size-1] == 'E'):
	     self.Afile.writeat(test_data,0)
    else:
	     self.Bfile.close()
	     removefile(self.Bfn)
	     self.Bfile_new = openfile(self.Bfn,True)
	     backup_data = self.Afile.readat(None,0)
	     self.Bfile_new.writeat(backup_data,0)
	     self.Bfile_new.close()
    restore_data = self.Afile.readat(None,0)
    self.temp_file.writeat(restore_data,0)
    self.Afile.close()
    self.temp_file.close()
def ABopenfile(filename, create):
  return ABFile(filename,create)
# The code here sets up type checking and variable hiding for you.  You
# should not need to change anything below here.
sec_file_def = {"obj-type":ABFile,
                "name":"ABFile",
                "writeat":{"type":"func","args":(str,int),"exceptions":Exception,"return":(int,type(None)),"target":ABFile.writeat},
                "readat":{"type":"func","args":((int,type(None)),(int)),"exceptions":Exception,"return":str,"target":ABFile.readat},
                "close":{"type":"func","args":None,"exceptions":None,"return":(bool,type(None)),"target":ABFile.close}
           }
CHILD_CONTEXT_DEF["ABopenfile"] = {TYPE:OBJC,ARGS:(str,bool),EXCP:Exception,RETURN:sec_file_def,TARGET:ABopenfile}
secure_dispatch_module()
