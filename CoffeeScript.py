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
	result = coffee.communicate()
	return {out:result[0], err:result[1]}

def _compile(text):
	return brew(['-e', '-b', '-p', text])

def _syntax(text):
	result = brew(['-e', '-b', '-p', text])
	if result.serr:
		return False
	else:
		return True

class CompileAndDisplayCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		result = _compile(getText(self.view))
		if result["err"]:
			sublime.error_message(result["err"].split("\n")[0])
		else:
			output = self.view.window().new_file()
			output.insert(edit, 0, result["out"])
			output.insert(edit, 0, "# " + self.view.file_name() + "\n")

class CheckSyntaxCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		result = _compile(getText(self.view))
		if result["err"]:
			status = 'Syntax Error'
		else:
			status = 'Syntax Valid'
		sublime.status_message(status)
