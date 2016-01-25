#!/usr/bin/python
from gi.repository import Gtk,Gdk, GdkPixbuf
import cairo

class picker(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self)
		self.connect('delete-event', Gtk.main_quit)
		self.connect('motion-notify-event', self.motion_cb)
		self.connect('button-press-event',self.button_press)
		box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

		#Setup area for coordinates and zoom window
		coordbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.xcoor=Gtk.Label("x: ")
		coordbox.pack_start(self.xcoor, True, False, 1)
		self.ycoor=Gtk.Label("y: ")
		coordbox.pack_start(self.ycoor, True, False, 1)
		self.zoomwin=Gtk.Image()
		#Trying to draw on Gtk.Image with cairo for crosshairs... Not working
		self.zoomwin.connect('draw', self.draw) 
		self.zoomwin.set_app_paintable(True)
		coordbox.pack_start(self.zoomwin,True,True,1)
		self.buttongo=Gtk.Button("Pick Color")
		self.buttongo.connect('clicked',self.gobutton_activate)
		coordbox.pack_start(self.buttongo,True,True,1)
		box.pack_start(coordbox, True, False, 5)

		#Put in color wheel for tweaking color
		self.cp=Gtk.ColorSelection()
		self.cp.connect('color-changed', self.on_color_changed)
		box.pack_start(self.cp, True, True, 5)
		self.add(box)
		self.show_all()

		#Set some initial parameters
		self.w,self.h=10,10 #Size of zoomed image in pixels
		self.count=0
		self.window=self.get_window()
		#set initial zoom image
		self.zoomwin.set_from_pixbuf(self.get_image().scale_simple(240,240,GdkPixbuf.InterpType.TILES))
		self.grabbing=False

	def on_color_changed(self,widget=None, data=None):
		#Print out x,y to widgets
		display=Gdk.Display.get_default()
		(screen,x,y,modifier)=display.get_pointer()
		self.xcoor.set_text("x: %i" %x)
		self.ycoor.set_text("y: %i" %y)


	def get_image(self,w=None,h=None):
		#Get a pixbuff image under pointer
		if w==None: w=self.w
		if h==None: h=self.h
		display=Gdk.Display.get_default()
		(screen,self.x,self.y,modifier)=display.get_pointer()
		window=Gdk.get_default_root_window()
		screenshot = Gdk.pixbuf_get_from_window(window,
			self.x-int(w/2), self.y-int(h/2), int(w), int(h))
		return screenshot

	def motion_cb(self, widget, data):
		#What to do while mouse pointer is moving
		#DONT capture every event! Causes too much backup
		if self.count==5:
			self.pixbuf=self.get_image().scale_simple(240,240,GdkPixbuf.InterpType.TILES)
			self.zoomwin.set_from_pixbuf(self.pixbuf)
			self.zoomwin.queue_draw()
			self.count=0
		self.count+=1

	def grab_start(self):
		#Grab control of pointer outside of window
		self.grabbing = True
		Gdk.pointer_grab(self.window, 
						True, #allow passage of pointer events to children
						Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.BUTTON_RELEASE_MASK,
						None,
						None,# could put a custom cursor here
						0)

	def button_press(self,widget,data):
		#capture color under the pointer and set the color selection
		cenpx=self.get_image(1,1)
		color=tuple(map(ord, cenpx.get_pixels()[:3]))
		col=Gdk.RGBA(float(color[0])/256.,float(color[1])/256.,float(color[2])/256.)
		self.cp.set_current_rgba(col)

	def grab_stop(self):
		#Stop Grabbing the pointer
		Gdk.pointer_ungrab(0)
		self.grabbing=False     

	def gobutton_activate(self, widget, data=None):
		#Button control
		if self.grabbing==False:
			self.grab_start()
			widget.set_label("Stop Picking")
		else:
			self.grab_stop()
			widget.set_label("Pick Color")

	def draw(self, widget, cr):
		#this gets called, but nothing is drawn that I can see...
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.set_source_rgba(1,1,1,1)
		w = self.w
		h = self.h
		cr.set_source_rgba(1,1,1,1)
		cr.set_line_width(10)
		cr.rectangle(w/2-1,h/2-1,w/2+1,h/2+1)
		cr.stroke()
		cr.set_operator(cairo.OPERATOR_OVER)


if __name__=="__main__":
	win=picker()
	Gtk.main()
