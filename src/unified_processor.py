import sys
import os
import re
import urllib.parse
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import trafilatura

# Find clarifai_engine
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from clarifai_engine import analyze_news


def extract_url_content(url):
    """
    Fetches webpage content using trafilatura with BeautifulSoup fallback.
    Extracts title, main body text, and source domain.
    """
    if not url or not isinstance(url, str):
        return {
            "success": False,
            "error": "Please provide a valid article URL."
        }

    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return {
            "success": False,
            "error": "Invalid URL format. Please provide a URL starting with http:// or https://"
        }

    # Extract source domain
    try:
        parsed_url = urllib.parse.urlparse(url)
        source_domain = parsed_url.netloc.replace("www.", "").lower()
        if not source_domain:
            return {
                "success": False,
                "error": "Could not identify a valid web domain in the provided URL."
            }
    except Exception:
        return {
            "success": False,
            "error": "Invalid URL syntax. Please check the web address."
        }

    title = None
    article_text = None

    # Step 1: Attempt extraction using Trafilatura
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted_text = trafilatura.extract(
                downloaded, 
                include_comments=False, 
                include_tables=False
            )
            metadata = trafilatura.extract_metadata(downloaded)
            
            if metadata and metadata.title:
                title = metadata.title.strip()
            
            if extracted_text and len(extracted_text.strip()) > 50:
                article_text = extracted_text.strip()
    except Exception:
        pass

    # Step 2: Fallback extraction using Requests + BeautifulSoup
    if not article_text or len(article_text.split()) < 15:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0.0.0 Safari/537.36"
            )
        }
        try:
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Extract title if missing
                if not title:
                    og_title = soup.find("meta", property="og:title")
                    if og_title and og_title.get("content"):
                        title = og_title["content"].strip()
                    elif soup.h1:
                        title = soup.h1.get_text().strip()
                    elif soup.title:
                        title = soup.title.get_text().strip()

                # Extract paragraph text
                paragraphs = soup.find_all("p")
                text_blocks = [
                    p.get_text().strip() for p in paragraphs 
                    if len(p.get_text().strip()) > 30
                ]
                fallback_text = "\n\n".join(text_blocks)
                if fallback_text and len(fallback_text.split()) >= 15:
                    article_text = fallback_text.strip()
            elif response.status_code in (403, 401):
                return {
                    "success": False,
                    "error": f"The website ({source_domain}) blocked automated access (HTTP {response.status_code}). Please switch to 'Paste Article' to enter text manually."
                }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"Network timeout while connecting to {source_domain}. Please check your connection or paste the article manually."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to fetch webpage content from {source_domain}. Please switch to 'Paste Article' to enter text manually."
            }

    # Step 3: Validate extracted content
    if not article_text or len(article_text.strip()) == 0:
        return {
            "success": False,
            "error": f"Could not automatically extract readable article text from {source_domain}. Please copy and paste the article text manually."
        }

    word_count = len(article_text.split())
    if word_count < 10:
        return {
            "success": False,
            "error": f"Insufficient article text extracted ({word_count} words). ClarifAI requires at least 10 words for accurate machine-learning evaluation."
        }

    if not title:
        title = f"Article from {source_domain}"

    return {
        "success": True,
        "title": title,
        "article_text": article_text,
        "source_url": url,
        "source_domain": source_domain
    }


def run_unified_analysis(title, article_text, input_method, source_url=None, source_domain=None):
    """
    Unified entry point for both manual and URL inputs.
    Validates input, calls ML engine, and returns standardized analysis object.
    """
    title = (title or "").strip()
    article_text = (article_text or "").strip()

    # Input validations
    if not title or not article_text:
        return {
            "success": False,
            "error": "Please provide both a headline and article body before running analysis."
        }

    word_count = len(article_text.split())
    if word_count < 10:
        return {
            "success": False,
            "error": f"Extremely short article ({word_count} words). ClarifAI requires at least 10 words in the article body for reliable classification."
        }

    # Execute ML Engine Pipeline
    try:
        engine_result = analyze_news(title, article_text)
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred during ML model inference: {str(e)}"
        }

    if not engine_result.get("success"):
        return {
            "success": False,
            "error": engine_result.get("error", "ML Engine analysis failed.")
        }

    # Standardized Analysis Object
    analysis_obj = {
        "title": title,
        "article_text": article_text,
        "source_url": source_url,
        "source_domain": source_domain or ("Pasted Input" if input_method == "manual" else None),
        "input_method": input_method,  # 'manual' or 'url'
        "prediction": engine_result["prediction"],
        "confidence": float(engine_result["confidence"]),
        "confidence_level": engine_result["confidence_level"],
        "signals": engine_result.get("signals", []),
        "word_count": word_count,
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return {
        "success": True,
        "analysis": analysis_obj
    }
