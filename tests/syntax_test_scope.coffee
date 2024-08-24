# SYNTAX TEST "CoffeeScript.sublime-syntax"

class App.Router extends Snakeskin.Router
# <- meta.class.coffee storage.type.class.coffee
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.coffee
#^^^^ storage.type.class.coffee
#     ^^^^^^^^^^ entity.name.type.class.coffee
#                ^^^^^^^ keyword.control.inheritance.coffee
#                        ^^^^^^^^^^^^^^^^ entity.other.inherited-class.coffee

  index: () =>
# <- meta.function.coffee
#^^^^^^ meta.function.coffee
# ^^^^^ entity.name.function.coffee - entity entity
#      ^ keyword.operator.coffee
#        ^^^^^ meta.inline.function.coffee
#        ^^ variable.parameter.function.coffee
#           ^^ storage.type.function.coffee
    "Hello"
#   ^^^^^^^ meta.string.coffee string.quoted.double.coffee
