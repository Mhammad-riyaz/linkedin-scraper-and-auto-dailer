require 'net/http'
require 'json'

class OpenrouterService
  def initialize
    @api_key = ENV['OPEN_ROUTER_API_KEY']
    @model = ENV['LLM_MODEL'] || 'openai/gpt-oss-20b:free'
  end

  def parse_command(user_input)
    begin
      uri = URI("https://openrouter.ai/api/v1/chat/completions")
      
      http = Net::HTTP.new(uri.host, uri.port)
      http.use_ssl = true
      
      request = Net::HTTP::Post.new(uri.request_uri)
      request['Content-Type'] = 'application/json'
      request['Authorization'] = "Bearer #{@api_key}"
      request['HTTP-Referer'] = 'http://localhost:3000'
      request['X-Title'] = 'Autodialer'
      
      request.body = {
        model: @model,
        messages: [
          {
            role: "system",
            content: "You are a helpful assistant that extracts phone numbers from user commands. 
When a user asks to make a call, extract the phone number(s) and respond with JSON only.
Format: {\"action\": \"make_call\", \"phone_numbers\": [\"number1\", \"number2\"]}
If no phone number is found, respond with: {\"action\": \"none\", \"message\": \"No phone number detected\"}
Respond with JSON only, no markdown or code blocks."
          },
          {
            role: "user",
            content: user_input
          }
        ],
        temperature: 0.3,
        max_tokens: 200
      }.to_json
      
      response = http.request(request)
      
      if response.code == '200'
        result = JSON.parse(response.body)
        content = result.dig('choices', 0, 'message', 'content')
        
        # Clean up markdown code blocks if present
        content = content.gsub(/```json\n?/, '').gsub(/```\n?/, '').strip
        
        JSON.parse(content)
      else
        {
          "action" => "error",
          "message" => "API error: #{response.code} - #{response.body}"
        }
      end
    rescue StandardError => e
      {
        "action" => "error",
        "message" => "Failed to parse command: #{e.message}"
      }
    end
  end
end
