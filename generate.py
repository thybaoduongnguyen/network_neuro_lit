"""
generate.py — Literature Network Visualizer
============================================
Run this script to generate an interactive HTML network from your papers.

Usage:
    python generate.py

Output:
    output/literature_network.html   ← open this in any browser

Requirements:
    pip install jinja2
    (No other dependencies — the HTML file is self-contained)
"""

import json
import os
import sys
from pathlib import Path

# ── Load papers from data file ───────────────────────────────────────────────

sys.path.insert(0, str(Path(__file__).parent))
from data.papers import PAPERS


def build_graph():
    """Convert PAPERS list into nodes + edges for the visualization."""
    nodes = []
    edges = []
    paper_ids = {p["id"] for p in PAPERS}

    for p in PAPERS:
        # Normalize react_to to always be a list
        react_to = p.get("react_to")
        if react_to is None:
            react_to = []
        elif isinstance(react_to, str):
            react_to = [react_to]

        nodes.append({
            "id":         p["id"],
            "title":      p.get("title", ""),
            "author":     p.get("author", ""),
            "year":       p.get("year"),
            "journal":    p.get("journal", ""),
            "type":       p.get("type", ""),
            "doi":        p.get("doi", ""),
            "keywords":   p.get("keywords", []),
            "background": p.get("background", ""),
            "context":    p.get("context", ""),
            "react_to":   react_to,
            "notes":      p.get("notes", ""),
        })

        for target in react_to:
            if target not in paper_ids:
                print(f"  ⚠  Warning: '{p['id']}' responds to '{target}', "
                      f"but '{target}' is not in PAPERS. Edge will still be drawn.")
            edges.append({"from": p["id"], "to": target})

    return nodes, edges


def generate_html(nodes, edges, output_path):
    """Inject data into the HTML template and write to disk."""
    data_json = json.dumps({"papers": nodes, "edges": edges}, ensure_ascii=False, indent=2)
    html = HTML_TEMPLATE.replace("__DATA_JSON__", data_json)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(html, encoding="utf-8")
    print(f"✓  Generated: {output_path}")
    print(f"   {len(nodes)} papers · {len(edges)} citation edges")


