#aponxi
import sys
import os
from os import path
from os import environ
from subprocess import Popen, PIPE
from sublime_plugin import TextCommand
from sublime_plugin import WindowCommand
import sublime_plugin
import sublime
import functools
import locale
import threading
import tempfile
from .sourcemap import load


def settings_get(name, default=None):
    # load up the plugin settings
    plugin_settings = sublime.load_settings('CoffeeScript.sublime-settings')
    # project plugin settings? sweet! no project plugin settings? ok, well promote plugin_settings up then
    if sublime.active_window() and sublime.active_window().active_view():
        project_settings = sublime.active_window().active_view().settings().get("CoffeeScript")
    else:
        project_settings = {}

    # what if this isn't a project?
    # the project_settings would return None (?)
    if project_settings is None:
        project_settings = {}

    setting = project_settings.get(name, plugin_settings.get(name, default))
    return setting


def run(cmd, args=[], source="", cwd=None, env=None, callback=None):
    """
    Run command. "coffee", "cake", etc.
    Will run on thread if callback function is passed.
    """
    if callback:
        threading.Thread(target=lambda cb: cb(_run(cmd, args=args, source=source, cwd=cwd, env=env)), args=(callback,)).start()
    else:
        res = _run(cmd, args=args, source=source, cwd=cwd, env=env)
        return res


