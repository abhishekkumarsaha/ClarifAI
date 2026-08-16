from article_extractor import extract_article


url = input("Enter a public news article URL: ").strip()

try:
    article = extract_article(url)

    print("\n================================")
    print("     CLARIFAI ARTICLE TEST")
    print("================================")

    print("Title:", article.title)
    print("Domain:", article.source_domain)
    print("Input:", article.input_method)
    print("Word Count:", article.word_count)
    print("URL:", article.source_url)

    print("\nArticle Preview:")
    print(article.article_text[:1000])

except Exception as error:
    print("\nExtraction failed:")
    print(error)