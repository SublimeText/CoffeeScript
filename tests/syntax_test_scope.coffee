# SYNTAX TEST "CoffeeScript.sublime-syntax"

###[ COMMENTS ]###############################################################

# comment
# <- comment.line.number-sign.coffee punctuation.definition.comment.coffee
#^^^^^^^^^ comment.line.number-sign.coffee

  ### comment ###
# ^^^^^^^^^^^^^^^ comment.block.coffee
# ^^^ punctuation.definition.comment.coffee
#             ^^^ punctuation.definition.comment.coffee

  ###
# ^^^^ comment.block.coffee
# ^^^ punctuation.definition.comment.coffee

  class Name
# <- comment.block.coffee
# ^^^^^^^^^^ comment.block.coffee - keyword

  @todo
# ^^^^^ comment.block.coffee variable.annotation.coffee
# ^ punctuation.definition.variable.coffee

  ###
# <- comment.block.coffee
#^^^^ comment.block.coffee
# ^^^ punctuation.definition.comment.coffee

###[ IMPORT / EXPORT ]########################################################

import {"foo"} from bar as baz
# <- keyword.control.import.coffee
#^^^^^ keyword.control.import.coffee
#              ^^^^ keyword.control.import.coffee
#                       ^^ keyword.operator.assignment.as.coffee

export parentClass
# <- keyword.control.export.coffee
#^^^^^ keyword.control.export.coffee

###[ CLASSES ]################################################################

class extends parentClass
# <- meta.class.coffee storage.type.class.coffee
#^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.coffee
#^^^^ storage.type.class.coffee
#     ^^^^^^^ keyword.control.inheritance.coffee
#             ^^^^^^^^^^^ entity.other.inherited-class.coffee
  constructor: ->
    return

class App.Router extends Snakeskin.Router
# <- meta.class.coffee storage.type.class.coffee
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.class.coffee
#^^^^ storage.type.class.coffee
#     ^^^^^^^^^^ entity.name.type.class.coffee
#                ^^^^^^^ keyword.control.inheritance.coffee
#                        ^^^^^^^^^^^^^^^^ entity.other.inherited-class.coffee

###[ FUNCTIONS ]###############################################################

  name:
# ^^^^^ - meta.function - entity.name.function

  name: ->
# ^^^^^^^^ - meta.function meta.function
# ^^^^ meta.function.identifier.coffee entity.name.function.coffee
#     ^^^^ meta.function.coffee
#     ^ keyword.operator.assignment.coffee
#       ^^ keyword.declaration.function.coffee

  @name: ->
# ^^^^^^^^^ - meta.function meta.function
# ^^^^^ meta.function.identifier.coffee entity.name.function.coffee
#      ^^^^ meta.function.coffee
#      ^ keyword.operator.assignment.coffee
#        ^^ keyword.declaration.function.coffee

  namespace.name: ->
# ^^^^^^^^^^^^^^^^^^ - meta.function meta.function
# ^^^^^^^^^^^^^^ meta.function.identifier.coffee entity.name.function.coffee
#               ^^^^ meta.function.coffee
#               ^ keyword.operator.assignment.coffee
#                 ^^ keyword.declaration.function.coffee

  name = =>
# ^^^^^^^^^ - meta.function meta.function
# ^^^^ meta.function.identifier.coffee entity.name.function.coffee
#     ^ meta.function.identifier.coffee - entity
#      ^^^^ meta.function.coffee
#      ^ keyword.operator.assignment.coffee
#        ^^ keyword.declaration.function.coffee

  namespace.name = =>
# ^^^^^^^^^^^^^^^^^^^ - meta.function meta.function
# ^^^^^^^^^^^^^^ meta.function.identifier.coffee entity.name.function.coffee
#               ^ meta.function.identifier.coffee - entity
#                ^^^^ meta.function.coffee
#                ^ keyword.operator.assignment.coffee
#                  ^^ keyword.declaration.function.coffee

  name: =>
