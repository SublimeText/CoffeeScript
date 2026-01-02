| SYNTAX TEST "CoffeeScript Literate.sublime-syntax"

# Heading
| <- markup.heading.1.markdown punctuation.definition.heading.begin.markdown
|^^^^^^^^^ text.html.markdown.litcoffee markup.heading.1.markdown

# Indendet Code Block

    class App.Router extends Snakeskin.Router
    | <- meta.embedded.litcoffee source.coffee.embedded.markdown meta.class.coffee keyword.declaration.class.coffee
    |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.embedded.litcoffee source.coffee.embedded.markdown meta.class
      index: () =>
        @ensureData((data) =>
          @_parseDates(data, ['trending', 'new', 'top'])
          App.layout.renderExchange('index', data, ['index', 'search'])
        )

- In list items

      class App.Router extends Snakeskin.Router
      | <- markup.list.unnumbered.markdown meta.embedded.litcoffee source.coffee.embedded.markdown meta.class.coffee keyword.declaration.class.coffee
      |^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ markup.list.unnumbered.markdown meta.embedded.litcoffee source.coffee.embedded.markdown meta.class
        index: () =>
          @ensureData((data) =>
            @_parseDates(data, ['trending', 'new', 'top'])
            App.layout.renderExchange('index', data, ['index', 'search'])
          )

> Not in block quotes
>
>     class App.Router extends Snakeskin.Router
|     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ markup.quote.markdown markup.raw.block.markdown - source.coffee

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

```coffee
| <- text.html.markdown.litcoffee meta.code-fence.definition.begin.markdown-gfm punctuation.definition.raw.code-fence.begin.markdown
|^^^^^^^^ text.html.markdown.litcoffee meta.code-fence.definition.begin.markdown-gfm
|^^ punctuation.definition.raw.code-fence.begin.markdown
|  ^^^^^^ constant.other.language-name.markdown

| <- text.html.markdown.litcoffee meta.code-fence.body.markdown.markdown-gfm markup.raw.code-fence.coffee.markdown-gfm source.coffee
```
| <- text.html.markdown.litcoffee meta.code-fence.definition.end.markdown-gfm punctuation.definition.raw.code-fence.end.markdown
|^^ text.html.markdown.litcoffee meta.code-fence.definition.end.markdown-gfm punctuation.definition.raw.code-fence.end.markdown