def _run(cmd, args=[], source="", cwd=None, env=None):
    if not type(args) is list:
        args = [args]
    if sys.platform == "win32":
        args = [cmd] + args
        if sys.version_info[0] == 2:
            for i in range(len(args)):
                args[i] = args[i].encode(locale.getdefaultlocale()[1])
        proc = Popen(args, env=env, cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        try:
            stat = proc.communicate(input=source)
        except:
            stat = proc.communicate(input=source.encode("utf8"))
        okay = proc.returncode == 0
        return {"okay": okay, "out": stat[0].decode(locale.getdefaultlocale()[1]), "err": stat[1].decode(locale.getdefaultlocale()[1])}
    else:
        if env is None:
            env = {"PATH": environ["PATH"]}
            env["PATH"] = settings_get('binDir', '/usr/local/bin')+":"+env["PATH"]

        # adding custom PATHs from settings
        customEnv = settings_get('envPATH', "")
        if customEnv:
            env["PATH"] = env["PATH"]+":"+customEnv
        if source == "":
            command = [cmd] + args
        else:
            command = [cmd] + args + [source]
        proc = Popen(command, env=env, cwd=cwd, stdout=PIPE, stderr=PIPE)
        stat = proc.communicate()
        okay = proc.returncode == 0
        return {"okay": okay, "out": stat[0].decode('utf-8'), "err": stat[1].decode('utf-8')}


def brew(args, source, cwd=None, callback=None):
    """
    Compile command
    """
    if sys.platform == "win32":
        args.append("-s")
    else:
        args.append("-e")
    return run("coffee", args=args, source=source.encode('utf-8'), callback=callback)


def cake(task, cwd, callback=None):
    return run("cake", args=task, cwd=cwd, callback=callback)


def isCoffee(view=None):
    if view is None:
        view = sublime.active_window().active_view()
    return 'source.coffee' in view.scope_name(0)


def isLitCoffee(view=None):
    if view is None:
        view = sublime.active_window().active_view()
    return 'source.litcoffee' in view.scope_name(0)


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
        return isCoffee(self.view) or isLitCoffee(self.view)

    def run(self, *args, **kwargs):
        no_wrapper = settings_get('noWrapper', True)
        compile_dir = settings_get('compileDir')
        source_file = self.view.file_name()
        source_dir = os.path.normcase(os.path.dirname(source_file))
        project_file = self.view.window().project_file_name()
        if project_file:
            project_dir = os.path.normcase(os.path.dirname(project_file))
        compile_paths = settings_get('compilePaths')
        sourcemaps = settings_get('sourceMaps', True)

        args = ['-c', source_file]
        if no_wrapper:
            args = ['-b'] + args
        if sourcemaps:
            args = ['-m'] + args
        if isLitCoffee(self.view):
            args = ['-l'] + args

        # check instance of compile_paths
        if isinstance(compile_paths, dict):
            appendix_len = None
            for key_path in compile_paths:
                norm_path = os.path.normcase(key_path)
                if not os.path.isabs(norm_path) and project_file:
                    norm_path = os.path.join(project_dir, norm_path)
                appendix = os.path.relpath(source_dir, norm_path)
                if not appendix.startswith('..') and (appendix_len is None or len(appendix) < appendix_len):
                    appendix_len = len(appendix)
                    compile_dir = compile_paths[key_path]
                    if not os.path.isabs(compile_dir):
                        compile_dir = os.path.join(norm_path, compile_dir)
                    compile_dir = os.path.join(compile_dir, appendix)

        if compile_dir and (isinstance(compile_dir, str)):
            # Check for absolute path or relative path for compile_dir
            if not os.path.isabs(compile_dir):
                compile_dir = os.path.join(source_dir, compile_dir)
            print("Compile to:" + compile_dir)
            # create folder if not exist
            if not os.path.exists(compile_dir):
                os.makedirs(compile_dir)
                print("Compile dir did not exist, created folder: " + compile_dir)
            folder, file_nm = os.path.split(source_file)
            args = ['--output', compile_dir] + args
        else:
            compile_dir = source_dir
            print("Compile to same directory")

        if sourcemaps:
            cwd = source_dir
        else:
            cwd = None
        result = run("coffee", args=args, cwd=cwd)

        if result['okay'] is True:
            status = 'Compilation Succeeded'
        else:
            errorFirstLine = result['err'].splitlines()[0]
            status = 'Compilation FAILED ' + errorFirstLine
            sublime.error_message(errorFirstLine)

        later = lambda: sublime.status_message(status)
        sublime.set_timeout(later, 300)


class CompileAndDisplayCommand(TextCommand):
    def is_enabled(self):
        return isCoffee(self.view) or isLitCoffee(self.view)

    def run(self, edit, **kwargs):
        no_wrapper = settings_get('noWrapper', True)
        output = self.view.window().new_file()
        output.set_scratch(True)
        opt = kwargs["opt"]
        if opt == '-p':
            output.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
        args = [opt]

        if no_wrapper:
            args = ['-b'] + args
        if isLitCoffee(self.view):
            args = ['-l'] + args

        res = brew(args, Text.get(self.view))
        if res["okay"] is True:
            output.insert(edit, 0, res["out"])
        else:
            output.insert(edit, 0, res["err"].split("\n")[0])


class FastCompileCommand(TextCommand):
    def is_enabled(self):
        return not isCoffee(self.view) and not isLitCoffee(self.view)

    def run(self, edit, **kwargs):
        res = brew(["-c", "-b"], Text.get(self.view))
        if res["okay"] is True:
            result = res["out"]
            if result.split("\n")[0][0:2] == "//":
                result = "\n".join(result.split("\n")[1:])
            current_auto_indent = self.view.settings().get("auto_indent")
            self.view.settings().set("auto_indent", False)
            self.view.run_command('insert', {'characters': result})
            self.view.settings().set("auto_indent", current_auto_indent)
        else:
            sublime.message_dialog("Compiling error: " + res["err"])


class CheckSyntaxCommand(TextCommand):
    def is_enabled(self):
        return isCoffee(self.view) or isLitCoffee(self.view)

    def run(self, edit):
        args = ['-b', '-p']
        if isLitCoffee(self.view):
            args = ['-l'] + args
        res = brew(args, Text.get(self.view))
        if res["okay"] is True:
            status = 'Valid'
        else:
            status = res["err"].split("\n")[0]
        sublime.message_dialog('Syntax %s' % status)


class ToggleParensCommand(TextCommand):
    def is_enabled(self):
        return isCoffee(self.view) or isLitCoffee(self.view)

    def run(self, edit):
        if self.view.sel()[0].empty():
            self.view.run_command('expand_selection', {'to': 'brackets'})
            for sel in self.view.sel():
                self.remove_parens(edit, sel)
        else:
            for sel in self.view.sel():
                self.add_parens(edit, sel)
            self.view.run_command('move', {'by': 'characters', 'forward': True})

    def add_parens(self, edit, sel):
        self.view.insert(edit, sel.end(), ')')

        if self.view.substr(sel.begin() - 1) is ' ':
            self.view.replace(edit, sublime.Region(sel.begin() - 1, sel.begin()), '(')
        else:
            self.view.insert(edit, sel.begin(), '(')

    def remove_parens(self, edit, sel):
        begin = sel.begin()
        end = sel.end()

        if self.view.substr(begin - 1) is '(':
            self.view.replace(edit, sublime.Region(begin - 1, begin), ' ')
        elif self.view.substr(begin) is '(':
            self.view.replace(edit, sublime.Region(begin, begin + 1), ' ')

        if self.view.substr(end) is ')':
            self.view.erase(edit, sublime.Region(end, end + 1))
        elif self.view.substr(end - 1) is ')':
            self.view.erase(edit, sublime.Region(end - 1, end))


class QuickRunBarCommand(WindowCommand):
    def finish(self, text):
        if text == '':
            return
        text = "{puts, print} = require 'util'\n" + text
        res = brew(['-b'], text)
        if res["okay"] is True:
            output = self.window.new_file()
            output.set_scratch(True)
            output.run_command('insert', {'characters': res["out"]})
        else:
            sublime.status_message('Syntax %s' % res["err"].split("\n")[0])

    def run(self):
        self.window.show_input_panel('Coffee >', '', self.finish, None, None)


class RunCakeTaskCommand(WindowCommand):
    def finish(self, task):
        if task == '':
            return

        if not self.window.folders():
            cakepath = path.dirname(self.window.active_view().file_name())
        else:
            cakepath = self.window.folders()[0]
            if not path.exists(cakepath):
                cakepath = path.dirname(self.window.active_view().file_name())

        if not path.exists(cakepath):
            return sublime.message_dialog("Cakefile not found.")

        def on_done(res):
            if res["okay"] is True:
                if "No such task" in res["out"]:
                    msg = "doesn't exist"
                else:
                    msg = "suceeded"
            else:
                print(res["err"])
                msg = "failed"
            sublime.status_message("Task %s - %s." % (task, msg))

        cake(task, cakepath, on_done)

    def run(self):
        self.window.show_input_panel('Cake >', '', self.finish, None, None)


#                               _
#   __ _ _ __   ___  _ __ __  _(_)
#  / _` | '_ \ / _ \| '_ \\ \/ / |
# | (_| | |_) | (_) | | | |>  <| |
#  \__,_| .__/ \___/|_| |_/_/\_\_|
#       |_|
class LintCommand(TextCommand):

    def is_enabled(self):
        return isCoffee(self.view)

    def run(self, edit):
        filepath = self.view.file_name()
        args = [filepath, "--reporter", "csv"]
        lintConfFile = settings_get("lintConfFile", False)
        if lintConfFile:
            if not path.isfile(lintConfFile):
                print("Lint configuration file not found. Path: " + lintConfFile)
            else:
                args += ["-f", lintConfFile]
        res = run("coffeelint", args=args)
        error_list = []
        for line in res["out"].split('\n'):
            if not len(line.split(","))-1:
                continue
            lineNum = line.split(",")[1]
            message = line.split(",")[-1]
            try:
                error_list.append({"message": message, "line": int(lineNum)-1})
            except:
                continue
        if len(error_list):
            self.popup_error_list(error_list)
        else:
            sublime.status_message("No lint errors.")

    def popup_error_list(self, error_list):

        panel_items = []

        for error in error_list:
            line_text = self.view.substr(self.view.full_line(self.view.text_point(error['line'], 0)))
            item = [error['message'], '{0}: {1}'.format(error['line'] + 1, line_text.strip())]
            panel_items.append(item)

        def on_done(selected_item):
            if selected_item == -1:
                return

            selected = self.view.sel()
            selected.clear()

            error = error_list[selected_item]
            region_begin = self.view.text_point(error['line'], 0)

            selected.add(sublime.Region(region_begin, region_begin))
            # We have to force a move to update the cursor position
            self.view.run_command('move', {'by': 'characters', 'forward': True})
            self.view.run_command('move', {'by': 'characters', 'forward': False})
            self.view.show_at_center(region_begin)

        self.view.window().show_quick_panel(panel_items, on_done)


class RunScriptCommand(TextCommand):
    PANEL_NAME = 'coffee_compile_output'
    PANEL_IS_OPEN = False

    def is_enabled(self):
        return isCoffee(self.view) or isLitCoffee(self.view)

    def run(self, edit):
        window = self.view.window()

        #refresh the output view
        no_wrapper = settings_get('noWrapper', True)

        source_dir, source_file = path.split(self.view.file_name())

        cwd = source_dir

        args = [self.view.file_name()]
        if no_wrapper:
            args = args + ['-b']
        if isLitCoffee(self.view):
            args = ['-l'] + args

        res = brew(args, "", cwd)
        panel = window.get_output_panel(self.PANEL_NAME)
        panel.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
        panel.set_read_only(False)
        output = panel

        if res["okay"] is True:
            output.run_command('append', {'characters': res["out"]})
        else:
            output.run_command('append', {'characters': res["err"].split("\n")[0]})
        output.sel().clear()
        output.set_read_only(True)

        window.run_command('show_panel', {'panel': 'output.%s' % self.PANEL_NAME})
        self.PANEL_IS_OPEN = True
        return

watchers = {}


def watched_filename(view):
    if view.file_name() is not None:
        filename = view.file_name().split('/')[-1]
    else:
        filename = "Unsaved File"
    return filename


class Tool():
    @staticmethod
    def get_file_name(file_path):
        if file_path:
            filename = os.path.split(file_path)[-1]
        else:
            filename = "Unsaved File"
        return filename

    @staticmethod
    def get_js_file_name(coffee_file_name):
        fileName, fileExtension = os.path.splitext(coffee_file_name)
        output_filename = fileName + '.js'
        return output_filename


class Watcher():
    def __init__(self, inputView):
        self.created_pane = False
        self.inputView = inputView
        print("Now watching " + watched_filename(inputView))
        self.determine_output_pane()
        self.create_output()

    def determine_output_pane(self):
        active_group = self.inputView.window().active_group()
        num_groups = self.inputView.window().num_groups()
        layout = self.inputView.window().get_layout()
        cells = layout['cells']
        cols = layout['cols']

        if num_groups == 1:
            # only pane. create a new one.
            self.output_pane_index = 1
            self.created_pane = True
            self.inputView.window().run_command('set_layout', {
                "cols": [0.0, 0.5, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
            })
        elif active_group == num_groups - 1:
            # last pane in window. output to the previous one.
            self.output_pane_index = active_group - 1
        elif len(cols) > 2 and cells[active_group][2] == len(cols) - 1:
            # last pane in row. output to previous one.
            self.output_pane_index = active_group - 1
        else:
            self.output_pane_index = active_group + 1

    def create_output(self):
        self.sourceFilePath = self.inputView.file_name()
        self.outputFileName = Tool.get_js_file_name(Tool.get_file_name(self.sourceFilePath))
        self.outputTempDir = tempfile.gettempdir()
        # print(self.outputTempDir)
        self.outputFilePath = path.join(self.outputTempDir, self.outputFileName)

        no_wrapper = settings_get('noWrapper', True)
        sourcemaps = settings_get('sourceMaps', True)
        args = []
        if no_wrapper:
            args = ['-b'] + args
        if sourcemaps:
            args = args + ['-m']
        args = args + ["-o", self.outputTempDir, self.sourceFilePath]

        res = run("coffee", args)
        if not res["okay"]:
            sublime.message_dialog("Error. See console.")
            print(res["err"])
            return
        # create new tab
        self.outputView = self.inputView.window().open_file(self.outputFilePath)
        # move it to second column
        self.outputView.window().focus_group(self.output_pane_index)
        self.outputView.window().set_view_index(self.outputView, self.outputView.window().active_group(), 0)
        # self.outputView.window().focus_group(0)
        self.inputView.window().focus_view(self.inputView)

    def refresh(self):
        no_wrapper = settings_get('noWrapper', True)
        sourcemaps = settings_get('sourceMaps', True)
        args = ["-o", self.outputTempDir]
        if sourcemaps:
            args = ['-m'] + args
        if no_wrapper:
            args = ['-b'] + args
        res = brew(args, source=Text.get(self.inputView))
        with open(self.outputFilePath, 'w', encoding='utf8') as f:
            f.write(res["out"])

        mapFile = path.join(self.outputTempDir, self.outputFileName.split(".")[0]+'.map')
        (inputRow, inputCol) = self.inputView.rowcol(self.inputView.sel()[0].begin())
        index = load(open(mapFile)).getpos(line=inputRow, column=inputCol)
        if not index:
            return
        (row, col) = index
        row = int(row)

        def goto():
            selected = self.outputView.sel()
            selected.clear()
            region_begin = self.outputView.text_point(row, 0)
            selected.add(sublime.Region(region_begin, region_begin))
            self.outputView.run_command('move', {'by': 'characters', 'forward': True})
            self.outputView.run_command('move', {'by': 'characters', 'forward': False})
            self.outputView.show_at_center(region_begin)
        sublime.set_timeout(goto, 10)

    def stop(self):
        if not self.inputView.id() in watchers:
            return
        print("Stop watching: " + self.inputView.file_name())
        del watchers[self.inputView.id()]
        window = self.outputView.window() or self.inputView.window()
        if self.outputView.window():
            window.focus_view(self.outputView)
            window.run_command("close")

        if self.created_pane and len(window.views_in_group(self.output_pane_index)) == 0:
            window.run_command('set_layout', {
                "cols": [0.0, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1]]
            })


class ToggleWatch(TextCommand):
    views = {}
    outputs = {}

    def is_enabled(self):
        return isCoffee(self.view)

    def run(self, edit):
        viewID = self.view.id()
        if not viewID in watchers:
            watchers[viewID] = Watcher(self.view)
        else:
            watchers[viewID].stop()


class CaptureEditing(sublime_plugin.EventListener):

    def is_enabled(self, view):
        return isCoffee(view)

    def handleTimeout(self, watcher):
        if self._new_modify and not self._refreshed:
            sublime.set_timeout(functools.partial(self.handleTimeout, watcher), 1000)
            self._new_modify = False
        else:
            if self._refreshed:
                return
            self._refreshed = True
            watcher.refresh()

    def on_modified(self, view):
        if not self.is_enabled(view):
            return
        viewID = view.id()
        watch_modified = settings_get('watchOnModified')
        self._new_modify = True
        if watch_modified is not False and viewID in watchers:
            self._refreshed = False
            self.handleTimeout(watchers[viewID])

    def on_post_save(self, view):
        if not self.is_enabled(view):
            return
        compile_on_save = settings_get('compileOnSave', True)
        if compile_on_save is True:
            print("Compiling on save...")
            view.run_command("compile")
            show_compile_output_on_save = settings_get('showOutputOnSave', True)
            if show_compile_output_on_save is True and isCoffee() is True and RunScriptCommand.PANEL_IS_OPEN is True:
                print("Updating output panel...")
                view.run_command("compile_output")

        watch_save = settings_get('watchOnSave', True)
        if watch_save:
            viewID = view.id()
            if viewID in watchers:
                watchers[viewID].refresh()

        if settings_get("checkSyntaxOnSave", True):
            args = ['-b', '-p']
            if isLitCoffee(view):
                args = ['-l'] + args
            res = brew(args, Text.get(view))
            if res["okay"] is True:
                sublime.status_message("Syntax is valid.")
            else:
                status = res["err"].split("\n")[0]
                sublime.message_dialog('Syntax error: %s' % status)

        if settings_get("lintOnSave", True):
            view.run_command("lint")

    def on_close(self, view):
        viewID = view.id()
        for k, watcher in watchers.items():
            if watcher.outputView.id() == viewID:
                watcher.stop()
                break

        if not self.is_enabled(view):
            return

        if viewID in watchers:
            watchers[viewID].stop()
