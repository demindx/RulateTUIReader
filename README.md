# RulateTUIReader

A terminal-based (TUI) reader for browsing and reading translated novels from **tl.rulate.ru**. Works entirely in your terminal — no browser needed.

## Features

- Browse your bookmarks (Reading, Favorites, In Plans, Dropped, Read)
- Read chapters with HTML-to-Markdown conversion rendered in the terminal
- Navigate between chapters (previous/next)
- View the full chapter list for any book in a modal window
- Vim-like keybindings (`j`/`k` — scroll, `h`/`l` — prev/next chapter, `o` — chapter list, `q` — close)
- Display book covers and user avatars (via Sixel / iTerm)
- Secure login with RSA-encrypted credentials
- Auth token stored in OS keyring
- Persistent bottom bar with user info (balance, avatar)

## Install & Run

Requires **Python 3.12+** and **uv**.

```bash
git clone https://github.com/demindx/RulateTUIReader.git
cd RulateTUIReader
uv sync
uv run python main.py
```

## Configuration

Copy and edit `.env`:

```
API_BASE_URL=https://tl.rulate.ru
X_API_KEY=your_api_key
RSA_PUBLIC_KEY=your_rsa_public_key
```

On first launch a login modal will appear asking for your credentials.

## Keybindings

| Key | Action |
|-----|--------|
| `j` / `k` | Scroll down / up |
| `g` / `G` | Go to top / bottom |
| `h` / `l` | Previous / next chapter |
| `o` | Open chapter list |
| `q` / `escape` | Close modal / quit |
| `/` | Search (in bookmarks) |

## Tech Stack

- **Python 3.12+**
- [Textual](https://github.com/Textualize/textual) — TUI framework
- [aiohttp](https://docs.aiohttp.org/) — async HTTP client
- [Pydantic](https://docs.pydantic.dev/) — data models
- [Pycryptodome](https://www.pycryptodome.org/) — RSA encryption
- [keyring](https://github.com/jaraco/keyring) — token storage
- [markdownify](https://github.com/matthewwithanm/python-markdownify) — HTML → Markdown
- [textual-image](https://github.com/Textualize/textual-image) — image rendering

## License

MIT
