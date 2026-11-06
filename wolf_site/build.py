#!/usr/bin/env python3
"""Builds index.html from src/style.css and src/body.html. Run: python3 build.py"""
import os
h = os.path.dirname(os.path.abspath(__file__))
css = open(os.path.join(h, "src/style.css")).read()
body = open(os.path.join(h, "src/body.html")).read()
html = f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0b1430"><meta name="robots" content="noindex"><title>Wolf</title>
<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icon-192.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<style>{css}</style></head><body>
{body}
<script src="app.js"></script></body></html>'''
open(os.path.join(h, "index.html"), "w").write(html)
print("built index.html", len(html) // 1024, "KB")
