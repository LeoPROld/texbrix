TeXBriX
=======
A granular approach to LaTeX
----------------------------

Texbrix is a file standard that comes with useful tools for managing and exporting latex code

Usage
-----
### Command Line

To generate a LaTeX document from your TeXBriX structure use the command

```
texbrix <top TeXBriK>
```

This will by default use the `default_template` located in the src directory. If you would like to use another
template file instead (e.g. to define Math environments which should be expected to work in all BriX),
pass it via the optional `-template` Flag.

### Brik Structure
A TeXBriK has the following basic structure:
```LaTeX
\usepackage{<some LaTeX package required for this BriK's content>}
...
\usepackage{<more packages>}
\prerequisite{<some brik>}
...
\prerequisite{<some other brik>}
\begin{content}
This is ordinary \LaTeX.
\newline

...
\brikinsert{<yet another brik>}

...
\end{content}

```

Both the `\prerequisite{}` and the `\brikinsert{}` Commands take a file path relative to the top BriK's
location (without the `.brik`-Postfix).
`\prerequisite{}` will make sure the mentioned BriK is included with all it's dependencies before the content, while
not generating any duplicates.
`\brikinsert{}` will insert the mentioned brik on the given position (with all not yet included dependencies) no matter whether
or not it has been previously used.

### Template File
You can write the general structure of your final LaTeX document in a template file (passed to TeXBriX via the `-template` argument).
Here you should use the following placeholders:

| Placeholder | Meaning |
| ----------- | ------- |
| $packages   | In the place where you want the LaTeX imports to be inserted |
| $content    | Where you want the BriK's content to be |


Other tools
---------------------------
### VSCodium
Add to settings.json

```json
"files.associations": {
	"*.brik": "latex"
}
```
If you use the `latex-workshop` extension:
```json
"latex-workshop.latex.tools":[
	{
		"name": "texbrix",
		"command": "texbrix",
		"args": [
			"%DOC%.brik"
		],
		"env": {}
	},
	{
		"name": "pdflatex",
		"command": "pdflatex",
		"args": [
			"-synctex=1",
			"-interaction=nonstopmode",
			"-file-line-error",
			"%DOC%.tex"
		],
		"env": {}
	}
]
"latex-workshop.latex.recipes":[
	{
		"name": "texbrix then pdflatex",
		"tools": [
			"texbrix",
			"pdflatex"
		]
	}
]

```
