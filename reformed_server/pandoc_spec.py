from typing import Dict, Tuple

__all__ = [
    "INPUT_FORMATS",
    "OUTPUT_FORMATS",
]


FormatDefinition = Tuple[str, str, str]


# Does not include stuff like HTML, where the descriptive text varies
# between input and output.
COMMON_FORMAT_DEFINITIONS: Dict[str, FormatDefinition] = {
    # Disabled because we don't currently support additional file uploads for --bibliography
    # "bibtex": "BibTeX bibliography",
    # "biblatex": "BibLaTeX bibliography",

    "commonmark": ("text/markdown", "md", "CommonMark Markdown"),
    "commonmark_x": ("text/markdown", "md", "CommonMark Markdown with extensions"),

    # Disabled because we don't currently support additional file uploads for --csl
    # "csljson": "CSL JSON bibliography",

    "docx": ("application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docx", "Word docx"),
    "dokuwiki": ("text/plain", "txt", "DokuWiki markup"),
    "fb2": ("text/xml", "fb2", "FictionBook2 e-book"),
    "haddock": ("text/plain", "txt", "Haddock markup"),
    "ipynb": ("application/x-ipynb+json", "ipynb", "Jupyter notebook"),
    "gfm": ("text/markdown", "md", "GitHub-Flavored Markdown"),
    "jira": ("text/plain", "txt", "Jira/Confluence wiki markup"),
    "json": ("application/json", "json", "JSON version of native AST"),
    "latex": ("text/x-tex", "tex", "LaTeX"),
    "man": ("application/x-troff-man", "man", "roff man"),
    "markdown": ("text/markdown", "md", "Pandoc's Markdown"),
    "markdown_mmd": ("text/plain", "txt", "MultiMarkdown"),
    "markdown_phpextra": ("text/markdown", "txt", "PHP Markdown Extra"),
    "markdown_strict": ("text/markdown", "md", "original unextended Markdown"),
    "mediawiki": ("text/plain", "txt", "MediaWiki markup"),
    "muse": ("text/plain", "muse", "Muse"),
    "native": ("text/x-haskell", "hs", "native Haskell"),
    "odt": ("application/vnd.oasis.opendocument.text", "odt", "OpenOffice text document"),
    "opml": ("text/x-opml", "opml", "OPML"),
    "org": ("text/org", "org", "Emacs Org mode"),
    "rst": ("text/x-rst", "rst", "reStructuredText"),
    "textile": ("text/x-textile", "textile", "Textile"),
}

INPUT_FORMATS: Dict[str, FormatDefinition] = {
    **COMMON_FORMAT_DEFINITIONS,

    "creole": ("text/plain", "txt", "Creole 1.0"),
    "csv": ("text/csv", "csv", "CSV table"),
    "docbook": ("application/sgml", "dbk", "DocBook"),
    "epub": ("application/epub+zip", "epub", "EPUB"),
    "html": ("text/html", "html", "HTML"),

    # Unsure about how this is handled
    # "jats": "JATS XML",

    "t2t": ("text/plain", "txt", "txt2tags"),
    "tikiwiki": ("text/plain", "txt", "TikiWiki markup"),
    "twiki": ("text/plain", "txt", "TWiki markup"),
    "vimwiki": ("text/plain", "txt", "Vimwiki"),
}

# TODO: mime types, file extensions
OUTPUT_FORMATS: Dict[str, FormatDefinition] = {
    **COMMON_FORMAT_DEFINITIONS,

    "asciidoc": ("text/plain", "adoc", "AsciiDoc"),
    "asciidoctor": ("text/plain", "adoc", "AsciiDoctor"),
    "beamer": ("text/x-tex", "tex", "LaTeX beamer slide show"),
    "context": ("text/x-tex", "tex", "ConTeXt"),
    "docbook": ("application/sgml", "dbk", "DocBook 4"),
    "docbook4": ("application/sgml", "dbk", "DocBook 4"),
    "docbook5": ("application/sgml", "dbk", "DocBook 5"),
    "epub": ("application/epub+zip", "epub", "EPUB v3 book"),
    "epub3": ("application/epub+zip", "epub", "EPUB v3 book"),
    "epub2": ("application/epub+zip", "epub", "EPUB v2"),
    "html": ("text/html", "html", "HTML, i.e. HTML5/XHTML polyglot markup"),
    "html5": ("text/html", "html", "HTML, i.e. HTML5/XHTML polyglot markup"),
    "html4": ("application/xhtml+xml", "html", "XHTML 1.0 Transitional"),

    # "icml": ("application/zip", "icml", "InDesign ICML"),  # TODO: Cannot find the mime type on this guy

    # Unsure about how these are handled
    # "jats": "JATS XML, Archiving and Interchange Tag Set",
    # "jats_archiving": "JATS XML, Archiving and Interchange Tag Set",
    # "jats_articleauthoring": "JATS XML, Article Authoring Tag Set",
    # "jats_publishing": "JATS XML, Journal Publishing Tag Set",

    "ms": ("application/x-troff-ms", "ms", "roff ms"),
    "opendocument": ("text/xml", "xml", "OpenDocument"),
    "pdf": ("application/pdf", "pdf", "PDF"),
    "plain": ("text/plain", "txt", "plain text"),
    "pptx": ("application/vnd.openxmlformats-officedocument.presentationml.presentation", "pptx",
             "PowerPoint slide show"),
    "rtf": ("application/rtf", "rtf", "Rich Text Format"),
    "texinfo": ("application/x-texinfo", "texi", "GNU Texinfo"),
    "slideous": ("text/html", "html", "Slideous HTML and JavaScript slide show"),
    "slidy": ("text/html", "html", "Slidy HTML and JavaScript slide show"),
    "dzslides": ("text/html", "html", "DZSlides HTML5 + JavaScript slide show"),
    "revealjs": ("text/html", "html", "reveal.js HTML5 + JavaScript slide show"),
    "s5": ("text/html", "html", "S5 HTML and JavaScript slide show"),

    # Unsure about how this is handled
    # "tei": "TEI Simple",

    "xwiki": ("text/plain", "txt", "XWiki markup"),
    "zimwiki": ("text/plain", "txt", "ZimWiki markup"),
}