# ^^^^^^^^ - meta.function meta.function
# ^^^^ meta.function.identifier.coffee entity.name.function.coffee
#     ^^^^ meta.function.coffee
#     ^ keyword.operator.assignment.coffee
#       ^^ keyword.declaration.function.coffee

  namespace.name: =>
# ^^^^^^^^^^^^^^^^^^ - meta.function meta.function
# ^^^^^^^^^^^^^^ meta.function.identifier.coffee entity.name.function.coffee
#               ^^^^ meta.function.coffee
#               ^ keyword.operator.assignment.coffee
#                 ^^ keyword.declaration.function.coffee

  name = =>
# ^^^^^^^^^ - meta.function meta.function
# ^^^^ meta.function.identifier.coffee entity.name.function.coffee
#     ^ meta.function.identifier.coffee - entity
#      ^^^^ meta.function.coffee
#      ^ keyword.operator.assignment.coffee
#        ^^ keyword.declaration.function.coffee

  namespace.name = =>
# ^^^^^^^^^^^^^^^^^^^ - meta.function meta.function
# ^^^^^^^^^^^^^^ meta.function.identifier.coffee entity.name.function.coffee
#               ^ meta.function.identifier.coffee - entity
#                ^^^^ meta.function.coffee
#                ^ keyword.operator.assignment.coffee
#                  ^^ keyword.declaration.function.coffee

  name: () ->
# ^^^^^^^^^^^ - meta.function meta.function
# ^^^^ meta.function.identifier.coffee entity.name.function.coffee
#     ^^ meta.function.coffee
#       ^^ meta.function.parameters.coffee
#         ^^^ meta.function.coffee
#     ^ keyword.operator.assignment.coffee
#       ^ punctuation.section.parameters.begin.coffee
#        ^ punctuation.section.parameters.end.coffee
#          ^^ keyword.declaration.function.coffee

  name: (foo, bar = undefined, baz="buuz", ...) ->
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - meta.function meta.function
# ^^^^ meta.function.identifier.coffee entity.name.function.coffee
#     ^^ meta.function.coffee
#       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.function.parameters.coffee
#                                              ^^^ meta.function.coffee
#     ^ keyword.operator.assignment.coffee
#       ^ punctuation.section.parameters.begin.coffee
#        ^^^ variable.parameter.coffee
#           ^ punctuation.separator.sequence.coffee
#             ^^^ variable.parameter.coffee
#                 ^ keyword.operator.assignment.coffee
#                   ^^^^^^^^^ constant.language.coffee
#                            ^ punctuation.separator.sequence.coffee
#                              ^^^ variable.parameter.coffee
#                                 ^ keyword.operator.assignment.coffee
#                                  ^^^^^^ meta.string.coffee string.quoted.double.coffee
#                                        ^ punctuation.separator.sequence.coffee
#                                          ^^^ keyword.operator.variadic.coffee
#                                             ^ punctuation.section.parameters.end.coffee
#                                               ^^ keyword.declaration.function.coffee

  name: (
# ^^^^ meta.function.identifier.coffee entity.name.function.coffee
#     ^^ meta.function.coffee
#       ^^ meta.function.parameters.coffee
#       ^ punctuation.section.parameters.begin.coffee
    foo,
#   ^^^ variable.parameter.coffee
#      ^ punctuation.separator.sequence.coffee

    bar = undefined,
#   ^^^ variable.parameter.coffee
#       ^ keyword.operator.assignment.coffee
#         ^^^^^^^^^ constant.language.coffee

    baz="buuz"
#   ^^^ variable.parameter.coffee
#      ^ keyword.operator.assignment.coffee
#       ^^^^^^ meta.string.coffee string.quoted.double.coffee
  ) ->
#^^ meta.function.parameters.coffee
# <- meta.function.parameters.coffee
# ^ punctuation.section.parameters.end.coffee
#   ^^ keyword.declaration.function.coffee

  () ->
