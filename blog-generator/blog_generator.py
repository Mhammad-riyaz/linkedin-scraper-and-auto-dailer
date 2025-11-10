import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BlogGenerator:
    def __init__(self):
        self.api_key = os.getenv('OPEN_ROUTER_API_KEY')
        self.model = os.getenv('LLM_MODEL', 'openai/gpt-4o-mini')
        self.api_url = 'https://openrouter.ai/api/v1/chat/completions'
        
    def generate_article(self, title, details=""):
        """Generate a blog article using OpenRouter API"""
        prompt = f"""Write a comprehensive blog article about: {title}

{details if details else ''}

The article should be:
- Well-structured with clear sections
- Include practical examples and code snippets where relevant
- Be informative and engaging
- Around 800-1200 words
- Written in markdown format

Please provide the full article content."""

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        
        data = {
            'model': self.model,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            return {
                'title': title,
                'content': content,
                'generated_at': datetime.now().isoformat(),
                'details': details
            }
        except Exception as e:
            print(f"Error generating article: {e}")
            return None
    
    def generate_multiple_articles(self, topics):
        """Generate multiple articles from a list of topics"""
        articles = []
        
        for i, topic in enumerate(topics, 1):
            print(f"Generating article {i}/{len(topics)}: {topic['title']}")
            article = self.generate_article(topic['title'], topic.get('details', ''))
            
            if article:
                articles.append(article)
                print(f"[OK] Generated: {topic['title']}")
            else:
                print(f"[FAILED] Failed: {topic['title']}")
        
        return articles
    
    def save_articles(self, articles, filename='articles.json'):
        """Save articles to a JSON file"""
        output_path = os.path.join('output', filename)
        os.makedirs('output', exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved {len(articles)} articles to {output_path}")
        return output_path

def main():
    # Sample programming topics
    topics = [
        {
            'title': 'Getting Started with Python Async/Await',
            'details': 'Cover the basics of asynchronous programming in Python, including async/await syntax, asyncio library, and practical use cases.'
        },
        {
            'title': 'Understanding REST API Design Principles',
            'details': 'Explain RESTful architecture, HTTP methods, status codes, and best practices for designing scalable APIs.'
        },
        {
            'title': 'Docker Containers: A Beginner\'s Guide',
            'details': 'Introduction to containerization, Docker basics, creating Dockerfiles, and managing containers.'
        },
        {
            'title': 'Git Branching Strategies for Teams',
            'details': 'Compare different branching strategies like Git Flow, GitHub Flow, and trunk-based development.'
        },
        {
            'title': 'Building Responsive UIs with CSS Grid',
            'details': 'Comprehensive guide to CSS Grid layout, including practical examples and responsive design patterns.'
        },
        {
            'title': 'Introduction to Machine Learning with Python',
            'details': 'Cover basics of ML, popular libraries like scikit-learn, and build a simple classification model.'
        },
        {
            'title': 'Securing Web Applications: OWASP Top 10',
            'details': 'Discuss the most critical security risks and how to protect against common vulnerabilities.'
        },
        {
            'title': 'Database Indexing: Performance Optimization',
            'details': 'Explain how database indexes work, when to use them, and their impact on query performance.'
        },
        {
            'title': 'Microservices Architecture Patterns',
            'details': 'Overview of microservices design patterns, benefits, challenges, and when to use them.'
        },
        {
            'title': 'Test-Driven Development in Practice',
            'details': 'Explain TDD methodology, write tests first approach, and practical examples in different languages.'
        }
    ]
    
    generator = BlogGenerator()
    articles = generator.generate_multiple_articles(topics)
    generator.save_articles(articles)

if __name__ == '__main__':
    main()
