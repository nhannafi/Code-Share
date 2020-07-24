from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def colorize(code, language) :
    lexer = get_lexer_by_name(language, stripall=True)

    formatter = HtmlFormatter(
        linenos=True,
        cssclass="source"
    )

    return highlight(code, lexer, formatter)