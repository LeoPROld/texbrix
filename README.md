TeXBriX
=======
A granular approach to LaTeX
----------------------------

Texbrix is a file standard that comes with useful tools for managing and exporting latex code

Other tools
---------------------------
###VSCodium
Add to settings.json

```json
"files.associations": {
	"*.brik": "latex"
}
```
If you use the `latex-workshop` extension:
```json
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
