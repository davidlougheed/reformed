# reformed

[![Lint Status](https://github.com/davidlougheed/reformed/workflows/Lint/badge.svg?branch=main)](https://github.com/davidlougheed/reformed/actions?query=workflow%3ALint+branch%3Amain)

Document format conversion service based on Pandoc.


## Usage

The API specification for the Reformed server is as follows:

### `GET /api/v1/formats`: Lists available input and output formats for documents

#### Response

```js
{
  "input": {
    "commonmark": {
      "mime": "text/markdown",
      "ext": "md",
      "detail": "CommonMark Markdown"
    },
    "docx": {
      "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "ext": "docx",
      "detail": "Word docx"
    },
    // ...
  },
  "output": {
    "commonmark": {
      "mime": "text/markdown",
      "ext": "md",
      "detail": "CommonMark Markdown"
    },
    "docx": {
      "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "ext": "docx",
      "detail": "Word docx"
    },
    // ...
    "latex": {
      "mime": "text/x-tex",
      "ext": "tex",
      "detail": "LaTeX"
    },
    // ...
  }
}
```


### `POST /api/v1/from/[input format]/to/[output format]`: Converts a document from one format to another

#### Request

The request should be made with the `multipart/form-data` encoding.

##### Parameters

The request parameters are as follows:

###### File `document`

Document to convert. For example, to convert a `docx` file to a `pdf`
file, the following cURL command will work:

```bash
curl -X POST -F 'document=@test.docx' http://localhost:8000/api/v1/from/docx/to/pdf > test.pdf
```

###### Boolean flags

This endpoint supports the following Pandoc standalone flags:
`ascii`, `html-q-tags`, `incremental`, `listings`, `no-highlight`, `preserve-tabs`, 
`reference-links`, `section-divs`, `standalone`, `strip-comments`, `toc`.

If the form value for a given flag is anything except a blank string, it will be added to 
the Pandoc call.

See [the Pandoc manual](https://pandoc.org/MANUAL.html) for more information on these
flags' effects.

###### Flags with choices

This endpoint supports the following Pandoc flags which have specific choices:
`eol`, `markdown-headings`, `reference-location`, `top-level-division`, `track-changes`, 
`wrap`.

If the form value for a given flag is valid, it will be added to the Pandoc call.

See [the Pandoc manual](https://pandoc.org/MANUAL.html) for more information on these
flags' effects.

###### Integer `columns`

If specified and a valid integer, this will add the `--columns=XX` option to the Pandoc 
call. The value is bounded to `1 <= columns <= 300` by Reformed.

See [the Pandoc manual's description](https://pandoc.org/MANUAL.html#option--columns) for more.

###### Integer `dpi`

If specified and a valid integer, this will add the `--dpi=XX` option to the Pandoc call.
The value is bounded to `36 <= dpi <= 600` by Reformed.

See [the Pandoc manual's description](https://pandoc.org/MANUAL.html#option--dpi) for more.

###### Integer `toc-depth`

If specified and a valid integer, this will add the `--toc-depth=XX` option to the Pandoc 
call. The value is bounded to `1 <= toc-depth <= 6` by Reformed.

See [the Pandoc manual's description](https://pandoc.org/MANUAL.html#option--toc-depth) for more.

#### Response

A binary stream with the MIME type specified in the list of formats. 
`Content-Disposition` is forced to be an `attachment` to prevent files from rendering in
the browser.

If an error is encountered, this will instead be a JSON response with an `error` key 
specifying what went wrong.


## Configuration

A few configuration environment variables are available for the Reformed server,
listed here with their default values:

```bash
# Maximum buffer size for requests, in bytes - mostly useful for controlling file uploads
# Defaults to 25 MiB
REFORMED_MAX_BUFFER_SIZE=26214400

# Port to accept requests on
REFORMED_PORT=8000

# Number of worker processes to start
REFORMED_WORKERS=2
```


## Deploying

Main-branch and tagged releases are both automatically published as Docker images to the
GitHub Container Registry. These images can be run in the standard fashion as a daemon, 
and expose a Tornado HTTP server on port 8000.

See [the package listing](https://github.com/davidlougheed/reformed/pkgs/container/reformed)
for more information on pulling the image.
