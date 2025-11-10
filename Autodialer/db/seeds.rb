require 'json'

# Path to the generated articles
articles_file = File.join(__dir__, '..', '..', 'blog-generator', 'output', 'articles.json')

if File.exist?(articles_file)
  puts "Loading articles from #{articles_file}..."
  
  articles_data = JSON.parse(File.read(articles_file))
  
  articles_data.each do |article_data|
    article = Article.create!(
      title: article_data['title'],
      content: article_data['content'],
      generated_at: article_data['generated_at']
    )
    puts "✓ Created: #{article.title}"
  end
  
  puts "\nSuccessfully imported #{articles_data.length} articles!"
else
  puts "Error: articles.json not found at #{articles_file}"
  puts "Please run the blog generator first: cd blog-generator && python blog_generator.py"
end
