import urllib.parse as urlparse

import feedparser
from documentcloud.addon import AddOn
from documentcloud.constants import BULK_LIMIT
from documentcloud.toolbox import grouper, requests_retry_session
from ratelimit import limits, sleep_and_retry

DOC_CUTOFF = 10
MAX_NEW_DOCS = 10


class Document:
    """Class to hold information about individual documents"""

    def __init__(self, url, title):
        self.url = url.strip()
        self.title = title.strip()

    # https://stackoverflow.com/questions/33049729/
    # how-to-handle-links-containing-space-between-them-in-python
    @property
    def fixed_url(self):
        """Fixes quoting of characters in file names to use with requests"""
        scheme, netloc, path, qs, anchor = urlparse.urlsplit(self.url)
        path = urlparse.quote(path, "/%")
        qs = urlparse.quote_plus(qs, ":&=")
        return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))


class Fetcher(AddOn):
    @sleep_and_retry
    @limits(calls=5, period=1)
    def fetch(self, feed, depth=0):
        """Fetch the feed and look for new documents"""
        print(f"🌐 Fetching {feed}")
        resp = requests_retry_session().get(feed)
        resp.raise_for_status()
        docs = []
        parsed = feedparser.parse(feed)
        for entry in parsed.entries:
            doc = Document(entry.link, entry.title)

            query = f"+project:{self.project} data_url:{doc.fixed_url}"
            found = list(self.client.documents.search(query))

            if found:
                continue

            print("📄 New link:", entry.link)
            docs.append(doc)
            # stop looking for new documents if we hit the max
            if len(docs) >= MAX_NEW_DOCS:
                break

        return docs

    def upload(self, docs):
        if self.data.get("dry_run"):
            return

        for doc_group in grouper(docs, BULK_LIMIT):
            # filter out None's from grouper padding
            doc_group = [d for d in doc_group if d]
            doc_group = [
                {
                    "file_url": d.fixed_url,
                    "source": self.data.get("source"),
                    "title": d.title,
                    "projects": [self.project],
                    # TK re-add below in future versions
                    # "original_extension": d.extension,
                    "access": self.data["access"],
                    "data": {"url": d.fixed_url},
                }
                for d in doc_group
            ]
            resp = self.client.post("documents/", json=doc_group)
            resp.raise_for_status()

    def send_notification(self, subject, message):
        """Send notifications via slack and email"""
        self.send_mail(subject, message)
        hook = self.data.get("slack_webhook")
        if hook:
            requests_retry_session().post(
                hook, json={"text": f"{subject}\n\n{message}"}
            )

    def send_scrape_message(self, new_docs):
        """Alert on new documents"""
        if not self.data.get("notify"):
            return

        src = self.data.get("feed_name", self.data.get("feed"))
        subj = f"Uploaded {len(new_docs)} new documents from {src}"

        body = "\n".join(f"- {d.fixed_url}" for d in new_docs[:DOC_CUTOFF])

        if len(new_docs) > DOC_CUTOFF:
            body += f"\n\n... plus {len(new_docs) - DOC_CUTOFF} more documents"

        self.send_notification(subj, body)

    def set_project(self, user_input):
        try:
            self.project = int(user_input)
        except ValueError:
            project, created = self.client.projects.get_or_create_by_title(user_input)
            self.project = project.id

    def main(self):
        self.set_project(self.data["project"])
        new_docs = self.fetch(self.data["feed"])
        if new_docs:
            self.upload(new_docs)
            self.send_scrape_message(new_docs)


if __name__ == "__main__":
    Fetcher().main()