# ── HTML template (self-contained, no server needed) ─────────────────────────

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Literature Network</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&display=swap');
  :root {
    --bg:#0e0e12;--surface:#15151c;--border:#2a2a38;
    --accent:#c8a96e;--accent2:#7b9ea8;--accent3:#a87ba8;
    --text:#e8e4dc;--muted:#7a7880;
    --node-core:#c8a96e;--node-react:#7b9ea8;--node-standalone:#a87ba8;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--text);font-family:'DM Mono',monospace;height:100vh;overflow:hidden;display:flex;flex-direction:column}
  header{padding:16px 24px 12px;border-bottom:1px solid var(--border);display:flex;align-items:baseline;gap:20px;flex-shrink:0}
  header h1{font-family:'DM Serif Display',serif;font-size:1.3rem;color:var(--accent)}
  header p{font-size:.7rem;color:var(--muted);letter-spacing:.08em;text-transform:uppercase}
  .legend{margin-left:auto;display:flex;gap:16px;align-items:center}
  .legend-item{display:flex;align-items:center;gap:6px;font-size:.65rem;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
  .legend-dot{width:10px;height:10px;border-radius:50%}
  .main{display:flex;flex:1;overflow:hidden}
  #network-area{flex:1;position:relative;overflow:hidden}
  svg{width:100%;height:100%}
  .node circle{cursor:pointer}
  .node:hover circle{filter:brightness(1.3)}
  .node text{pointer-events:none;font-family:'DM Mono',monospace;font-size:9px;fill:var(--text);opacity:.8}
  .link{stroke:var(--accent);stroke-opacity:.6;stroke-width:1.5;fill:none;marker-end:url(#arrowhead)}
  .link.dimmed{stroke-opacity:.08}
  .node.dimmed circle{opacity:.15}
  .node.dimmed text{opacity:.08}
  #panel{width:340px;border-left:1px solid var(--border);overflow-y:auto;flex-shrink:0;background:var(--surface)}
  .panel-empty{padding:40px 20px;color:var(--muted);font-size:.72rem;text-align:center;line-height:1.8}
  #panel-content{padding:20px;display:none}
  .paper-type-tag{font-size:.62rem;text-transform:uppercase;letter-spacing:.1em;color:var(--accent);border:1px solid var(--accent);padding:2px 8px;display:inline-block;margin-bottom:10px}
  .paper-title{font-family:'DM Serif Display',serif;font-size:1rem;line-height:1.4;margin-bottom:6px}
  .paper-meta{font-size:.68rem;color:var(--muted);margin-bottom:14px;line-height:1.7}
  .citekey{font-family:'DM Mono',monospace;font-size:.65rem;color:var(--accent3);background:rgba(168,123,168,.1);padding:1px 6px;border-radius:2px}
  .section-label{font-size:.6rem;text-transform:uppercase;letter-spacing:.12em;color:var(--accent2);border-bottom:1px solid var(--border);padding-bottom:4px;margin-bottom:8px;margin-top:16px}
  .section-body{font-size:.7rem;line-height:1.7;color:#b0adb8}
  .conn-badge{display:inline-flex;align-items:center;gap:5px;font-size:.65rem;padding:4px 8px;border-radius:2px;margin:3px 3px 0 0;cursor:pointer}
  .conn-badge.cited-by{background:rgba(123,158,168,.15);color:var(--accent2);border:1px solid rgba(123,158,168,.3)}
  .conn-badge.reply-to{background:rgba(200,169,110,.15);color:var(--accent);border:1px solid rgba(200,169,110,.3)}
  .conn-badge:hover{opacity:.7}
  .tabs{display:flex;border-bottom:1px solid var(--border);flex-shrink:0}
  .tab{flex:1;padding:12px 8px;font-size:.65rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);cursor:pointer;text-align:center;border-bottom:2px solid transparent;transition:all .2s}
  .tab.active{color:var(--accent);border-bottom-color:var(--accent)}
  .tab-panel{display:none}
  .tab-panel.active{display:block}
  #list-view{padding:12px;display:flex;flex-direction:column;gap:6px}
  .list-item{padding:10px 12px;border:1px solid var(--border);border-radius:2px;cursor:pointer;transition:border-color .2s,background .2s}
  .list-item:hover{border-color:var(--accent);background:rgba(200,169,110,.05)}
  .list-item-title{font-family:'DM Serif Display',serif;font-size:.82rem;line-height:1.3;margin-bottom:3px}
  .list-item-meta{font-size:.62rem;color:var(--muted)}
  .journal-tag{font-size:.6rem;color:var(--accent2)}
  .doi-link{font-size:.65rem;color:var(--accent2);text-decoration:none;word-break:break-all}
  .doi-link:hover{text-decoration:underline}
  .keyword-pill{display:inline-block;font-size:.58rem;padding:1px 6px;border:1px solid var(--border);border-radius:10px;margin:2px 2px 0 0;color:var(--muted)}
  .tooltip{position:absolute;background:var(--surface);border:1px solid var(--border);padding:8px 12px;font-size:.68rem;pointer-events:none;max-width:220px;line-height:1.6;color:var(--text);z-index:100;opacity:0;transition:opacity .15s}
  .zoom-controls{position:absolute;bottom:16px;left:16px;display:flex;flex-direction:column;gap:4px}
  .zoom-btn{width:30px;height:30px;background:var(--surface);border:1px solid var(--border);color:var(--text);font-size:1rem;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:border-color .2s}
  .zoom-btn:hover{border-color:var(--accent);color:var(--accent)}
  .hint{position:absolute;bottom:16px;right:16px;font-size:.6rem;color:var(--muted);text-align:right;line-height:1.8;letter-spacing:.04em}
  .stat-bar{display:flex;gap:16px;padding:10px 20px;border-bottom:1px solid var(--border);flex-shrink:0}
  .stat{text-align:center}
  .stat-n{font-family:'DM Serif Display',serif;font-size:1.4rem;color:var(--accent)}
  .stat-l{font-size:.58rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
</style>
</head>
<body>
<header>
  <h1>Literature Network</h1>
  <p id="header-subtitle">citation map</p>
  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:var(--node-core)"></div>Cited by others</div>
    <div class="legend-item"><div class="legend-dot" style="background:var(--node-react)"></div>Responds to another</div>
    <div class="legend-item"><div class="legend-dot" style="background:var(--node-standalone)"></div>Standalone</div>
  </div>
</header>

<div class="main">
  <div id="network-area">
    <svg id="svg"></svg>
    <div class="tooltip" id="tooltip"></div>
    <div class="zoom-controls">
      <button class="zoom-btn" id="zoom-in">+</button>
      <button class="zoom-btn" id="zoom-out">−</button>
      <button class="zoom-btn" id="zoom-reset" style="font-size:.6rem">⊡</button>
    </div>
    <div class="hint">Scroll to zoom · drag to pan<br>Click node for details</div>
  </div>
  <div id="panel">
    <div class="tabs">
      <div class="tab active" data-tab="detail">Detail</div>
      <div class="tab" data-tab="list">All Papers</div>
    </div>
    <div class="tab-panel active" id="tab-detail">
      <div class="panel-empty" id="panel-empty">← Click a node to explore<br>a paper's details &amp; connections</div>
      <div id="panel-content"></div>
    </div>
    <div class="tab-panel" id="tab-list">
      <div id="list-view"></div>
    </div>
  </div>
</div>

<script>
const RAW = __DATA_JSON__;

const paperMap = {};
RAW.papers.forEach(p => paperMap[p.id] = p);

// Build lookup: who cites whom
const citedBy = {};   // id -> list of ids that respond TO it
const respondsTo = {}; // id -> list of ids it responds to
RAW.edges.forEach(e => {
  if (!citedBy[e.to]) citedBy[e.to] = [];
  citedBy[e.to].push(e.from);
  if (!respondsTo[e.from]) respondsTo[e.from] = [];
  respondsTo[e.from].push(e.to);
});

function nodeColor(d) {
  if (citedBy[d.id]?.length) return 'var(--node-core)';
  if (respondsTo[d.id]?.length) return 'var(--node-react)';
  return 'var(--node-standalone)';
}
function nodeRadius(d) {
  return 14 + (citedBy[d.id]?.length || 0) * 5;
}

// Header subtitle
document.getElementById('header-subtitle').textContent =
  `${RAW.papers.length} papers · ${RAW.edges.length} citation edges`;

// Tabs
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
  });
});

// List view
const listView = document.getElementById('list-view');
[...RAW.papers].sort((a,b) => (b.year||0)-(a.year||0)).forEach(p => {
  const div = document.createElement('div');
  div.className = 'list-item';
  div.innerHTML = `<div class="list-item-title">${p.title}</div>
    <div class="list-item-meta">${p.author} · ${p.year||'—'}
    ${p.journal ? `<br><span class="journal-tag">${p.journal}</span>` : ''}</div>`;
  div.addEventListener('click', () => {
    selectPaper(p.id);
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(t=>t.classList.remove('active'));
    document.querySelector('[data-tab="detail"]').classList.add('active');
    document.getElementById('tab-detail').classList.add('active');
  });
  listView.appendChild(div);
});

// Network
const svg = d3.select('#svg');
const area = document.getElementById('network-area');
const W = area.clientWidth, H = area.clientHeight;

svg.append('defs').append('marker')
  .attr('id','arrowhead').attr('viewBox','0 -4 8 8')
  .attr('refX',8).attr('refY',0).attr('markerWidth',6).attr('markerHeight',6).attr('orient','auto')
  .append('path').attr('d','M0,-4L8,0L0,4').attr('fill','var(--accent)');

const g = svg.append('g');
const zoom = d3.zoom().scaleExtent([0.25,3]).on('zoom', e => g.attr('transform', e.transform));
svg.call(zoom);

document.getElementById('zoom-in').addEventListener('click', () => svg.transition().call(zoom.scaleBy, 1.3));
document.getElementById('zoom-out').addEventListener('click', () => svg.transition().call(zoom.scaleBy, 0.77));
document.getElementById('zoom-reset').addEventListener('click', () => svg.transition().call(zoom.transform, d3.zoomIdentity));

const nodes = RAW.papers.map(p => ({...p}));
const links = RAW.edges.map(e => ({...e, source: e.from, target: e.to}));

const sim = d3.forceSimulation(nodes)
  .force('link', d3.forceLink(links).id(d=>d.id).distance(130).strength(0.6))
  .force('charge', d3.forceManyBody().strength(-300))
  .force('center', d3.forceCenter(W/2, H/2))
  .force('collision', d3.forceCollide(d => nodeRadius(d)+14));

const link = g.append('g').selectAll('line').data(links).enter().append('line').attr('class','link');

const node = g.append('g').selectAll('.node').data(nodes).enter().append('g').attr('class','node')
  .call(d3.drag()
    .on('start', (e,d)=>{ if(!e.active) sim.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; })
    .on('drag',  (e,d)=>{ d.fx=e.x; d.fy=e.y; })
    .on('end',   (e,d)=>{ if(!e.active) sim.alphaTarget(0); d.fx=null; d.fy=null; }));

node.append('circle')
  .attr('r', d=>nodeRadius(d))
  .attr('fill', d=>nodeColor(d))
  .attr('fill-opacity', 0.18)
  .attr('stroke', d=>nodeColor(d))
  .attr('stroke-width', 1.5);

node.append('text')
  .attr('text-anchor','middle')
  .attr('dy', d => nodeRadius(d)+12)
  .text(d => d.id.replace('@',''));

const tooltip = document.getElementById('tooltip');
node.on('mouseover', (e,d) => {
  tooltip.style.opacity='1';
  tooltip.innerHTML = `<strong style="color:var(--accent)">${d.id}</strong><br>${d.author}<br><em style="color:var(--muted)">${d.journal||''}</em>`;
}).on('mousemove', e => {
  const r = area.getBoundingClientRect();
  let x = e.clientX-r.left+12, y = e.clientY-r.top-10;
  if (x+230 > r.width) x -= 240;
  tooltip.style.left=x+'px'; tooltip.style.top=y+'px';
}).on('mouseout', () => { tooltip.style.opacity='0'; })
  .on('click', (e,d) => {
    selectPaper(d.id);
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(t=>t.classList.remove('active'));
    document.querySelector('[data-tab="detail"]').classList.add('active');
    document.getElementById('tab-detail').classList.add('active');
  });

sim.on('tick', () => {
  link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y)
    .attr('x2', d => {
      const dx=d.target.x-d.source.x, dy=d.target.y-d.source.y;
      const dist=Math.sqrt(dx*dx+dy*dy), r=nodeRadius(d.target)+2;
      return d.source.x+dx*(1-r/dist);
    })
    .attr('y2', d => {
      const dx=d.target.x-d.source.x, dy=d.target.y-d.source.y;
      const dist=Math.sqrt(dx*dx+dy*dy), r=nodeRadius(d.target)+2;
      return d.source.y+dy*(1-r/dist);
    });
  node.attr('transform', d=>`translate(${d.x},${d.y})`);
});

