# Use Ruby 3.2 as base image
FROM ruby:3.2-slim

# Install system dependencies
RUN apt-get update -qq && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    libyaml-dev \
    nodejs \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Gemfile and install Ruby dependencies
COPY Gemfile Gemfile.lock ./
RUN bundle install

# Install Python dependencies for blog generator
RUN pip3 install --no-cache-dir --break-system-packages \
    requests \
    python-dotenv

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p tmp/pids tmp/cache tmp/sockets log lib/python_scripts/output

# Precompile assets (if using asset pipeline)
RUN bundle exec rake assets:precompile RAILS_ENV=production || true

# Create database and run migrations
RUN bundle exec rake db:create db:migrate RAILS_ENV=production || true

# Expose port 3000
EXPOSE 3000

# Set environment variables
ENV RAILS_ENV=production
ENV RAILS_LOG_TO_STDOUT=true
ENV RAILS_SERVE_STATIC_FILES=true

# Start Rails server
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-p", "3000"]
