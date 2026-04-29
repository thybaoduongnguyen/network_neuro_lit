# Literature Network Visualizer

Interactive citation network for academic literature review. Add papers manually in one Python file — run one script — get a self-contained HTML visualization.

## What it does

- Visualizes papers as nodes in a force-directed network
- Shows "responds to / cites" relationships as directed edges
- Node size = how many papers in your corpus cite it (bigger = more central)
- Node color = role (gold: cited by others · blue: responds to another · purple: standalone)
- Click any node for full paper details in the side panel

## Setup

```bash
# No dependencies needed beyond the standard library + jinja2
pip install jinja2

# Clone / download the repo, then:
python generate.py

# Open the output in your browser:
open output/literature_network.html
```

## How to add papers

Open **`data/papers.py`** and add a block to the `PAPERS` list:

```python
{
    "id":          "@lastname2024",         # unique citekey, always starts with @
    "title":       "Full paper title",
    "author":      "Last, F. & Other, A.",
    "year":        2024,
    "journal":     "Journal Name",
    "type":        "Perspective article",   # Opinion / Review / Comment / Commentary / etc.
    "doi":         "https://doi.org/...",   # or just the DOI string
    "keywords":    ["keyword1", "keyword2"],
    "background":  "Disciplinary background of authors",
    "context":     "US / Europe / Global",
    "react_to":    None,                    # "@othercitekey" or ["@key1", "@key2"] or None
    "notes":       "Any personal notes",    # appears in the visualization panel
},
```

### Connections (`react_to`)

This is how you encode citation relationships:

```python
# This paper responds to one other paper:
"react_to": "@cubelli2018a",

# This paper responds to multiple papers:
"react_to": ["@webb2022", "@ricard2023"],

# No direct response relationship:
"react_to": None,
```

Then run `python generate.py` again. That's it.

## File structure

```
lit-network/
├── data/
│   └── papers.py          ← Edit this file to add papers
├── output/
│   └── literature_network.html   ← Generated output (open in browser)
├── generate.py            ← Run this to regenerate
└── README.md
```

## Tips

- You don't need to fill in every field — use `None` for anything you don't have yet
- Papers listed in `react_to` that aren't in `PAPERS` will still show as edges (with a warning), so you can reference external works
- The `notes` field is for your own annotations — useful for thesis writing
- Re-run `generate.py` any time you add papers; the HTML is fully self-contained (no server needed)
