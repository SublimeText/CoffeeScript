import sublime, sublime_plugin
from subprocess import Popen, PIPE

settings = sublime.load_settings('CoffeeScript.sublime-settings')

def selectedText(view):
	text = []
	for region in view.sel():
		if not region.empty():
			text.append(view.substr(region))
	if len(text) > 0:
		return "".join(text)
	else:
		return False

def getText(view):
	text = []
	for region in view.sel():
		if region.empty():
			text.append(view.substr(sublime.Region(0, view.size())))
			break
		else:
			text.append(view.substr(region))
	return "".join(text)

def run(cmd, args = [], cwd = None, env = None):
	if env is None:
		env = {"PATH": settings.get('binDir', '/usr/local/bin')}
	proc = Popen([cmd] + args, cwd=cwd, env=env, stdout=PIPE, stderr=PIPE)
	stat = proc.communicate()
	if proc.returncode is 0:
		return (True, stat[0])
	else:
		return (False, stat[1])

def brew(args):
	return run("coffee", args)

def cake(task, cwd):
	return run("cake", [task], cwd)

class CompileAndDisplayCommand(sublime_plugin.TextCommand):
	def run(self, edit, **kwargs):
		opt = kwargs["opt"]
		res = brew(['-e', '-b', opt, getText(self.view)])
		output = self.view.window().new_file()
		if opt == '-p':
			output.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
		if res[0] is True:
			output.insert(edit, 0, res[1])
		else:
			output.insert(edit, 0, res[1].split("\n")[0])

class CheckSyntaxCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		res = brew(['-e', '-b', getText(self.view)])
		if res[0] is True:
			status = 'Valid'
		else:
			status = res[1].split("\n")[0]
		sublime.status_message('Syntax ' + status)

class RunScriptCommand(sublime_plugin.WindowCommand):
	def finish(self, text):
		if text == '':
			return
		res = brew(['-e', '-b', text])
		if res[0] is True:
			output = self.window.new_file()
			edit = output.begin_edit()
			output.insert(edit, 0, res[1])
			output.end_edit(edit)
		else:
			sublime.status_message('Syntax ' + res[1].split("\n")[0])

	def run(self):
		self.window.show_input_panel('Coffee>', '', self.finish, None, None)

class RunCakeTaskCommand(sublime_plugin.WindowCommand):
	def finish(self, task):
		if task == '':
			return
		res = cake(task, self.window.folders()[0])
		if res[0] is True:
			sublime.status_message("Task '" + task + "' succeeded.")
		else:
			sublime.status_message("Task '" + task + "' failed.")

	def run(self):
		self.window.show_input_panel('Enter a Cake task:', '', self.finish, None, None)
