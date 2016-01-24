#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# splashscreen.py
#
# Copyright (C) 2012 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#

from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import Gdk
from gi.repository import GdkPixbuf
import cairo
import time
import os
import math

from comun import _
		
class Capturer(Gtk.Window):     
	def __init__(self,zoom):
		Gtk.Window.__init__(self,type=Gtk.WindowType.TOPLEVEL)
		self.set_keep_above(True)
		#self.set_skip_taskbar_hint(True) # Not show in taskbar
		#self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
		#self.set_icon_from_file(comun.ICON)		
		self.set_decorated(False)
		self.set_app_paintable(True)
		self.add_events(Gdk.EventMask.ALL_EVENTS_MASK)
		self.connect('draw', self.on_expose, None)
		self.connect("button-release-event", self.release)
		self.connect("motion-notify-event", self.mousemove)		
		#
		screen = self.get_screen()
		visual = screen.get_rgba_visual()
		if visual and screen.is_composited():
			self.set_visual(visual)
		self.zoom = zoom
		self.pb = None
		self.fullscreen()
		self.show_all()

	def release(self, widget, event):
		self.drag =  False
		self.destroy()
		
	def mousemove(self,widget,event):
		pointer,x,y,mods = self.get_screen().get_root_window().get_pointer()
		print(get_pixel_colour(x, y))
		w = Gdk.get_default_root_window()
		width = w.get_width()
		height = w.get_height()		
		pb = Gdk.pixbuf_get_from_window(w, x-100,y-100, 200, 200)
		if self.zoom>1:
			npb = GdkPixbuf.Pixbuf.scale_simple(pb,200*self.zoom,200*self.zoom, GdkPixbuf.InterpType.BILINEAR)
			#npb = GdkPixbuf.Pixbuf.scale_simple(pb,150*self.zoom,150*self.zoom, GdkPixbuf.InterpType.HYPER)
			width = npb.get_width()
			height = npb.get_height()
			npb.copy_area(width/2-100, height/2-100, 200, 200, pb, 0,0)
		self.pb = pb

	def on_expose(self, widget, cr, data):
		cr.save()
		cr.set_operator(cairo.OPERATOR_CLEAR)
		cr.rectangle(0.0, 0.0, *widget.get_size())
		cr.fill()
		cr.restore()

def get_surface_from_file(filename):
	if os.path.exists(filename):
		pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
		if pixbuf:		
			surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, pixbuf.get_width(),pixbuf.get_height())
			context = cairo.Context(surface)
			Gdk.cairo_set_source_pixbuf(context, pixbuf,0,0)
			context.paint()
			return surface
	return None
	
def get_pixel_colour(i_x, i_y):
	w = Gdk.get_default_root_window()
	pb = Gdk.pixbuf_get_from_window(w, i_x, i_y, 1, 1)
	return get_array_of_colors(pb)

def get_array_of_colors(pixbuf):
	colors = []
	alist = pixbuf.get_pixels()
	if pixbuf.get_has_alpha():
		rows = 4
	else:
		rows = 3
	for cont in range(0,len(alist),rows):
		color=tuple(alist[cont:cont+rows])
		colors.append(color)
	return colors	

if __name__ == "__main__":
    ss = WeatherWidget()
    ss.show()
    ss2 = WeatherWidget()
    ss2.show()
    Gtk.main()
    exit(0)
