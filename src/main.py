import json
import datetime
from scraper import scrape_quora, scrape_reddit
from gemini_filter import is_problem_statement
from product_matcher import match_product
from generate_comment import generate_comment

def main():
    questions = scrape_quora() + scrape_reddit()
    results = []

    for question in questions:
        if is_problem_statement(question):
            product_name, product_link = match_product(question)
            if product_name:
                comment = generate_comment(question, product_name, product_link)
                results.append({
                    "timestamp": str(datetime.datetime.now()),
                    "question": question,
                    "url": "N/A",
                    "response": comment
                })

    with open("data/results.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()