# ^^ meta.function.parameters.coffee
#   ^^^ meta.function.coffee
# ^ punctuation.section.parameters.begin.coffee
#  ^ punctuation.section.parameters.end.coffee
#    ^^ keyword.declaration.function.coffee

  () =>
# ^^ meta.function.parameters.coffee
#   ^^^ meta.function.coffee
# ^ punctuation.section.parameters.begin.coffee
#  ^ punctuation.section.parameters.end.coffee
#    ^^ keyword.declaration.function.coffee

  (foo) ->
# ^^^^^ meta.function.parameters.coffee
#      ^^^ meta.function.coffee
# ^ punctuation.section.parameters.begin.coffee
#  ^^^ variable.parameter.coffee
#     ^ punctuation.section.parameters.end.coffee
#       ^^ keyword.declaration.function.coffee

###[ KEYWORDS ]################################################################

  if .if _if $if
# ^^ keyword.control.conditional.if.coffee
#   ^^^^^^^^^^^^ - keyword

  for .for _for $for
# ^^^ keyword.control.loop.for.coffee
#    ^^^^^^^^^^^^^^^^ - keyword

  break .break _break $break
# ^^^^^ keyword.control.flow.coffee
#      ^^^^^^^^^^^^^^^^^^^^^ - keyword

  continue .continue _continue $continue
# ^^^^^^^^ keyword.control.flow.coffee
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ - keyword

  yield @foo
# ^^^^^ keyword.control.flow.coffee
#       ^^^^ variable.other.readwrite.instance.coffee

  yield from @foo
# ^^^^^^^^^^ keyword.control.flow.coffee
#            ^^^^ variable.other.readwrite.instance.coffee

###[ OPERATORS ]###############################################################

  as
# ^^ keyword.operator.assignment.as.coffee

  in of
# ^^ keyword.operator.iterator.coffee
#    ^^ keyword.operator.iterator.coffee

  and or is isnt not
# ^^^ keyword.operator.logical.coffee
#     ^^ keyword.operator.logical.coffee
#        ^^ keyword.operator.logical.coffee
#           ^^^^ keyword.operator.logical.coffee
#                ^^^ keyword.operator.logical.coffee

  new
# ^^^ keyword.operator.object.new.coffee

  new Class()
# ^^^ keyword.operator.object.new.coffee
#     ^^^^^ support.class.coffee

  new My.Class()
# ^^^ keyword.operator.object.new.coffee
#     ^^ support.class.coffee
#       ^ punctuation.accessor.dot.coffee
#        ^^^^^ support.class.coffee

  delete
# ^^^^^^ keyword.operator.object.delete.coffee

  delete obj
# ^^^^^^ keyword.operator.object.delete.coffee
#        ^^^ variable.other.readwrite.coffee

  obj typeof Bar
# ^^^ variable.other.readwrite.coffee
#     ^^^^^^ keyword.operator.comparison.type.coffee
#            ^^^ support.class.coffee

  obj instanceof Bar
# ^^^ variable.other.readwrite.coffee
#     ^^^^^^^^^^ keyword.operator.comparison.type.coffee
#                ^^^ support.class.coffee

  and= or= += -= *= /= %= &= |= ^= <<= >>= >>>=
# ^^^^ keyword.operator.assignment.augmented.coffee
#      ^^^ keyword.operator.assignment.augmented.coffee
#          ^^ keyword.operator.assignment.augmented.coffee
#             ^^ keyword.operator.assignment.augmented.coffee
#                ^^ keyword.operator.assignment.augmented.coffee
#                   ^^ keyword.operator.assignment.augmented.coffee
#                      ^^ keyword.operator.assignment.augmented.coffee
#                         ^^ keyword.operator.assignment.augmented.coffee
#                            ^^ keyword.operator.assignment.augmented.coffee
#                               ^^ keyword.operator.assignment.augmented.coffee
#                                  ^^^ keyword.operator.assignment.augmented.coffee
#                                      ^^^ keyword.operator.assignment.augmented.coffee
#                                          ^^^^ keyword.operator.assignment.augmented.coffee

  === == !== != <= >=
