import os
from urllib.parse import urlsplit, urlunsplit, urlencode
import datetime
from typing import List, Mapping, Any

def search_highlights(result: List[Mapping[str, Any]]) -> List[Mapping[str, dict]]:
    """Prepare the most useful pieces of information for users on the search results page."""
    search_highlights = list()
    for name in ["description", "publisher name", "date published"]:
        value = result[0].get(name)
        value_type = "str"

        # Parse a date if it's a date. All dates expected isoformat
        if name == "date published":
            value = datetime.datetime.fromisoformat(value)
            value_type = "date"
        elif name == "tags":
            value = ", ".join(value)

        # Add the value to the list
        search_highlights.append(
            {
                "name": name,
                "title": name.capitalize(),
                "value": value,
                "type": value_type,
            }
        )
    return search_highlights

def title(result):
    """The title for this Globus Search subject"""
    return result[0]["name"]

def globus_app_link(result):
    """A Globus Webapp link for the transfer/sync button on the detail page"""
    url = result[0]["url"]
    parsed = urlsplit(url)
    query_params = {
        "origin_id": parsed.netloc,
        "origin_path": os.path.dirname(parsed.path),
    }
    return urlunsplit(
        ("https", "app.globus.org", "file-manager", urlencode(query_params), "")
    )

def https_url(result):
    """Add a direct download link to files over HTTPS"""
    path = urlsplit(result[0]["url"]).path
    return urlunsplit(("https", "g-71c9e9.10bac.8443.data.globus.org", path, "", ""))

