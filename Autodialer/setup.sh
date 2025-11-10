#!/usr/bin/env bash

echo "🚀 Setting up Autodialer..."

# Install gems
echo "📦 Installing dependencies..."
bundle install

# Create database
echo "🗄️  Creating database..."
rails db:create

# Run migrations
echo "📊 Running database migrations..."
rails db:migrate

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add your OpenAI API key to .env file"
echo "2. Run: rails server"
echo "3. Open: http://localhost:3000"
echo ""
echo "🧪 Use Twilio test numbers:"
echo "   +15005550006 (valid)"
echo "   +15005550009 (busy)"
echo "   +15005550001 (invalid)"
