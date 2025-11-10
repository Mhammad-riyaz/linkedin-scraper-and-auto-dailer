# 🚀 Quick Start Guide

## Step 1: Add Your OpenAI API Key

Edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key.

## Step 2: Run Setup

**For Windows (PowerShell):**
```powershell
.\setup.bat
```

**For Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Or manually:**
```bash
bundle install
rails db:create
rails db:migrate
```

## Step 3: Start the Server

```bash
rails server
```

## Step 4: Open Your Browser

Navigate to: http://localhost:3000

## 🧪 Testing with Twilio Magic Numbers

Since we're using Twilio's test credentials, use these magic numbers for testing:

- **+15005550006** - Valid number (call will complete successfully)
- **+15005550009** - Busy signal
- **+15005550001** - Invalid number (will fail)
- **+15005550007** - Answered then hung up

## 📱 Features to Try

### 1. Bulk Add Numbers
- Paste multiple numbers in the text area
- One per line or comma-separated
- Click "Add Numbers"

### 2. AI Command
- Type: "Make a call to +15005550006"
- Or: "Call +15005550009"
- The AI will understand and execute

### 3. Start Calling
- Click "Start Calling" to call all pending numbers
- Watch the live status updates

### 4. View Logs
- See real-time call statistics
- Check detailed call logs
- Monitor success/failure rates

## 📊 Dashboard Features

- **Total Calls**: All calls in the system
- **Pending**: Numbers waiting to be called
- **Completed**: Successfully completed calls
- **Failed**: Failed calls, busy signals, no answers

## 🎯 Example Workflow

1. Add test numbers using the form:
   ```
   +15005550006
   +15005550009
   +15005550001
   ```

2. Click "Start Calling (All Pending)"

3. Watch the status update in real-time

4. Check logs to see results

5. Try AI command: "Make a call to +15005550006"

## 🔧 Troubleshooting

**Issue**: Rails doesn't start
- Solution: Run `bundle install` again

**Issue**: Database error
- Solution: Run `rails db:create db:migrate`

**Issue**: AI command doesn't work
- Solution: Check that your OpenAI API key is set in `.env`

**Issue**: Calls not working
- Solution: Verify Twilio credentials in `.env` (they should already be set)

## 📝 Notes

- All calls are in TEST MODE using Twilio test credentials
- No real calls are made
- Use only Twilio magic test numbers for reliable results
- OpenAI API requires a valid key (not free)

Enjoy your Autodialer! 🎉
