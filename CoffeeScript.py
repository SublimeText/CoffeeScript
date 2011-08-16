import sublime
from os import path
from subprocess import Popen, PIPE
from sublime_plugin import TextCommand, WindowCommand

settings = sublime.load_settings('CoffeeScript.sublime-settings')

def run(cmd, args = [], cwd = None, env = None):
	if not type(args) is list:
		args = [args]
	if env is None:
		env = {"PATH": settings.get('binDir', '/usr/local/bin')}
	proc = Popen([cmd]+args, env=env, cwd=cwd, stdout=PIPE, stderr=PIPE)
	stat = proc.communicate()
	okay = proc.returncode == 0
	return {"okay": okay, "out": stat[0], "err": stat[1]}

def brew(args):
	return run("coffee", args=args)

def cake(task, cwd):
	return run("cake", args=task, cwd=cwd)

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

class CompileAndDisplayCommand(TextCommand):
	def run(self, edit, **kwargs):
		opt = kwargs["opt"]
		res = brew(['-e', '-b', opt, Text.get(self.view)])
		output = self.view.window().new_file()
		output.set_scratch(True)
		if opt == '-p':
			output.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
		if res["okay"] is True:
			output.insert(edit, 0, res["out"])
		else:
			output.insert(edit, 0, res["err"].split("\n")[0])

class CheckSyntaxCommand(TextCommand):
	def run(self, edit):
		res = brew(['-e', '-b', '-p', Text.get(self.view)])
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
		res = brew(['-e', '-b', text])
		if res["okay"] is True:
			output = self.window.new_file()
			output.set_scratch(True)
			edit = output.begin_edit()
			output.insert(edit, 0, res["out"])
			output.end_edit(edit)
		else:
			sublime.status_message('Syntax %s' % res["err"].split("\n")[0])

	def run(self):
		self.window.show_input_panel('Coffee>', '', self.finish, None, None)

class RunCakeTaskCommand(WindowCommand):
	def finish(self, task):
		if task == '':
			return

		if not path.exists(path.join(self.window.folders()[0], 'Cakefile')):
			return sublime.status_message("Cakefile not found.")

		res = cake(task, self.window.folders()[0])
		if res["okay"] is True:
			if "No such task" in res["out"]:
				msg = "doesn't exist"
			else:
				msg = "suceeded"
		else:
			msg = "failed"
		sublime.status_message("Task %s - %s." % (task, msg))

	def run(self):
		self.window.show_input_panel('Enter a Cake task:', '', self.finish, None, None)
