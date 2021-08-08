from typing import Dict, Tuple

__all__ = [
    "INPUT_FORMATS",
    "OUTPUT_FORMATS",
]


FormatDefinition = Tuple[str, str, str]


# Does not include stuff like HTML, where the descriptive text varies
# between input and output.
COMMON_FORMAT_DEFINITIONS: Dict[str, FormatDefinition] = {
    "bibtex": "BibTeX bibliography",
    "biblatex": "BibLaTeX bibliography",
    "commonmark": ("text/markdown", "md", "CommonMark Markdown"),
    "commonmark_x": "CommonMark Markdown with extensions",
    "csljson": "CSL JSON bibliography",
    "docx": ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docx", "Word docx"),
    "dokuwiki": "DokuWiki markup",
    "haddock": "Haddock markup",
    "ipynb": "Jupyter notebook",
    "gfm": ("text/markdown", "md", "GitHub-Flavored Markdown"),
    "jira": "Jira/Confluence wiki markup",
    "json": ("application/json", "json", "JSON version of native AST"),
    "latex": ("text/x-tex", "tex", "LaTeX"),
    "man": "roff man",
    "markdown": ("text/markdown", "md", "Pandoc's Markdown"),
    "markdown_mmd": ("text/plain", "txt", "MultiMarkdown"),
    "markdown_phpextra": "PHP Markdown Extra",
    "markdown_strict": ("text/markdown", "md", "original unextended Markdown"),
    "mediawiki": "MediaWiki markup",
    "muse": "Muse",
    "native": "native Haskell",
    "odt": ("application/vnd.oasis.opendocument.text", "odt", "OpenOffice text document"),
    "opml": "OPML",
    "org": "Emacs Org mode",
    "rst": ("text/x-rst", "rst", "reStructuredText"),
    "textile": "Textile",
}

INPUT_FORMATS: Dict[str, FormatDefinition] = {
    **COMMON_FORMAT_DEFINITIONS,

    "creole": "Creole 1.0",
    "csv": ("text/csv", "csv", "CSV table"),
    "docbook": "DocBook",
    "epub": "EPUB",
    "fb2": "FictionBook2 e-book",
    "html": ("text/html", "html", "HTML"),
    "jats": "JATS XML",
    "t2t": "txt2tags",
    "tikiwiki": "TikiWiki markup",
    "twiki": "TWiki markup",
    "vimwiki": "Vimwiki",
}

# TODO: mime types, file extensions
OUTPUT_FORMATS: Dict[str, FormatDefinition] = {
    **COMMON_FORMAT_DEFINITIONS,

    "asciidoc": "AsciiDoc",
    "asciidoctor": "AsciiDoctor",
    "beamer": "LaTeX beamer slide show",
    "context": "ConTeXt",
    "docbook": "DocBook 4",
    "docbook4": "DocBook 4",
    "docbook5": "DocBook 5",
    "epub": "EPUB v3 book",
    "epub3": "EPUB v3 book",
    "epub2": "EPUB v2",
    "fb2": "FictionBook2 e-book",
    "html": ("text/html", "html", "HTML, i.e. HTML5/XHTML polyglot markup"),
    "html5": ("text/html", "html", "HTML, i.e. HTML5/XHTML polyglot markup"),
    "html4": ("text/html", "html", "XHTML 1.0 Transitional"),  # TODO: XHTML mime type?
    "icml": "InDesign ICML",
    "jats": "JATS XML, Archiving and Interchange Tag Set",
    "jats_archiving": "JATS XML, Archiving and Interchange Tag Set",
    "jats_articleauthoring": "JATS XML, Article Authoring Tag Set",
    "jats_publishing": "JATS XML, Journal Publishing Tag Set",
    "ms": "roff ms",
    "opendocument": "OpenDocument",
    "pdf": ("application/pdf", "pdf", "PDF"),
    "plain": ("text/plain", "txt", "plain text"),
    "pptx": ("application/vnd.openxmlformats-officedocument.presentationml.presentation", "pptx",
             "PowerPoint slide show"),
    "rtf": ("application/rtf", "rtf", "Rich Text Format"),
    "texinfo": "GNU Texinfo",
    "slideous": "Slideous HTML and JavaScript slide show",
    "slidy": "Slidy HTML and JavaScript slide show",
    "dzslides": "DZSlides HTML5 + JavaScript slide show",
    "revealjs": "reveal.js HTML5 + JavaScript slide show",
    "s5": "S5 HTML and JavaScript slide show",
    "tei": "TEI Simple",
    "xwiki": "XWiki markup",
    "zimwiki": "ZimWiki markup",
}
