| SYNTAX TEST "CoffeeScript Literate.sublime-syntax"

# Heading
| <- meta.block-level.markdown markup.heading.markdown punctuation.definition.heading.markdown
|^^^^^^^^^ meta.block-level.markdown markup.heading.markdown


    class App.Router extends Snakeskin.Router
      errorRoutes: {
        '404': 'fourOhFour',
        '500': 'fiveHundred'
      }
      index: () =>
        @ensureData((data) =>
          @_parseDates(data, ['trending', 'new', 'top'])
          App.layout.renderExchange('index', data, ['index', 'search'])
        )
