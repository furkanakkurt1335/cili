#!/usr/bin/env python3

"""
Requirements:
    - Python 3.6+
    - rdflib
Usage:
    python3 make-html.py OUTDIR

"""

from typing import Dict
import sys
from pathlib import Path

from rdflib import Graph
from rdflib.namespace import RDF, DC, SKOS, Namespace

if len(sys.argv) != 2:
    sys.exit('usage: python3 make-html.py OUTDIR')
OUTDIR = Path(sys.argv[1])
if OUTDIR.exists():
    sys.exit(f'{OUTDIR!s} already exists; remove or rename it, then try again')
OUTDIR.mkdir()

content = '''\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{ili}</title>
</head>
<body>
  <article class="ili" itemscope itemtype="{type!s}" itemid="{subject!s}">
    <h1>{ili}</h1>

    <div class="ili-type">{short_type!s}</div>

    <blockquote itemprop="http://www.w3.org/2004/02/skos/core#definition">
    {definition!s}
    </blockquote>

    <dl>
      <dt>Status</dt>
      <dd itemprop="status">{status!s}</dd>
      <dt>Source</dt>
      <dd><a href="{source_info[url]}">{source_info[name]}</a>
          &ndash;
          <a itemprop="http://purl.org/dc/elements/1.1/source" href="{source!s}">{source_info[local]}</a>
      </dd>
    </dl>

  </article>
</body>
</html>
'''

ILI = Namespace('http://globalwordnet.org/ili/')

sources = {
    'http://wordnet-rdf.princeton.edu/wn30/': ('Princeton WordNet 3.0',
                                               'https://wordnet.princeton.edu/'),
}


def source_info(url: str) -> Dict[str, str]:
    for src in sources:
        if url.startswith(src):
            local = url.removeprefix(src).lstrip('/#')
            name, project_url = sources[src]
            return {'name': name, 'url': project_url, 'local': local}
    raise LookupError(f'source info not found for {url!s}')


def short_name(s: str) -> str:
    return s.rpartition('/')[2]


g = Graph()
g.parse("ili.ttl", format='ttl')

for subj in g.subjects():
    type = g.value(subject=subj, predicate=RDF.type)
    if type not in (ILI.Concept, ILI.Instance):
        continue
    ili = short_name(subj)
    source = g.value(subject=subj, predicate=DC.source)
    data = {
        'ili': ili,
        'subject': subj,
        'type': type,
        'short_type': short_name(type),
        'definition': g.value(subject=subj, predicate=SKOS.definition),
        'status': g.value(subject=subj, predicate=ILI.status, default='active'),
        'source': source,
        'source_info': source_info(source),
    }

    filename = OUTDIR / f'{ili}.html'
    with filename.open('wt') as htmlfile:
        print(content.format(**data), file=htmlfile)
