# PicoPage

A minimalistic Website generator.

PicoPage creates simple static websites from markdown files.

## Directory Structure

```
my_site
|- site.config (main website config)
|- navigation.config (definition of the nav bar)
|- footer.config (definition of the footer)
|- pages (holds all sites)
|   |- page01.md
|   |- page02.md
|   |- ...
|- resources (resource files for the site)
|   |- site.css
|   |- site.js
|   |- favicon.ico
|- static (images, documents, ...)
|   |- image.png
|   |- document.doc
|   |- my_files
|       |- file01.txt
|       |- ...
|- publish (holds the compiled HTML files)
|   |- index.html
|   |- ...
```