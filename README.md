# Installation

**Package Path**

Sublime stores packages in the following locations:

	Nix: ~/.config/sublime-text-2/packages
	Mac: ~/Library/Application\ Support/Sublime\ Text\ 2/Packages
	Win: %APPDATA%\Sublime Text 2\Packages

When you see *PACKAGE_PATH*, replace it with one of the above.

### Nix/Mac

	cd PACKAGE_PATH
	git clone https://github.com/Xavura/CoffeeScript-Sublime-Plugin.git CoffeeScript


# Updating

	cd PACKAGE_PATH/CoffeeScript
	git fetch origin
	git merge origin/master

# Commands/Shortcuts

You can access the commands either using the command palette (meta+shift+P) or via shortcuts.

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
- Use `TAB` & `shift+TAB` to cycle forward/backward through fields.
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
