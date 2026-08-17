"""
Live Web Search Service for Autonomous Real-Time Intelligence
Performs real-time live web queries to verify companies, get actual market prices, regulations, and import news.
"""
import httpx
import urllib.parse
import re
from bs4 import BeautifulSoup
import asyncio

class WebSearchService:
    @staticmethod
    async def search(query: str, max_results: int = 4) -> list:
        """
        جستجوی زنده در وب و استخراج عناوین، خلاصه‌ها و لینک‌های مرتبط
        """
        results = []
        clean_q = query.strip()
        if not clean_q:
            return results

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "fa,en-US;q=0.9,en;q=0.8"
        }

        # 1. Try DuckDuckGo HTML endpoint
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(clean_q)}"
            async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
                resp = await client.get(url, headers=headers)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    snippets = soup.find_all('a', class_='result__snippet')
                    titles = soup.find_all('a', class_='result__url')

                    for i in range(min(len(snippets), max_results)):
                        snippet_text = snippets[i].get_text().strip()
                        raw_link = titles[i].get('href', '') if i < len(titles) else ''
                        title_tag = snippets[i].find_previous('h2')
                        title_text = title_tag.get_text().strip() if title_tag else f"Result {i+1}"
                        
                        if snippet_text:
                            results.append({
                                "title": title_text,
                                "snippet": snippet_text,
                                "link": raw_link
                            })
        except Exception as e:
            print(f"[WebSearch] DuckDuckGo search error: {e}")

        # 2. If no results, fallback to Open Search / DuckDuckGo Lite
        if not results:
            try:
                lite_url = f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(clean_q)}"
                async with httpx.AsyncClient(timeout=8.0, follow_redirects=True) as client:
                    resp = await client.post(lite_url, data={"q": clean_q}, headers=headers)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        rows = soup.find_all('td', class_='result-snippet')
                        for i, row in enumerate(rows[:max_results]):
                            text = row.get_text().strip()
                            if text:
                                results.append({
                                    "title": f"Web Intelligence Result {i+1}",
                                    "snippet": text,
                                    "link": ""
                                })
            except Exception as e:
                print(f"[WebSearch] Lite search error: {e}")

        return results

    @staticmethod
    def format_search_context(search_results: list) -> str:
        """
        قالب‌بندی نتایج جستجو به عنوان Context زنده برای مدل هوش مصنوعی
        """
        if not search_results:
            return ""

        context_lines = ["\n[🌐 داده‌های زنده و اعتبارسنجی استخراج‌شده از وب در این لحظه:]"]
        for i, res in enumerate(search_results, 1):
            context_lines.append(f"{i}. {res['title']}: {res['snippet']}")
        context_lines.append("[دستور به هوش مصنوعی: از این داده‌های زنده وب برای تحلیل دقیق، ارزیابی اعتبار، اعتبارسنجی شرکت و پاسخگویی جامع استفاده کن.]\n")
        return "\n".join(context_lines)