# ^^^ keyword.operator.comparison.coffee
#     ^^ keyword.operator.comparison.coffee
#        ^^^ keyword.operator.comparison.coffee
#            ^^ keyword.operator.comparison.coffee
#               ^^ keyword.operator.comparison.coffee
#                  ^^ keyword.operator.comparison.coffee

  i++ i--
#  ^^ keyword.operator.arithmetic.coffee
#      ^^ keyword.operator.arithmetic.coffee

  ! ? && ||
# ^ keyword.operator.logical.coffee
#   ^ keyword.operator.logical.coffee
#     ^^ keyword.operator.logical.coffee
#        ^^ keyword.operator.logical.coffee

  ^ ~ & |
# ^ keyword.operator.bitwise.coffee
#   ^ keyword.operator.bitwise.coffee
#     ^ keyword.operator.bitwise.coffee
#       ^ keyword.operator.bitwise.coffee

  + - * / %
# ^ keyword.operator.arithmetic.coffee
#   ^ keyword.operator.arithmetic.coffee
#     ^ keyword.operator.arithmetic.coffee
#       ^ keyword.operator.arithmetic.coffee
#         ^ keyword.operator.arithmetic.coffee

  = :
# ^ keyword.operator.assignment.coffee
#   ^ keyword.operator.assignment.coffee

  ...
# ^^^ keyword.operator.variadic.coffee

###[ BUILTIN FUNCTIONS ]#######################################################

  console.log()
# ^^^^^^^ variable.language.console.coffee
#        ^ punctuation.accessor.dot.coffee
#         ^^^ support.function.console.coffee
#            ^ punctuation.section.group.begin.coffee
#             ^ punctuation.section.group.end.coffee

  Map
# ^^^ support.class.coffee

  Object.create()
# ^^^^^^ support.class.coffee
#       ^ punctuation.accessor.dot.coffee
#        ^^^^^^ support.function.static.object.coffee
#              ^ punctuation.section.group.begin.coffee
#               ^ punctuation.section.group.end.coffee

###[ OBJECT MEMBERS ]##########################################################

  this.key
# ^^^^ variable.language.coffee
#     ^ meta.path.coffee punctuation.accessor.dot.coffee
#      ^^^ meta.path.coffee variable.other.member.coffee

  obj.Object
# ^^^^^^^^^^ meta.path.coffee
# ^^^ variable.other.object.coffee
#    ^ punctuation.accessor.dot.coffee
#     ^^^^^^ variable.other.member.coffee

  obj.member
# ^^^^^^^^^^ meta.path.coffee
# ^^^ variable.other.object.coffee
#    ^ punctuation.accessor.dot.coffee
#     ^^^^^^ variable.other.member.coffee

  obj.child.member
# ^^^^^^^^^^^^^^^^ meta.path.coffee
# ^^^ variable.other.object.coffee
#    ^ punctuation.accessor.dot.coffee
#     ^^^^^ variable.other.object.coffee
#          ^ punctuation.accessor.dot.coffee
#           ^^^^^^ variable.other.member.coffee

  obj.method(1+1, "foo")
# ^^^^^^^^^^ meta.path.coffee
#     ^^^^^^ meta.function-call.identifier.coffee
#           ^^^^^^^^^^^^ meta.function-call.arguments.coffee
# ^^^ variable.other.object.coffee
#    ^ punctuation.accessor.dot.coffee
#     ^^^^^^ variable.function.coffee
#           ^ punctuation.section.group.begin.coffee
#            ^ meta.number.integer.decimal.coffee constant.numeric.value.coffee
#             ^ keyword.operator.arithmetic.coffee
#              ^ meta.number.integer.decimal.coffee constant.numeric.value.coffee
#               ^ punctuation.separator.sequence.coffee
#                 ^^^^^ meta.string.coffee string.quoted.double.coffee
#                      ^ punctuation.section.group.end.coffee

