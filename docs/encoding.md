# 文字コード対応ガイド

## 概要

Windows 11日本語環境での文字化け問題を解決するため、すべてのスクリプトファイルを適切な文字コード設定で修正しました。

## 実装された対策

### 1. バッチファイル (.bat)

**問題**: 特殊文字（絵文字、罫線文字）が文字化けする

**対策**:
```batch
@echo off
chcp 65001 >nul 2>&1
REM UTF-8コードページを設定
```

**変更内容**:
- 絵文字や特殊文字をASCII文字に置換
- 罫線文字を等号（=）やハイフン（-）に変更
- UTF-8コードページ（65001）を設定

### 2. Pythonスクリプト (.py)

**問題**: 標準出力での文字化け

**対策**:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Windows環境での文字コード設定
if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    os.environ['PYTHONIOENCODING'] = 'utf-8'
```

**適用ファイル**:
- `gemini_query.py`
- `setup.py`
- `debug_test.py`

### 3. JavaScriptファイル (.js)

**状況**: 既にUTF-8で適切に記述済み

**確認事項**:
- ファイルがUTF-8 BOMなしで保存されている
- 特殊文字は適切にエスケープされている

## 使用方法

### 推奨される実行方法

**1. バッチファイル使用（最も安全）**:
```batch
REM ダブルクリックまたはコマンドラインから
gemini-query.bat
```

**2. PowerShell使用**:
```powershell
$env:PYTHONIOENCODING="utf-8"
python gemini_query.py "質問内容"
```

**3. コマンドプロンプト使用**:
```cmd
chcp 65001
set PYTHONIOENCODING=utf-8
python gemini_query.py "質問内容"
```

### 避けるべき実行方法

**❌ 設定なしでのコマンドプロンプト実行**:
```cmd
REM 文字化けの可能性あり
python gemini_query.py "日本語の質問"
```

## トラブルシューティング

### 文字化けが発生する場合

**1. 環境変数の確認**:
```cmd
echo %PYTHONIOENCODING%
REM utf-8 と表示されるべき
```

**2. コードページの確認**:
```cmd
chcp
REM アクティブ コード ページ: 65001 と表示されるべき
```

**3. 強制的なUTF-8設定**:
```cmd
chcp 65001
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
```

### ファイル保存時の注意

**テキストエディタでの保存設定**:
- エンコーディング: UTF-8
- BOM: なし（UTF-8 without BOM）
- 改行コード: LF または CRLF

**Visual Studio Code設定例**:
```json
{
    "files.encoding": "utf8",
    "files.eol": "\n"
}
```

## 検証方法

### 1. デバッグテスト実行
```cmd
python debug_test.py
```

### 2. インタラクティブテスト実行
```cmd
test_interactive.bat
```

### 3. 実際の動作テスト
```cmd
gemini-query.bat
REM 日本語で質問を入力してテスト
```

## 技術的詳細

### Windows文字コード環境

**従来の問題**:
- デフォルトコードページ: CP932 (Shift_JIS)
- UTF-8文字の表示不可
- 絵文字や特殊文字の文字化け

**解決策**:
- UTF-8コードページ（65001）の使用
- Python環境変数での強制UTF-8設定
- 安全な文字セットの使用

### ファイル形式の統一

**バッチファイル**:
- エンコーディング: UTF-8 (BOMなし)
- 改行コード: CRLF
- 特殊文字: ASCII範囲内のみ使用

**Pythonファイル**:
- エンコーディング: UTF-8 (BOMなし)
- 改行コード: LF
- 文字コード宣言: `# -*- coding: utf-8 -*-`

**JavaScriptファイル**:
- エンコーディング: UTF-8 (BOMなし)
- 改行コード: LF
- 文字列リテラル: 適切にエスケープ

## 今後の保守について

### 新しいファイル作成時

**1. 適切なヘッダーを追加**:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

**2. Windows対応コードを追加**:
```python
if sys.platform == "win32":
    # UTF-8設定コード
```

**3. 文字コードテストを実行**:
```cmd
python debug_test.py
```

### 既存ファイル修正時

**1. エンコーディング確認**
**2. 特殊文字の使用を避ける**
**3. テスト実行で動作確認**

---

この文字コード対応により、Windows 11日本語環境での安定した動作が保証されます。