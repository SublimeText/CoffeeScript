import sublime, sublime_plugin
from subprocess import Popen, PIPE

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
	coffee = Popen(args, env={"PATH": "/usr/local/bin"}, stdout=PIPE, stderr=PIPE)
	status = coffee.communicate()
	if coffee.returncode is 0:
		return (True, status[0])
	else:
		return (False, status[1])

class CompileAndDisplayCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		res = brew(['-e', '-b', '-p', getText(self.view)])
		if res[0] is True:
			output = self.view.window().new_file()
			output.insert(edit, 0, res[1])
		else:
			sublime.error_message(res[1].split("\n")[0])

class CheckSyntaxCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		res = brew(['-e', '-b', getText(self.view)])
		if res[0] is True:
			status = 'Valid'
		else:
			status = res[1].split("\n")[0]
		sublime.status_message('Syntax ' + status)