###[ LITERALS ]################################################################

  Infinity NaN undefined .Infinity .NaN .undefined
# ^^^^^^^^ constant.language.coffee
#          ^^^ constant.language.coffee
#              ^^^^^^^^^ constant.language.coffee
#                        ^ punctuation.accessor.dot.coffee
#                         ^^^^^^^^ variable.other.member.coffee
#                                  ^ punctuation.accessor.dot.coffee
#                                   ^^^ variable.other.member.coffee
#                                       ^ punctuation.accessor.dot.coffee
#                                        ^^^^^^^^^ variable.other.member.coffee

  true on yes .true .on .yes
# ^^^^ constant.language.boolean.true.coffee
#      ^^ constant.language.boolean.true.coffee
#         ^^^ constant.language.boolean.true.coffee
#             ^ punctuation.accessor.dot.coffee
#              ^^^^ variable.other.member.coffee
#                   ^ punctuation.accessor.dot.coffee
#                    ^^ variable.other.member.coffee
#                       ^ punctuation.accessor.dot.coffee
#                        ^^^ variable.other.member.coffee

  false off no .false .off .no
# ^^^^^ constant.language.boolean.false.coffee
#       ^^^ constant.language.boolean.false.coffee
#           ^^ constant.language.boolean.false.coffee
#              ^ punctuation.accessor.dot.coffee
#               ^^^^^ variable.other.member.coffee
#                     ^ punctuation.accessor.dot.coffee
#                      ^^^ variable.other.member.coffee
#                          ^ punctuation.accessor.dot.coffee
#                           ^^ variable.other.member.coffee

  null _null .null
# ^^^^ constant.language.null.coffee
#      ^^^^^ variable.other.readwrite.coffee
#            ^^^^^ meta.path.coffee
#            ^ punctuation.accessor.dot.coffee
#             ^^^^ variable.other.member.coffee

  0b1000111101
# ^^ meta.number.integer.binary.coffee constant.numeric.base.coffee
#   ^^^^^^^^^^ meta.number.integer.binary.coffee constant.numeric.value.coffee

  0o12340576
# ^^ meta.number.integer.octal.coffee constant.numeric.base.coffee
#   ^^^^^^^^ meta.number.integer.octal.coffee constant.numeric.value.coffee

  0x1234567890ABCDEF
# ^^ meta.number.integer.hexadecimal.coffee constant.numeric.base.coffee
#   ^^^^^^^^^^^^^^^^ meta.number.integer.hexadecimal.coffee constant.numeric.value.coffee

  10e5
# ^^^^ meta.number.float.decimal.coffee constant.numeric.value.coffee

  10.e5
# ^^^^^ meta.number.float.decimal.coffee constant.numeric.value.coffee

  10.23
# ^^^^^ meta.number.float.decimal.coffee constant.numeric.value.coffee

  10.23e-5
# ^^^^^^^^ meta.number.float.decimal.coffee constant.numeric.value.coffee

  52
# ^^ meta.number.integer.decimal.coffee constant.numeric.value.coffee

  "foo \. \x28 bar\""
# ^^^^^^^^^^^^^^^^^^^ meta.string.coffee string.quoted.double.coffee
# ^ punctuation.definition.string.begin.coffee
#      ^^ constant.character.escape.coffee
#         ^^^^ constant.character.escape.coffee
#                 ^^ constant.character.escape.coffee
#                   ^ punctuation.definition.string.end.coffee

  'foo \. \x28 bar\''
# ^^^^^^^^^^^^^^^^^^^ meta.string.coffee string.quoted.single.coffee
# ^ punctuation.definition.string.begin.coffee
#      ^^ constant.character.escape.coffee
#         ^^^^ constant.character.escape.coffee
#                 ^^ constant.character.escape.coffee
#                   ^ punctuation.definition.string.end.coffee

  """
#^ - meta.string - string
# ^^^ meta.string.heredoc.coffee string.quoted.double.coffee punctuation.definition.string.begin.coffee
  """
