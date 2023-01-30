# DocumentCloud Add-On: RSS Document Fetcher 

This [DocumentCloud add-on](https://www.muckrock.com/news/archives/2022/mar/05/documentcloud-add-ons/) will monitor an RSS/Atom feed for documents and upload them to your DocumentCloud account. 

__Note__: For now, this Add-On expects that each feed entry's `<link>` element will point to PDF and that its `<title>` element will indicate the PDF's title.

This repository is forked from [`MuckRock/documentcloud-scraper-addon`](https://github.com/MuckRock/documentcloud-scraper-addon) and reuses much of its code.

## Setup
### 1) Create your accounts if needed

First, you'll need to have a verified MuckRock account. If you've ever uploaded documents to DocumentCloud before, you're already set. If not, [register a free account here](https://accounts.muckrock.com/accounts/signup/?intent=squarelet) and then [request verification](https://airtable.com/shrZrgdmuOwW0ZLPM).

### 2) Create a DocumentCloud project for your documents
Next, log in to DocumentCloud and create a new project to store the documents that this Add-On will upload documents to. <br>
![An image of the project create button in DocumentCloud](https://user-images.githubusercontent.com/136939/159478474-53a770e5-a826-44f1-bb80-b1844bf4c263.png) <br>
Click on your newly created project on the left-hand side of the screen, and note the numbers to the right of its name — this is the project ID, in this example, 207354. <br>
![Screen Shot 2022-03-22 at 8 08 11 AM](https://user-images.githubusercontent.com/136939/159478630-c6cbcb24-308c-4b0e-a42c-f10cf2653836.png)
<br>

### 3) Run the Add-On from within DocumentCloud
Click on the Add-Ons dropdown menu -> "Browse All Add-Ons" -> "RSS Document Fetcher" -> Click the inactive button to mark the Add-On as active and finally hit Done. Click on the Add-Ons dropdown menu once more and click on the RSS Document Fetcher which will now be active. 

## Potential future improvements

- Re-add the extension detection from `documentcloud-scraper-addon`, to enable uploading of non-PDF files.
- Re-add title detection from `documentcloud-scraper-addon`, and give the user the option to use the feed entry's `<title>` element or the detected title.
- Allow user to pass a regular expression or CSS selector instead of relying on each entry's `<link>` element.

## Questions

Open an issue in this repository or email Jeremy Singer-Vine at `jsvine@gmail.com`.
