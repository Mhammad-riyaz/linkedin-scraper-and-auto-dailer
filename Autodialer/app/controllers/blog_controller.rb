class BlogController < ApplicationController
  def index
    @articles = Article.order(created_at: :desc)
  end

  def new
  end

  def show
    @article = Article.find(params[:id])
  end

  def destroy
    @article = Article.find(params[:id])
    @article.destroy
    
    flash[:notice] = "Article deleted successfully"
    redirect_to blog_path
  end

  def generate
    topics_input = params[:topics]
    
    if topics_input.blank?
      flash[:error] = "Please provide topics to generate articles"
      redirect_to blog_new_path and return
    end

    topics = parse_topics(topics_input)
    
    if topics.empty?
      flash[:error] = "Could not parse topics. Please use format: 'Title - Details' on each line"
      redirect_to blog_new_path and return
    end

    # generating articles using Python script
    generated_count = generate_articles_via_python(topics)
    
    flash[:notice] = "Successfully generated #{generated_count} article(s)!"
    redirect_to blog_path
  end

  private

  def parse_topics(input)
    topics = []
    current_title = nil
    current_details = nil
    
    input.split("\n").each do |line|
      line = line.strip
      next if line.empty?
      
      
      if line =~ /^title\s*[:|-]/i
        # Save previous topic if exists
        topics << { title: current_title, details: current_details || "" } if current_title.present?
        
        # extracting title after the colon/dash
        current_title = line.sub(/^title\s*[:|-]\s*/i, '').strip
        current_details = nil
      elsif line =~ /^details?\s*[:|-]/i
        current_details = line.sub(/^details?\s*[:|-]\s*/i, '').strip
      else
        if line.include?('-') || line.include?(':') || line.include?('|')
          parts = line.split(/[-:|]/, 2)
          title = parts[0]&.strip
          details = parts[1]&.strip || ""
          topics << { title: title, details: details } if title.present?
        else
          topics << { title: line, details: "" }
        end
      end
    end
    
    topics << { title: current_title, details: current_details || "" } if current_title.present?
    
    topics
  end

  def generate_articles_via_python(topics)
    require 'open3'
    require 'json'
    require 'fileutils'
    
    temp_file = Rails.root.join('tmp', 'topics.json')
    FileUtils.mkdir_p(File.dirname(temp_file))
    File.write(temp_file, topics.to_json)
    
    # Use Python scripts from lib/python_scripts
    python_scripts_path = Rails.root.join('lib', 'python_scripts')
    python_script = python_scripts_path.join('generate_from_topics.py')
    
    unless File.exist?(python_script)
      Rails.logger.error("Python script not found at: #{python_script}")
      return 0
    end
    
    # Execute Python script
    stdout, stderr, status = Open3.capture3(
      'python',
      python_script.to_s,
      temp_file.to_s,
      chdir: python_scripts_path.to_s
    )
    
    Rails.logger.info("Python stdout: #{stdout}")
    Rails.logger.error("Python stderr: #{stderr}") unless stderr.blank?
    
    if status.success?
      # Loading the generated articles from lib/python_scripts/output
      output_file = python_scripts_path.join('output', 'articles.json')
      if File.exist?(output_file)
        articles_data = JSON.parse(File.read(output_file))
        
        # saving to database - newest first
        count = 0
        articles_data.reverse.each do |article_data|
          Article.create!(
            title: article_data['title'],
            content: article_data['content'],
            generated_at: article_data['generated_at']
          )
          count += 1
        end
        
        File.delete(temp_file) if File.exist?(temp_file)
        
        return count
      else
        Rails.logger.error("Output file not found at: #{output_file}")
      end
    else
      Rails.logger.error("Python script failed with status: #{status.exitstatus}")
      Rails.logger.error("Error: #{stderr}")
    end
    
    0
  end
end
