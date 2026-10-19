# My empty template


## Get PDF file from artifacts
https://gitlab.com/api/v4/projects/75814734/jobs/artifacts/main/raw/main.pdf?job=build-pdf

## Deploy cookiecutter
- Create a new blank project on overleaf
- Clone it
```bash
git clone <yourURL>
```
- use cruft in another folder
```bash
cruft create https://git@git.overleaf.com/6062d5d472816c3a14767b6d
```
- combine the 2 folders.
- push
```bash
git add .
git status
git commit -a
git push
```

## How is it organized
- at root level are the major files to look at as a new-comer or a naive supervisor. We do not want to scrutinize all your file to find the relevant information, so we want to file it in the compiled output from a root-level file.
- resources folder contains all the 'header'/preamble files that are shared by all the other files
- supplies folder contains the figures, plots, data, tabular, and other pieces that are include in you latex files
- sources
- original
- old
- parts folder contains all your sub latex files, such files typically correspond to a sections or parts of your reports or progress notes or logbook.


## Compile the main document
At project root dir run the following command:
```bash
latexmk -pdf -auxdir=./build/
```


## Cleaning Up
```bash
latexmk -c -auxdir=./build/
```


## Generate a flat latex file for submission
step 0
```bash
MAINFILE=main
echo $MAINFILE
```

step 1
```bash
printf '%s\n%s\n' "\RequirePackage{snapshot}" "$(cat $MAINFILE.tex)" >$MAINFILE.tex
latexmk -pdf
pdflatex -recorder $MAINFILE.tex
okular $MAINFILE.pdf
```

step 2
```bash
bundledoc   --verbose   --include=./*.glstex   --include=./*.fls   --localonly   $(find supplies -type f -name "*.csv" -exec printf -- "--include=%s " {} \;)   "$MAINFILE.dep"
tar -xvf $MAINFILE.tar.gz
cp -r ./supplies/ ././$MAINFILE/supplies
cd ./$MAINFILE
```

step 3
```bash
grep -rl '\PathP/' ./ | xargs sed -i 's|\\PathP/|./parts/|g'
grep -rl '\PathR/' ./ | xargs sed -i 's|\\PathR/|./resources/|g'
grep -rl '\PathSO/' ./ | xargs sed -i 's|\\PathSO/|./sources/|g'
grep -rl '\PathS/' ./ | xargs sed -i 's|\\PathS/|./supplies/|g'
find . -type f -name "*.tex" ! -name "$MAINFILE.tex" -exec grep -q '\\begin{document}' {} \; -exec sed -i '1,/\\begin{document}/d; /\\end{document}/,$d' {} \;
find . -type f -name "*.tex" ! -name "$MAINFILE.tex" -exec sed -i '/\\ifnum\\value{levelstanda}>1/,/\\fi/ { /\\ifnum\\value{levelstanda}>1/s/^/%%/; /\\else/{ }; /\\fi/s/^/%%\\fi\n%%/;}' {} \;
find . -type f -name "*.tex" ! -name "$MAINFILE.tex" -exec grep -q '%%\\ifnum\\value{levelstanda}>1' {} \; -exec sed -i '/\\else/,/%%\\fi/ {/\\else/,$d; /%%\\fi/{ }; }' {} \;
```

REPLACE BY HAND ALL THE \includestandalone[...]{} BY \input{}

step 4
```bash
latex-flatten -vvv --replace-bib --copy --outdir outdir
cp -r ./outdir/ ./outdir2test
cd ./outdir2test/
find . -type f -name "*.tex" -exec sed -i -E 's@(\{\.\/)[^/]+\/([^}/]+\.csv\})@\1\2@g' {} \;
pdflatex $MAINFILE.tex
pdflatex $MAINFILE.tex
okular $MAINFILE.pdf
```

step 5
```bash
cp ./$MAINFILE.tex ../outdir/$MAINFILE.tex
cd ../
zip -r outdir.zip ./outdir
```


### Memo of LaTeX useful commands
```latex
\gls{}
\chhighlight[id=RN]{something in color}
\chcomment[id=RN]{comment in margin}
\chdeleted[id=RN]{to del}
\chadded[id=RN]{new}
\chreplaced[id=RN]{new}{old}
```