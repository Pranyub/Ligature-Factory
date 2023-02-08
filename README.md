# Ligature-Factory
A lightweight tool to create custom fontpacks for XSLeaks exploitation.

Based on [this tool](https://sekurak.pl/wykradanie-danych-w-swietnym-stylu-czyli-jak-wykorzystac-css-y-do-atakow-na-webaplikacje/) but without all the npm server requirements!

## Requirements
This tool requires [FontForge](https://fontforge.org/en-US/) to create .woff packs. If you're not using this program on a unix operating system, you may need to respecify the `FONTFORGE_PATH` variable in `factory.py` to point to your installation directory.

## Usage

`python3 factory.py [flags] [ligature_1] [ligature_2] ... [ligature_n]`

There are a few different flags that specify different modes of operation. For a full list, use the `-h` flag.

- `--prefix (-p)`: the prefix of the ligature

- `--xml (-x)`: outputs unformatted svg of the generated fontpack (does not require fontforge)
- `--file (-f)`: creates a .woff fontpack with the given filename
- `--base64 (-b)`: outputs a base64 encoded woff fontpack

Example:
`python3 factory.py --base64 --prefix "im a bea" n rd` will generate a fontpack with both the ligatures `im a bean` and `im a beard`