svg.on('click', e => {
  if (e.target === svg.node()) {
    node.classed('dimmed',false); link.classed('dimmed',false);
    document.getElementById('panel-empty').style.display='';
    document.getElementById('panel-content').style.display='none';
  }
});

function selectPaper(id) {
  const p = paperMap[id];
  if (!p) return;
  const connected = new Set([id, ...(citedBy[id]||[]), ...(respondsTo[id]||[])]);
  node.classed('dimmed', d => !connected.has(d.id));
  link.classed('dimmed', d => d.source.id!==id && d.target.id!==id);

  document.getElementById('panel-empty').style.display='none';
  const pc = document.getElementById('panel-content');
  pc.style.display='block';

  const cb = citedBy[id]||[];
  const rt = respondsTo[id]||[];
  const kwHtml = (p.keywords||[]).map(k=>`<span class="keyword-pill">${k}</span>`).join('');

  pc.innerHTML = `
    ${p.type ? `<div class="paper-type-tag">${p.type}</div>` : ''}
    <div class="paper-title">${p.title}</div>
    <div class="paper-meta">
      <span class="citekey">${p.id}</span><br>
      ${p.author}<br>
      ${p.year?p.year+' · ':''}${p.journal}
      ${p.doi ? `<br><a class="doi-link" href="${p.doi.startsWith('http')?p.doi:'https://doi.org/'+p.doi}" target="_blank">↗ DOI</a>` : ''}
    </div>
    ${cb.length||rt.length ? `
      <div class="section-label">Connections</div>
      <div class="section-body">
        ${cb.length?'<div style="margin-bottom:6px"><span style="font-size:.6rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em">Cited by</span><br>'+cb.map(x=>`<span class="conn-badge cited-by" onclick="selectPaper('${x}')">${x}</span>`).join('')+'</div>':''}
        ${rt.length?'<div><span style="font-size:.6rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em">Replies to</span><br>'+rt.map(x=>`<span class="conn-badge reply-to" onclick="selectPaper('${x}')">${x}</span>`).join('')+'</div>':''}
      </div>` : ''}
    ${kwHtml ? `<div class="section-label">Keywords</div><div class="section-body">${kwHtml}</div>` : ''}
    ${p.background ? `<div class="section-label">Disciplinary Background</div><div class="section-body">${p.background.replace(/\n/g,'<br>')}</div>` : ''}
    ${p.context ? `<div class="section-label">Geographic Context</div><div class="section-body">${p.context}</div>` : ''}
    ${p.notes ? `<div class="section-label">Notes</div><div class="section-body">${p.notes}</div>` : ''}
  `;
}
</script>
</body>
</html>
"""


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Building literature network...")
    nodes, edges = build_graph()
    output_path = Path(__file__).parent / "output" / "literature_network.html"
    generate_html(nodes, edges, output_path)
    print(f"\nOpen this file in your browser:\n  {output_path.resolve()}")
