# VectorCraft on Fedora

VectorCraft runs natively on Fedora Linux: no Docker, WSL or compatibility
layer needed. These steps were written for Fedora 41 and 42 (Python 3.13). Any
Fedora release with Python 3.9 or newer should work.

## Quick install

```bash
git clone https://github.com/IronShing/VectorCraft.git
cd VectorCraft
scripts/fedora/install.sh --with faiss-cpu
```

The installer:

1. Installs the build prerequisites with `dnf` (`python3-devel`, `gcc`,
   `gcc-c++`, `git`, …). It uses `sudo` when you are not root.
2. Creates a virtual environment in `~/.local/share/vectorcraft/venv`, so the
   system Python that dnf manages is never modified.
3. Installs VectorCraft plus any extra packages you pass with `--with`.
4. Adds a `~/.local/bin/vectorcraft-python` launcher.

Check that it works:

```bash
vectorcraft-python scripts/fedora/smoke_test.py
```

Use it:

```bash
source ~/.local/share/vectorcraft/venv/bin/activate
python -c "from vectorcraft.vectorstores import FAISS; print('ready')"
```

### Installer options

| Option | Purpose |
| --- | --- |
| `--venv DIR` | Put the virtual environment somewhere else |
| `--python BIN` | Use a specific interpreter, e.g. `python3.12` (`sudo dnf install python3.12`) |
| `--with "PKGS"` | Extra pip packages, e.g. `"faiss-cpu beautifulsoup4 pypdf"` |
| `--editable` | Editable install, for working on VectorCraft itself |
| `--no-system-deps` | Skip the `dnf` step (no sudo) |

## Manual install

```bash
sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++ git
python3 -m venv ~/.venvs/vectorcraft
source ~/.venvs/vectorcraft/bin/activate
pip install --upgrade pip
pip install .            # from the repository root
```

## Podman (optional)

To keep everything inside a container, build the Fedora image with Podman:

```bash
podman build -f scripts/fedora/Containerfile -t vectorcraft:fedora .
podman run --rm -it -v "$PWD":/work:Z vectorcraft:fedora python
```

The `:Z` suffix relabels the mounted directory for SELinux, which Fedora
enables by default.

## Notes

- **numpy 2:** Fedora 41+ ships Python 3.13, and numpy 1.x has no prebuilt
  wheels for it. VectorCraft therefore accepts numpy 2 on Python ≥ 3.9, so pip
  downloads a wheel and doesn't have to compile numpy.
- **Why not an RPM?** VectorCraft depends on `langchain-core` and `langsmith`,
  which Fedora doesn't package, so a native RPM can't be built from Fedora
  repositories alone. The virtual environment approach avoids that problem.
