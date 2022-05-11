all: main.tex main.bib
	lualatex -shell-escape main.tex
	biber main
	lualatex -shell-escape main.tex

clean:
	rm main.aux main.bcf main.log main.out main.pdf main.run.xml main.blg main.bbl
