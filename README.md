# Installation

## via Package Control

If you have Sublime Package Control, you know what to do. If not, well it's a package manager for Sublime Text 2.

To install Package Control, open the Python Console (ctrl+' or cmd+`) and paste the following into it:

    import urllib2,os; pf='Package Control.sublime-package'; ipp=sublime.installed_packages_path(); os.makedirs(ipp) if not os.path.exists(ipp) else None; urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler())); open(os.path.join(ipp,pf),'wb').write(urllib2.urlopen('http://sublime.wbond.net/'+pf.replace(' ','%20')).read()); print 'Please restart Sublime Text to finish installation'

After installing the package and restarting the editor:

* Open the Command Pallete (ctrl+shift+P or cmd+shift+P).
* Type "Install Package" and hit return.
* Type "CoffeeScript" and hit return.

## via Source Control

Sublime stores packages in the following locations:

	Nix: ~/.config/sublime-text-2/packages
	Mac: ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
	Win: %APPDATA%\Sublime Text 2\Packages

Open a Terminal/Console and run the following two commands, replacing *PACKAGE_PATH* with the path corresponding to your OS above.

	cd PACKAGE_PATH
	git clone https://github.com/Xavura/CoffeeScript-Sublime-Plugin.git CoffeeScript


# Updating

If you are using Package Control, updating will be automatic and you don't have to worry about it.

If using Source Control:

	cd PACKAGE_PATH/CoffeeScript
	git fetch origin
	git merge origin/master

# Commands/Shortcuts

You can access the commands either using the command palette (ctrl+shift+P or cmd+shift+P) or via shortcuts.

	alt+shift+t - Run a Cake task
	alt+shift+r - Run some CoffeeScript (puts/print for output)
	alt+shift+s - Run a syntax check
	alt+shift+c - Compile a file
	alt+shift+d - Display compiled JavaScript
	alt+shift+l - Display lexer tokens
	alt+shift+n - Display parser nodes
	alt+shift+w - Toggle watch mode
	alt+shift+z - Toggle output panel

**Note:** Some of the commands use the status bar for output, so you'll probably want to enable it (Tools - Show Status Bar)

# Snippets

- Use `TAB` to run a snippet after typing the trigger.
- Use `TAB` and `shift+TAB` to cycle forward/backward through fields.
- Use `ESC` to exit snippet mode.

### Snippet Triggers

**Comprehension**

	Array:  forin
	Object: forof
	Range:  fori (inclusive)
	Range:  forx (exclusive)

**Statements**

	If:        if
	Else:      el
	If Else:   ifel
	Else If:   elif
	Switch:    swi
	Ternary:   ter
	Try Catch: try
	Unless:    unl

**Classes**

	Class - cla

**Other**

	Function:      -
	Function:      = (bound)
	Interpolation: #

# Building

Hitting `F7` (Tools - Build) will run the Cake task 'sbuild'.

# Settings

You can ignore these for now as they don't yet do anything.

**binDir**
If your Coffee binary isn't in `/usr/local/bin` then you can change this.

**noWrapper**
Compile without the top level function wrapper (`coffee --bare`).

**watchEnabled**
Globally enable/disable watch mode (a wrapper over `coffee --watch`).

**watchOutputMode**
Where output from watch mode will be sent (panel, status, console).

**watchOutputOnSuccess
watchOutputOnFailure**
Useful if you, for instance, only want to show compile errors.

**watchHighlightErrors**
Files will be automagically opened, if they contain an error. Also, your cursor shall of course be placed on the offending line.
