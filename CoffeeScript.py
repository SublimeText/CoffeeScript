import sublime, sublime_plugin
from subprocess import Popen, PIPE

settings = sublime.load_settings('CoffeeScript.sublime-settings')

def getText(view):
	text = []
	for region in view.sel():
		if region.empty():
			text.append(view.substr(sublime.Region(0, view.size())))
			break
		else:
			text.append(view.substr(region))
	return "".join(text)

def brew(args):
	args = ["coffee"] + args
	coffee = Popen(args, env={"PATH": settings.get('binDir', '/usr/local/bin')}, stdout=PIPE, stderr=PIPE)
	status = coffee.communicate()
	if coffee.returncode is 0:
		return (True, status[0])
	else:
		return (False, status[1])

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
