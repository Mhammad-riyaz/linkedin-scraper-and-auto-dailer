# Blog Generator with AI Integration

This Python-based blog generator uses OpenRouter API to automatically generate high-quality programming articles. It integrates with the Autodialer Rails application to provide a web interface for generating and displaying articles.

## Features

- 🤖 AI-powered article generation using OpenRouter API
- 📝 Support for custom topics with detailed instructions
- 💾 JSON-based article storage
- 🔗 Seamless integration with Rails application
- 📊 Batch article generation
- 🎯 Customizable article parameters

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create or edit the `.env` file:

```properties
OPEN_ROUTER_API_KEY=your_api_key_here
LLM_MODEL=openai/gpt-4o-mini
```

Available model options:
- `openai/gpt-4o-mini` (recommended for cost-effective generation)
- `openai/gpt-4o` (higher quality, more expensive)
- `openai/gpt-3.5-turbo` (faster, budget-friendly)
- Any other model available on OpenRouter

## Usage

### Method 1: Generate 10 Default Articles

Run the default generator with predefined programming topics:

```bash
python blog_generator.py
```

This will generate 10 articles on topics like:
- Python Async/Await
- REST API Design
- Docker Containers
- Git Branching
- CSS Grid
- Machine Learning
- Security (OWASP Top 10)
- Database Indexing
- Microservices
- Test-Driven Development

### Method 2: Generate Custom Articles from Python

```python
from blog_generator import BlogGenerator

generator = BlogGenerator()

topics = [
    {
        'title': 'Advanced Python Decorators',
        'details': 'Explain decorators, closures, and practical examples'
    },
    {
        'title': 'GraphQL vs REST',
        'details': 'Compare both approaches with pros and cons'
    }
]

articles = generator.generate_multiple_articles(topics)
generator.save_articles(articles)
```

### Method 3: Generate from Rails Application

1. Navigate to `http://localhost:3000/blog` in your browser
2. Click "Generate New Articles"
3. Enter topics in the format:
   ```
   Topic Title - Additional details or requirements
   Another Topic - More context here
   ```
4. Click "Generate Articles"

The Rails application will automatically:
- Call the Python generator
- Save articles to the database
- Display them in the blog section

## File Structure

```
blog-generator/
├── .env                        # Environment variables (API key, model)
├── requirements.txt            # Python dependencies
├── blog_generator.py          # Main generator class
├── generate_from_topics.py    # CLI tool for Rails integration
├── README.md                  # This file
└── output/
    └── articles.json          # Generated articles (JSON format)
```

## Output Format

Articles are saved as JSON with the following structure:

```json
[
  {
    "title": "Article Title",
    "content": "Full markdown content...",
    "generated_at": "2025-11-10T09:00:00",
    "details": "Original topic details"
  }
]
```

## Integration with Rails App

The blog generator is designed to work seamlessly with the Autodialer Rails application:

1. **Separation**: Code is kept separate in the `blog-generator` folder
2. **Communication**: Rails calls Python scripts via `Open3.capture3`
3. **Data Flow**: 
   - Rails creates `tmp/topics.json` with user input
   - Python reads topics and generates articles
   - Python saves to `output/articles.json`
   - Rails imports articles into database

## Rails Application Features

The integrated blog section at `/blog` provides:

- 📋 **Article List**: Display all generated articles
- ➕ **Generate Interface**: Text area to input topics
- 👁️ **Article View**: Read individual articles with proper formatting
- 🔄 **Real-time Generation**: Generate articles on-demand from the web UI

## Topic Format

When entering topics (via web UI or Python), use this format:

```
Title - Details
```

Examples:
```
Python Type Hints - Cover basic usage and advanced features
Kubernetes Deployments - Explain pods, services, and ingress
React Hooks Deep Dive - Focus on useState, useEffect, and custom hooks
```

The separator can be:
- Dash: `Title - Details`
- Colon: `Title : Details`
- Pipe: `Title | Details`

Details are optional but help generate better content.

## Troubleshooting

### API Key Issues

If you see authentication errors:
1. Check your `.env` file has the correct `OPEN_ROUTER_API_KEY`
2. Verify the key is valid at https://openrouter.ai
3. Ensure no extra spaces or quotes around the key

### Model Not Found

If the model isn't available:
1. Check the model name in your `.env` file
2. Visit https://openrouter.ai/docs to see available models
3. Update `LLM_MODEL` to a valid model

### Generation Fails

If article generation fails:
1. Check your internet connection
2. Verify you have API credits on OpenRouter
3. Review the error message in the terminal
4. Try with a simpler topic first

### Rails Integration Issues

If Rails can't call the Python script:
1. Ensure Python is in your PATH
2. Check that `blog-generator` folder is next to `Autodialer` folder
3. Verify `generate_from_topics.py` exists and is executable
4. Check Rails logs for detailed error messages

## Cost Estimation

Using `openai/gpt-4o-mini`:
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens
- Typical article: ~500 input tokens, ~1500 output tokens
- Cost per article: ~$0.001 (very cheap!)

For 10 articles: approximately $0.01

## Advanced Configuration

### Custom Prompt Templates

Edit `blog_generator.py` to customize the generation prompt:

```python
def generate_article(self, title, details=""):
    prompt = f"""Your custom prompt template here
    
    Title: {title}
    Details: {details}
    
    Your custom requirements...
    """
```

### Adjust Article Length

Modify the prompt in `generate_article()`:
- For shorter articles: "Around 500-800 words"
- For longer articles: "Around 1500-2000 words"

### Change Output Format

Articles are currently generated in markdown. To change:
1. Update the prompt to specify your desired format
2. Modify the `save_articles()` method if needed

## License

This project is part of the Autodialer application suite.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review OpenRouter documentation: https://openrouter.ai/docs
3. Check Rails logs: `tail -f Autodialer/log/development.log`