# <- meta.string.heredoc.coffee string.quoted.double.coffee
#^ meta.string.heredoc.coffee string.quoted.double.coffee
# ^^^ meta.string.heredoc.coffee string.quoted.double.coffee punctuation.definition.string.end.coffee
#    ^ - meta.string - string

  '''
#^ - meta.string - string
# ^^^ meta.string.heredoc.coffee string.quoted.single.coffee punctuation.definition.string.begin.coffee
  '''
# <- meta.string.heredoc.coffee string.quoted.single.coffee
#^ meta.string.heredoc.coffee string.quoted.single.coffee
# ^^^ meta.string.heredoc.coffee string.quoted.single.coffee punctuation.definition.string.end.coffee
#    ^ - meta.string - string

  ```
# ^^^ meta.string.heredoc.coffee string.quoted.script.coffee punctuation.definition.string.begin.coffee
#    ^ meta.string.heredoc.coffee meta.embedded.coffee source.jsx.embedded.coffee - string

  var i = `back ${tick} string`;
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.string.heredoc.coffee meta.embedded.coffee source.jsx.embedded.coffee - source.jsx source.jsx
# ^^^ keyword.declaration
#         ^^^^^^ meta.string string.quoted.other.js
#               ^^^^^^^ meta.string meta.interpolation.js
#                       ^^^^^^^ meta.string string.quoted.other.js
  return (<h1>Hello {World}</h1>)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.string.heredoc.coffee meta.embedded.coffee source.jsx.embedded.coffee - source.jsx source.jsx
#         ^^^^^^^^^^^^^^^^^^^^^^ meta.group.js meta.jsx.js
#         ^^^^ meta.tag
#                          ^^^^^ meta.tag
  ```
# <- meta.string.heredoc.coffee meta.embedded.coffee source.jsx.embedded.coffee - string
#^ meta.string.heredoc.coffee meta.embedded.coffee source.jsx.embedded.coffee - string
# ^^^ meta.string.heredoc.coffee string.quoted.script.coffee punctuation.definition.string.end.coffee
#    ^ - meta.string - string

  `
# ^ meta.string.coffee string.quoted.script.coffee punctuation.definition.string.begin.coffee
#  ^ meta.string.coffee meta.embedded.coffee source.jsx.embedded.coffee - string
  var i = 0;
# ^^^^^^^^^^^ meta.string.coffee meta.embedded.coffee source.jsx.embedded.coffee - source.jsx source.jsx
# ^^^ keyword.declaration
  return (<h1>Hello {World}</h1>)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.string.coffee meta.embedded.coffee source.jsx.embedded.coffee - source.jsx source.jsx
#         ^^^^^^^^^^^^^^^^^^^^^^ meta.group.js meta.jsx.js
#         ^^^^ meta.tag
#                          ^^^^^ meta.tag
  `
# <- meta.string.coffee meta.embedded.coffee source.jsx.embedded.coffee - string
#^ meta.string.coffee meta.embedded.coffee source.jsx.embedded.coffee - string
# ^ meta.string.coffee string.quoted.script.coffee punctuation.definition.string.end.coffee
#  ^ - meta.string - string

  ///
# <- - meta.string
#^ - meta.string
# ^^^ meta.string.heredoc.coffee punctuation.definition.string.begin.coffee
#    ^ meta.string.heredoc.coffee string.regexp.coffee
  \. #{var}
#^^^^^^^^^^^ meta.string.heredoc.coffee
# ^^ string.regexp.coffee constant.character.escape.coffee
#    ^^^^^^ meta.embedded.coffee source.coffee.embedded.source
  ///
# <- meta.string.heredoc.coffee string.regexp.coffee
#^ meta.string.heredoc.coffee string.regexp.coffee
# ^^^ meta.string.heredoc.coffee punctuation.definition.string.end.coffee

  /[0-9]bar/img
