require 'twilio-ruby'

class TwilioService
  def initialize
    @client = Twilio::REST::Client.new(
      ENV['ACCOUNT_SID'],
      ENV['AUTH_TOKEN']
    )
  end

  # Twilio's Magic Test Numbers:
  # +15005550006 - Valid number, call will be completed
  # +15005550001 - Invalid phone number
  # +15005550007 - Call answered, then hung up
  # +15005550008 - Call forwarded
  # +15005550009 - Call busy
  
  def make_call(to_number, from_number = '+15005550006')
    begin
      call = @client.calls.create(
        to: to_number,
        from: from_number,
        url: 'http://demo.twilio.com/docs/voice.xml', # Basic test TwiML
        status_callback: callback_url,
        status_callback_event: ['initiated', 'ringing', 'answered', 'completed']
      )
      
      {
        success: true,
        call_sid: call.sid,
        status: call.status,
        to: call.to,
        from: call.from
      }
    rescue Twilio::REST::RestError => e
      {
        success: false,
        error_message: e.message,
        error_code: e.code
      }
    end
  end

  def get_call_status(call_sid)
    begin
      call = @client.calls(call_sid).fetch
      {
        success: true,
        status: call.status,
        duration: call.duration,
        direction: call.direction
      }
    rescue Twilio::REST::RestError => e
      {
        success: false,
        error_message: e.message
      }
    end
  end

  private

  def callback_url
    # This would be your actual callback URL in production
    # For testing, Twilio will accept this even if not reachable
    'http://localhost:3000/calls/callback'
  end
end
