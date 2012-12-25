import sublime
import sys
from os import path
from subprocess import Popen, PIPE
from sublime_plugin import TextCommand, WindowCommand, EventListener
import sublime, sublime_plugin
import time
import functools

settings = sublime.load_settings('CoffeeScript.sublime-settings')


def run(cmd, args = [], source="", cwd = None, env = None):
	if not type(args) is list:
		args = [args]
	if sys.platform == "win32":
		proc = Popen([cmd]+args, env=env, cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
		stat = proc.communicate(input=source)
	else:
		if env is None:
			env = {"PATH": settings.get('binDir', '/usr/local/bin')}
		if source == "":
			command = [cmd]+args
		else:
			command = [cmd]+args+[source]
			#print command
		proc = Popen(command, env=env, cwd=cwd, stdout=PIPE, stderr=PIPE)
		stat = proc.communicate()
	okay = proc.returncode == 0
	return {"okay": okay, "out": stat[0], "err": stat[1]}

def brew(args, source):
	if sys.platform == "win32":
		args.append("-s")
	else:
		args.append("-e")
	return run("coffee", args=args, source=source)

def cake(task, cwd):
	return run("cake", args=task, cwd=cwd)

def isCoffee(view = None):
	if view is None:
		view = sublime.active_window().active_view()
	return 'source.coffee' in view.scope_name(0)

class Text():
	@staticmethod
	def all(view):
		return view.substr(sublime.Region(0, view.size()))
	@staticmethod
	def sel(view):
		text = []
		for region in view.sel():
			if region.empty():
				continue
			text.append(view.substr(region))
		return "".join(text)

	@staticmethod
	def get(view):
		text = Text.sel(view)
		if len(text) > 0:
			return text
		return Text.all(view)

class CompileCommand(TextCommand):
	def is_enabled(self):
		return isCoffee(self.view)

	def run(self, *args, **kwargs):
		no_wrapper = settings.get('noWrapper', True)
		args = ['-c', self.view.file_name()]
		if no_wrapper:
			args = ['-b'] + args
		result = run("coffee", args=args)

		if result['okay'] is True:
			status = 'Compilation Succeeded'
		else:
			status = 'Compilation Failed'

		sublime.status_message(status)

class CompileAndDisplayCommand(TextCommand):
	def is_enabled(self):
		return isCoffee(self.view)

	def run(self, edit, **kwargs):
		output = self.view.window().new_file()
		output.set_scratch(True)
		opt = kwargs["opt"]
		if opt == '-p':
			output.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
		no_wrapper = settings.get('noWrapper', True)

		args = [opt]
		print args
		if no_wrapper:
			args = ['-b'] + args

		res = brew(args, Text.get(self.view))
		if res["okay"] is True:
			output.insert(edit, 0, res["out"])
		else:
			output.insert(edit, 0, res["err"].split("\n")[0])


class CheckSyntaxCommand(TextCommand):
	def is_enabled(self):
		return isCoffee(self.view)

	def run(self, edit):
		res = brew(['-b', '-p'], Text.get(self.view))
		if res["okay"] is True:
			status = 'Valid'
		else:
			status = res["err"].split("\n")[0]
		sublime.status_message('Syntax %s' % status)

class RunScriptCommand(WindowCommand):
	def finish(self, text):
		if text == '':
			return
		text = "{puts, print} = require 'util'\n" + text
		res = brew(['-b'], text)
		if res["okay"] is True:
			output = self.window.new_file()
			output.set_scratch(True)
			edit = output.begin_edit()
			output.insert(edit, 0, res["out"])
			output.end_edit(edit)
		else:
			sublime.status_message('Syntax %s' % res["err"].split("\n")[0])

	def run(self):
		sel = Text.sel(sublime.active_window().active_view())
		if len(sel) > 0:
			if not isCoffee(): return
			self.finish(sel)
		else:
			self.window.show_input_panel('Coffee >', '', self.finish, None, None)

class RunCakeTaskCommand(WindowCommand):
	def finish(self, task):
		if task == '':
			return

		if not self.window.folders():
			cakepath = path.dirname(self.window.active_view().file_name())
		else:
			cakepath = path.join(self.window.folders()[0], 'Cakefile')
			if not path.exists(cakepath):
				cakepath = path.dirname(self.window.active_view().file_name())

		if not path.exists(cakepath):
			return sublime.status_message("Cakefile not found.")

		res = cake(task, cakepath)
		if res["okay"] is True:
			if "No such task" in res["out"]:
				msg = "doesn't exist"
			else:
				msg = "suceeded"
		else:
			msg = "failed"
		sublime.status_message("Task %s - %s." % (task, msg))

	def run(self):
		self.window.show_input_panel('Cake >', '', self.finish, None, None)


class ToggleWatch(TextCommand):
	views = {}
	outputs = {}
	


	def is_enabled(self):
		return isCoffee(self.view)

	def run(self, edit):
		myvid = self.view.id()
		if not ToggleWatch.views.has_key(myvid):
			views = ToggleWatch.views
			views[myvid] = {'watched' : True, 'modified' : True}
			views[myvid]["input_obj"] = self.view
			output = createOut(myvid)
			
			#print "edit", edit
			refreshOut(myvid)
		else :
			views = ToggleWatch.views

			views[myvid]['watched'] = not views[myvid]['watched']
			if views[myvid]['watched'] is True :
				refreshOut(myvid)


		
		


def createOut(input_view_id):
	#create output panel and save
	this_view = ToggleWatch.views[input_view_id]
	outputs = ToggleWatch.outputs
	#print this_view

	output = this_view["input_obj"].window().new_file()
	output.set_scratch(True)
	output.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
	this_view['output_id'] = output.id()
	this_view["output_obj"] = output
	this_view["output_open"] = True
	if not outputs.has_key(output.id()):
		outputs[output.id()] = {'boundto': input_view_id}
	
	return output


def refreshOut (view_id):

	this_view = ToggleWatch.views[view_id]
	this_view['last_modified'] = time.mktime(time.gmtime())
	#refresh the output view
	no_wrapper = settings.get('noWrapper', True)

	args = ['-p']
	if no_wrapper:
		args = ['-b'] + args

	
	res = brew(args, Text.get(this_view['input_obj']))
	output = this_view['output_obj']
	this_view['modified'] = False
	
	if res["okay"] is True:
		edit = output.begin_edit()
		output.erase(edit, sublime.Region(0, output.size()))
		output.insert(edit, 0, res["out"])
		output.end_edit(edit)
		#print "Refreshed"
	else:
		edit = output.begin_edit()
		output.erase(edit, sublime.Region(0, output.size()))
		output.insert(edit, 0, res["err"].split("\n")[0])
		output.end_edit(edit)
	

	return 

def isView(view_id):
	# are they modifying a view (rather than a panel, etc.)
	if not view_id: return False
	window = sublime.active_window()
	view = window.active_view() if window != None else None
	return (view is not None and view.id() == view_id)


class CaptureEditing(sublime_plugin.EventListener):
	#edit_info = {}
	
	  
	def handleTimeout(self, vid):  
		this_view = ToggleWatch.views[vid]
		modified = this_view['modified']
		if modified is True:  
			# There are no more queued up calls to handleTimeout, so it must have  
			# been 1000ms since the last modification  
			print "handling"
			refreshOut(vid)

	def on_modified(self, view):
		vid = view.id()
		now = time.mktime(time.gmtime())
		#print "now ", now
		#if not isView(vid):
			# I only want to use views, not 
			# the input-panel, etc..
		#	return
		#if not CaptureEditing.edit_info.has_key(vid):
			# create a dictionary entry based on the 
			# current views' id
		#	CaptureEditing.edit_info[vid] = {}
		#cview = CaptureEditing.edit_info[vid]
		# I can now store details of the current edit 
		# in the edit_info dictionary, via cview.
		watch_modified = settings.get('watchOnModified')

		if watch_modified is not False and ToggleWatch.views.has_key(vid):
			if watch_modified is True:
				delay = 1
			elif watch_modified == 0:
				delay = 1
			else :
				delay = watch_modified
			#then we have a watched input.
			this_view = ToggleWatch.views[vid]
			#print " this view is ", this_view
			if this_view['watched'] is True and this_view['modified'] is False:
				this_view['modified'] = True
				print " trigger "

				#if this_view['last_modified'] <  now - delay:
				sublime.set_timeout(functools.partial(self.handleTimeout, vid), delay*1000)  
				

			return

	def on_post_save ( self, view):
		watch_save = settings.get('watchOnSave', True)
		if watch_save :
			save_id = view.id()
			views = ToggleWatch.views
			if views.has_key(save_id):
				refreshOut(save_id)

		return
	def on_close(self,view):
		close_id = view.id()
		views = ToggleWatch.views
		if views.has_key(close_id):
			#this is an input
			this_view = views[close_id]
			#this_view['output_obj'].close()
		
		if ToggleWatch.outputs.has_key(close_id):
			#this is an output
			print "an output was closed!"
			boundview = ToggleWatch.outputs[close_id]['boundto']
			thatview = views[boundview]
			thatview['output_open'] = False
			thatview['watched'] = False
			print "The output was closed, no longer watching"

		return
