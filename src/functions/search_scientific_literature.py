from serpapi import GoogleSearch
import os
import json

def search_scientific_literature(question, 
                                 source="google_scholar", 
                                 n_search_results=3):
    all_sources = {
        "pubmed": "pubmed.ncbi.nlm.nih.gov",
        "bioarchive": "biorxiv.org",
        "neurips": "proceedings.neurips.cc",
        "google_scholar": "scholar.google.com"
    }
    chosen_source = all_sources[source]

    ### DEFINE GOOGLE SEARCH
    prompt = f"{question} site:{chosen_source}"
    params = {
        "q": prompt,
        "engine": "google",
        "api_key": os.getenv("SERPAPI_API_KEY")
    }
    search = GoogleSearch(params)
    search_results = search.get_dict()

    ### PARSE RESULTS TO JSON
    final_results = {}
    try:
        for i in search_results['organic_results'][:n_search_results]:
            response_value = {
                    'snippet': i.get('snippet', ''),
                    'markdown_link': f"[{i.get('title', 'Link')}]({i.get('link', '')})"
            }
            title = i.get('title', None)
            if title:
                final_results[title] = response_value
        return final_results
    except:
        return "No results were found."
    #     return "No results were found"