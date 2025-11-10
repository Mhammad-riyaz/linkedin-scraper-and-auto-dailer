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
RUN mkdir -p tmp/pids tmp/cache tmp/sockets log lib/python_scripts/output db

# Precompile assets (if using asset pipeline)
RUN bundle exec rake assets:precompile RAILS_ENV=production || true

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Starting Autodialer..."\n\
\n\
# Remove any existing server.pid\n\
rm -f /app/tmp/pids/server.pid\n\
\n\
# Setup database if it does not exist\n\
if [ ! -f /app/db/production.sqlite3 ]; then\n\
  echo "Database not found, creating..."\n\
  bundle exec rake db:create RAILS_ENV=production\n\
  bundle exec rake db:migrate RAILS_ENV=production\n\
  bundle exec rake db:seed RAILS_ENV=production || true\n\
else\n\
  echo "Database found, running migrations..."\n\
  bundle exec rake db:migrate RAILS_ENV=production\n\
fi\n\
\n\
echo "Starting Rails server..."\n\
exec bundle exec rails server -b 0.0.0.0 -p 3000\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port 3000
EXPOSE 3000

# Set environment variables
ENV RAILS_ENV=production
ENV RAILS_LOG_TO_STDOUT=true
ENV RAILS_SERVE_STATIC_FILES=true

# Start Rails server
CMD ["/app/start.sh"]
