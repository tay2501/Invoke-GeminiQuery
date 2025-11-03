#!/usr/bin/env python3
"""
URL生成テスト用スクリプト
"""

import urllib.parse
import json
from pathlib import Path

def load_config():
    """設定を読み込み"""
    config_path = Path(__file__).parent / "config.json"
    
    default_config = {
        "gemini_url": "https://aistudio.google.com/prompts/new_chat",
        "max_prompt_length": 10000
    }
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            print(f"Warning: Could not load config.json: {e}")
    
    return default_config

def create_test_url(prompt):
    """テスト用URL生成"""
    config = load_config()
    
    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Create final URL properly
    base_url = config['gemini_url']
    
    # Check if base_url already has parameters
    if '?' in base_url:
        # Add as additional parameter
        final_url = f"{base_url}&prompt={encoded_prompt}"
    else:
        # Add as first parameter
        final_url = f"{base_url}?prompt={encoded_prompt}"
    
    return final_url

def main():
    """メイン関数"""
    test_prompts = [
        "関税が高い食品一覧",
        "URLパラメータのテストです",
        "Hello World",
        "これは日本語のテストです"
    ]
    
    print("=== URL生成テスト ===")
    
    for prompt in test_prompts:
        url = create_test_url(prompt)
        print(f"\nプロンプト: {prompt}")
        print(f"生成URL: {url}")
        
        # URLパラメータを解析
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        print("パラメータ:")
        for key, values in params.items():
            print(f"  {key}: {values[0] if values else 'None'}")
    
    print("\n=== 手動テスト用URL ===")
    manual_prompt = input("手動テスト用のプロンプトを入力してください: ")
    if manual_prompt.strip():
        manual_url = create_test_url(manual_prompt.strip())
        print(f"\n手動テスト用URL:")
        print(manual_url)
        print(f"\nこのURLをブラウザで開いて、Greasemonkeyスクリプトの動作を確認してください。")

if __name__ == "__main__":
    main()