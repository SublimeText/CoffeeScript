| SYNTAX TEST "CoffeeScript Literate.sublime-syntax"

# Heading
| <- meta.block-level.markdown markup.heading.markdown punctuation.definition.heading.markdown
|^^^^^^^^^ meta.block-level.markdown markup.heading.markdown

# Indendet Code Block

    class App.Router extends Snakeskin.Router
    | <- markup.raw.block.markdown meta.class.coffee storage.type.class.coffee
    |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ markup.raw.block.markdown meta.class.coffee

      @index: () =>
    | ^^^^^^ meta.function.identifier.coffee entity.name.function.coffee
    |       ^^ meta.function.coffee
    |         ^^ meta.function.parameters.coffee
    |           ^^^ meta.function.coffee
    |            ^^ keyword.declaration.function.coffee
        @ensureData((data) =>
          @_parseDates(data, ['trending', 'new', 'top'])
          App.layout.renderExchange('index', data, ['index', 'search'])
        )

> Not in block quotes
>
>     class App.Router extends Snakeskin.Router
|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.block-level.markdown markup.quote.markdown - markdup.raw

# https://github.com/SublimeText/CoffeeScript/issues/203

This is a test showcasing that multiline string interpolation is broken. Copy this post
into a .litcoffee file and open it in Sublime to see the breakage.

    foo = 69
    baz = 420

    bar = "This is the value of foo: #{
    |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.string.coffee string.quoted.double.coffee
    |                                ^^^ meta.string.coffee meta.embedded.coffee source.coffee.embedded.source
      foo
    } and this is another variable, baz: #{
    | <- meta.string.coffee meta.embedded.coffee source.coffee.embedded.source punctuation.section.embedded.coffee
    |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.string.coffee string.quoted.double.coffee
    |                                    ^^^ meta.string.coffee meta.embedded.coffee source.coffee.embedded.source
      baz
    }"
    | <- meta.string.coffee meta.embedded.coffee source.coffee.embedded.source punctuation.section.embedded.coffee
    |^ meta.string.coffee string.quoted.double.coffee punctuation.definition.string.end.coffee
    | ^ - meta.string - string

    nowThis.isInterpretedAs 'string'
    | <- meta.path.coffee variable.other.object.coffee
    |^^^^^^^^^^^^^^^^^^^^^^ meta.path.coffee
    |                       ^^^^^^^^ meta.string.coffee string.quoted.single.coffee

...even this markdown is as well. :(
| <- meta.paragraph.markdown
|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.paragraph.markdown
