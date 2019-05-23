# How to structure your site

Here are some examples on how to structure your markdown files so that picopage can parse them.

## The most basic setup
```
my-page
|- somefile.md
```
If you run ``$ picopage my-page`` you will get a website containing nothing but the content of ``somefile.md`` in 
a single HTML file.

```
my-page
|- somefile.md
|- otherfile.md
|- even-more-files.md
```

Similarly this setup will also produce a single, self contained HTML file which serves as the index page of your website.

## Adding pages to your website
```
my-page
|- somefile.md
|- otherfile.md
|- even-more-files.md
|- my-page
|   |- topic.md
|   |- more-content.md
```
Because a folder that contains ``.md`` files was added picopage recognizes it as a page for your website.
The three files at the top level will still be generated into the start page for your website.
Additionally a new sub-page with the name ``my-page`` will be created, 
containing the contents of ``topic.md`` and ``more-content.md``

There is no limit to the number of pages that can be added to your site this way.

## Sub-Sub pages

**Crating sub-pages under normal pages is not supported by picopage in this version.**

See: [Features](../#features)


