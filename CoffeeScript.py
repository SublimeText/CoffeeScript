#aponxi v0.6
import sublime
import sys
from os import path
import os
from subprocess import Popen, PIPE
from sublime_plugin import TextCommand
from sublime_plugin import WindowCommand
import sublime_plugin
import time
import functools
import locale


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


def run(cmd, args=[], source="", cwd=None, env=None):
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
    else:
        if env is None:
            env = {"PATH": settings_get('binDir', '/usr/local/bin')}

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


def brew(args, source, cwd=None):
    if sys.platform == "win32":
        args.append("-s")
    else:
        args.append("-e")

    return run("coffee", args=args, source=source.encode('utf-8'))


def cake(task, cwd):
    return run("cake", args=task, cwd=cwd)


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
        compile_paths = settings_get('compilePaths')
        sourcemaps = settings_get('sourceMaps', True)

        # print "Compiling: " + source_file
        # if sys.platform == "win32":
        #     args = ['-c', source_file.encode('utf8')]
        # else:
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
            print("Compile to same directory")

        result = run("coffee", args=args)

        if result['okay'] is True:
            status = 'Compilation Succeeded'
        else:
            errorFirstLine = result['err'].splitlines()[0]
            status = 'Compilation FAILED '+errorFirstLine
            sublime.error_message(errorFirstLine)

        sublime.status_message(status)

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
        sublime.status_message('Syntax %s' % status)


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


#                               _
#   __ _ _ __   ___  _ __ __  _(_)
#  / _` | '_ \ / _ \| '_ \\ \/ / |
# | (_| | |_) | (_) | | | |>  <| |
#  \__,_| .__/ \___/|_| |_/_/\_\_|
#       |_|

def watched_filename(view_id):
    view = ToggleWatch.views[view_id]['input_obj']
    if view.file_name() is not None:
        filename = view.file_name().split('/')[-1]
    else:
        filename = "Unsaved File"
    return filename


class ToggleWatch(TextCommand):
    views = {}
    outputs = {}

    def is_enabled(self):
        return isCoffee(self.view)

    def run(self, edit):
        myvid = self.view.id()
        if not myvid in ToggleWatch.views:

            views = ToggleWatch.views
            views[myvid] = {'watched': True, 'modified': True, 'input_closed': False}
            views[myvid]["input_obj"] = self.view

            print("Now watching", watched_filename(myvid))
            self.view.window().run_command('set_layout', {
                "cols": [0.0, 0.5, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
            })
            # return
            createOut(myvid, edit)

        else:
            views = ToggleWatch.views

            views[myvid]['watched'] = not views[myvid]['watched']
            if not views[myvid]['watched']:
                print("Stopped watching", watched_filename(myvid))

            if views[myvid]['output_open'] is False:
                print("Openning output and watching", watched_filename(myvid))
                createOut(myvid, edit)

            elif views[myvid]['watched'] is True:
                print("Resuming watching", watched_filename(myvid))
                refreshOut(myvid, edit)


def cleanUp(input_view_id):
    # print(ToggleWatch.views[input_view_id])
    # window = ToggleWatch.views[input_view_id]["input_obj"].window()
    del ToggleWatch.outputs[ToggleWatch.views[input_view_id]['output_id']]
    del ToggleWatch.views[input_view_id]

    return


def get_output_filename(input_view_id):
    input_filename = watched_filename(input_view_id)
    fileName, fileExtension = os.path.splitext(input_filename)
    output_filename = fileName + '.js'
    return output_filename


def createOut(input_view_id, edit):
    #create output panel and save
    this_view = ToggleWatch.views[input_view_id]
    outputs = ToggleWatch.outputs
    output = this_view["input_obj"].window().new_file()
    output.window().focus_group(1)
    output.window().set_view_index(output, output.window().active_group(), 0)
    # print(output.index)
    output.set_scratch(True)
    output.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
    this_view['output_id'] = output.id()
    this_view["output_obj"] = output
    this_view["output_open"] = True
    this_view["edit"] = edit
    # Getting file extension
    output_filename = get_output_filename(input_view_id)
    output.set_name(output_filename)

    if not output.id() in outputs:
        outputs[output.id()] = {'boundto': input_view_id}
    refreshOut(input_view_id, edit)
    return output


def refreshOut(view_id, edit):
    this_view = ToggleWatch.views[view_id]
    this_view['last_modified'] = time.mktime(time.gmtime())
    #refresh the output view
    no_wrapper = settings_get('noWrapper', True)

    args = ['-p']
    if no_wrapper:
        args = ['-b'] + args

    res = brew(args, Text.get(this_view['input_obj']))
    output = this_view['output_obj']
    this_view['modified'] = False
    current_auto_indent = output.settings().get("auto_indent")
    output.settings().set("auto_indent", False)
    if res["okay"] is True:
        output.run_command('select_all')
        output.run_command('insert', {'characters': res["out"]})
    else:
        output.run_command('insert', {'characters': res["err"].split("\n")[0]})
    output.settings().set("auto_indent", current_auto_indent)

    return


def isView(view_id):
    # are they modifying a view (rather than a panel, etc.)
    if not view_id:
        return False
    window = sublime.active_window()
    view = window.active_view() if window is not None else None
    return (view is not None and view.id() == view_id)


def close_output(input_id):
    views = ToggleWatch.views
    v = views[input_id]
    output = v['output_obj']
    if v['output_open'] is True:
        output.window().focus_view(output)
        if len(ToggleWatch.views) == 1:
            output.window().run_command('set_layout', {
                "cols": [0.0, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1]]
            })
        output.window().run_command("close")
        print(watched_filename(input_id), "was closed. Closing the Output")
        cleanUp(input_id)

    return