# ^^^^^^^^^^^^^ meta.string.regexp.coffee
# ^ punctuation.definition.string.begin.coffee
#  ^^^^^^^^ string.regexp.coffee
#          ^ punctuation.definition.string.end.coffee
#           ^^^ constant.language.flags.coffee

  .replace(/\\/g, "/")
#         ^^^^^^^^^^^^ meta.function-call.arguments.coffee
#          ^^^^^ meta.string.regexp.coffee
#          ^ punctuation.definition.string.begin.coffee
#           ^^ string.regexp.coffee
#             ^ punctuation.definition.string.end.coffee
#              ^ constant.language.flags.coffee
#               ^ punctuation.separator.sequence.coffee
#                 ^^^ meta.string.coffee string.quoted.double.coffee

###[ VARIABLES ]###############################################################

  [object.variable] = 0
# ^ punctuation.section.brackets.begin.coffee
#  ^^^^^^ variable.other.object.coffee
#        ^ punctuation.accessor.dot.coffee
#         ^^^^^^^^ variable.other.member.coffee
#                 ^ punctuation.section.brackets.end.coffee
#                   ^ keyword.operator.assignment.coffee
#                     ^ meta.number.integer.decimal.coffee constant.numeric.value.coffee

  @variable
# ^^^^^^^^^ variable.other.readwrite.instance.coffee
# ^ punctuation.definition.variable.coffee

###[ JSX ]#####################################################################

  <Component attrib="va{@lue}">
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.jsx.coffee meta.tag.coffee
# ^ punctuation.definition.tag.begin.coffee
#  ^^^^^^^^^ entity.name.tag.component.coffee
#            ^^^^^^^^^^^^^^^^^ meta.attribute-with-value.coffee
#            ^^^^^^ entity.other.attribute-name.coffee
#                  ^ punctuation.separator.key-value.coffee
#                   ^^^ meta.string.coffee string.quoted.double.coffee
#                      ^^^^^^ meta.string.coffee meta.interpolation.coffee
#                      ^ punctuation.section.interpolation.begin.coffee
#                       ^^^^ source.coffee.embedded.jsx variable.other.readwrite.instance.coffee
#                           ^ punctuation.section.interpolation.end.coffee
#                            ^ meta.string.coffee string.quoted.double.coffee punctuation.definition.string.end.coffee
#                             ^ punctuation.definition.tag.end.coffee
    <h1>Text {# comment}!</h1>
#   ^^^^ meta.jsx.coffee meta.tag.coffee
#   ^ punctuation.definition.tag.begin.coffee
#    ^^ entity.name.tag.coffee
#      ^ punctuation.definition.tag.end.coffee
#       ^^^^^ meta.jsx.coffee - meta.interpolation
#            ^^^^^^^^^^^ meta.jsx.coffee meta.interpolation.coffee comment.block.coffee
#            ^^ punctuation.definition.comment.begin.coffee
#                      ^ punctuation.definition.comment.end.coffee
#                       ^ meta.jsx.coffee - meta.interpolation
#                        ^^^^^ meta.jsx.coffee meta.tag.coffee
#                        ^^ punctuation.definition.tag.begin.coffee
#                          ^^ entity.name.tag.coffee
#                            ^ punctuation.definition.tag.end.coffee
  </Component>
# ^^^^^^^^^^^^ meta.jsx.coffee meta.tag.coffee
# ^^ punctuation.definition.tag.begin.coffee
#   ^^^^^^^^^ entity.name.tag.component.coffee
#            ^ punctuation.definition.tag.end.coffee
#             ^ - meta.jsx - meta.tag

  <EmailInput
    {# THIS IS A GOOD COMMENT }
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.jsx.coffee meta.tag.coffee meta.attribute-with-value.coffee meta.interpolation.coffee comment.block.coffee
    {...@props}
#   ^^^^^^^^^^^ meta.jsx.coffee meta.tag.coffee meta.attribute-with-value.coffee meta.interpolation.coffee
  />
# ^^ meta.jsx.coffee meta.tag.coffee punctuation.definition.tag.end.coffee
#   ^ - meta.jsx - meta.tag
