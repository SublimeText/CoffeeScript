
	                                         __    
	   __     _____     ___     ___    __  _/\_\   
	 /'__`\  /\ '__`\  / __`\ /' _ `\ /\ \/'\/\ \  
	/\ \L\.\_\ \ \L\ \/\ \L\ \/\ \/\ \\/>  </\ \ \ 
	\ \__/.\_\\ \ ,__/\ \____/\ \_\ \_\/\_/\_\\ \_\
	 \/__/\/_/ \ \ \/  \/___/  \/_/\/_/\//\/_/ \/_/
	            \ \_\                              
	             \/_/                              


	 ____            __    __                   
	/\  _`\         /\ \__/\ \__                
	\ \ \L\ \     __\ \ ,_\ \ ,_\    __   _ __  
	 \ \  _ <'  /'__`\ \ \/\ \ \/  /'__`\/\`'__\
	  \ \ \L\ \/\  __/\ \ \_\ \ \_/\  __/\ \ \/ 
	   \ \____/\ \____\\ \__\\ \__\ \____\\ \_\ 
	    \/___/  \/____/ \/__/ \/__/\/____/ \/_/ 
	                                            
	             
			                ___    ___                                                __      
			              /'___\ /'___\                                    __        /\ \__   
			  ___    ___ /\ \__//\ \__/   __     __    ____    ___   _ __ /\_\  _____\ \ ,_\  
			 /'___\ / __`\ \ ,__\ \ ,__\/'__`\ /'__`\ /',__\  /'___\/\`'__\/\ \/\ '__`\ \ \/  
			/\ \__//\ \L\ \ \ \_/\ \ \_/\  __//\  __//\__, `\/\ \__/\ \ \/ \ \ \ \ \L\ \ \ \_ 
			\ \____\ \____/\ \_\  \ \_\\ \____\ \____\/\____/\ \____\\ \_\  \ \_\ \ ,__/\ \__\
			 \/____/\/___/  \/_/   \/_/ \/____/\/____/\/___/  \/____/ \/_/   \/_/\ \ \/  \/__/
			                                                                      \ \_\       
			                                                                       \/_/       
                               
# Jump to Section

