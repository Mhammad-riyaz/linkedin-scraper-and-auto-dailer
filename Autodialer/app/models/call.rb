class Call < ApplicationRecord
  # Status values: pending, calling, completed, failed, no_answer, busy
  validates :phone_number, presence: true, format: { with: /\A\+?[0-9\s\-()]+\z/ }
  
  before_validation :set_default_status
  
  scope :pending, -> { where(status: 'pending') }
  scope :completed, -> { where(status: 'completed') }
  scope :failed, -> { where(status: ['failed', 'no_answer', 'busy']) }
  scope :in_progress, -> { where(status: 'calling') }
  
  def self.stats
    {
      total: count,
      pending: pending.count,
      completed: completed.count,
      failed: failed.count,
      in_progress: in_progress.count
    }
  end
  
  def format_phone_number
    # Ensure phone number has +91 prefix for Indian numbers
    number = phone_number.gsub(/[\s\-()]/, '')
    number = "+91#{number}" unless number.start_with?('+')
    number
  end
  
  private
  
  def set_default_status
    self.status ||= 'pending'
  end
end
