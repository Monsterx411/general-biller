# macOS Desktop Packaging

## Option A: Electron

1. Create an Electron app wrapping the `frontend` build
2. Use `electron-builder` to generate `.dmg`/`.pkg`
3. Main window loads your hosted domain `https://globe-swift.org`

## Option B: PyInstaller (local binary)

1. Install PyInstaller:
   - `pip install pyinstaller`
2. Build macOS binary:
   - `pyinstaller -n LoanManager src/api/app.py`
3. Distribute the generated app (note: API would run locally)
