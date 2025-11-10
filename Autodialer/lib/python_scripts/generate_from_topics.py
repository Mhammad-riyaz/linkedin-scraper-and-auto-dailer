import sys
import json
from blog_generator import BlogGenerator

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_from_topics.py <topics_json_file>")
        sys.exit(1)
    
    topics_file = sys.argv[1]
    
    # Load topics from JSON file
    with open(topics_file, 'r', encoding='utf-8') as f:
        topics = json.load(f)
    
    # Generate articles
    generator = BlogGenerator()
    articles = generator.generate_multiple_articles(topics)
    generator.save_articles(articles)
    
    print(f"Successfully generated {len(articles)} articles")

if __name__ == '__main__':
    main()