* [Latest Change Log](#latest-changelog)
* [Installation](#installation)
* [Updating](#updating)
* [Commands/Shortcuts](#commandsshortcuts)
* [Snippets](#snippets)
* [Building](#building)
* [Settings](#settings)
* [Special Thanks](#special-thanks)
* [Support this Project: ![](https://www.gittip.com/assets/widgets/heart.gif) Tip Me!](https://www.gittip.com/aponxi/)

# Overview

This package is for Sublime Text 3. If you are looking for Sublime Text 2, then please refer to st2 branch.

## Description

CoffeeScript plugin was originally created by @Xavura. As I began writing a lot of code in CoffeeScript I felt the need for side-by-side view for compiled CoffeeScript. Since Xavura's repo have been inactive I decided to branch out my own version. The biggest change in my branch is the Watch Mode which updates the compiled JavaScript view whenever you modify the CoffeeScript thus enabling you to view your progress side-by-side.

I use this plugin everyday so whenever I am not developing I am in testing stage. I'll make sure every request or bug will be patched since I'm a frequent user.

## Contributing

- Please use [aponxi/issues page](https://github.com/aponxi/sublime-better-coffeescript/issues) to make requests or report bugs.
- Please make _pull requests_ to develop branch.

# Installation

## via Package Control

> This is the recommended installation method.

If you have Sublime Package Control, you know what to do. If not, well: it's a package manager for Sublime Text 2; it's awesome and you can [read about it here](http://wbond.net/sublime_packages/package_control).

To install Package Control by Git:

The Packages/ folder listed below refers to the folder that opens when you use the Preferences > Browse Packages… menu.
```
cd Packages/
git clone https://github.com/wbond/sublime_package_control.git "Package Control"
cd "Package Control"
git checkout python3
```

After installing the package manager:

* Open the Command Pallete (`ctrl+shift+P` or `cmd+shift+P`).
* Type "Install Package" and hit return.
* Type "Better CoffeeScript" and hit return.

## via Source Control

> If you plan to contribute, then you should install via this method. Otherwise it is recommended that you install the package via Package Control, see above.

Sublime stores packages in the following locations:

	Nix: ~/.config/sublime-text-3/packages
	Mac: ~/Library/Application\ Support/Sublime\ Text\ 3/Packages
	Win: %APPDATA%\Sublime Text 3\Packages

### As a repository within the packages directory

Open a Terminal/Console and run the following commands, replacing `PACKAGE_PATH` with the path corresponding to your OS above.

	cd PACKAGE_PATH
	git clone https://github.com/aponxi/sublime-better-coffeescript.git "Better CoffeeScript"

### As a repository outside of the packages directory

If you use Github for Mac/Windows which store repositories in a specific location, or if you just don't want a repository in your packages directory, then instead you can use a link.

If you don't yet have the repository, then grab it via your GUI program or via the command line:

	cd WHEREVER_YOU_WANT
	git clone https://github.com/aponxi/sublime-better-coffeescript.git

Once that is done, we will create the link:

#### Windows:

	cd PACKAGE_PATH
	mklink /D "Better CoffeeScript" ABSOLUTE_PATH_TO_REPOSITORY

#### Nix/Mac:

	cd PACKAGE_PATH
	ln -s ABSOLUTE_PATH_TO_REPOSITORY "Better CoffeeScript"

#### A note on Package Control

When Package Control tries to update your packages, if you have a repository in your packages directory then it will try to pull down and merge any changes. If you don't want this to happen and would rather handle everything yourself, then you can add the following to your settings (Preferences » Package Settings » Package Control » Settings - User):

	"auto_upgrade_ignore": ["Better CoffeeScript"]

# Updating

If you are using Package Control, updating will be automatic and you don't have to worry about it.

If using Source Control:

	cd "PACKAGE_PATH/Better CoffeeScript"
	git fetch origin
	git merge origin/master

# Commands/Shortcuts

You can access the commands either using the command palette (`ctrl+shift+P` or `cmd+shift+P`) or via shortcuts.

	alt+shift+t - Run a Cake task
	alt+shift+r - Run some CoffeeScript (prints output to a panel on the bottom)
	alt+shift+s - Run a syntax check
	alt+shift+c - Compile a file
	alt+shift+d - Display compiled JavaScript
	alt+shift+l - Display lexer tokens
	alt+shift+n - Display parser nodes
	alt+shift+w - Toggle watch mode
	alt+shift+p - Toggle output panel


Context menu has `Compile Output` that compiles the current CoffeeScript and outputs the javascript code that is run, in a panel.

**Note:** Some of the commands use the Status Bar for output, so you'll probably want to enable it (Tools » Show Status Bar).



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

> When using the build system, it is assumed that your `.sublime-project` file lives in your project's base directory (due to limitations with the build system).

Hitting `F7` (Tools » Build) will run the Cake task 'sbuild'.

If you're not quite sure what the point of this is then read on.

Let's say before distributing your project that you would like to combine all of your `.js` files into one and then minify them them using UglifyJS or something.

That's what this is for! You would create a `Cakefile` and inside it you would write a task:

	task 'sbuild', 'Prepare project for distribution.', ->
		# ...

# Settings

Go to `Preferences > Package Settings > CoffeeScript > Settings - User` to change settings.

```Javascript
{
	/*
		The directories you would like to include in $PATH environment variable.
		Use this if your node installation is at a seperate location and getting errors such as `cannot find node executable`

		example:
		"envPATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

	*/
	"envPATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
	/*
		The directory containing your coffee binary. Usually
		/usr/local/bin.
	*/
	"binDir": "/usr/local/bin"

	/*
		Compile without the top-level function wrapper (coffee -b).
	*/

,	"noWrapper": true

	/*
		Enable or disable refresh the compiled Output on Save.
		Only available for watch mode.
	*/
,	"watchOnSave": true
	/*
		Enable refreshing compiled JS when CoffeeScript is modified.

		Put false to disable
		Put a number of seconds to delay the refresh
	*/
,	"watchOnModified": 0.5
	/*
		Enable Compiling on save. It will compile into the same folder.
	*/
,	"compileOnSave": true
	/*
		## Enable outputting the results of the compiled coffeescript in a panel
	*/
,	"showOutputOnSave": false
	/*
		## Enable compiling to a specific directory.
		#### Description

		if it is a string like 'some/directory' then `-o some/directory` will be added to `coffee` compiler. 
		if it is false or not string then it will compile your `script.coffee` to the directory it is in.

		#### Example:
		Directory is relative to the file you are editting if specified such as
			compileDir": "out"
		Directory is absolute if specified such as
			compileDir": "/home/logan/Desktop/out"
		
	*/
,	"compileDir": false
	/*
		## Enable compiling to a specific relative directory.

		#### Example:
		Set absolute path for compile dir:
			"compileDir": "/home/user/projects/js"
		And relative folder
			"relativeDir": "/home/user/projects/coffee"

		So
			"/home/user/projects/coffee/app.coffee" will compile to "/home/user/projects/js/app.js"
			"/home/user/projects/coffee/models/prod.coffee" will compile to "/home/user/projects/js/models/prod.js"
		
	*/
,	"relativeDir": false



}


```

## Project settings

Go to `Project > Edit Project` to change project settings.

```Javascript
{
	"folders":
	[
		...
	],
	"settings":
	{
		"CoffeeScript":
		{
			"noWrapper": true,
			"compileOnSave": true,
			"compileDir": "out"
		}
	}
}


```
# Latest Changelog
### v0.7.0 01/June/2013

- merged st3 with master branch
- now the sublime text 2 support is in st2 branch
- fixed the @ highlight in language definitions
- fixed an error you would get when it was looking for project settings when it wasn't a project we were editing

# Special Thanks

* [agibsonsw](https://github.com/agibsonsw) for his help in writing WatchMode
* [Xavura](https://github.com/Xavura) for writing the base of this plugin
* [lavrton](https://github.com/lavrton) for his contributions 