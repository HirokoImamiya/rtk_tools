from .widget import rtkWidget
from . import dictlib
from . import paramlib

import tkinter as tk
import roslib
import rospy

class rtkCheck(rtkWidget):
  interval=1
  def on_init(self):
    super(rtkCheck,self).on_init()
    dictlib.merge(self.prop,{"format":""})

  def __init__(self,page,prop):
    super(rtkCheck,self).__init__(page,prop)
    self.parse(prop["name"])
    self.check_value=tk.BooleanVar(value = False)
    self.io=tk.Checkbutton(page.frame,command=self.cb_check,variable=self.check_value)
    self.io.grid(row=len(page.widgets),column=1,sticky="nsw")
    self.set_timeout(1)

  def parse(self,str):
    keys=str.split("/")
    self.lb=""
    self.rb=""
    for k in keys:
      if len(k)==0: continue
      self.lb=self.lb+"{'"+k+"':"
      self.rb=self.rb+'}'
  def set(self,value):
    paramlib.set_param(self.prop["name"],value)
    param=eval(self.lb+str(value)+self.rb)
    try:
      dictlib.merge(self.Param,param)
    except:
      pass
  def cb_check(self):
    value=self.check_value.get()
    self.set(value)
  def on_timeout(self):
    try:
      value=paramlib.get_param(self.prop["name"])
      if value!=self.check_value.get():
        self.check_value.set(value)
        self.set(value)
    except:
#      rospy.logwarn("param "+self.prop["name"]+" not found")
      pass
    self.set_timeout(self.interval)
    return
