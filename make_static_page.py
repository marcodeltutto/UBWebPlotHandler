#!/usr/bin/env python

import config

import json
from time import strftime


# Ensure closing tag is written. Don't use for standalone tags like <img>
class Tag:
    # **kwargs seems like a nice idea here. Except "class" is a common thing to
    # want and is a reserved word :(
    def __init__(self, fout, tag, args = {}):
        self._fout = fout
        self._tag = tag
        self._args = args

    def __enter__(self):
        self._fout.write('<'+self._tag)

        for key in self._args:
            self._fout.write(' '+key+'="'+self._args[key]+'"')
        self._fout.write('>')

    def __exit__(self, a, b, c):
        self._fout.write('</'+self._tag+'>')


header = '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>MicroBooNE Approved Plots</title>

<style type="text/css">
  a:link{color:black}
  a:visited{color:black}
  a:hover{color:red}
  a:active{color:red}

  .plot
  {
    display: inline-block;
    text-align: center;
    border: 2px solid gray;
    background-color: white;
    padding: 5px;
    margin: 5px;
    vertical-align: top
  }
  .sublink
  {
    display: inline-block;
    border: 2px solid gray;
    background-color: white;
    padding: 5px;
    margin: 5px;
    vertical-align: top;
    width: 400px
  }
  .caption
  {
    text-align: left;
    max-width: 400px;
  }
</style>

<script>
function Hide()
{
  document.getElementById("showbutton").hidden = false;
  document.getElementById("hidebutton").hidden = true;

  cs = document.getElementsByClassName("caption")
  for(var i = 0; i < cs.length; i++){
    cs[i].hidden = true;
  }
}

function Show()
{
  document.getElementById("hidebutton").hidden = false;
  document.getElementById("showbutton").hidden = true;

  cs = document.getElementsByClassName("caption")
  for(var i = 0; i < cs.length; i++){
    cs[i].hidden = false;
  }
}
</script>

<script type="text/x-mathjax-config">
  MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$']]}});
</script>
<script type="text/javascript"
  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

</head>
<body bgcolor="#f0f0f0">
'''

header2 = '''
<div style="position:fixed;right:0;top:0">
  <button type="button" title="Hide" onclick="Hide()" id="hidebutton">Hide captions</button>
  <button type="button" title="Show" onclick="Show()" hidden id="showbutton">Show captions</button>
</div>
'''

def footer():
    return '\n<hr>\nLast updated '+strftime('%Y-%m-%d %H:%M:%S %Z')+'\n</body></html>'


def AddFile(fout, deets, f):
    thumb = 'plots/'+str(deets['id'])+'/thumbs/'+f['base']+'_thumb.png'

    with Tag(fout, 'span', {'class': 'plot'}):
        fout.write('<img src="'+thumb+'"><br>\n')
        for ext in f['exts']:
            with Tag(fout, 'a', {'href': 'plots/'+str(deets['id'])+'/'+f['base']+'.'+ext}):
                fout.write('['+ext+']')
            fout.write('\n')

        with Tag(fout, 'div', {'class': 'caption'}):
            fout.write(f['caption'])

    fout.write('\n\n')


page_cfg = json.load(file(config.BLESSED_PLOTS))
doc_deets = json.load(file(config.WEB_PATH + config.JSON_FILENAME))

allNos = [d['id'] for d in doc_deets]
allCatNos = [[n for n in page['docs']] for page in page_cfg]
allCatNos = sum(allCatNos, []) # flatten
new = [n for n in allNos if n not in allCatNos]

# Synthesize a "New" page at the top
if len(new) > 0:
    page_cfg = [{'category': 'New / uncategorized',
                 'docs': new,
                 'caption': 'Plots that have not yet been categorized. Please edit Utilities/BlessedPlots/BlessedPlots.json to do so.'}] + page_cfg


fout_main = open(config.WEB_PATH + '/index.html', 'w')
fout_main.write(header)
with Tag(fout_main, 'h1'):
    fout_main.write('MicroBooNE Approved Plots')


for page in page_cfg:
    cat = page['category']
    safe_cat = cat.replace(' ', '_').replace('/', 'and')

    with Tag(fout_main, 'span', {'class': 'sublink'}):
        with Tag(fout_main, 'h3'):
            with Tag(fout_main, 'a', {'href': safe_cat+'.html'}):
                fout_main.write(cat)

        with Tag(fout_main, 'table'):
            with Tag(fout_main, 'tr'):
                if 'thumb' in page:
                    with Tag(fout_main, 'td', {'valign': 'top'}):
                        fout_main.write('<img src="plots/'+page['thumb']+'" width="200px">')
                if 'caption' in page:
                    with Tag(fout_main, 'td', {'valign': 'top'}):
                        fout_main.write(page['caption'])

    fout_main.write('\n')

    fout_sub = open(config.WEB_PATH + '/' + safe_cat+'.html', 'w')
    fout_sub.write(header)
    fout_sub.write(header2)
    with Tag(fout_sub, 'h1'): fout_sub.write(cat)

    for docNo in page['docs']:
        deets = [d for d in doc_deets if d['id'] == docNo]
        if len(deets) == 0:
            print 'No info for doc', docNo, 'skipping'
            continue
        assert len(deets) == 1
        deets = deets[0]

        with Tag(fout_sub, 'h2'):
            with Tag(fout_sub, 'a', {'href': deets['url']}):
                fout_sub.write('docdb '+str(docNo))
            fout_sub.write(' - '+deets['title'])

        for f in deets['files']:
            AddFile(fout_sub, deets, f)

    fout_sub.write(footer())

fout_main.write(footer())