class CaptureEditing(sublime_plugin.EventListener):

    def handleTimeout(self, vid):
        this_view = ToggleWatch.views[vid]
        modified = this_view['modified']
        if modified is True:
            # been 1000ms since the last modification
            refreshOut(vid, this_view["edit"])

    def on_modified(self, view):
        vid = view.id()
        watch_modified = settings_get('watchOnModified')

        if watch_modified is not False and vid in ToggleWatch.views:
            if watch_modified is True:
                delay = 0.5
            elif watch_modified < 0.5:
                delay = 0.5
            else:
                delay = watch_modified
            #then we have a watched input.
            this_view = ToggleWatch.views[vid]
            if this_view['modified'] is False:
                this_view['modified'] = True
                if this_view['watched'] is True:
                    sublime.set_timeout(functools.partial(self.handleTimeout, vid), int(delay * 1000))
            return

    def on_post_save(self, view):
        # print "isCoffee " + str(isCoffee())
        watch_save = settings_get('watchOnSave', True)
        if watch_save:
            save_id = view.id()
            views = ToggleWatch.views
            if save_id in views:
                # getting view object
                save_view = ToggleWatch.views[save_id]
                # check if modified
                if save_view['modified'] is True:
                    refreshOut(save_id, save_view['edit'])
        compile_on_save = settings_get('compileOnSave', True)
        if compile_on_save is True and isCoffee() is True:

            print("Compiling on save...")
            view.run_command("compile")
        show_compile_output_on_save = settings_get('showOutputOnSave', True)
        if show_compile_output_on_save is True and isCoffee() is True and RunScriptCommand.PANEL_IS_OPEN is True:
            print("Updating output panel...")
            view.run_command("compile_output")

        return

    def on_close(self, view):
        close_id = view.id()
        views = ToggleWatch.views
        if close_id in views:
            #this is an input
            views[close_id]['input_closed'] = True
            close_output(close_id)

        if close_id in ToggleWatch.outputs and views[ToggleWatch.outputs[close_id]['boundto']]['input_closed'] is not True:
            #this is an output
            boundview = ToggleWatch.outputs[close_id]['boundto']
            thatview = views[boundview]
            thatview['output_open'] = False
            thatview['watched'] = False

            filename = watched_filename(boundview)
            cleanUp(ToggleWatch.outputs[close_id]['boundto'])
            if len(ToggleWatch.views) == 0:
                thatview['input_obj'].window().run_command('set_layout', {
                    "cols": [0.0, 1.0],
                    "rows": [0.0, 1.0],
                    "cells": [[0, 0, 1, 1]]
                })
            print("The output was closed. No longer watching", filename)

        return


class LintCommand(TextCommand):

    def is_enabled(self):
        return isCoffee(self.view)

    def run(self, edit):
        filepath = self.view.file_name()
        res = run("coffeelint", args=[filepath, "--csv"])
        error_list = []
        for line in res["out"].split('\n'):
            if not len(line.split(","))-1:
                continue
            file, line, type, message = line.split(",")
            error_list.append({"message": message, "line": int(line)-1})
        self.popup_error_list(error_list)

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
