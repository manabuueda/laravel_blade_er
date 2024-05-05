# venv起動
`source ./bin/activate`

# venv上のtkinterについて
https://zenn.dev/k41531/articles/6133b1b045d1aa

# pygraphvizについて
環境変数に設定するパスは、brewで`graphviz`をインストールした際のパスを指定
```shell
brew install graphviz
pip install --global-option=build_ext \
            --global-option="-I/usr/local/Cellar/graphviz/10.0.1/include/" \
            --global-option="-L/usr/local/Cellar/graphviz/10.0.1/lib/" \
            pygraphviz
```