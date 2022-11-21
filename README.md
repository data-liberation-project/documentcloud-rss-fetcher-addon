# DocumentCloud Add-On: RSS Document Fetcher 

This [DocumentCloud add-on](https://www.muckrock.com/news/archives/2022/mar/05/documentcloud-add-ons/) will monitor an RSS/Atom feed for documents and upload them to your DocumentCloud account. 

__Note__: For now, this Add-On expects that each feed entry's `<link>` element will point to PDF and that its `<title>` element will indicate the PDF's title.

This repository is forked from [`MuckRock/documentcloud-scraper-addon`](https://github.com/MuckRock/documentcloud-scraper-addon) and reuses much of its code.

## Setup

To use this add-on for your own DocumentCloud project, please follow the instructions in [`MuckRock/documentcloud-scraper-addon`](https://github.com/MuckRock/documentcloud-scraper-addon). (Step 7, however, is not required.)

## Potential future improvements

- Re-add the extension detection from `documentcloud-scraper-addon`, to enable uploading of non-PDF files.
- Re-add title detection from `documentcloud-scraper-addon`, and give the user the option to use the feed entry's `<title>` element or the detected title.
- Allow user to pass a regular expression or CSS selector instead of relying on each entry's `<link>` element.

## Questions

Open an issue in this repository or email Jeremy Singer-Vine at `jsvine@gmail.com`.
