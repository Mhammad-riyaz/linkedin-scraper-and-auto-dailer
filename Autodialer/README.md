# Autodialer - Ruby on Rails Automated Calling System

A Ruby on Rails application that automates phone calls using Twilio API with AI-powered natural language commands via OpenAI.

## Features

- 📞 **Automated Calling**: Make calls to up to 100 numbers automatically
- 🤖 **AI Commands**: Use natural language to make calls (e.g., "Make a call to +919876543210")
- 📊 **Live Dashboard**: Real-time stats showing pending, completed, and failed calls
- 📋 **Bulk Upload**: Paste or upload multiple phone numbers at once
- 🔍 **Call Logs**: Detailed logs of all calls with status tracking
- 🧪 **Test Mode**: Uses Twilio test credentials and magic numbers

## Prerequisites

- Ruby 3.0+
- Rails 7.1+
- Bundler
- Twilio Account (using test credentials)
- OpenAI API Key

## Installation

1. **Install dependencies:**
   ```bash
   bundle install
   ```

2. **Set up the database:**
   ```bash
   rails db:create
   rails db:migrate
   ```

3. **Configure environment variables:**
   
   Edit `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key
   ```
   
   (Twilio credentials are already configured for testing)

4. **Start the server:**
   ```bash
   rails server
   ```

5. **Open your browser:**
   ```
   http://localhost:3000
   ```

## Usage

### Adding Phone Numbers

1. **Manual Entry**: Use the bulk add form to paste phone numbers (one per line or comma-separated)
2. **Test Numbers**: Use Twilio's magic test numbers for testing:
   - `+15005550006` - Valid number (call will complete)
   - `+15005550009` - Busy signal
   - `+15005550001` - Invalid number

### Making Calls

1. **Bulk Calling**: Click "Start Calling" to call all pending numbers
2. **AI Commands**: Use the AI prompt to make calls with natural language:
   - "Make a call to +919876543210"
   - "Call +911234567890"

### Viewing Logs

- Dashboard shows recent 10 calls
- Click "View All Logs" for complete call history
- Each log shows: status, call SID, duration, timestamp, and errors

## Call Status Types

- **Pending**: Number added but not yet called
- **Calling**: Call in progress
- **Completed**: Call successfully answered and completed
- **Failed**: Call failed due to error
- **No Answer**: Recipient didn't answer
- **Busy**: Line was busy

## API Integration

### Twilio

The app uses Twilio's test credentials for safe testing without actual calls. Test numbers simulate different scenarios:
- Valid calls
- Busy signals
- Invalid numbers
- No answer scenarios

### OpenAI

The AI command feature uses GPT-4 to parse natural language and extract phone numbers from user commands.

## Project Structure

```
Autodialer/
├── app/
│   ├── controllers/
│   │   └── calls_controller.rb
│   ├── models/
│   │   └── call.rb
│   ├── services/
│   │   ├── twilio_service.rb
│   │   └── openai_service.rb
│   └── views/
│       ├── calls/
│       │   ├── index.html.erb
│       │   └── logs.html.erb
│       └── layouts/
│           └── application.html.erb
├── config/
│   ├── routes.rb
│   └── database.yml
├── db/
│   └── migrate/
│       └── create_calls.rb
├── .env
├── Gemfile
└── README.md
```

## Technologies Used

- **Ruby on Rails 7.1**
- **Twilio Ruby SDK** - For making phone calls
- **OpenAI Ruby SDK** - For AI command processing
- **SQLite** - Database
- **Dotenv** - Environment variable management

## Development Notes

- Using Twilio test credentials means no actual calls are made
- All test calls use Twilio's magic numbers
- AI parsing requires valid OpenAI API key
- Database is SQLite for simplicity (change to PostgreSQL for production)

## Future Enhancements

- Upload CSV files with phone numbers
- Schedule calls for specific times
- Add custom voice messages (TTS)
- Webhook integration for real-time call status updates
- Export call logs to CSV
- Multiple campaign management

## License

MIT
